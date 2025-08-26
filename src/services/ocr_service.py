"""
OCR服务模块
提供图片OCR识别功能，基于SimpleTex API
"""

import datetime
import json
import hashlib
import requests
from random import Random
from typing import Dict, Any, Optional, Tuple
import logging
from pathlib import Path
import io

from ..config.ocr_config import ocr_config

logger = logging.getLogger(__name__)


class SimpleTexOCRService:
    """SimpleTex OCR服务类"""
    
    def __init__(self):
        self.config = ocr_config.simpletex
        self.session = requests.Session()
        self.session.timeout = self.config.timeout
    
    def _random_str(self, randomlength: int = 16) -> str:
        """生成随机字符串"""
        chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
        length = len(chars) - 1
        random = Random()
        return ''.join(chars[random.randint(0, length)] for _ in range(randomlength))
    
    def _get_req_data(self, req_data: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, Any]]:
        """生成请求头和签名"""
        header = {}
        header["timestamp"] = str(int(datetime.datetime.now().timestamp()))
        header["random-str"] = self._random_str(16)
        header["app-id"] = self.config.app_id
        
        # 构建签名字符串
        pre_sign_string = ""
        sorted_keys = list(req_data.keys()) + list(header.keys())
        sorted_keys.sort()
        
        for key in sorted_keys:
            if pre_sign_string:
                pre_sign_string += "&"
            if key in header:
                pre_sign_string += key + "=" + str(header[key])
            else:
                pre_sign_string += key + "=" + str(req_data[key])
        
        pre_sign_string += "&secret=" + self.config.app_secret
        header["sign"] = hashlib.md5(pre_sign_string.encode()).hexdigest()
        
        return header, req_data
    
    def _validate_file(self, file_path: str) -> Tuple[bool, str]:
        """验证文件"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return False, "文件不存在"
            
            # 检查文件格式
            if not ocr_config.is_format_supported(file_path.name):
                supported_formats = ', '.join(ocr_config.get_supported_formats())
                return False, f"不支持的文件格式。支持的格式: {supported_formats}"
            
            # 检查文件大小
            file_size = file_path.stat().st_size
            if not ocr_config.validate_file_size(file_size):
                max_size_mb = self.config.max_file_size / (1024 * 1024)
                return False, f"文件过大。最大支持: {max_size_mb}MB"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"文件验证失败: {e}")
            return False, f"文件验证失败: {str(e)}"
    
    def _validate_file_data(self, file_data: bytes, filename: str) -> Tuple[bool, str]:
        """验证文件数据"""
        try:
            # 检查文件格式
            if not ocr_config.is_format_supported(filename):
                supported_formats = ', '.join(ocr_config.get_supported_formats())
                return False, f"不支持的文件格式。支持的格式: {supported_formats}"
            
            # 检查文件大小
            file_size = len(file_data)
            if not ocr_config.validate_file_size(file_size):
                max_size_mb = self.config.max_file_size / (1024 * 1024)
                return False, f"文件过大。最大支持: {max_size_mb}MB"
            
            return True, ""
            
        except Exception as e:
            logger.error(f"文件数据验证失败: {e}")
            return False, f"文件数据验证失败: {str(e)}"
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """处理API响应"""
        try:
            response.raise_for_status()
            result = response.json()
            
            # 检查API返回的状态
            if not result.get('status'):
                # 处理错误情况
                error_msg = result.get('res', {}).get('errType', 'unknown_error')
                return {
                    'success': False,
                    'error': ocr_config.get_error_message(error_msg),
                    'error_code': error_msg,
                    'request_id': result.get('request_id')
                }
            
            # 处理成功情况
            res_data = result.get('res', {})
            
            # 根据返回的数据类型处理
            if res_data.get('type') == 'formula':
                # 数学公式类型
                ocr_text = res_data.get('info', '')
                confidence = res_data.get('conf', 0.0)
                return {
                    'success': True,
                    'data': {
                        'text': ocr_text,
                        'type': 'formula',
                        'confidence': confidence,
                        'raw_info': res_data.get('info', ''),
                        'raw_confidence': res_data.get('conf', 0.0)
                    },
                    'request_id': result.get('request_id')
                }
            elif res_data.get('type') == 'text':
                # 普通文本类型
                ocr_text = res_data.get('info', '')
                confidence = res_data.get('conf', 0.0)
                return {
                    'success': True,
                    'data': {
                        'text': ocr_text,
                        'type': 'text',
                        'confidence': confidence,
                        'raw_info': res_data.get('info', ''),
                        'raw_confidence': res_data.get('conf', 0.0)
                    },
                    'request_id': result.get('request_id')
                }
            else:
                # 其他类型或未知类型，尝试提取文本
                ocr_text = res_data.get('info', res_data.get('text', ''))
                confidence = res_data.get('conf', res_data.get('confidence', 0.0))
                return {
                    'success': True,
                    'data': {
                        'text': ocr_text,
                        'type': res_data.get('type', 'unknown'),
                        'confidence': confidence,
                        'raw_info': res_data.get('info', ''),
                        'raw_confidence': res_data.get('conf', 0.0)
                    },
                    'request_id': result.get('request_id')
                }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {e}")
            return {
                'success': False,
                'error': f"网络请求失败: {str(e)}",
                'error_code': 'network_error'
            }
        except json.JSONDecodeError as e:
            logger.error(f"响应解析失败: {e}")
            return {
                'success': False,
                'error': f"响应解析失败: {str(e)}",
                'error_code': 'parse_error'
            }
        except Exception as e:
            logger.error(f"处理响应时发生错误: {e}")
            return {
                'success': False,
                'error': f"处理响应时发生错误: {str(e)}",
                'error_code': 'unknown_error'
            }
    
    def ocr_from_file(self, file_path: str) -> Dict[str, Any]:
        """从文件路径进行OCR识别"""
        try:
            # 验证文件
            is_valid, error_msg = self._validate_file(file_path)
            if not is_valid:
                return {
                    'success': False,
                    'error': error_msg,
                    'error_code': 'validation_error'
                }
            
            # 准备请求数据
            with open(file_path, 'rb') as f:
                files = {"file": f}
                data = {}
                header, data = self._get_req_data(data)
                
                # 发送请求
                response = self.session.post(
                    self.config.api_url,
                    files=files,
                    data=data,
                    headers=header
                )
            
            return self._handle_response(response)
            
        except Exception as e:
            logger.error(f"OCR识别失败: {e}")
            return {
                'success': False,
                'error': f"OCR识别失败: {str(e)}",
                'error_code': 'ocr_error'
            }
    
    def ocr_from_data(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """从文件数据进行OCR识别"""
        try:
            # 验证文件数据
            is_valid, error_msg = self._validate_file_data(file_data, filename)
            if not is_valid:
                return {
                    'success': False,
                    'error': error_msg,
                    'error_code': 'validation_error'
                }
            
            # 准备请求数据
            files = {"file": (filename, io.BytesIO(file_data), 'application/octet-stream')}
            data = {}
            header, data = self._get_req_data(data)
            
            # 发送请求
            response = self.session.post(
                self.config.api_url,
                files=files,
                data=data,
                headers=header
            )
            
            return self._handle_response(response)
            
        except Exception as e:
            logger.error(f"OCR识别失败: {e}")
            return {
                'success': False,
                'error': f"OCR识别失败: {str(e)}",
                'error_code': 'ocr_error'
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """测试API连接"""
        try:
            # 创建一个简单的测试图片（1x1像素的PNG）
            test_image_data = (
                b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
                b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00'
                b'\x00\x04\x00\x01\xf5\xa7\xe4\xd9\x00\x00\x00\x00IEND\xaeB`\x82'
            )
            
            result = self.ocr_from_data(test_image_data, 'test.png')
            
            if result['success']:
                return {
                    'success': True,
                    'message': 'API连接正常',
                    'request_id': result.get('request_id')
                }
            else:
                return {
                    'success': False,
                    'error': result['error'],
                    'error_code': result.get('error_code', 'unknown')
                }
                
        except Exception as e:
            logger.error(f"连接测试失败: {e}")
            return {
                'success': False,
                'error': f"连接测试失败: {str(e)}",
                'error_code': 'test_error'
            }


class OCRService:
    """OCR服务主类"""
    
    def __init__(self):
        self.simpletex_service = SimpleTexOCRService()
    
    def process_image(self, file_path: str) -> Dict[str, Any]:
        """处理图片文件"""
        return self.simpletex_service.ocr_from_file(file_path)
    
    def process_image_data(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """处理图片数据"""
        return self.simpletex_service.ocr_from_data(file_data, filename)
    
    def test_api_connection(self) -> Dict[str, Any]:
        """测试API连接"""
        return self.simpletex_service.test_connection()
    
    def get_supported_formats(self) -> tuple:
        """获取支持的图片格式"""
        return ocr_config.get_supported_formats()
    
    def validate_file(self, file_path: str) -> Tuple[bool, str]:
        """验证文件"""
        return self.simpletex_service._validate_file(file_path)
    
    def validate_file_data(self, file_data: bytes, filename: str) -> Tuple[bool, str]:
        """验证文件数据"""
        return self.simpletex_service._validate_file_data(file_data, filename)


# 全局OCR服务实例
ocr_service = OCRService()

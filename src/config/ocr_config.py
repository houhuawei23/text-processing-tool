"""
OCR服务配置文件
提供SimpleTex OCR API的配置信息
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class SimpleTexConfig:
    """SimpleTex OCR API配置"""

    app_id: str
    app_secret: str
    api_url: str = "https://server.simpletex.cn/api/simpletex_ocr"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    supported_formats: tuple = ("png", "jpg", "jpeg", "bmp", "tiff", "webp")
    timeout: int = 30  # 请求超时时间（秒）
    max_retries: int = 3  # 最大重试次数


class OCRConfig:
    """OCR配置管理类"""

    def __init__(self):
        self._simpletex_config = None
        self._load_config()

    def _load_config(self):
        """加载OCR配置"""
        # 从环境变量加载SimpleTex配置
        app_id = os.getenv("SIMPLETEX_APP_ID", "")
        app_secret = os.getenv("SIMPLETEX_APP_SECRET", "")

        # 从环境变量加载其他配置
        api_url = os.getenv("SIMPLETEX_API_URL", "https://server.simpletex.cn/api/simpletex_ocr")
        max_file_size = int(os.getenv("OCR_MAX_FILE_SIZE", 10 * 1024 * 1024))
        timeout = int(os.getenv("OCR_TIMEOUT", 30))
        max_retries = int(os.getenv("OCR_MAX_RETRIES", 3))

        self._simpletex_config = SimpleTexConfig(
            app_id=app_id,
            app_secret=app_secret,
            api_url=api_url,
            max_file_size=max_file_size,
            timeout=timeout,
            max_retries=max_retries,
        )

    @property
    def simpletex(self) -> SimpleTexConfig:
        """获取SimpleTex配置"""
        return self._simpletex_config

    def get_supported_formats(self) -> tuple:
        """获取支持的图片格式"""
        return self._simpletex_config.supported_formats

    def is_format_supported(self, filename: str) -> bool:
        """检查文件格式是否支持"""
        if not filename:
            return False

        # 获取文件扩展名
        ext = filename.lower().split(".")[-1] if "." in filename else ""
        return ext in self._simpletex_config.supported_formats

    def validate_file_size(self, file_size: int) -> bool:
        """验证文件大小"""
        return file_size <= self._simpletex_config.max_file_size

    def get_error_message(self, error_code: str) -> str:
        """根据错误代码获取错误消息"""
        error_messages = {
            "api_not_find": "API或对应版本未找到",
            "req_method_error": "请求方法错误",
            "req_unauthorized": "认证失败，请检查API密钥",
            "resource_no_valid": "没有可用的资源包或账户余额不足",
            "image_missing": "未上传图片文件",
            "image_oversize": "图片文件过大",
            "sever_closed": "服务器未启动或正在维护",
            "server_error": "服务器内部错误",
            "exceed_max_qps": "超出最大QPS限制，请稍后重试",
            "exceed_max_ccy": "超出最大并发请求数，请稍后重试",
            "server_inference_error": "服务器推理错误",
            "image_proc_error": "图片处理错误",
            "invalid_param": "无效参数",
            "too_many_file": "文件数量过多",
            "no_file_error": "未找到文件",
        }

        return error_messages.get(error_code, f"未知错误: {error_code}")


# 全局OCR配置实例
ocr_config = OCRConfig()

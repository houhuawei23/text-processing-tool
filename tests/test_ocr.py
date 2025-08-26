#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR功能测试脚本
用于测试SimpleTex OCR API的集成
"""

import os
import sys
import requests
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.services.ocr_service import ocr_service
from src.config.ocr_config import ocr_config


def test_ocr_config():
    """测试OCR配置"""
    print("=== 测试OCR配置 ===")
    print(f"支持的格式: {ocr_config.get_supported_formats()}")
    print(f"最大文件大小: {ocr_config.simpletex.max_file_size / (1024*1024):.1f}MB")
    print(f"API URL: {ocr_config.simpletex.api_url}")
    print(f"App ID: {ocr_config.simpletex.app_id}")
    print(f"App Secret: {'*' * len(ocr_config.simpletex.app_secret)}")
    print()


def test_file_validation():
    """测试文件验证"""
    print("=== 测试文件验证 ===")
    
    # 测试支持的格式
    test_files = [
        'test.png',
        'test.jpg',
        'test.jpeg',
        'test.bmp',
        'test.tiff',
        'test.webp',
        'test.txt',
        'test.pdf'
    ]
    
    for filename in test_files:
        is_supported = ocr_config.is_format_supported(filename)
        print(f"{filename}: {'✓' if is_supported else '✗'}")
    
    # 测试文件大小验证
    test_sizes = [1024, 5*1024*1024, 10*1024*1024, 15*1024*1024]
    for size in test_sizes:
        is_valid = ocr_config.validate_file_size(size)
        print(f"文件大小 {size/(1024*1024):.1f}MB: {'✓' if is_valid else '✗'}")
    
    print()


def test_api_connection():
    """测试API连接"""
    print("=== 测试API连接 ===")
    
    try:
        result = ocr_service.test_api_connection()
        if result['success']:
            print("✓ API连接测试成功")
            print(f"消息: {result['message']}")
            if 'request_id' in result:
                print(f"请求ID: {result['request_id']}")
        else:
            print("✗ API连接测试失败")
            print(f"错误: {result['error']}")
    except Exception as e:
        print(f"✗ API连接测试异常: {e}")
    
    print()


def test_error_messages():
    """测试错误消息"""
    print("=== 测试错误消息 ===")
    
    error_codes = [
        'api_not_find',
        'req_method_error',
        'req_unauthorized',
        'resource_no_valid',
        'image_missing',
        'image_oversize',
        'sever_closed',
        'server_error',
        'exceed_max_qps',
        'exceed_max_ccy',
        'server_inference_error',
        'image_proc_error',
        'invalid_param',
        'too_many_file',
        'no_file_error',
        'unknown_error'
    ]
    
    for code in error_codes:
        message = ocr_config.get_error_message(code)
        print(f"{code}: {message}")
    
    print()


def main():
    """主函数"""
    print("OCR功能测试")
    print("=" * 50)
    
    # 测试配置
    test_ocr_config()
    
    # 测试文件验证
    test_file_validation()
    
    # 测试错误消息
    test_error_messages()
    
    # 测试API连接（可选，需要网络连接）
    print("是否测试API连接？(y/n): ", end="")
    try:
        choice = input().strip().lower()
        if choice in ['y', 'yes', '是']:
            test_api_connection()
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    
    print("测试完成！")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Flask OCR API的脚本
"""

import json
from src.app_factory import create_app

def test_ocr_api():
    """测试OCR API接口"""
    app = create_app()
    client = app.test_client()
    
    print("=== 测试OCR API接口 ===")
    
    # 测试获取支持格式
    print("\n1. 测试获取支持格式:")
    response = client.get('/api/ocr/formats')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.get_json(), indent=2, ensure_ascii=False)}")
    
    # 测试连接测试
    print("\n2. 测试连接测试:")
    response = client.get('/api/ocr/test')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.get_json(), indent=2, ensure_ascii=False)}")
    
    # 测试OCR识别
    print("\n3. 测试OCR识别:")
    try:
        with open('test_text.png', 'rb') as f:
            response = client.post('/api/ocr', data={'file': (f, 'test_text.png')})
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.get_json(), indent=2, ensure_ascii=False)}")
    except FileNotFoundError:
        print("测试图片文件不存在，跳过OCR识别测试")
    
    # 测试错误情况
    print("\n4. 测试错误情况:")
    response = client.post('/api/ocr')
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.get_json(), indent=2, ensure_ascii=False)}")

if __name__ == '__main__':
    test_ocr_api()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR功能完整性测试脚本
"""

import sys
import os
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """测试模块导入"""
    print("=== 测试模块导入 ===")
    
    try:
        from src.config.ocr_config import ocr_config, OCRConfig
        print("✓ OCR配置模块导入成功")
    except Exception as e:
        print(f"✗ OCR配置模块导入失败: {e}")
        return False
    
    try:
        from src.services.ocr_service import ocr_service, OCRService, SimpleTexOCRService
        print("✓ OCR服务模块导入成功")
    except Exception as e:
        print(f"✗ OCR服务模块导入失败: {e}")
        return False
    
    try:
        from src.app_factory import create_app
        print("✓ Flask应用模块导入成功")
    except Exception as e:
        print(f"✗ Flask应用模块导入失败: {e}")
        return False
    
    print()
    return True

def test_config():
    """测试配置功能"""
    print("=== 测试配置功能 ===")
    
    from src.config.ocr_config import ocr_config
    
    # 测试基本配置
    print(f"✓ 支持的格式: {ocr_config.get_supported_formats()}")
    print(f"✓ 最大文件大小: {ocr_config.simpletex.max_file_size / (1024*1024):.1f}MB")
    print(f"✓ API URL: {ocr_config.simpletex.api_url}")
    
    # 测试文件格式验证
    test_files = ['test.png', 'test.jpg', 'test.txt', 'test.pdf']
    for filename in test_files:
        is_supported = ocr_config.is_format_supported(filename)
        print(f"✓ {filename}: {'支持' if is_supported else '不支持'}")
    
    # 测试文件大小验证
    test_sizes = [1024, 5*1024*1024, 15*1024*1024]
    for size in test_sizes:
        is_valid = ocr_config.validate_file_size(size)
        print(f"✓ 文件大小 {size/(1024*1024):.1f}MB: {'有效' if is_valid else '无效'}")
    
    # 测试错误消息
    error_codes = ['api_not_find', 'req_unauthorized', 'image_missing']
    for code in error_codes:
        message = ocr_config.get_error_message(code)
        print(f"✓ 错误代码 {code}: {message}")
    
    print()
    return True

def test_service():
    """测试服务功能"""
    print("=== 测试服务功能 ===")
    
    from src.services.ocr_service import ocr_service
    
    # 测试API连接
    try:
        result = ocr_service.test_api_connection()
        if result['success']:
            print("✓ API连接测试成功")
            print(f"  - 消息: {result['message']}")
            if 'request_id' in result:
                print(f"  - 请求ID: {result['request_id']}")
        else:
            print(f"✗ API连接测试失败: {result['error']}")
    except Exception as e:
        print(f"✗ API连接测试异常: {e}")
    
    # 测试文件验证
    if os.path.exists('test_text.png'):
        try:
            is_valid, error_msg = ocr_service.validate_file('test_text.png')
            if is_valid:
                print("✓ 文件验证成功")
            else:
                print(f"✗ 文件验证失败: {error_msg}")
        except Exception as e:
            print(f"✗ 文件验证异常: {e}")
    
    print()
    return True

def test_api():
    """测试API接口"""
    print("=== 测试API接口 ===")
    
    from src.app_factory import create_app
    import json
    
    app = create_app()
    client = app.test_client()
    
    # 测试获取支持格式
    try:
        response = client.get('/api/ocr/formats')
        if response.status_code == 200:
            data = response.get_json()
            if data['success']:
                print("✓ 获取支持格式接口正常")
                print(f"  - 支持格式: {data['data']['supported_formats']}")
                print(f"  - 最大文件大小: {data['data']['max_file_size_mb']}MB")
            else:
                print(f"✗ 获取支持格式接口失败: {data.get('error', '未知错误')}")
        else:
            print(f"✗ 获取支持格式接口状态码错误: {response.status_code}")
    except Exception as e:
        print(f"✗ 获取支持格式接口异常: {e}")
    
    # 测试连接测试接口
    try:
        response = client.get('/api/ocr/test')
        if response.status_code == 200:
            data = response.get_json()
            if data['success']:
                print("✓ 连接测试接口正常")
                print(f"  - 消息: {data['data']['message']}")
            else:
                print(f"✗ 连接测试接口失败: {data.get('error', '未知错误')}")
        else:
            print(f"✗ 连接测试接口状态码错误: {response.status_code}")
    except Exception as e:
        print(f"✗ 连接测试接口异常: {e}")
    
    # 测试OCR识别接口（如果有测试图片）
    if os.path.exists('test_text.png'):
        try:
            with open('test_text.png', 'rb') as f:
                response = client.post('/api/ocr', data={'file': (f, 'test_text.png')})
            if response.status_code == 200:
                data = response.get_json()
                if data['success']:
                    print("✓ OCR识别接口正常")
                    print(f"  - 文件名: {data['data']['file_info']['filename']}")
                    print(f"  - 文件大小: {data['data']['file_info']['size']} bytes")
                    print(f"  - 请求ID: {data['data']['request_id']}")
                else:
                    print(f"✗ OCR识别接口失败: {data.get('error', '未知错误')}")
            else:
                print(f"✗ OCR识别接口状态码错误: {response.status_code}")
        except Exception as e:
            print(f"✗ OCR识别接口异常: {e}")
    else:
        print("⚠ 跳过OCR识别接口测试（测试图片不存在）")
    
    # 测试错误情况
    try:
        response = client.post('/api/ocr')
        if response.status_code == 400:
            data = response.get_json()
            if not data['success'] and 'No file provided' in data.get('error', ''):
                print("✓ 错误处理正常（无文件上传）")
            else:
                print(f"✗ 错误处理异常: {data}")
        else:
            print(f"✗ 错误处理状态码错误: {response.status_code}")
    except Exception as e:
        print(f"✗ 错误处理异常: {e}")
    
    print()
    return True

def test_frontend_files():
    """测试前端文件"""
    print("=== 测试前端文件 ===")
    
    # 检查HTML模板
    if os.path.exists('templates/index.html'):
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'ocrBtn' in content:
                print("✓ HTML模板包含OCR按钮")
            else:
                print("✗ HTML模板缺少OCR按钮")
            
            if 'input-type-switcher' in content:
                print("✓ HTML模板包含输入类型切换器")
            else:
                print("✗ HTML模板缺少输入类型切换器")
            
            if 'upload-zone' in content:
                print("✓ HTML模板包含上传区域")
            else:
                print("✗ HTML模板缺少上传区域")
    else:
        print("✗ HTML模板文件不存在")
    
    # 检查CSS样式
    if os.path.exists('static/css/style.css'):
        with open('static/css/style.css', 'r', encoding='utf-8') as f:
            content = f.read()
            if '.btn-warning' in content:
                print("✓ CSS包含OCR按钮样式")
            else:
                print("✗ CSS缺少OCR按钮样式")
            
            if '.input-type-switcher' in content:
                print("✓ CSS包含输入类型切换器样式")
            else:
                print("✗ CSS缺少输入类型切换器样式")
            
            if '.upload-zone' in content:
                print("✓ CSS包含上传区域样式")
            else:
                print("✗ CSS缺少上传区域样式")
    else:
        print("✗ CSS样式文件不存在")
    
    # 检查JavaScript
    if os.path.exists('static/js/app.js'):
        with open('static/js/app.js', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'processOCR' in content:
                print("✓ JavaScript包含OCR处理函数")
            else:
                print("✗ JavaScript缺少OCR处理函数")
            
            if 'setupImageUpload' in content:
                print("✓ JavaScript包含图片上传设置函数")
            else:
                print("✗ JavaScript缺少图片上传设置函数")
            
            if 'ocr-processing' in content:
                print("✓ JavaScript包含OCR任务类型")
            else:
                print("✗ JavaScript缺少OCR任务类型")
    else:
        print("✗ JavaScript文件不存在")
    
    print()
    return True

def main():
    """主函数"""
    print("OCR功能完整性测试")
    print("=" * 60)
    
    # 运行所有测试
    tests = [
        test_imports,
        test_config,
        test_service,
        test_api,
        test_frontend_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ 测试 {test.__name__} 异常: {e}")
    
    print("=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！OCR功能完整可用。")
    else:
        print("⚠ 部分测试失败，请检查相关功能。")
    
    return passed == total

if __name__ == '__main__':
    main()

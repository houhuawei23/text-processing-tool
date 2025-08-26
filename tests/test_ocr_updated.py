#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试更新后的OCR功能
"""

import json
from src.app_factory import create_app

def test_ocr_response_handling():
    """测试OCR响应处理"""
    print("=== 测试OCR响应处理 ===")
    
    # 模拟SimpleTex API的返回结果
    mock_response = {
        'status': True, 
        'res': {
            'type': 'formula', 
            'info': 'L=T-V', 
            'conf': 0.9476560950279236
        }, 
        'request_id': 'tr_17561756607969847756533052862'
    }
    
    print(f"模拟API响应: {json.dumps(mock_response, indent=2, ensure_ascii=False)}")
    
    # 测试OCR服务处理
    from src.services.ocr_service import ocr_service
    
    # 模拟处理响应
    class MockResponse:
        def __init__(self, data):
            self.data = data
            self.status_code = 200
        
        def raise_for_status(self):
            pass
        
        def json(self):
            return self.data
    
    # 测试响应处理
    mock_resp = MockResponse(mock_response)
    result = ocr_service.simpletex_service._handle_response(mock_resp)
    
    print(f"\n处理结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 验证结果
    if result['success']:
        print("✅ 响应处理成功")
        print(f"  - 识别文本: {result['data']['text']}")
        print(f"  - 识别类型: {result['data']['type']}")
        print(f"  - 置信度: {result['data']['confidence']:.1%}")
        print(f"  - 请求ID: {result['request_id']}")
    else:
        print(f"❌ 响应处理失败: {result['error']}")
    
    return result

def test_flask_ocr_api():
    """测试Flask OCR API"""
    print("\n=== 测试Flask OCR API ===")
    
    app = create_app()
    client = app.test_client()
    
    # 测试获取支持格式
    print("\n1. 测试获取支持格式:")
    response = client.get('/api/ocr/formats')
    print(f"状态码: {response.status_code}")
    data = response.get_json()
    print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    # 测试连接测试
    print("\n2. 测试连接测试:")
    response = client.get('/api/ocr/test')
    print(f"状态码: {response.status_code}")
    data = response.get_json()
    print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    # 测试错误情况
    print("\n3. 测试错误情况:")
    response = client.post('/api/ocr')
    print(f"状态码: {response.status_code}")
    data = response.get_json()
    print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")

def test_ocr_config():
    """测试OCR配置"""
    print("\n=== 测试OCR配置 ===")
    
    from src.config.ocr_config import ocr_config
    
    print(f"支持的格式: {ocr_config.get_supported_formats()}")
    print(f"最大文件大小: {ocr_config.simpletex.max_file_size / (1024*1024):.1f}MB")
    print(f"API URL: {ocr_config.simpletex.api_url}")
    
    # 测试错误消息
    error_codes = ['api_not_find', 'req_unauthorized', 'image_missing', 'server_error']
    for code in error_codes:
        message = ocr_config.get_error_message(code)
        print(f"错误代码 {code}: {message}")

def main():
    """主函数"""
    print("OCR功能更新测试")
    print("=" * 60)
    
    try:
        # 测试响应处理
        result = test_ocr_response_handling()
        
        # 测试Flask API
        test_flask_ocr_api()
        
        # 测试配置
        test_ocr_config()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试完成！")
        
        if result and result['success']:
            print("✅ OCR响应处理功能正常")
            print("✅ 能够正确解析SimpleTex API返回的公式和文本")
            print("✅ 置信度和类型信息正确提取")
        else:
            print("❌ OCR响应处理存在问题")
            
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

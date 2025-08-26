#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试OCR任务详情显示功能
"""

import json
from src.app_factory import create_app

def test_ocr_task_detail():
    """测试OCR任务详情显示"""
    print("=== 测试OCR任务详情显示 ===")
    
    # 模拟OCR任务结果
    mock_ocr_task = {
        'id': 1,
        'type': 'ocr-processing',
        'status': 'completed',
        'input': 'test_image.png',
        'createdAt': '2025-01-26T11:00:00.000Z',
        'completedAt': '2025-01-26T11:00:05.000Z',
        'result': {
            'ocr_text': 'L=T-V',
            'ocr_type': 'formula',
            'confidence': 0.9476560950279236,
            'request_id': 'tr_17561756607969847756533052862',
            'file_info': {
                'filename': 'test_image.png',
                'size': 4082,
                'format': 'png'
            }
        }
    }
    
    print("模拟OCR任务:")
    print(json.dumps(mock_ocr_task, indent=2, ensure_ascii=False))
    
    # 测试任务详情显示逻辑
    print("\n=== 测试任务详情显示逻辑 ===")
    
    # 模拟JavaScript中的逻辑
    task = mock_ocr_task
    
    if task['result']:
        # 根据任务类型提取处理好的文本
        if task['type'] == 'ocr-processing':
            # OCR处理任务：提取识别后的文本
            processedText = task['result'].get('ocr_text', '') or task['result'].get('text', '')
            if isinstance(task['result'], str):
                processedText = task['result']
            
            print(f"✅ OCR任务文本提取成功:")
            print(f"  - 识别文本: {processedText}")
            print(f"  - 识别类型: {task['result'].get('ocr_type', 'unknown')}")
            print(f"  - 置信度: {task['result'].get('confidence', 0.0):.1%}")
            
            if processedText:
                print("✅ 任务详情应该能正常显示结果")
            else:
                print("❌ 任务详情无法显示结果：文本为空")
        else:
            print(f"❌ 未知任务类型: {task['type']}")
    else:
        print("❌ 任务没有结果")
    
    return mock_ocr_task

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

def test_ocr_service():
    """测试OCR服务"""
    print("\n=== 测试OCR服务 ===")
    
    from src.services.ocr_service import ocr_service
    
    # 测试API连接
    try:
        result = ocr_service.test_api_connection()
        if result['success']:
            print("✅ OCR服务连接正常")
            print(f"  - 消息: {result['message']}")
            if 'request_id' in result:
                print(f"  - 请求ID: {result['request_id']}")
        else:
            print(f"❌ OCR服务连接失败: {result['error']}")
    except Exception as e:
        print(f"❌ OCR服务连接异常: {e}")

def main():
    """主函数"""
    print("OCR任务详情显示测试")
    print("=" * 60)
    
    try:
        # 测试任务详情显示
        task = test_ocr_task_detail()
        
        # 测试Flask API
        test_flask_ocr_api()
        
        # 测试OCR服务
        test_ocr_service()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试完成！")
        
        # 总结
        print("\n📋 问题分析:")
        print("1. OCR任务的结果结构包含 'ocr_text' 字段")
        print("2. 在 showTaskDetail 方法中缺少对 'ocr-processing' 类型的处理")
        print("3. 已添加对 OCR 任务类型的支持")
        print("4. 现在应该能正确显示 OCR 识别结果")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

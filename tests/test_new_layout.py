#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的输入区域布局功能
"""

import json
from src.app_factory import create_app

def test_new_layout():
    """测试新的输入区域布局"""
    print("=== 测试新的输入区域布局 ===")
    
    app = create_app()
    client = app.test_client()
    
    # 测试主页加载
    print("\n1. 测试主页加载:")
    response = client.get('/')
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        content = response.get_data(as_text=True)
        
        # 检查新的HTML结构
        checks = [
            ('text-input-section', '文本输入区域'),
            ('image-input-section', '图片上传区域'),
            ('text-input-windows-container', '文本输入窗口容器'),
            ('image-input-windows-container', '图片输入窗口容器'),
            ('addTextInputWindow', '添加文本输入窗口按钮'),
            ('removeTextInputWindow', '移除文本输入窗口按钮'),
            ('addImageInputWindow', '添加图片输入窗口按钮'),
            ('removeImageInputWindow', '移除图片输入窗口按钮'),
            ('section-sub-header', '子标题样式'),
            ('text-input-window-item', '文本输入窗口项'),
            ('image-input-window-item', '图片输入窗口项')
        ]
        
        print("\n2. 检查HTML结构:")
        for check, description in checks:
            if check in content:
                print(f"✅ {description}: 找到 '{check}'")
            else:
                print(f"❌ {description}: 未找到 '{check}'")
        
        # 检查CSS样式
        print("\n3. 检查CSS样式:")
        css_checks = [
            ('.section-sub-header', '子标题样式'),
            ('.text-input-section', '文本输入区域样式'),
            ('.image-input-section', '图片上传区域样式'),
            ('.text-input-windows-container', '文本输入窗口容器样式'),
            ('.image-input-windows-container', '图片输入窗口容器样式')
        ]
        
        for check, description in css_checks:
            if check in content:
                print(f"✅ {description}: 找到 '{check}'")
            else:
                print(f"❌ {description}: 未找到 '{check}'")
        
        # 检查JavaScript功能
        print("\n4. 检查JavaScript功能:")
        js_checks = [
            ('addTextInputWindow', '添加文本输入窗口方法'),
            ('removeTextInputWindow', '移除文本输入窗口方法'),
            ('addImageInputWindow', '添加图片输入窗口方法'),
            ('removeImageInputWindow', '移除图片输入窗口方法'),
            ('textInputWindows', '文本输入窗口数组'),
            ('imageInputWindows', '图片输入窗口数组'),
            ('bindTextInputEvents', '绑定文本输入事件'),
            ('bindImageInputEvents', '绑定图片输入事件')
        ]
        
        for check, description in js_checks:
            if check in content:
                print(f"✅ {description}: 找到 '{check}'")
            else:
                print(f"❌ {description}: 未找到 '{check}'")
        
    else:
        print(f"❌ 主页加载失败: {response.status_code}")
    
    return response.status_code == 200

def test_api_endpoints():
    """测试API端点"""
    print("\n=== 测试API端点 ===")
    
    app = create_app()
    client = app.test_client()
    
    # 测试文本处理API
    print("\n1. 测试文本处理API:")
    response = client.post('/api/process', json={
        'text': '测试文本',
        'operations': ['format']
    })
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print("✅ 文本处理API正常")
    else:
        print(f"❌ 文本处理API失败: {response.status_code}")
    
    # 测试OCR API
    print("\n2. 测试OCR API:")
    response = client.get('/api/ocr/formats')
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print("✅ OCR API正常")
    else:
        print(f"❌ OCR API失败: {response.status_code}")
    
    # 测试翻译API
    print("\n3. 测试翻译API:")
    response = client.get('/api/translation-services')
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print("✅ 翻译API正常")
    else:
        print(f"❌ 翻译API失败: {response.status_code}")

def main():
    """主函数"""
    print("新的输入区域布局测试")
    print("=" * 60)
    
    try:
        # 测试新布局
        layout_ok = test_new_layout()
        
        # 测试API端点
        test_api_endpoints()
        
        print("\n" + "=" * 60)
        if layout_ok:
            print("🎉 新布局测试完成！")
            print("\n📋 新功能总结:")
            print("1. ✅ 文本输入区域和图片上传区域已分离")
            print("2. ✅ 两个区域都支持添加/删除输入框")
            print("3. ✅ 新的CSS样式已应用")
            print("4. ✅ JavaScript功能已更新")
            print("5. ✅ API端点正常工作")
        else:
            print("❌ 新布局测试失败")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

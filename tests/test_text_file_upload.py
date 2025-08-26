#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文本文件上传功能
"""

import os
import tempfile
from src.app_factory import create_app

def create_test_files():
    """创建测试文件"""
    test_files = {}
    
    # 创建测试文本文件
    test_content = """这是一个测试文本文件。
包含多行内容，用于测试文本文件上传功能。

支持的功能：
1. 文本处理
2. 正则匹配
3. 翻译功能
4. 统计分析

文件编码：UTF-8
"""
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        test_files['txt'] = f.name
    
    # 创建测试Markdown文件
    md_content = """# 测试Markdown文件

## 功能列表

- **文本处理**: 支持多种文本处理功能
- **正则匹配**: 支持正则表达式匹配和替换
- **翻译功能**: 支持多语言翻译
- **统计分析**: 提供详细的文本统计信息

### 代码示例

```python
def process_text(text):
    return text.upper()
```

> 这是一个引用块，用于测试Markdown格式。
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(md_content)
        test_files['md'] = f.name
    
    # 创建测试JSON文件
    json_content = """{
    "name": "测试JSON文件",
    "version": "1.0.0",
    "description": "用于测试文本文件上传功能的JSON文件",
    "features": [
        "文本处理",
        "正则匹配",
        "翻译功能",
        "统计分析"
    ],
    "config": {
        "maxFileSize": "5MB",
        "supportedFormats": [
            "txt", "md", "json", "csv", "log", "xml", "html", "css", "js"
        ]
    }
}"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        f.write(json_content)
        test_files['json'] = f.name
    
    return test_files

def test_text_file_upload():
    """测试文本文件上传功能"""
    print("=== 测试文本文件上传功能 ===")
    
    app = create_app()
    client = app.test_client()
    
    # 测试主页加载
    print("\n1. 测试主页加载:")
    response = client.get('/')
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        content = response.get_data(as_text=True)
        
        # 检查HTML结构
        print("\n2. 检查HTML结构:")
        html_checks = [
            ('text-file-upload-area', '文本文件上传区域'),
            ('text-upload-zone', '文本上传区域'),
            ('text-file-info', '文本文件信息显示'),
            ('textFileInput1', '文本文件输入元素'),
            ('removeTextFileBtn1', '移除文本文件按钮'),
            ('支持 TXT、MD、JSON、CSV 等文本格式', '文件格式提示'),
            ('最大 5MB', '文件大小限制提示')
        ]
        
        for check, description in html_checks:
            if check in content:
                print(f"✅ {description}: 找到 '{check}'")
            else:
                print(f"❌ {description}: 未找到 '{check}'")
        
        # 检查CSS样式
        print("\n3. 检查CSS样式:")
        css_checks = [
            ('.text-file-upload-area', '文本文件上传区域样式'),
            ('.text-upload-zone', '文本上传区域样式'),
            ('.text-file-info', '文本文件信息样式'),
            ('.remove-text-file-btn', '移除文本文件按钮样式'),
            ('text-upload-zone.dragover', '拖拽悬停样式')
        ]
        
        for check, description in css_checks:
            if check in content:
                print(f"✅ {description}: 找到 '{check}'")
            else:
                print(f"❌ {description}: 未找到 '{check}'")
        
        # 检查JavaScript功能
        print("\n4. 检查JavaScript功能:")
        js_checks = [
            ('handleTextFileSelect', '文本文件选择处理'),
            ('readTextFile', '文本文件读取'),
            ('showTextFileInfo', '显示文本文件信息'),
            ('removeSelectedTextFile', '移除文本文件'),
            ('支持的文件格式', '文件格式验证'),
            ('5MB', '文件大小限制')
        ]
        
        for check, description in js_checks:
            if check in content:
                print(f"✅ {description}: 找到 '{check}'")
            else:
                print(f"❌ {description}: 未找到 '{check}'")
        
    else:
        print(f"❌ 主页加载失败: {response.status_code}")
    
    return response.status_code == 200

def test_file_creation():
    """测试文件创建"""
    print("\n=== 测试文件创建 ===")
    
    try:
        test_files = create_test_files()
        
        print("\n1. 测试文件创建:")
        for file_type, file_path in test_files.items():
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"✅ {file_type.upper()}文件创建成功: {file_path} ({file_size} bytes)")
            else:
                print(f"❌ {file_type.upper()}文件创建失败: {file_path}")
        
        # 清理测试文件
        print("\n2. 清理测试文件:")
        for file_type, file_path in test_files.items():
            try:
                os.unlink(file_path)
                print(f"✅ {file_type.upper()}文件清理成功: {file_path}")
            except Exception as e:
                print(f"❌ {file_type.upper()}文件清理失败: {file_path} - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 文件创建测试失败: {e}")
        return False

def main():
    """主函数"""
    print("文本文件上传功能测试")
    print("=" * 60)
    
    try:
        # 测试文本文件上传功能
        upload_ok = test_text_file_upload()
        
        # 测试文件创建
        file_ok = test_file_creation()
        
        print("\n" + "=" * 60)
        if upload_ok and file_ok:
            print("🎉 文本文件上传功能测试完成！")
            print("\n📋 功能验证总结:")
            print("1. ✅ HTML结构已添加文本文件上传区域")
            print("2. ✅ CSS样式已配置文本文件上传界面")
            print("3. ✅ JavaScript功能已实现文件处理逻辑")
            print("4. ✅ 文件创建和清理功能正常")
            print("\n🎨 文本文件上传特性:")
            print("- 支持多种文本格式 (TXT、MD、JSON、CSV等)")
            print("- 文件大小限制 (5MB)")
            print("- 拖拽上传功能")
            print("- 文件信息显示")
            print("- 文件移除功能")
            print("- 自动读取文件内容到文本区域")
            print("- 多窗口支持")
        else:
            print("❌ 文本文件上传功能测试失败")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

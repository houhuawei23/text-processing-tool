#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test script to verify the restructured application works correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing imports...")
    
    try:
        from src import create_app
        print("✅ create_app imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import create_app: {e}")
        return False
    
    try:
        from src.core.text_processor import text_processor
        print("✅ text_processor imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import text_processor: {e}")
        return False
    
    try:
        from src.config.app_config import AppConfig
        print("✅ AppConfig imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import AppConfig: {e}")
        return False
    
    try:
        from src.config.translation_config import TranslationConfig
        print("✅ TranslationConfig imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import TranslationConfig: {e}")
        return False
    
    return True


def test_text_processing():
    """Test basic text processing functionality."""
    print("\nTesting text processing...")
    
    try:
        from src.core.text_processor import text_processor
        
        test_text = "This is a test text. It contains multiple sentences! And some numbers 123."
        
        # Test basic processing
        result = text_processor.process_text(test_text)
        print("✅ Basic text processing works")
        
        # Test regex processing
        regex_rules = [("test", "TEST"), ("text", "TEXT")]
        regex_result = text_processor.process_text_with_regex(test_text, regex_rules)
        print("✅ Regex processing works")
        
        # Test statistics
        if 'statistics' in result and 'basic' in result['statistics']:
            stats = result['statistics']['basic']
            print(f"✅ Statistics generated: {stats['characters']} chars, {stats['words']} words, {stats['sentences']} sentences")
        
        return True
        
    except Exception as e:
        print(f"❌ Text processing failed: {e}")
        return False


def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from src.config.app_config import AppConfig
        from src.config.translation_config import TranslationConfig
        
        # Test AppConfig
        print(f"✅ App name: {AppConfig.APP_NAME}")
        print(f"✅ App version: {AppConfig.APP_VERSION}")
        print(f"✅ Default port: {AppConfig.DEFAULT_PORT}")
        
        # Test TranslationConfig
        print(f"✅ Default translation service: {TranslationConfig.DEFAULT_TRANSLATION_SERVICE}")
        print(f"✅ Available services: {list(TranslationConfig.AVAILABLE_SERVICES.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_app_creation():
    """Test Flask app creation."""
    print("\nTesting Flask app creation...")
    
    try:
        from src import create_app
        
        app = create_app()
        print("✅ Flask app created successfully")
        
        # Test basic app properties
        print(f"✅ App name: {app.name}")
        print(f"✅ App config: {app.config.get('APP_NAME', 'Not set')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False


def main():
    """Main test function."""
    print("🧪 Testing Restructured Application")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_configuration),
        ("Text Processing Test", test_text_processing),
        ("Flask App Test", test_app_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The restructured application is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 
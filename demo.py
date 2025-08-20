#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstration Script for Restructured Application
Shows the capabilities and improvements of the restructured text processing application.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_text_processing():
    """Demonstrate text processing capabilities."""
    print("🔤 Text Processing Demo")
    print("=" * 50)
    
    from src.core.text_processor import text_processor
    
    # Sample text
    sample_text = """
    This is a sample text for demonstration purposes. It contains multiple sentences!
    The text has some formatting issues    with extra spaces and inconsistent punctuation.
    We will process this text to clean it up and analyze its content.
    """
    
    print(f"Original text:\n{sample_text}")
    
    # Process text
    result = text_processor.process_text(sample_text)
    
    print(f"\nProcessed text:\n{result['processed_text']}")
    
    # Show statistics
    if 'statistics' in result:
        stats = result['statistics']
        print(f"\n📊 Statistics:")
        print(f"  Characters: {stats['basic']['characters']}")
        print(f"  Words: {stats['basic']['words']}")
        print(f"  Sentences: {stats['basic']['sentences']}")
        print(f"  Lines: {stats['basic']['lines']}")
    
    # Show analysis
    if 'analysis' in result:
        analysis = result['analysis']
        print(f"\n📈 Analysis:")
        print(f"  Readability Score: {analysis['readability']['flesch_reading_ease']}")
        print(f"  Sentiment: {analysis['sentiment']['sentiment']}")
        print(f"  Language Type: {analysis['language_features']['language_type']}")


def demo_regex_processing():
    """Demonstrate regex processing capabilities."""
    print("\n\n🔍 Regex Processing Demo")
    print("=" * 50)
    
    from src.core.text_processor import text_processor
    
    # Sample text
    sample_text = "Hello world! This is a test text with some patterns to replace."
    
    # Regex rules
    regex_rules = [
        ("Hello", "Hi"),
        ("test", "demo"),
        ("world", "universe"),
        (r"\s+", " ")  # Replace multiple spaces with single space
    ]
    
    print(f"Original text: {sample_text}")
    print(f"Regex rules: {regex_rules}")
    
    # Process with regex
    result = text_processor.process_text_with_regex(sample_text, regex_rules)
    
    print(f"Processed text: {result['processed_text']}")


def demo_text_analysis():
    """Demonstrate text analysis capabilities."""
    print("\n\n📊 Text Analysis Demo")
    print("=" * 50)
    
    from src.core.text_analyzer import TextAnalyzer
    
    analyzer = TextAnalyzer()
    
    # Sample texts
    texts = [
        "I love this amazing product! It's fantastic and wonderful.",
        "This is terrible. I hate it. It's awful and disappointing.",
        "This is a neutral text with no strong emotions."
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\nText {i}: {text}")
        
        # Analyze sentiment
        analysis = analyzer.analyze_text(text)
        sentiment = analysis['sentiment']
        
        print(f"  Sentiment: {sentiment['sentiment']}")
        print(f"  Positive ratio: {sentiment['positive_ratio']:.3f}")
        print(f"  Negative ratio: {sentiment['negative_ratio']:.3f}")


def demo_configuration():
    """Demonstrate configuration capabilities."""
    print("\n\n⚙️ Configuration Demo")
    print("=" * 50)
    
    from src.config.app_config import AppConfig
    from src.config.translation_config import TranslationConfig
    
    print("Application Configuration:")
    print(f"  Name: {AppConfig.APP_NAME}")
    print(f"  Version: {AppConfig.APP_VERSION}")
    print(f"  Default Port: {AppConfig.DEFAULT_PORT}")
    print(f"  Max File Size: {AppConfig.MAX_FILE_SIZE // (1024*1024)}MB")
    
    print("\nTranslation Configuration:")
    print(f"  Default Service: {TranslationConfig.DEFAULT_TRANSLATION_SERVICE}")
    print(f"  Available Services: {list(TranslationConfig.AVAILABLE_SERVICES.keys())}")
    
    # Show enabled services
    enabled_services = TranslationConfig.get_enabled_services()
    print(f"  Enabled Services: {list(enabled_services.keys())}")


def demo_validation():
    """Demonstrate input validation capabilities."""
    print("\n\n✅ Input Validation Demo")
    print("=" * 50)
    
    from src.utils.validators import validate_text_input, validate_regex_rules
    
    # Test cases
    test_cases = [
        ("Valid text", "This is valid text"),
        ("Empty text", ""),
        ("None text", None),
        ("Non-string", 123),
        ("Very long text", "x" * 1000000)
    ]
    
    for test_name, text in test_cases:
        result = validate_text_input(text)
        status = "✅ Valid" if result['valid'] else "❌ Invalid"
        print(f"  {test_name}: {status}")
        if not result['valid']:
            print(f"    Error: {result['error']}")
    
    # Test regex rules
    print("\nRegex Rules Validation:")
    regex_test_cases = [
        ("Valid rules", [["pattern", "replacement"]]),
        ("Empty rules", []),
        ("Invalid rule", [["pattern"]]),  # Missing replacement
        ("Invalid pattern", [["[invalid", "replacement"]])  # Invalid regex
    ]
    
    for test_name, rules in regex_test_cases:
        result = validate_regex_rules(rules)
        status = "✅ Valid" if result['valid'] else "❌ Invalid"
        print(f"  {test_name}: {status}")
        if not result['valid']:
            print(f"    Error: {result['error']}")


def demo_api_responses():
    """Demonstrate API response helpers."""
    print("\n\n🌐 API Response Demo")
    print("=" * 50)
    
    from src.utils.response_helpers import (
        create_success_response, 
        create_error_response,
        create_validation_error_response
    )
    
    # Create a simple Flask app context for testing
    from flask import Flask
    app = Flask(__name__)
    
    with app.app_context():
        # Success response
        success_data = {"message": "Text processed successfully", "characters": 150}
        success_response = create_success_response(success_data, "Processing completed")
        print("Success Response:")
        print(f"  {success_response.json}")
        
        # Error response
        error_response = create_error_response("Invalid input", 400, {"field": "text"})
        print("\nError Response:")
        print(f"  {error_response[0].json}")
        print(f"  Status Code: {error_response[1]}")


def main():
    """Main demonstration function."""
    print("🎯 Restructured Application Demonstration")
    print("=" * 60)
    print("This demo showcases the improvements and capabilities")
    print("of the restructured text processing application.\n")
    
    try:
        # Run demonstrations
        demo_text_processing()
        demo_regex_processing()
        demo_text_analysis()
        demo_configuration()
        demo_validation()
        demo_api_responses()
        
        print("\n" + "=" * 60)
        print("🎉 Demonstration completed successfully!")
        print("The restructured application is working correctly.")
        print("\nKey improvements demonstrated:")
        print("  ✅ Modular architecture")
        print("  ✅ Comprehensive validation")
        print("  ✅ Better error handling")
        print("  ✅ Centralized configuration")
        print("  ✅ Standardized API responses")
        print("  ✅ Enhanced text processing")
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        print("Please check that all modules are properly installed.")
        return False
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 
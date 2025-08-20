#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic functionality tests for the restructured application.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.text_processor import text_processor
from core.text_analyzer import TextAnalyzer
from core.text_formatter import TextFormatter
from config.app_config import AppConfig
from config.translation_config import TranslationConfig


class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality of the restructured application."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_text = "This is a test text. It contains multiple sentences! And some numbers 123."
        self.analyzer = TextAnalyzer()
        self.formatter = TextFormatter()
    
    def test_text_processor_initialization(self):
        """Test that text processor initializes correctly."""
        self.assertIsNotNone(text_processor)
        self.assertIsNotNone(text_processor.analyzer)
        self.assertIsNotNone(text_processor.formatter)
    
    def test_text_processing(self):
        """Test basic text processing functionality."""
        result = text_processor.process_text(self.test_text)
        
        self.assertIsNotNone(result)
        self.assertIn('original_text', result)
        self.assertIn('processed_text', result)
        self.assertIn('statistics', result)
        self.assertIn('analysis', result)
        self.assertEqual(result['original_text'], self.test_text)
    
    def test_text_analysis(self):
        """Test text analysis functionality."""
        stats = self.analyzer.generate_statistics(self.test_text)
        
        self.assertIsNotNone(stats)
        self.assertIn('basic', stats)
        self.assertIn('character_types', stats)
        self.assertIn('word_frequency', stats)
        self.assertIn('averages', stats)
        
        # Check basic statistics
        basic_stats = stats['basic']
        self.assertGreater(basic_stats['characters'], 0)
        self.assertGreater(basic_stats['words'], 0)
        self.assertGreater(basic_stats['sentences'], 0)
    
    def test_text_formatting(self):
        """Test text formatting functionality."""
        formatted_text = self.formatter.format_text(self.test_text)
        
        self.assertIsNotNone(formatted_text)
        self.assertIsInstance(formatted_text, str)
        self.assertGreater(len(formatted_text), 0)
    
    def test_regex_processing(self):
        """Test regex processing functionality."""
        regex_rules = [("test", "TEST"), ("text", "TEXT")]
        result = text_processor.process_text_with_regex(self.test_text, regex_rules)
        
        self.assertIsNotNone(result)
        self.assertIn('original_text', result)
        self.assertIn('processed_text', result)
        self.assertIn('regex_rules', result)
        self.assertEqual(result['original_text'], self.test_text)
    
    def test_configuration(self):
        """Test configuration loading."""
        # Test AppConfig
        self.assertIsNotNone(AppConfig.APP_NAME)
        self.assertIsNotNone(AppConfig.APP_VERSION)
        self.assertIsInstance(AppConfig.DEFAULT_PORT, int)
        
        # Test TranslationConfig
        self.assertIsNotNone(TranslationConfig.DEFAULT_TRANSLATION_SERVICE)
        self.assertIsInstance(TranslationConfig.AVAILABLE_SERVICES, dict)
    
    def test_input_validation(self):
        """Test input validation."""
        # Test empty text
        result = text_processor.process_text("")
        self.assertIn('error', result)
        
        # Test None text
        result = text_processor.process_text(None)
        self.assertIn('error', result)
    
    def test_regex_rule_parsing(self):
        """Test regex rule parsing."""
        rules_text = """
        (test, TEST)
        (text, TEXT)
        """
        rules = self.formatter.parse_regex_rules_from_text(rules_text)
        
        self.assertIsInstance(rules, list)
        self.assertGreater(len(rules), 0)
        
        for rule in rules:
            self.assertIsInstance(rule, tuple)
            self.assertEqual(len(rule), 2)


if __name__ == '__main__':
    unittest.main() 
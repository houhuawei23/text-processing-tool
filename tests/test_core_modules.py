#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for core modules.
Tests text processor, analyzer, and formatter functionality.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.text_processor import TextProcessor, text_processor
from core.text_analyzer import TextAnalyzer
from core.text_formatter import TextFormatter


class TestTextProcessor(unittest.TestCase):
    """Test TextProcessor class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = TextProcessor()
        self.test_text = "Hello world! This is a test text. It contains multiple sentences."
        self.chinese_text = "你好世界！这是一个测试文本。它包含多个句子。"
        self.mixed_text = "Hello 世界! This is 测试 text. 它包含 multiple sentences."
    
    def test_initialization(self):
        """Test TextProcessor initialization."""
        self.assertIsNotNone(self.processor.analyzer)
        self.assertIsNotNone(self.processor.formatter)
        self.assertEqual(len(self.processor.processing_history), 0)
    
    def test_process_text_basic(self):
        """Test basic text processing."""
        result = self.processor.process_text(self.test_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['original_text'], self.test_text)
        self.assertIn('processed_text', result)
        self.assertIn('statistics', result)
        self.assertIn('analysis', result)
        self.assertIn('operations', result)
        self.assertIn('timestamp', result)
        self.assertIsNone(result['error'])
    
    def test_process_text_with_specific_operations(self):
        """Test text processing with specific operations."""
        result = self.processor.process_text(self.test_text, ['format', 'statistics'])
        
        self.assertIsNotNone(result)
        self.assertEqual(result['operations'], ['format', 'statistics'])
        self.assertIn('statistics', result)
        # Note: analysis field is always included but may be empty
        self.assertIn('analysis', result)
        # Check that analysis is empty when not requested
        self.assertEqual(result['analysis'], {})
    
    def test_process_text_with_regex(self):
        """Test regex text processing."""
        regex_rules = [("Hello", "Hi"), ("world", "universe")]
        result = self.processor.process_text_with_regex(self.test_text, regex_rules)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['original_text'], self.test_text)
        self.assertIn('processed_text', result)
        self.assertEqual(result['regex_rules'], regex_rules)
        self.assertIsNone(result['error'])
    
    def test_input_validation(self):
        """Test input validation."""
        # Test None input
        result = self.processor.process_text(None)
        self.assertIn('error', result)
        
        # Test empty input
        result = self.processor.process_text("")
        self.assertIn('error', result)
        
        # Test whitespace-only input
        result = self.processor.process_text("   ")
        self.assertIn('error', result)
        
        # Test non-string input
        result = self.processor.process_text(123)
        self.assertIn('error', result)
    
    def test_processing_history(self):
        """Test processing history recording."""
        initial_history_length = len(self.processor.processing_history)
        
        self.processor.process_text(self.test_text)
        
        self.assertEqual(len(self.processor.processing_history), initial_history_length + 1)
        
        history_entry = self.processor.processing_history[-1]
        self.assertIn('timestamp', history_entry)
        self.assertIn('operations', history_entry)
        self.assertIn('text_length', history_entry)
    
    def test_clear_history(self):
        """Test history clearing."""
        self.processor.process_text(self.test_text)
        self.assertGreater(len(self.processor.processing_history), 0)
        
        self.processor.clear_history()
        self.assertEqual(len(self.processor.processing_history), 0)
    
    def test_global_instance(self):
        """Test global text processor instance."""
        self.assertIsNotNone(text_processor)
        self.assertIsInstance(text_processor, TextProcessor)


class TestTextAnalyzer(unittest.TestCase):
    """Test TextAnalyzer class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = TextAnalyzer()
        self.test_text = "Hello world! This is a test text. It contains multiple sentences."
        self.chinese_text = "你好世界！这是一个测试文本。它包含多个句子。"
        self.mixed_text = "Hello 世界! This is 测试 text. 它包含 multiple sentences."
    
    def test_generate_statistics_basic(self):
        """Test basic statistics generation."""
        stats = self.analyzer.generate_statistics(self.test_text)
        
        self.assertIsNotNone(stats)
        self.assertIn('basic', stats)
        self.assertIn('character_types', stats)
        self.assertIn('word_frequency', stats)
        self.assertIn('averages', stats)
        
        # Check basic statistics
        basic = stats['basic']
        self.assertGreater(basic['characters'], 0)
        self.assertGreater(basic['words'], 0)
        self.assertGreater(basic['sentences'], 0)
        self.assertGreater(basic['lines'], 0)
    
    def test_generate_statistics_empty(self):
        """Test statistics generation with empty text."""
        stats = self.analyzer.generate_statistics("")
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats['basic']['characters'], 0)
        self.assertEqual(stats['basic']['words'], 0)
        self.assertEqual(stats['basic']['sentences'], 0)
    
    def test_analyze_text(self):
        """Test text analysis."""
        analysis = self.analyzer.analyze_text(self.test_text)
        
        self.assertIsNotNone(analysis)
        self.assertIn('readability', analysis)
        self.assertIn('sentiment', analysis)
        self.assertIn('language_features', analysis)
        
        # Check readability
        readability = analysis['readability']
        self.assertIn('flesch_reading_ease', readability)
        self.assertIn('average_sentence_length', readability)
        
        # Check sentiment
        sentiment = analysis['sentiment']
        self.assertIn('sentiment', sentiment)
        self.assertIn('positive_ratio', sentiment)
        self.assertIn('negative_ratio', sentiment)
        
        # Check language features
        features = analysis['language_features']
        self.assertIn('language_type', features)
        self.assertIn('chinese_ratio', features)
        self.assertIn('english_ratio', features)
    
    def test_character_statistics(self):
        """Test character type statistics."""
        stats = self.analyzer.generate_statistics(self.test_text)
        char_stats = stats['character_types']
        
        self.assertIn('letters', char_stats)
        self.assertIn('digits', char_stats)
        self.assertIn('spaces', char_stats)
        self.assertIn('punctuation', char_stats)
        
        # Verify totals
        total_chars = char_stats['letters'] + char_stats['digits'] + char_stats['spaces'] + char_stats['punctuation']
        self.assertEqual(total_chars, len(self.test_text))
    
    def test_word_frequency(self):
        """Test word frequency analysis."""
        stats = self.analyzer.generate_statistics(self.test_text)
        word_freq = stats['word_frequency']
        
        self.assertIsInstance(word_freq, list)
        # Should not include very common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        for word, count in word_freq:
            self.assertNotIn(word.lower(), stop_words)
    
    def test_language_detection(self):
        """Test language type detection."""
        # Test English text
        analysis = self.analyzer.analyze_text(self.test_text)
        self.assertEqual(analysis['language_features']['language_type'], 'english')
        
        # Test Chinese text
        analysis = self.analyzer.analyze_text(self.chinese_text)
        self.assertEqual(analysis['language_features']['language_type'], 'chinese')
        
        # Test mixed text
        analysis = self.analyzer.analyze_text(self.mixed_text)
        self.assertEqual(analysis['language_features']['language_type'], 'mixed')
    
    def test_sentiment_analysis(self):
        """Test sentiment analysis."""
        # Test positive text
        positive_text = "I love this amazing product! It's fantastic and wonderful."
        analysis = self.analyzer.analyze_text(positive_text)
        self.assertEqual(analysis['sentiment']['sentiment'], 'positive')
        
        # Test negative text
        negative_text = "This is terrible. I hate it. It's awful and disappointing."
        analysis = self.analyzer.analyze_text(negative_text)
        self.assertEqual(analysis['sentiment']['sentiment'], 'negative')
        
        # Test neutral text
        neutral_text = "This is a neutral text with no strong emotions."
        analysis = self.analyzer.analyze_text(neutral_text)
        self.assertEqual(analysis['sentiment']['sentiment'], 'neutral')


class TestTextFormatter(unittest.TestCase):
    """Test TextFormatter class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.formatter = TextFormatter()
        self.test_text = "Hello   world!   This   is   a   test   text."
        self.test_text_with_punctuation = "Hello world. This is a test text! And another sentence?"
    
    def test_format_text_basic(self):
        """Test basic text formatting."""
        formatted = self.formatter.format_text(self.test_text)
        
        self.assertIsNotNone(formatted)
        self.assertIsInstance(formatted, str)
        # Should normalize whitespace
        self.assertNotIn("   ", formatted)
        self.assertIn(" ", formatted)
    
    def test_format_text_empty(self):
        """Test formatting empty text."""
        formatted = self.formatter.format_text("")
        self.assertEqual(formatted, "")
        
        formatted = self.formatter.format_text(None)
        self.assertEqual(formatted, None)
    
    def test_apply_regex_replacements(self):
        """Test regex replacement functionality."""
        text = "Hello world! Hello universe!"
        rules = [("Hello", "Hi"), ("world", "universe")]
        
        result = self.formatter.apply_regex_replacements(text, rules)
        
        self.assertEqual(result, "Hi universe! Hi universe!")
    
    def test_apply_regex_replacements_empty(self):
        """Test regex replacement with empty rules."""
        text = "Hello world!"
        result = self.formatter.apply_regex_replacements(text, [])
        self.assertEqual(result, text)
    
    def test_parse_regex_rules_from_text(self):
        """Test parsing regex rules from text."""
        rules_text = """
        (r"Hello", r"Hi")
        (r"world", r"universe")
        """
        
        rules = self.formatter.parse_regex_rules_from_text(rules_text)
        
        self.assertIsInstance(rules, list)
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0], ("Hello", "Hi"))
        self.assertEqual(rules[1], ("world", "universe"))
    
    def test_parse_regex_rules_arrow_format(self):
        """Test parsing regex rules in arrow format."""
        rules_text = """
        Hello -> Hi
        world -> universe
        """
        
        rules = self.formatter.parse_regex_rules_from_text(rules_text)
        
        self.assertIsInstance(rules, list)
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0], ("Hello", "Hi"))
        self.assertEqual(rules[1], ("world", "universe"))
    
    def test_parse_regex_rules_simple_format(self):
        """Test parsing regex rules in simple format."""
        rules_text = """
        Hello=Hi
        world=universe
        """
        
        rules = self.formatter.parse_regex_rules_from_text(rules_text)
        
        self.assertIsInstance(rules, list)
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0], ("Hello", "Hi"))
        self.assertEqual(rules[1], ("world", "universe"))
    
    def test_validate_regex_pattern(self):
        """Test regex pattern validation."""
        # Valid patterns
        self.assertTrue(self.formatter.validate_regex_pattern(r"Hello"))
        self.assertTrue(self.formatter.validate_regex_pattern(r"\d+"))
        self.assertTrue(self.formatter.validate_regex_pattern(r"[a-z]+"))
        
        # Invalid patterns
        self.assertFalse(self.formatter.validate_regex_pattern(r"[invalid"))
        self.assertFalse(self.formatter.validate_regex_pattern(r"(unclosed"))
    
    def test_escape_special_characters(self):
        """Test special character escaping."""
        text = "Hello.world*test+regex"
        escaped = self.formatter.escape_special_characters(text)
        
        self.assertIn(r"\.", escaped)
        self.assertIn(r"\*", escaped)
        self.assertIn(r"\+", escaped)
    
    def test_normalize_sentence_endings(self):
        """Test sentence ending normalization."""
        text = "Hello world This is a test"
        normalized = self.formatter._normalize_sentence_endings(text)
        
        self.assertIn(".", normalized)
        self.assertTrue(normalized.endswith("."))


class TestCoreIntegration(unittest.TestCase):
    """Test integration between core modules."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = TextProcessor()
        self.test_text = "Hello world! This is a test text. It contains multiple sentences."
    
    def test_full_processing_pipeline(self):
        """Test the complete processing pipeline."""
        result = self.processor.process_text(self.test_text, ['format', 'statistics', 'analysis'])
        
        # Check that all components worked together
        self.assertIsNotNone(result['processed_text'])
        self.assertIsNotNone(result['statistics'])
        self.assertIsNotNone(result['analysis'])
        
        # Check that formatting was applied
        self.assertNotEqual(result['original_text'], result['processed_text'])
        
        # Check that statistics were generated
        self.assertGreater(result['statistics']['basic']['characters'], 0)
        
        # Check that analysis was performed
        self.assertIn('sentiment', result['analysis'])
    
    def test_regex_processing_pipeline(self):
        """Test regex processing pipeline."""
        regex_rules = [("Hello", "Hi"), ("world", "universe")]
        result = self.processor.process_text_with_regex(self.test_text, regex_rules)
        
        # Check that regex processing worked
        self.assertIn("Hi", result['processed_text'])
        self.assertIn("universe", result['processed_text'])
        self.assertNotIn("Hello", result['processed_text'])
        self.assertNotIn("world", result['processed_text'])


if __name__ == '__main__':
    unittest.main() 
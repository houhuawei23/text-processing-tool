#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive integration tests.
Tests the entire application workflow from frontend to backend.
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src import create_app
from src.core.text_processor import text_processor
from src.services.translation_service import translation_service


class TestFullApplicationIntegration(unittest.TestCase):
    """Test full application integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create temporary directories
        self.temp_dir = tempfile.mkdtemp()
        self.original_upload_folder = self.app.config.get('UPLOAD_FOLDER', 'uploads')
        self.app.config['UPLOAD_FOLDER'] = os.path.join(self.temp_dir, 'uploads')
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directories
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_complete_text_processing_workflow(self):
        """Test complete text processing workflow."""
        # Step 1: Test health endpoint
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        # Step 2: Test configuration endpoint
        response = self.client.get('/api/config')
        self.assertEqual(response.status_code, 200)
        
        # Step 3: Test text processing
        payload = {
            'text': 'Hello world! This is a comprehensive test.',
            'operations': ['format', 'statistics', 'analysis']
        }
        
        response = self.client.post('/api/process',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        
        result = data['data']
        self.assertIn('original_text', result)
        self.assertIn('processed_text', result)
        self.assertIn('statistics', result)
        self.assertIn('analysis', result)
        
        # Verify statistics
        stats = result['statistics']
        self.assertIn('basic', stats)
        self.assertIn('character_types', stats)
        self.assertIn('word_frequency', stats)
        self.assertIn('averages', stats)
        
        # Verify analysis
        analysis = result['analysis']
        self.assertIn('readability', analysis)
        self.assertIn('sentiment', analysis)
        self.assertIn('language_features', analysis)
        
        # Step 4: Test history endpoint
        response = self.client.get('/api/history')
        self.assertEqual(response.status_code, 200)
        
        # Step 5: Test clear endpoint
        response = self.client.post('/api/clear')
        self.assertEqual(response.status_code, 200)
    
    def test_complete_regex_processing_workflow(self):
        """Test complete regex processing workflow."""
        # Step 1: Test regex processing
        payload = {
            'text': 'Hello world! Hello universe!',
            'regex_rules': [['Hello', 'Hi'], ['world', 'universe']]
        }
        
        response = self.client.post('/api/regex',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        
        result = data['data']
        self.assertIn('original_text', result)
        self.assertIn('processed_text', result)
        self.assertIn('regex_rules', result)
        
        # Verify regex replacement worked
        self.assertIn('Hi', result['processed_text'])
        self.assertIn('universe', result['processed_text'])
        self.assertNotIn('Hello', result['processed_text'])
        self.assertNotIn('world', result['processed_text'])
        
        # Step 2: Test history to see regex processing was recorded
        response = self.client.get('/api/history')
        self.assertEqual(response.status_code, 200)
    
    def test_complete_translation_workflow(self):
        """Test complete translation workflow."""
        # Step 1: Test translation services endpoint
        response = self.client.get('/api/translation-services')
        self.assertEqual(response.status_code, 200)
        
        # Step 2: Test translation with mock
        with patch('src.services.translation_service.translation_service.translate_text') as mock_translate:
            mock_translate.return_value = {
                'translated_text': '你好世界！',
                'service_used': 'deepseek',
                'prompt_used': 'Translate to Chinese',
                'error': None
            }
            
            payload = {
                'text': 'Hello world!',
                'prompt': 'Translate to Chinese',
                'service_name': 'deepseek'
            }
            
            response = self.client.post('/api/translate',
                                      data=json.dumps(payload),
                                      content_type='application/json')
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            
            result = data['data']
            self.assertIn('translated_text', result)
            self.assertIn('service_used', result)
            self.assertIn('prompt_used', result)
    
    def test_error_handling_integration(self):
        """Test error handling integration."""
        # Test invalid JSON
        response = self.client.post('/api/process',
                                  data='invalid json',
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test empty text
        payload = {'text': '', 'operations': ['format']}
        response = self.client.post('/api/process',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test invalid regex rules
        payload = {'text': 'Hello', 'regex_rules': [['invalid[regex', 'replacement']]}
        response = self.client.post('/api/regex',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Test missing prompt for translation
        payload = {'text': 'Hello', 'service_name': 'deepseek'}
        response = self.client.post('/api/translate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_session_management_integration(self):
        """Test session management integration."""
        with self.client.session_transaction() as sess:
            # Test that session is created
            self.assertIsInstance(sess, dict)
            
            # Test processing history in session
            payload = {'text': 'Test text', 'operations': ['format']}
            response = self.client.post('/api/process',
                                      data=json.dumps(payload),
                                      content_type='application/json')
            self.assertEqual(response.status_code, 200)
            
            # Check that history was recorded
            response = self.client.get('/api/history')
            data = json.loads(response.data)
            self.assertIn('session_history', data['data'])
    
    def test_static_file_serving(self):
        """Test static file serving."""
        # Test CSS file
        response = self.client.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/css', response.headers['Content-Type'])
        
        # Test JavaScript file
        response = self.client.get('/static/js/app.js')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/javascript', response.headers['Content-Type'])
    
    def test_template_rendering(self):
        """Test template rendering."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)
        self.assertIn(b'Text Processing Tool', response.data)


class TestCoreServiceIntegration(unittest.TestCase):
    """Test core service integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_text = "Hello world! This is a comprehensive integration test."
        self.chinese_text = "你好世界！这是一个综合集成测试。"
        self.mixed_text = "Hello 世界! This is 测试 text. 它包含 multiple sentences."
    
    def test_text_processor_integration(self):
        """Test text processor integration with all components."""
        # Test full processing pipeline
        result = text_processor.process_text(self.test_text, ['format', 'statistics', 'analysis'])
        
        # Verify all components worked together
        self.assertIsNotNone(result['processed_text'])
        self.assertIsNotNone(result['statistics'])
        self.assertIsNotNone(result['analysis'])
        
        # Verify formatting was applied
        self.assertNotEqual(result['original_text'], result['processed_text'])
        
        # Verify statistics were generated
        stats = result['statistics']
        self.assertGreater(stats['basic']['characters'], 0)
        self.assertGreater(stats['basic']['words'], 0)
        self.assertGreater(stats['basic']['sentences'], 0)
        
        # Verify analysis was performed
        analysis = result['analysis']
        self.assertIn('sentiment', analysis)
        self.assertIn('readability', analysis)
        self.assertIn('language_features', analysis)
    
    def test_regex_processing_integration(self):
        """Test regex processing integration."""
        regex_rules = [("Hello", "Hi"), ("world", "universe"), ("test", "demo")]
        result = text_processor.process_text_with_regex(self.test_text, regex_rules)
        
        # Verify regex processing worked
        processed_text = result['processed_text']
        self.assertIn("Hi", processed_text)
        self.assertIn("universe", processed_text)
        self.assertIn("demo", processed_text)
        self.assertNotIn("Hello", processed_text)
        self.assertNotIn("world", processed_text)
        self.assertNotIn("test", processed_text)
    
    def test_language_detection_integration(self):
        """Test language detection integration."""
        # Test English text
        result = text_processor.process_text(self.test_text, ['analysis'])
        language_type = result['analysis']['language_features']['language_type']
        self.assertEqual(language_type, 'english')
        
        # Test Chinese text
        result = text_processor.process_text(self.chinese_text, ['analysis'])
        language_type = result['analysis']['language_features']['language_type']
        self.assertEqual(language_type, 'chinese')
        
        # Test mixed text
        result = text_processor.process_text(self.mixed_text, ['analysis'])
        language_type = result['analysis']['language_features']['language_type']
        self.assertEqual(language_type, 'mixed')
    
    def test_sentiment_analysis_integration(self):
        """Test sentiment analysis integration."""
        # Test positive text
        positive_text = "I love this amazing product! It's fantastic and wonderful."
        result = text_processor.process_text(positive_text, ['analysis'])
        sentiment = result['analysis']['sentiment']['sentiment']
        self.assertEqual(sentiment, 'positive')
        
        # Test negative text
        negative_text = "This is terrible. I hate it. It's awful and disappointing."
        result = text_processor.process_text(negative_text, ['analysis'])
        sentiment = result['analysis']['sentiment']['sentiment']
        self.assertEqual(sentiment, 'negative')
        
        # Test neutral text
        neutral_text = "This is a neutral text with no strong emotions."
        result = text_processor.process_text(neutral_text, ['analysis'])
        sentiment = result['analysis']['sentiment']['sentiment']
        self.assertEqual(sentiment, 'neutral')
    
    def test_processing_history_integration(self):
        """Test processing history integration."""
        # Clear history first
        text_processor.clear_history()
        initial_count = len(text_processor.processing_history)
        
        # Process some text
        text_processor.process_text(self.test_text, ['format'])
        self.assertEqual(len(text_processor.processing_history), initial_count + 1)
        
        # Process with regex
        regex_rules = [("Hello", "Hi")]
        text_processor.process_text_with_regex(self.test_text, regex_rules)
        self.assertEqual(len(text_processor.processing_history), initial_count + 2)
        
        # Verify history entries
        history = text_processor.get_processing_history()
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)
        
        # Verify history entry structure
        entry = history[-1]
        self.assertIn('timestamp', entry)
        self.assertIn('operations', entry)
        self.assertIn('text_length', entry)


class TestTranslationServiceIntegration(unittest.TestCase):
    """Test translation service integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_text = "Hello world! This is a test."
        self.test_prompt = "Translate to Chinese"
    
    @patch('src.services.translation_service.translation_service._translate_with_deepseek')
    @patch('src.services.translation_service.TranslationConfig.is_service_available')
    def test_deepseek_translation_integration(self, mock_is_available, mock_deepseek):
        """Test DeepSeek translation integration."""
        mock_is_available.return_value = True
        mock_deepseek.return_value = {
            'translated_text': '你好世界！这是一个测试。',
            'service_used': 'deepseek',
            'prompt_used': self.test_prompt,
            'error': None
        }
        
        result = translation_service.translate_text(self.test_text, self.test_prompt, 'deepseek')
        
        self.assertIsNotNone(result)
        self.assertIn('translated_text', result)
        self.assertIn('service_used', result)
        self.assertIn('prompt_used', result)
        self.assertIsNone(result['error'])
        
        self.assertEqual(result['service_used'], 'deepseek')
        self.assertEqual(result['prompt_used'], self.test_prompt)
    
    @patch('src.services.translation_service.translation_service._translate_with_openai')
    @patch('src.services.translation_service.TranslationConfig.is_service_available')
    def test_openai_translation_integration(self, mock_is_available, mock_openai):
        """Test OpenAI translation integration."""
        mock_is_available.return_value = True
        mock_openai.return_value = {
            'translated_text': '你好世界！这是一个测试。',
            'service_used': 'openai',
            'prompt_used': self.test_prompt,
            'error': None
        }
        
        result = translation_service.translate_text(self.test_text, self.test_prompt, 'openai')
        
        self.assertIsNotNone(result)
        self.assertIn('translated_text', result)
        self.assertIn('service_used', result)
        self.assertIn('prompt_used', result)
        self.assertIsNone(result['error'])
        
        self.assertEqual(result['service_used'], 'openai')
        self.assertEqual(result['prompt_used'], self.test_prompt)
    
    @patch('src.services.translation_service.translation_service._translate_with_microsoft')
    @patch('src.services.translation_service.TranslationConfig.is_service_available')
    def test_microsoft_translation_integration(self, mock_is_available, mock_microsoft):
        """Test Microsoft Translator integration."""
        mock_is_available.return_value = True
        mock_microsoft.return_value = {
            'translated_text': '你好世界！这是一个测试。',
            'service_used': 'microsoft',
            'prompt_used': self.test_prompt,
            'error': None,
            'target_language': 'zh'
        }
        
        result = translation_service.translate_text(self.test_text, self.test_prompt, 'microsoft')
        
        self.assertIsNotNone(result)
        self.assertIn('translated_text', result)
        self.assertIn('service_used', result)
        self.assertIn('prompt_used', result)
        self.assertIsNone(result['error'])
        
        self.assertEqual(result['service_used'], 'microsoft')
        self.assertEqual(result['prompt_used'], self.test_prompt)
        self.assertEqual(result['target_language'], 'zh')
    
    def test_translation_service_availability(self):
        """Test translation service availability."""
        services = translation_service.get_available_services()
        self.assertIsInstance(services, dict)
        
        # Should have at least one service configured
        self.assertGreaterEqual(len(services), 0)
    
    def test_translation_input_validation(self):
        """Test translation input validation."""
        # Test empty text
        result = translation_service.translate_text("", self.test_prompt)
        self.assertIn('error', result)
        
        # Test empty prompt
        result = translation_service.translate_text(self.test_text, "")
        self.assertIn('error', result)
        
        # Test None text
        result = translation_service.translate_text(None, self.test_prompt)
        self.assertIn('error', result)
        
        # Test None prompt
        result = translation_service.translate_text(self.test_text, None)
        self.assertIn('error', result)


class TestPerformanceIntegration(unittest.TestCase):
    """Test performance integration."""
    
    def test_large_text_processing(self):
        """Test processing of large text."""
        # Create a large text (but not too large to avoid memory issues)
        large_text = "This is a test sentence. " * 1000  # ~25KB
        
        result = text_processor.process_text(large_text, ['format', 'statistics'])
        
        self.assertIsNotNone(result)
        self.assertIn('processed_text', result)
        self.assertIn('statistics', result)
        
        # Verify statistics are reasonable
        stats = result['statistics']['basic']
        self.assertGreater(stats['characters'], 10000)
        self.assertGreater(stats['words'], 1000)
        self.assertGreater(stats['sentences'], 100)
    
    def test_multiple_operations_performance(self):
        """Test performance of multiple operations."""
        test_text = "Hello world! This is a test. " * 100
        
        # Test all operations together
        result = text_processor.process_text(test_text, ['format', 'statistics', 'analysis'])
        
        self.assertIsNotNone(result)
        self.assertIn('processed_text', result)
        self.assertIn('statistics', result)
        self.assertIn('analysis', result)
        
        # Verify all operations completed successfully
        self.assertIsNotNone(result['processed_text'])
        self.assertIsNotNone(result['statistics'])
        self.assertIsNotNone(result['analysis'])
    
    def test_regex_performance(self):
        """Test regex processing performance."""
        test_text = "Hello world! Hello universe! " * 100
        regex_rules = [("Hello", "Hi"), ("world", "universe"), ("test", "demo")]
        
        result = text_processor.process_text_with_regex(test_text, regex_rules)
        
        self.assertIsNotNone(result)
        self.assertIn('processed_text', result)
        
        # Verify all replacements were applied
        processed_text = result['processed_text']
        self.assertIn("Hi", processed_text)
        self.assertIn("universe", processed_text)
        self.assertNotIn("Hello", processed_text)
        self.assertNotIn("world", processed_text)


if __name__ == '__main__':
    unittest.main() 
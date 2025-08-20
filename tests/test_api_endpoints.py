#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for API endpoints.
Tests routes, validation, and response formats.
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src import create_app
from src.utils.validators import validate_text_input, validate_regex_rules, validate_operations
from src.utils.response_helpers import create_success_response, create_error_response


class TestAPIEndpoints(unittest.TestCase):
    """Test API endpoints functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/api/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', data['data'])
        self.assertEqual(data['data']['status'], 'healthy')
        self.assertIn('timestamp', data['data'])
        self.assertIn('version', data['data'])
    
    def test_config_endpoint(self):
        """Test configuration endpoint."""
        response = self.client.get('/api/config')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('app', data['data'])
        self.assertIn('translation', data['data'])
        self.assertIn('name', data['data']['app'])
        self.assertIn('version', data['data']['app'])
    
    def test_translation_services_endpoint(self):
        """Test translation services endpoint."""
        response = self.client.get('/api/translation-services')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('services', data['data'])
        self.assertIn('count', data['data'])
        self.assertIsInstance(data['data']['services'], dict)
    
    def test_process_text_endpoint_success(self):
        """Test successful text processing endpoint."""
        payload = {
            'text': 'Hello world! This is a test.',
            'operations': ['format', 'statistics']
        }
        
        response = self.client.post('/api/process',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('original_text', data['data'])
        self.assertIn('processed_text', data['data'])
        self.assertIn('statistics', data['data'])
    
    def test_process_text_endpoint_invalid_json(self):
        """Test text processing endpoint with invalid JSON."""
        response = self.client.post('/api/process',
                                  data='invalid json',
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_process_text_endpoint_empty_text(self):
        """Test text processing endpoint with empty text."""
        payload = {
            'text': '',
            'operations': ['format', 'statistics']
        }
        
        response = self.client.post('/api/process',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_process_text_endpoint_no_text(self):
        """Test text processing endpoint without text field."""
        payload = {
            'operations': ['format', 'statistics']
        }
        
        response = self.client.post('/api/process',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_regex_endpoint_success(self):
        """Test successful regex processing endpoint."""
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
        self.assertIn('data', data)
        self.assertIn('original_text', data['data'])
        self.assertIn('processed_text', data['data'])
        self.assertIn('regex_rules', data['data'])
    
    def test_regex_endpoint_empty_rules(self):
        """Test regex endpoint with empty rules."""
        payload = {
            'text': 'Hello world!',
            'regex_rules': []
        }
        
        response = self.client.post('/api/regex',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_regex_endpoint_invalid_rules(self):
        """Test regex endpoint with invalid rules."""
        payload = {
            'text': 'Hello world!',
            'regex_rules': [['invalid[regex', 'replacement']]
        }
        
        response = self.client.post('/api/regex',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_translate_endpoint_success(self):
        """Test successful translation endpoint."""
        payload = {
            'text': 'Hello world!',
            'prompt': 'Translate to Chinese',
            'service_name': 'deepseek'
        }
        
        with patch('src.services.translation_service.translation_service.translate_text') as mock_translate:
            mock_translate.return_value = {
                'translated_text': '你好世界！',
                'service_used': 'deepseek',
                'prompt_used': 'Translate to Chinese',
                'error': None
            }
            
            response = self.client.post('/api/translate',
                                      data=json.dumps(payload),
                                      content_type='application/json')
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertIn('data', data)
    
    def test_translate_endpoint_no_prompt(self):
        """Test translation endpoint without prompt."""
        payload = {
            'text': 'Hello world!',
            'service_name': 'deepseek'
        }
        
        response = self.client.post('/api/translate',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_clear_endpoint(self):
        """Test clear endpoint."""
        response = self.client.post('/api/clear')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('message', data['data'])
    
    def test_history_endpoint(self):
        """Test history endpoint."""
        response = self.client.get('/api/history')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('global_history', data['data'])
        self.assertIn('session_history', data['data'])
    
    def test_main_page_endpoint(self):
        """Test main page endpoint."""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)
    
    def test_404_error_handler(self):
        """Test 404 error handler."""
        response = self.client.get('/nonexistent-endpoint')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('error', data)


class TestValidators(unittest.TestCase):
    """Test validation functions."""
    
    def test_validate_text_input_valid(self):
        """Test valid text input validation."""
        result = validate_text_input("Valid text")
        self.assertTrue(result['valid'])
        self.assertIsNone(result['error'])
    
    def test_validate_text_input_none(self):
        """Test None text input validation."""
        result = validate_text_input(None)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_validate_text_input_empty(self):
        """Test empty text input validation."""
        result = validate_text_input("")
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_validate_text_input_whitespace(self):
        """Test whitespace-only text input validation."""
        result = validate_text_input("   ")
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_validate_text_input_non_string(self):
        """Test non-string text input validation."""
        result = validate_text_input(123)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_validate_text_input_too_long(self):
        """Test too long text input validation."""
        long_text = "x" * 2000000  # 2MB
        result = validate_text_input(long_text)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_validate_regex_rules_valid(self):
        """Test valid regex rules validation."""
        rules = [["pattern", "replacement"], ["\\d+", "number"]]
        result = validate_regex_rules(rules)
        self.assertTrue(result['valid'])
        self.assertIsNone(result['error'])
    
    def test_validate_regex_rules_empty(self):
        """Test empty regex rules validation."""
        result = validate_regex_rules([])
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_validate_regex_rules_not_list(self):
        """Test non-list regex rules validation."""
        result = validate_regex_rules("not a list")
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_validate_regex_rules_invalid_pattern(self):
        """Test invalid regex pattern validation."""
        rules = [["[invalid", "replacement"]]
        result = validate_regex_rules(rules)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_validate_regex_rules_wrong_format(self):
        """Test wrong format regex rules validation."""
        rules = [["pattern"]]  # Missing replacement
        result = validate_regex_rules(rules)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_validate_operations_valid(self):
        """Test valid operations validation."""
        operations = ['format', 'statistics', 'analysis']
        result = validate_operations(operations)
        self.assertTrue(result['valid'])
        self.assertIsNone(result['error'])
    
    def test_validate_operations_invalid(self):
        """Test invalid operations validation."""
        operations = ['format', 'invalid_operation']
        result = validate_operations(operations)
        self.assertFalse(result['valid'])
        self.assertIn('error', result)
    
    def test_validate_operations_not_list(self):
        """Test non-list operations validation."""
        result = validate_operations("not a list")
        self.assertFalse(result['valid'])
        self.assertIn('error', result)


class TestResponseHelpers(unittest.TestCase):
    """Test response helper functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app()
        self.app.config['TESTING'] = True
    
    def test_create_success_response(self):
        """Test success response creation."""
        with self.app.app_context():
            data = {'message': 'Success', 'count': 5}
            response = create_success_response(data, 'Operation completed')
            
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.data)
            self.assertTrue(response_data['success'])
            self.assertEqual(response_data['data'], data)
            self.assertEqual(response_data['message'], 'Operation completed')
    
    def test_create_error_response(self):
        """Test error response creation."""
        with self.app.app_context():
            response = create_error_response('Bad request', 400, {'field': 'text'})
            
            self.assertEqual(response[1], 400)  # status code
            response_data = json.loads(response[0].data)
            self.assertFalse(response_data['success'])
            self.assertEqual(response_data['error'], 'Bad request')
            self.assertEqual(response_data['details'], {'field': 'text'})
    
    def test_create_validation_error_response(self):
        """Test validation error response creation."""
        with self.app.app_context():
            validation_result = {'valid': False, 'error': 'Invalid input'}
            response = create_error_response(validation_result['error'], 400)
            
            self.assertEqual(response[1], 400)
            response_data = json.loads(response[0].data)
            self.assertFalse(response_data['success'])
            self.assertEqual(response_data['error'], 'Invalid input')
    
    def test_create_not_found_response(self):
        """Test not found response creation."""
        with self.app.app_context():
            response = create_error_response('Resource not found', 404)
            
            self.assertEqual(response[1], 404)
            response_data = json.loads(response[0].data)
            self.assertFalse(response_data['success'])
            self.assertEqual(response_data['error'], 'Resource not found')
    
    def test_create_server_error_response(self):
        """Test server error response creation."""
        with self.app.app_context():
            response = create_error_response('Internal server error', 500)
            
            self.assertEqual(response[1], 500)
            response_data = json.loads(response[0].data)
            self.assertFalse(response_data['success'])
            self.assertEqual(response_data['error'], 'Internal server error')


class TestAPIErrorHandling(unittest.TestCase):
    """Test API error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_method_not_allowed(self):
        """Test method not allowed error."""
        response = self.client.get('/api/process')  # GET instead of POST
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 405)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_internal_server_error(self):
        """Test internal server error handling."""
        with patch('src.core.text_processor.text_processor.process_text') as mock_process:
            mock_process.side_effect = Exception("Test error")
            
            payload = {'text': 'Test text', 'operations': ['format']}
            response = self.client.post('/api/process',
                                      data=json.dumps(payload),
                                      content_type='application/json')
            data = json.loads(response.data)
            
            self.assertEqual(response.status_code, 500)
            self.assertFalse(data['success'])
            self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main() 
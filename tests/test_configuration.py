#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive tests for configuration modules.
Tests app config and translation config functionality.
"""

import unittest
import sys
import os
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config.app_config import AppConfig
from src.config.translation_config import TranslationConfig


class TestAppConfig(unittest.TestCase):
    """Test AppConfig class functionality."""
    
    def test_basic_configuration(self):
        """Test basic configuration values."""
        self.assertIsNotNone(AppConfig.SECRET_KEY)
        self.assertIsInstance(AppConfig.MAX_CONTENT_LENGTH, int)
        self.assertIsInstance(AppConfig.APP_NAME, str)
        self.assertIsInstance(AppConfig.APP_VERSION, str)
        self.assertIsInstance(AppConfig.DEFAULT_PORT, int)
        self.assertIsInstance(AppConfig.DEFAULT_HOST, str)
    
    def test_app_name_and_version(self):
        """Test app name and version."""
        self.assertEqual(AppConfig.APP_NAME, 'Text Processing Tool')
        self.assertEqual(AppConfig.APP_VERSION, '2.0.0')
    
    def test_default_settings(self):
        """Test default settings."""
        self.assertEqual(AppConfig.DEFAULT_HOST, '127.0.0.1')
        self.assertEqual(AppConfig.DEFAULT_PORT, 5009)
        self.assertEqual(AppConfig.MAX_CONTENT_LENGTH, 16 * 1024 * 1024)  # 16MB
    
    def test_upload_settings(self):
        """Test upload settings."""
        self.assertEqual(AppConfig.UPLOAD_FOLDER, 'uploads')
        self.assertIsInstance(AppConfig.ALLOWED_EXTENSIONS, set)
        self.assertIn('txt', AppConfig.ALLOWED_EXTENSIONS)
        self.assertIn('md', AppConfig.ALLOWED_EXTENSIONS)
        self.assertIn('json', AppConfig.ALLOWED_EXTENSIONS)
        self.assertIn('csv', AppConfig.ALLOWED_EXTENSIONS)
    
    def test_text_processing_settings(self):
        """Test text processing settings."""
        self.assertIsInstance(AppConfig.MAX_TEXT_LENGTH, int)
        self.assertGreater(AppConfig.MAX_TEXT_LENGTH, 0)
        self.assertIsInstance(AppConfig.DEFAULT_OPERATIONS, list)
        self.assertIn('format', AppConfig.DEFAULT_OPERATIONS)
        self.assertIn('statistics', AppConfig.DEFAULT_OPERATIONS)
        self.assertIn('analysis', AppConfig.DEFAULT_OPERATIONS)
    
    def test_logging_settings(self):
        """Test logging settings."""
        self.assertIsInstance(AppConfig.LOG_LEVEL, str)
        self.assertIsInstance(AppConfig.LOG_FILE, str)
        self.assertIn(AppConfig.LOG_LEVEL.upper(), ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    
    def test_get_config_dict(self):
        """Test get_config_dict method."""
        config_dict = AppConfig.get_config_dict()
        
        self.assertIsInstance(config_dict, dict)
        self.assertIn('SECRET_KEY', config_dict)
        self.assertIn('APP_NAME', config_dict)
        self.assertIn('APP_VERSION', config_dict)
        self.assertIn('DEFAULT_PORT', config_dict)
        self.assertIn('DEFAULT_HOST', config_dict)
        self.assertIn('UPLOAD_FOLDER', config_dict)
        self.assertIn('ALLOWED_EXTENSIONS', config_dict)
        self.assertIn('MAX_FILE_SIZE', config_dict)
        self.assertIn('LOG_LEVEL', config_dict)
        self.assertIn('LOG_FILE', config_dict)
        self.assertIn('MAX_TEXT_LENGTH', config_dict)
        self.assertIn('DEFAULT_OPERATIONS', config_dict)
    
    @patch('os.environ.get')
    def test_environment_variable_override(self, mock_env_get):
        """Test environment variable override."""
        # Mock environment variables
        mock_env_get.side_effect = lambda key, default=None: {
            'SECRET_KEY': 'test-secret-key',
            'FLASK_DEBUG': 'true',
            'LOG_LEVEL': 'DEBUG'
        }.get(key, default)
        
        # Re-import to get updated values
        import importlib
        import src.config.app_config
        importlib.reload(src.config.app_config)
        
        # Test that environment variables are used
        self.assertEqual(src.config.app_config.AppConfig.SECRET_KEY, 'test-secret-key')
        self.assertTrue(src.config.app_config.AppConfig.DEBUG)
        self.assertEqual(src.config.app_config.AppConfig.LOG_LEVEL, 'DEBUG')
    
    def test_validate_config(self):
        """Test configuration validation."""
        validation_result = AppConfig.validate_config()
        
        self.assertIsInstance(validation_result, dict)
        self.assertIn('valid', validation_result)
        self.assertIn('errors', validation_result)
        self.assertIn('warnings', validation_result)
        
        self.assertIsInstance(validation_result['valid'], bool)
        self.assertIsInstance(validation_result['errors'], list)
        self.assertIsInstance(validation_result['warnings'], list)
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_validate_config_creates_directories(self, mock_makedirs, mock_exists):
        """Test that validation creates missing directories."""
        # Mock that directories don't exist
        mock_exists.return_value = False
        
        validation_result = AppConfig.validate_config()
        
        # Should have called makedirs for required directories
        mock_makedirs.assert_called()
        
        # Should have warnings about created directories
        self.assertTrue(any('Created directory' in warning for warning in validation_result['warnings']))
    
    def test_validate_config_secret_key_warning(self):
        """Test secret key warning in validation."""
        validation_result = AppConfig.validate_config()
        
        # Should warn about default secret key
        warnings = validation_result['warnings']
        secret_key_warnings = [w for w in warnings if 'secret key' in w.lower()]
        self.assertGreater(len(secret_key_warnings), 0)


class TestTranslationConfig(unittest.TestCase):
    """Test TranslationConfig class functionality."""
    
    def test_translation_config_constants(self):
        """Test translation config constants."""
        self.assertIsNotNone(TranslationConfig.DEEPSEEK_API_KEY)
        self.assertIsNotNone(TranslationConfig.DEEPSEEK_API_URL)
        self.assertIsNotNone(TranslationConfig.DEEPSEEK_MODEL)
        self.assertIsNotNone(TranslationConfig.OPENAI_API_KEY)
        self.assertIsNotNone(TranslationConfig.OPENAI_API_URL)
        self.assertIsNotNone(TranslationConfig.OPENAI_MODEL)
        self.assertIsNotNone(TranslationConfig.MICROSOFT_API_KEY)
        self.assertIsNotNone(TranslationConfig.MICROSOFT_API_URL)
        self.assertIsNotNone(TranslationConfig.MICROSOFT_REGION)
        self.assertIsNotNone(TranslationConfig.DEFAULT_TRANSLATION_SERVICE)
    
    def test_translation_config_urls(self):
        """Test translation config URLs."""
        self.assertEqual(TranslationConfig.DEEPSEEK_API_URL, "https://api.deepseek.com/v1/chat/completions")
        self.assertEqual(TranslationConfig.OPENAI_API_URL, "https://api.openai.com/v1/chat/completions")
        self.assertEqual(TranslationConfig.MICROSOFT_API_URL, "https://api.cognitive.microsofttranslator.com")
    
    def test_translation_config_models(self):
        """Test translation config models."""
        self.assertEqual(TranslationConfig.DEEPSEEK_MODEL, "deepseek-chat")
        self.assertEqual(TranslationConfig.OPENAI_MODEL, "gpt-3.5-turbo")
        self.assertEqual(TranslationConfig.MICROSOFT_REGION, "southeastasia")
    
    def test_default_translation_service(self):
        """Test default translation service."""
        self.assertEqual(TranslationConfig.DEFAULT_TRANSLATION_SERVICE, "deepseek")
    
    def test_available_services(self):
        """Test available services configuration."""
        services = TranslationConfig.AVAILABLE_SERVICES
        
        # Check that all expected services are present
        self.assertIn('deepseek', services)
        self.assertIn('openai', services)
        self.assertIn('microsoft', services)
        
        # Check service configurations
        deepseek_config = services['deepseek']
        self.assertIn('name', deepseek_config)
        self.assertIn('api_key', deepseek_config)
        self.assertIn('api_url', deepseek_config)
        self.assertIn('model', deepseek_config)
        self.assertIn('enabled', deepseek_config)
        
        openai_config = services['openai']
        self.assertIn('name', openai_config)
        self.assertIn('api_key', openai_config)
        self.assertIn('api_url', openai_config)
        self.assertIn('model', openai_config)
        self.assertIn('enabled', openai_config)
        
        microsoft_config = services['microsoft']
        self.assertIn('name', microsoft_config)
        self.assertIn('api_key', microsoft_config)
        self.assertIn('api_url', microsoft_config)
        self.assertIn('region', microsoft_config)
        self.assertIn('model', microsoft_config)
        self.assertIn('enabled', microsoft_config)
    
    def test_available_models(self):
        """Test available models configuration."""
        models = TranslationConfig.AVAILABLE_MODELS
        
        self.assertIn('deepseek', models)
        self.assertIn('openai', models)
        self.assertIn('microsoft', models)
        
        # Check that models are lists
        self.assertIsInstance(models['deepseek'], list)
        self.assertIsInstance(models['openai'], list)
        self.assertIsInstance(models['microsoft'], list)
        
        # Check Microsoft models (should have API version)
        self.assertIn('api-version-3.0', models['microsoft'])

    def test_get_service_config(self):
        """Test get_service_config method."""
        # Test existing service
        deepseek_config = TranslationConfig.get_service_config('deepseek')
        self.assertIsInstance(deepseek_config, dict)
        self.assertIn('name', deepseek_config)
        self.assertIn('api_key', deepseek_config)
        self.assertIn('api_url', deepseek_config)
        self.assertIn('model', deepseek_config)
        
        # Test non-existing service
        non_existing_config = TranslationConfig.get_service_config('non_existing')
        self.assertEqual(non_existing_config, {})
    
    def test_get_enabled_services(self):
        """Test get_enabled_services method."""
        enabled_services = TranslationConfig.get_enabled_services()
        
        self.assertIsInstance(enabled_services, dict)
        
        # All services in enabled_services should have enabled=True
        for service_name, service_config in enabled_services.items():
            self.assertTrue(service_config.get('enabled', False))
    
    def test_is_service_available(self):
        """Test is_service_available method."""
        # Test with existing service
        result = TranslationConfig.is_service_available('deepseek')
        self.assertIsInstance(result, bool)
        
        # Test with non-existing service
        result = TranslationConfig.is_service_available('non_existing')
        self.assertFalse(result)
    
    def test_get_service_names(self):
        """Test get_service_names method."""
        service_names = TranslationConfig.get_service_names()
        
        self.assertIsInstance(service_names, list)
        self.assertIn('deepseek', service_names)
        self.assertIn('openai', service_names)
        self.assertEqual(len(service_names), 3)
    
    def test_validate_service_config(self):
        """Test validate_service_config method."""
        # Test valid service
        validation = TranslationConfig.validate_service_config('deepseek')
        
        self.assertIsInstance(validation, dict)
        self.assertIn('valid', validation)
        self.assertIn('errors', validation)
        self.assertIn('warnings', validation)
        
        self.assertIsInstance(validation['valid'], bool)
        self.assertIsInstance(validation['errors'], list)
        self.assertIsInstance(validation['warnings'], list)
        
        # Test non-existing service
        validation = TranslationConfig.validate_service_config('non_existing')
        self.assertFalse(validation['valid'])
        self.assertGreater(len(validation['errors']), 0)
    
    def test_get_config_summary(self):
        """Test get_config_summary method."""
        summary = TranslationConfig.get_config_summary()
        
        self.assertIsInstance(summary, dict)
        self.assertIn('total_services', summary)
        self.assertIn('enabled_services', summary)
        self.assertIn('default_service', summary)
        self.assertIn('enabled_service_names', summary)
        self.assertIn('all_service_names', summary)
        
        self.assertIsInstance(summary['total_services'], int)
        self.assertIsInstance(summary['enabled_services'], int)
        self.assertIsInstance(summary['default_service'], str)
        self.assertIsInstance(summary['enabled_service_names'], list)
        self.assertIsInstance(summary['all_service_names'], list)
        
        self.assertEqual(summary['total_services'], 3)
        self.assertEqual(summary['default_service'], 'deepseek')
        self.assertIn('deepseek', summary['all_service_names'])
        self.assertIn('openai', summary['all_service_names'])
    
    @patch('os.environ.get')
    def test_environment_variable_override(self, mock_env_get):
        """Test environment variable override."""
        # Mock environment variables
        mock_env_get.side_effect = lambda key, default="": {
            'DEEPSEEK_API_KEY': 'test-deepseek-key',
            'OPENAI_API_KEY': 'test-openai-key'
        }.get(key, default)
        
        # Re-import to get updated values
        import importlib
        import src.config.translation_config
        importlib.reload(src.config.translation_config)
        
        # Test that environment variables are used
        self.assertEqual(src.config.translation_config.TranslationConfig.DEEPSEEK_API_KEY, 'test-deepseek-key')
        self.assertEqual(src.config.translation_config.TranslationConfig.OPENAI_API_KEY, 'test-openai-key')
        
        # Test that services are enabled when API keys are provided
        services = src.config.translation_config.TranslationConfig.AVAILABLE_SERVICES
        self.assertTrue(services['deepseek']['enabled'])
        self.assertTrue(services['openai']['enabled'])
    
    def test_service_enabled_logic(self):
        """Test service enabled logic."""
        services = TranslationConfig.AVAILABLE_SERVICES
        
        # Services should be enabled if API key is not empty
        for service_name, service_config in services.items():
            enabled = service_config.get('enabled', False)
            api_key = service_config.get('api_key', '')
            
            # If API key is provided, service should be enabled
            if api_key:
                self.assertTrue(enabled, f"Service {service_name} should be enabled when API key is provided")
            else:
                self.assertFalse(enabled, f"Service {service_name} should be disabled when API key is empty")


class TestConfigurationIntegration(unittest.TestCase):
    """Test configuration integration."""
    
    def test_config_consistency(self):
        """Test configuration consistency between modules."""
        # Test that app config and translation config work together
        app_config_dict = AppConfig.get_config_dict()
        translation_summary = TranslationConfig.get_config_summary()
        
        # Both should be valid
        self.assertIsInstance(app_config_dict, dict)
        self.assertIsInstance(translation_summary, dict)
        
        # App config should have reasonable values
        self.assertGreater(app_config_dict['MAX_FILE_SIZE'], 0)
        self.assertGreater(app_config_dict['MAX_TEXT_LENGTH'], 0)
        self.assertIsInstance(app_config_dict['DEFAULT_OPERATIONS'], list)
        
        # Translation config should have reasonable values
        self.assertGreater(translation_summary['total_services'], 0)
        self.assertGreaterEqual(translation_summary['enabled_services'], 0)
        self.assertLessEqual(translation_summary['enabled_services'], translation_summary['total_services'])
    
    def test_config_validation_integration(self):
        """Test configuration validation integration."""
        # Both configs should validate successfully
        app_validation = AppConfig.validate_config()
        self.assertTrue(app_validation['valid'])
        
        # Translation services should be valid
        for service_name in TranslationConfig.get_service_names():
            validation = TranslationConfig.validate_service_config(service_name)
            # Should be valid even if API key is missing (just warnings)
            self.assertIsInstance(validation['valid'], bool)
            self.assertIsInstance(validation['errors'], list)
            self.assertIsInstance(validation['warnings'], list)


if __name__ == '__main__':
    unittest.main() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Configuration Module
Contains main application settings and configuration.
"""

import os
from typing import Dict, Any


class AppConfig:
    """Main application configuration class."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    SESSION_TYPE = 'filesystem'
    
    # Application settings
    APP_NAME = 'Text Processing Tool'
    APP_VERSION = '2.0.0'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Server settings
    DEFAULT_HOST = '127.0.0.1'
    DEFAULT_PORT = 5009
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'md', 'json', 'csv'}
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = 'logs/app.log'
    
    # Text processing settings
    MAX_TEXT_LENGTH = 1000000  # 1MB text limit
    DEFAULT_OPERATIONS = ['format', 'statistics', 'analysis']
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """
        Get configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return {
            'SECRET_KEY': cls.SECRET_KEY,
            'MAX_CONTENT_LENGTH': cls.MAX_CONTENT_LENGTH,
            'SESSION_TYPE': cls.SESSION_TYPE,
            'APP_NAME': cls.APP_NAME,
            'APP_VERSION': cls.APP_VERSION,
            'DEBUG': cls.DEBUG,
            'DEFAULT_HOST': cls.DEFAULT_HOST,
            'DEFAULT_PORT': cls.DEFAULT_PORT,
            'UPLOAD_FOLDER': cls.UPLOAD_FOLDER,
            'ALLOWED_EXTENSIONS': cls.ALLOWED_EXTENSIONS,
            'MAX_FILE_SIZE': cls.MAX_FILE_SIZE,
            'LOG_LEVEL': cls.LOG_LEVEL,
            'LOG_FILE': cls.LOG_FILE,
            'MAX_TEXT_LENGTH': cls.MAX_TEXT_LENGTH,
            'DEFAULT_OPERATIONS': cls.DEFAULT_OPERATIONS
        }
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """
        Validate configuration settings.
        
        Returns:
            Validation results
        """
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required directories
        required_dirs = [cls.UPLOAD_FOLDER, 'logs']
        for directory in required_dirs:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                    validation_results['warnings'].append(f'Created directory: {directory}')
                except Exception as e:
                    validation_results['errors'].append(f'Cannot create directory {directory}: {e}')
                    validation_results['valid'] = False
        
        # Check secret key
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            validation_results['warnings'].append('Using default secret key. Change in production.')
        
        # Check file size limits
        if cls.MAX_FILE_SIZE > 50 * 1024 * 1024:  # 50MB
            validation_results['warnings'].append('File size limit is very high (>50MB)')
        
        return validation_results 
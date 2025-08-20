#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translation Configuration Module
Contains translation service settings and API configurations.
"""

import os
from typing import Dict, Any


class TranslationConfig:
    """Translation service configuration class."""

    # DeepSeek API configuration
    DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    DEEPSEEK_MODEL = "deepseek-chat"

    # OpenAI ChatGPT API configuration
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    OPENAI_MODEL = "gpt-3.5-turbo"

    # Default translation service
    DEFAULT_TRANSLATION_SERVICE = "deepseek"

    # Available translation services
    AVAILABLE_SERVICES = {
        "deepseek": {
            "name": "DeepSeek",
            "api_key": DEEPSEEK_API_KEY,
            "api_url": DEEPSEEK_API_URL,
            "model": DEEPSEEK_MODEL,
            "enabled": bool(DEEPSEEK_API_KEY),
        },
        "openai": {
            "name": "OpenAI ChatGPT",
            "api_key": OPENAI_API_KEY,
            "api_url": OPENAI_API_URL,
            "model": OPENAI_MODEL,
            "enabled": bool(OPENAI_API_KEY),
        },
    }

    @classmethod
    def get_service_config(cls, service_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific service.

        Args:
            service_name: Name of the service

        Returns:
            Service configuration dictionary
        """
        return cls.AVAILABLE_SERVICES.get(service_name, {})

    @classmethod
    def get_enabled_services(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get all enabled services.

        Returns:
            Dictionary of enabled services
        """
        return {
            name: config
            for name, config in cls.AVAILABLE_SERVICES.items()
            if config.get("enabled", False)
        }

    @classmethod
    def is_service_available(cls, service_name: str) -> bool:
        """
        Check if a service is available.

        Args:
            service_name: Name of the service

        Returns:
            True if service is available, False otherwise
        """
        config = cls.get_service_config(service_name)
        return config.get("enabled", False)

    @classmethod
    def get_service_names(cls) -> list:
        """
        Get list of all service names.

        Returns:
            List of service names
        """
        return list(cls.AVAILABLE_SERVICES.keys())

    @classmethod
    def validate_service_config(cls, service_name: str) -> Dict[str, Any]:
        """
        Validate configuration for a specific service.

        Args:
            service_name: Name of the service

        Returns:
            Validation results
        """
        config = cls.get_service_config(service_name)
        
        validation = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        if not config:
            validation['valid'] = False
            validation['errors'].append(f'Service {service_name} not found')
            return validation
        
        # Check API key
        if not config.get('api_key'):
            validation['valid'] = False
            validation['errors'].append(f'API key not configured for {service_name}')
        
        # Check API URL
        if not config.get('api_url'):
            validation['valid'] = False
            validation['errors'].append(f'API URL not configured for {service_name}')
        
        # Check model
        if not config.get('model'):
            validation['warnings'].append(f'Model not specified for {service_name}')
        
        return validation

    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """
        Get configuration summary.

        Returns:
            Configuration summary
        """
        enabled_services = cls.get_enabled_services()
        
        return {
            'total_services': len(cls.AVAILABLE_SERVICES),
            'enabled_services': len(enabled_services),
            'default_service': cls.DEFAULT_TRANSLATION_SERVICE,
            'enabled_service_names': list(enabled_services.keys()),
            'all_service_names': cls.get_service_names()
        } 
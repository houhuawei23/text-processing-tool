#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translation Configuration Module
Contains translation service settings and API configurations.
"""

import os
from typing import Dict, Any
from flask import session


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

    # Available models for each service
    AVAILABLE_MODELS = {
        "deepseek": [
            "deepseek-chat",
            "deepseek-coder",
            "deepseek-chat-33b"
        ],
        "openai": [
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4-32k"
        ]
    }

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
    def get_user_config(cls, service_name: str) -> Dict[str, Any]:
        """
        Get user-provided configuration for a specific service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            User configuration dictionary
        """
        user_configs = session.get('user_translation_configs', {})
        return user_configs.get(service_name, {})

    @classmethod
    def set_user_config(cls, service_name: str, api_key: str, model: str = None) -> None:
        """
        Set user-provided configuration for a specific service.
        
        Args:
            service_name: Name of the service
            api_key: User-provided API key
            model: User-selected model (optional)
        """
        # Ensure base container exists
        if 'user_translation_configs' not in session:
            session['user_translation_configs'] = {}

        # Build the user config
        user_config = {
            'api_key': api_key,
            'enabled': bool(api_key.strip())
        }

        if model:
            user_config['model'] = model

        # Update via reassignment so Flask detects the change
        configs = dict(session.get('user_translation_configs', {}))
        configs[service_name] = user_config
        session['user_translation_configs'] = configs
        session.modified = True

    @classmethod
    def clear_user_config(cls, service_name: str) -> None:
        """
        Clear user-provided configuration for a specific service.
        
        Args:
            service_name: Name of the service
        """
        if 'user_translation_configs' in session:
            configs = dict(session.get('user_translation_configs', {}))
            configs.pop(service_name, None)
            session['user_translation_configs'] = configs
            session.modified = True

    @classmethod
    def get_service_config(cls, service_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific service.
        Prioritizes user-provided configuration over environment variables.

        Args:
            service_name: Name of the service

        Returns:
            Service configuration dictionary
        """
        # First check for user-provided configuration
        user_config = cls.get_user_config(service_name)
        if user_config and user_config.get('api_key'):  # Check for API key instead of enabled
            base_config = cls.AVAILABLE_SERVICES.get(service_name, {}).copy()
            # Only override specific user-provided fields, keep base config intact
            if user_config.get('api_key'):
                base_config['api_key'] = user_config['api_key']
            if user_config.get('model'):
                base_config['model'] = user_config['model']
            base_config['enabled'] = user_config.get('enabled', False)
            return base_config
        
        # Fall back to environment-based configuration
        return cls.AVAILABLE_SERVICES.get(service_name, {})

    @classmethod
    def get_all_services(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get all available services (enabled and disabled).

        Returns:
            Dictionary of all available services
        """
        all_services = {}
        
        # Add all available services
        for name, config in cls.AVAILABLE_SERVICES.items():
            service_config = config.copy()
            
            # Check if user has configured this service
            user_config = cls.get_user_config(name)
            if user_config:
                # Only override specific user-provided fields, keep base config intact
                if user_config.get('api_key'):
                    service_config['api_key'] = user_config['api_key']
                if user_config.get('model'):
                    service_config['model'] = user_config['model']
                service_config['enabled'] = user_config.get('enabled', False)
                service_config['is_user_configured'] = True
            else:
                service_config['is_user_configured'] = False
            
            all_services[name] = service_config
        
        return all_services

    @classmethod
    def get_enabled_services(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get all enabled services (including user-provided ones).

        Returns:
            Dictionary of enabled services
        """
        enabled_services = {}
        
        # Check environment-based services
        for name, config in cls.AVAILABLE_SERVICES.items():
            if config.get("enabled", False):
                enabled_services[name] = config.copy()
        
        # Check user-provided services
        user_configs = session.get('user_translation_configs', {})
        for name, user_config in user_configs.items():
            if user_config.get('enabled', False):
                base_config = cls.AVAILABLE_SERVICES.get(name, {}).copy()
                # Only override specific user-provided fields, keep base config intact
                if user_config.get('api_key'):
                    base_config['api_key'] = user_config['api_key']
                if user_config.get('model'):
                    base_config['model'] = user_config['model']
                base_config['enabled'] = user_config.get('enabled', False)
                enabled_services[name] = base_config
        
        return enabled_services

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
    def get_available_models_for_service(cls, service_name: str) -> list:
        """
        Get available models for a specific service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            List of available models
        """
        return cls.AVAILABLE_MODELS.get(service_name, [])

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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input Validation Module
Contains validation functions for API inputs.
"""

import re
from typing import Dict, Any, List
from ..config.app_config import AppConfig


def validate_text_input(text: str) -> Dict[str, Any]:
    """
    Validate text input for processing.
    
    Args:
        text: Text to validate
        
    Returns:
        Validation result dictionary
    """
    result = {
        'valid': True,
        'error': None
    }
    
    # Check if text is None
    if text is None:
        result['valid'] = False
        result['error'] = 'Text input cannot be None'
        return result
    
    # Check if text is a string
    if not isinstance(text, str):
        result['valid'] = False
        result['error'] = 'Text input must be a string'
        return result
    
    # Check if text is empty
    if not text or not text.strip():
        result['valid'] = False
        result['error'] = 'Text input cannot be empty'
        return result
    
    # Check text length
    if len(text) > AppConfig.MAX_TEXT_LENGTH:
        result['valid'] = False
        result['error'] = f'Text is too long. Maximum length is {AppConfig.MAX_TEXT_LENGTH} characters'
        return result
    
    return result


def validate_regex_rules(regex_rules: List) -> Dict[str, Any]:
    """
    Validate regex rules input.
    
    Args:
        regex_rules: List of regex rules to validate
        
    Returns:
        Validation result dictionary
    """
    result = {
        'valid': True,
        'error': None
    }
    
    # Check if rules is a list
    if not isinstance(regex_rules, list):
        result['valid'] = False
        result['error'] = 'Regex rules must be a list'
        return result
    
    # Check if rules list is empty
    if not regex_rules:
        result['valid'] = False
        result['error'] = 'Regex rules cannot be empty'
        return result
    
    # Validate each rule
    for i, rule in enumerate(regex_rules):
        rule_validation = _validate_single_regex_rule(rule, i)
        if not rule_validation['valid']:
            result['valid'] = False
            result['error'] = rule_validation['error']
            return result
    
    return result


def validate_operations(operations: List[str]) -> Dict[str, Any]:
    """
    Validate processing operations.
    
    Args:
        operations: List of operations to validate
        
    Returns:
        Validation result dictionary
    """
    result = {
        'valid': True,
        'error': None
    }
    
    # Check if operations is a list
    if not isinstance(operations, list):
        result['valid'] = False
        result['error'] = 'Operations must be a list'
        return result
    
    # Valid operations
    valid_operations = {'format', 'statistics', 'analysis', 'regex'}
    
    # Check each operation
    for operation in operations:
        if operation not in valid_operations:
            result['valid'] = False
            result['error'] = f'Invalid operation: {operation}. Valid operations are: {", ".join(valid_operations)}'
            return result
    
    return result


def validate_translation_input(text: str, prompt: str, service_name: str = None) -> Dict[str, Any]:
    """
    Validate translation input parameters.
    
    Args:
        text: Text to translate
        prompt: Translation prompt
        service_name: Translation service name
        
    Returns:
        Validation result dictionary
    """
    result = {
        'valid': True,
        'error': None
    }
    
    # Validate text
    text_validation = validate_text_input(text)
    if not text_validation['valid']:
        return text_validation
    
    # Validate prompt
    if not prompt or not prompt.strip():
        result['valid'] = False
        result['error'] = 'Translation prompt cannot be empty'
        return result
    
    # Validate service name if provided
    if service_name:
        from ..config.translation_config import TranslationConfig
        if not TranslationConfig.is_service_available(service_name):
            result['valid'] = False
            result['error'] = f'Translation service "{service_name}" is not available'
            return result
    
    return result


def _validate_single_regex_rule(rule, index: int) -> Dict[str, Any]:
    """
    Validate a single regex rule.
    
    Args:
        rule: Regex rule to validate
        index: Index of the rule in the list
        
    Returns:
        Validation result dictionary
    """
    result = {
        'valid': True,
        'error': None
    }
    
    # Check if rule is a string
    if isinstance(rule, str):
        if " -> " not in rule:
            result['valid'] = False
            result['error'] = f'Rule {index}: Invalid string format. Expected "pattern -> replacement"'
            return result
        return result
    
    # Check if rule is a list or tuple with 2 elements
    if isinstance(rule, (list, tuple)):
        if len(rule) != 2:
            result['valid'] = False
            result['error'] = f'Rule {index}: Must have exactly 2 elements (pattern and replacement)'
            return result
        
        # Validate pattern and replacement are strings
        pattern, replacement = rule
        if not isinstance(pattern, str) or not isinstance(replacement, str):
            result['valid'] = False
            result['error'] = f'Rule {index}: Pattern and replacement must be strings'
            return result
        
        # Validate regex pattern
        try:
            re.compile(pattern)
        except re.error as e:
            result['valid'] = False
            result['error'] = f'Rule {index}: Invalid regex pattern: {str(e)}'
            return result
        
        return result
    
    # Invalid rule type
    result['valid'] = False
    result['error'] = f'Rule {index}: Invalid rule type. Must be string or list/tuple'
    return result


def validate_file_upload(filename: str, file_size: int) -> Dict[str, Any]:
    """
    Validate file upload.
    
    Args:
        filename: Name of the uploaded file
        file_size: Size of the uploaded file in bytes
        
    Returns:
        Validation result dictionary
    """
    result = {
        'valid': True,
        'error': None
    }
    
    # Check file extension
    if '.' not in filename:
        result['valid'] = False
        result['error'] = 'File must have an extension'
        return result
    
    extension = filename.rsplit('.', 1)[1].lower()
    if extension not in AppConfig.ALLOWED_EXTENSIONS:
        result['valid'] = False
        result['error'] = f'File type not allowed. Allowed types: {", ".join(AppConfig.ALLOWED_EXTENSIONS)}'
        return result
    
    # Check file size
    if file_size > AppConfig.MAX_FILE_SIZE:
        result['valid'] = False
        result['error'] = f'File too large. Maximum size is {AppConfig.MAX_FILE_SIZE // (1024*1024)}MB'
        return result
    
    return result 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Routes Module
Contains all Flask API route handlers with improved error handling and validation.
"""

import json
from datetime import datetime
from flask import Blueprint, request, jsonify, session, current_app
from ..core.text_processor import text_processor
from ..services.translation_service import translation_service
from ..utils.validators import validate_text_input, validate_regex_rules
from ..utils.response_helpers import create_success_response, create_error_response


# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/process', methods=['POST'])
def process_text_api():
    """
    Text processing API endpoint.
    
    Expected JSON payload:
    {
        "text": "text to process",
        "operations": ["format", "statistics", "analysis"]
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return create_error_response('Request must be JSON', 400)
        
        data = request.get_json()
        if not data:
            return create_error_response('Invalid request data', 400)
        
        # Extract and validate input
        text = data.get('text', '').strip()
        operations = data.get('operations', None)
        
        # Validate text input
        validation_result = validate_text_input(text)
        if not validation_result['valid']:
            return create_error_response(validation_result['error'], 400)
        
        # Process text
        result = text_processor.process_text(text, operations)
        
        # Record processing history
        _record_processing_history(operations or ['format', 'statistics', 'analysis'], len(text))
        
        return create_success_response(result)
        
    except Exception as e:
        current_app.logger.error(f"Text processing error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/regex', methods=['POST'])
def regex_process_api():
    """
    Regex processing API endpoint.
    
    Expected JSON payload:
    {
        "text": "text to process",
        "regex_rules": [["pattern", "replacement"], ...]
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return create_error_response('Request must be JSON', 400)
        
        data = request.get_json()
        if not data:
            return create_error_response('Invalid request data', 400)
        
        # Extract and validate input
        text = data.get('text', '').strip()
        regex_rules = data.get('regex_rules', [])
        
        # Validate text input
        validation_result = validate_text_input(text)
        if not validation_result['valid']:
            return create_error_response(validation_result['error'], 400)
        
        # Validate regex rules
        validation_result = validate_regex_rules(regex_rules)
        if not validation_result['valid']:
            return create_error_response(validation_result['error'], 400)
        
        # Convert rules format
        converted_rules = _convert_regex_rules_format(regex_rules)
        
        # Process text with regex
        result = text_processor.process_text_with_regex(text, converted_rules)
        
        # Record processing history
        _record_processing_history(['regex'], len(text), regex_rules_count=len(converted_rules))
        
        return create_success_response(result)
        
    except Exception as e:
        current_app.logger.error(f"Regex processing error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/translate', methods=['POST'])
def translate_text_api():
    """
    Text translation API endpoint.
    
    Expected JSON payload:
    {
        "text": "text to translate",
        "prompt": "translation prompt",
        "service_name": "deepseek"
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return create_error_response('Request must be JSON', 400)
        
        data = request.get_json()
        if not data:
            return create_error_response('Invalid request data', 400)
        
        # Extract and validate input
        text = data.get('text', '').strip()
        prompt = data.get('prompt', '').strip()
        service_name = data.get('service_name', None)
        
        # Validate text input
        validation_result = validate_text_input(text)
        if not validation_result['valid']:
            return create_error_response(validation_result['error'], 400)
        
        # Validate prompt
        if not prompt:
            return create_error_response('Translation prompt cannot be empty', 400)
        
        # Debug logging
        current_app.logger.info(f"DEBUG: Translating with service: {service_name}")
        
        # Translate text
        result = translation_service.translate_text(text, prompt, service_name)
        
        # Record processing history
        _record_processing_history(['translate'], len(text), 
                                 service_used=result.get('service_used', ''),
                                 prompt_used=prompt)
        
        return create_success_response(result)
        
    except Exception as e:
        current_app.logger.error(f"Translation error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/translation-services', methods=['GET'])
def get_translation_services():
    """Get available translation services."""
    try:
        from ..config.translation_config import TranslationConfig
        
        # Get all services (enabled and disabled)
        services = TranslationConfig.get_all_services()
        enabled_count = len([s for s in services.values() if s.get('enabled', False)])
        
        return create_success_response({
            'services': services,
            'count': len(services),
            'enabled_count': enabled_count
        })
        
    except Exception as e:
        current_app.logger.error(f"Get translation services error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/translation-services/<service_name>/models', methods=['GET'])
def get_translation_models(service_name):
    """Get available models for a specific translation service."""
    try:
        from ..config.translation_config import TranslationConfig
        
        models = TranslationConfig.get_available_models_for_service(service_name)
        return create_success_response({
            'service_name': service_name,
            'models': models,
            'count': len(models)
        })
        
    except Exception as e:
        current_app.logger.error(f"Get translation models error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/translation-services/<service_name>/config', methods=['POST'])
def set_translation_service_config(service_name):
    """Set user-provided API key and model for a translation service."""
    try:
        from ..config.translation_config import TranslationConfig
        
        # Validate request
        if not request.is_json:
            return create_error_response('Request must be JSON', 400)
        
        data = request.get_json()
        if not data:
            return create_error_response('Invalid request data', 400)
        
        # Extract and validate input
        api_key = data.get('api_key', '').strip()
        model = data.get('model', '').strip()
        
        if not api_key:
            return create_error_response('API key cannot be empty', 400)
        
        # Validate API key format
        if len(api_key) < 10:
            return create_error_response('API key is too short', 400)

        # Reject placeholders and keys containing whitespace/newlines (e.g., accidental commands like "python run.py")
        if api_key == '••••••••••••••••' or any(ch.isspace() for ch in api_key):
            return create_error_response('Invalid API key format (no spaces or placeholders allowed)', 400)
        
        # Validate service name
        if service_name not in TranslationConfig.get_service_names():
            return create_error_response(f'Invalid service name: {service_name}', 400)
        
        # Validate model if provided
        if model:
            available_models = TranslationConfig.get_available_models_for_service(service_name)
            if model not in available_models:
                return create_error_response(f'Invalid model: {model}', 400)
        
        # Debug logging
        current_app.logger.info(f"DEBUG: Setting API key for {service_name}, length: {len(api_key)}, starts with: {api_key[:10]}")
        
        # Set user configuration
        TranslationConfig.set_user_config(service_name, api_key, model)
        
        return create_success_response({
            'message': f'Configuration updated for {service_name}',
            'service_name': service_name,
            'has_api_key': bool(api_key),
            'model': model
        })
        
    except Exception as e:
        current_app.logger.error(f"Set translation service config error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/translation-services/<service_name>/config', methods=['DELETE'])
def clear_translation_service_config(service_name):
    """Clear user-provided configuration for a translation service."""
    try:
        from ..config.translation_config import TranslationConfig
        
        # Validate service name
        if service_name not in TranslationConfig.get_service_names():
            return create_error_response(f'Invalid service name: {service_name}', 400)
        
        # Clear user configuration
        TranslationConfig.clear_user_config(service_name)
        
        return create_success_response({
            'message': f'Configuration cleared for {service_name}',
            'service_name': service_name
        })
        
    except Exception as e:
        current_app.logger.error(f"Clear translation service config error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/translation-services/<service_name>/config', methods=['GET'])
def get_translation_service_config(service_name):
    """Get current configuration for a translation service."""
    try:
        from ..config.translation_config import TranslationConfig
        
        # Validate service name
        if service_name not in TranslationConfig.get_service_names():
            return create_error_response(f'Invalid service name: {service_name}', 400)
        
        # Get configuration
        config = TranslationConfig.get_service_config(service_name)
        user_config = TranslationConfig.get_user_config(service_name)
        available_models = TranslationConfig.get_available_models_for_service(service_name)
        
        return create_success_response({
            'service_name': service_name,
            'config': {
                'enabled': config.get('enabled', False),
                'has_api_key': bool(config.get('api_key')),
                'model': config.get('model'),
                'is_user_configured': bool(user_config.get('api_key'))
            },
            'available_models': available_models,
            'user_config': {
                'has_api_key': bool(user_config.get('api_key')),
                'model': user_config.get('model')
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Get translation service config error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/clear', methods=['POST'])
def clear_data():
    """Clear processing history and session data."""
    try:
        # Clear session history
        if 'processing_history' in session:
            session.pop('processing_history')
        
        # Clear global history
        text_processor.clear_history()
        
        return create_success_response({'message': 'Data cleared successfully'})
        
    except Exception as e:
        current_app.logger.error(f"Clear data error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/history', methods=['GET'])
def get_history():
    """Get processing history."""
    try:
        # Get global processing history
        global_history = text_processor.get_processing_history()
        
        # Get session history
        session_history = session.get('processing_history', [])
        
        return create_success_response({
            'global_history': global_history,
            'session_history': session_history
        })
        
    except Exception as e:
        current_app.logger.error(f"Get history error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        from ..config.app_config import AppConfig
        
        return create_success_response({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': AppConfig.APP_VERSION,
            'app_name': AppConfig.APP_NAME
        })
        
    except Exception as e:
        current_app.logger.error(f"Health check error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/config', methods=['GET'])
def get_config():
    """Get application configuration (non-sensitive)."""
    try:
        from ..config.app_config import AppConfig
        from ..config.translation_config import TranslationConfig
        
        config_info = {
            'app': {
                'name': AppConfig.APP_NAME,
                'version': AppConfig.APP_VERSION,
                'debug': AppConfig.DEBUG,
                'max_file_size': AppConfig.MAX_FILE_SIZE,
                'max_text_length': AppConfig.MAX_TEXT_LENGTH,
                'default_operations': AppConfig.DEFAULT_OPERATIONS
            },
            'translation': TranslationConfig.get_config_summary()
        }
        
        return create_success_response(config_info)
        
    except Exception as e:
        current_app.logger.error(f"Get config error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


# Prompt management endpoints
@api_bp.route('/prompts', methods=['GET'])
def get_prompts():
    """Get all available prompts (default + user prompts)."""
    try:
        from ..config.translation_config import TranslationConfig
        
        all_prompts = TranslationConfig.get_all_prompts()
        user_prompts = TranslationConfig.get_user_prompts()
        
        return create_success_response({
            'prompts': all_prompts,
            'total_count': len(all_prompts),
            'user_count': len(user_prompts),
            'default_count': len(all_prompts) - len(user_prompts)
        })
        
    except Exception as e:
        current_app.logger.error(f"Get prompts error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/prompts', methods=['POST'])
def add_prompt():
    """Add a new user prompt."""
    try:
        from ..config.translation_config import TranslationConfig
        
        # Validate request
        if not request.is_json:
            return create_error_response('Request must be JSON', 400)
        
        data = request.get_json()
        if not data:
            return create_error_response('Invalid request data', 400)
        
        # Extract and validate input
        name = data.get('name', '').strip()
        content = data.get('content', '').strip()
        category = data.get('category', 'custom').strip()
        
        if not name:
            return create_error_response('Prompt name cannot be empty', 400)
        
        if not content:
            return create_error_response('Prompt content cannot be empty', 400)
        
        # Check for duplicate names
        existing_prompts = TranslationConfig.get_user_prompts()
        if any(p['name'] == name for p in existing_prompts):
            return create_error_response(f'Prompt with name "{name}" already exists', 400)
        
        # Add the prompt
        new_prompt = TranslationConfig.add_user_prompt(name, content, category)
        
        return create_success_response({
            'message': 'Prompt added successfully',
            'prompt': new_prompt
        })
        
    except Exception as e:
        current_app.logger.error(f"Add prompt error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/prompts/<prompt_id>', methods=['PUT'])
def update_prompt(prompt_id):
    """Update an existing user prompt."""
    try:
        from ..config.translation_config import TranslationConfig
        
        # Validate request
        if not request.is_json:
            return create_error_response('Request must be JSON', 400)
        
        data = request.get_json()
        if not data:
            return create_error_response('Invalid request data', 400)
        
        # Extract input
        name = data.get('name', '').strip()
        content = data.get('content', '').strip()
        category = data.get('category', '').strip()
        
        # Validate that at least one field is provided
        if not any([name, content, category]):
            return create_error_response('At least one field must be provided for update', 400)
        
        # Check if prompt exists and is user-created
        prompt = TranslationConfig.get_prompt_by_id(prompt_id)
        if not prompt:
            return create_error_response(f'Prompt with ID {prompt_id} not found', 404)
        
        if not prompt.get('is_user_created'):
            return create_error_response('Cannot modify default prompts', 403)
        
        # Check for duplicate names if name is being updated
        if name:
            existing_prompts = TranslationConfig.get_user_prompts()
            if any(p['name'] == name and p['id'] != prompt_id for p in existing_prompts):
                return create_error_response(f'Prompt with name "{name}" already exists', 400)
        
        # Update the prompt
        updated_prompt = TranslationConfig.update_user_prompt(
            prompt_id, 
            name if name else None,
            content if content else None,
            category if category else None
        )
        
        return create_success_response({
            'message': 'Prompt updated successfully',
            'prompt': updated_prompt
        })
        
    except ValueError as e:
        return create_error_response(str(e), 404)
    except Exception as e:
        current_app.logger.error(f"Update prompt error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/prompts/<prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    """Delete a user prompt."""
    try:
        from ..config.translation_config import TranslationConfig
        
        # Check if prompt exists and is user-created
        prompt = TranslationConfig.get_prompt_by_id(prompt_id)
        if not prompt:
            return create_error_response(f'Prompt with ID {prompt_id} not found', 404)
        
        if not prompt.get('is_user_created'):
            return create_error_response('Cannot delete default prompts', 403)
        
        # Delete the prompt
        success = TranslationConfig.delete_user_prompt(prompt_id)
        
        if success:
            return create_success_response({
                'message': 'Prompt deleted successfully',
                'prompt_id': prompt_id
            })
        else:
            return create_error_response(f'Failed to delete prompt {prompt_id}', 500)
        
    except Exception as e:
        current_app.logger.error(f"Delete prompt error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/prompts/<prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    """Get a specific prompt by ID."""
    try:
        from ..config.translation_config import TranslationConfig
        
        prompt = TranslationConfig.get_prompt_by_id(prompt_id)
        
        if not prompt:
            return create_error_response(f'Prompt with ID {prompt_id} not found', 404)
        
        return create_success_response({
            'prompt': prompt
        })
        
    except Exception as e:
        current_app.logger.error(f"Get prompt error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/prompts/category/<category>', methods=['GET'])
def get_prompts_by_category(category):
    """Get prompts by category."""
    try:
        from ..config.translation_config import TranslationConfig
        
        prompts = TranslationConfig.get_prompts_by_category(category)
        
        return create_success_response({
            'category': category,
            'prompts': prompts,
            'count': len(prompts)
        })
        
    except Exception as e:
        current_app.logger.error(f"Get prompts by category error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/prompts/export', methods=['GET'])
def export_prompts():
    """Export all user prompts."""
    try:
        from ..config.translation_config import TranslationConfig
        
        export_data = TranslationConfig.export_prompts()
        
        return create_success_response({
            'export_data': export_data,
            'format': 'json'
        })
        
    except Exception as e:
        current_app.logger.error(f"Export prompts error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/prompts/import', methods=['POST'])
def import_prompts():
    """Import prompts from JSON data."""
    try:
        from ..config.translation_config import TranslationConfig
        
        # Validate request
        if not request.is_json:
            return create_error_response('Request must be JSON', 400)
        
        data = request.get_json()
        if not data:
            return create_error_response('Invalid request data', 400)
        
        # Extract JSON data
        json_data = data.get('json_data', '')
        if not json_data:
            return create_error_response('JSON data cannot be empty', 400)
        
        # Import prompts
        result = TranslationConfig.import_prompts(json_data)
        
        if result['success']:
            return create_success_response({
                'message': 'Prompts imported successfully',
                'imported_count': result['imported_count'],
                'skipped_count': result['skipped_count'],
                'errors': result.get('errors', [])
            })
        else:
            return create_error_response(result['error'], 400)
        
    except Exception as e:
        current_app.logger.error(f"Import prompts error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


@api_bp.route('/prompts/clear', methods=['DELETE'])
def clear_user_prompts():
    """Clear all user prompts."""
    try:
        from ..config.translation_config import TranslationConfig
        
        TranslationConfig.clear_all_user_prompts()
        
        return create_success_response({
            'message': 'All user prompts cleared successfully'
        })
        
    except Exception as e:
        current_app.logger.error(f"Clear prompts error: {str(e)}")
        return create_error_response(f'Server error: {str(e)}', 500)


def _convert_regex_rules_format(regex_rules):
    """
    Convert regex rules from various formats to standard tuple format.
    
    Args:
        regex_rules: List of rules in various formats
        
    Returns:
        List of (pattern, replacement) tuples
    """
    converted_rules = []
    
    for rule in regex_rules:
        if isinstance(rule, str):
            # String format: "pattern -> replacement"
            if " -> " in rule:
                pattern, replacement = rule.split(" -> ", 1)
                converted_rules.append((pattern.strip(), replacement.strip()))
            else:
                raise ValueError(f'Invalid rule format: {rule}')
        elif isinstance(rule, (list, tuple)) and len(rule) == 2:
            # Tuple/list format: (pattern, replacement)
            converted_rules.append((str(rule[0]), str(rule[1])))
        else:
            raise ValueError(f'Invalid rule format: {rule}')
    
    return converted_rules


def _record_processing_history(operations, text_length, **kwargs):
    """Record processing operation in session history."""
    if 'processing_history' not in session:
        session['processing_history'] = []
    
    history_entry = {
        'timestamp': datetime.now().isoformat(),
        'text_length': text_length,
        'operations': operations,
        **kwargs
    }
    
    session['processing_history'].append(history_entry)
    
    # Keep only last 50 entries
    if len(session['processing_history']) > 50:
        session['processing_history'] = session['processing_history'][-50:] 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Response Helpers Module
Contains helper functions for creating standardized API responses.
"""

from typing import Dict, Any, Optional
from flask import jsonify


def create_success_response(data: Any, message: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        message: Optional success message
        
    Returns:
        JSON response
    """
    response = {
        'success': True,
        'data': data
    }
    
    if message:
        response['message'] = message
    
    return jsonify(response)


def create_error_response(error: str, status_code: int = 400, details: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        error: Error message
        status_code: HTTP status code
        details: Optional error details
        
    Returns:
        JSON response
    """
    response = {
        'success': False,
        'error': error
    }
    
    if details:
        response['details'] = details
    
    return jsonify(response), status_code


def create_validation_error_response(validation_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a standardized validation error response.
    
    Args:
        validation_result: Validation result dictionary
        
    Returns:
        JSON response
    """
    return create_error_response(
        error=validation_result.get('error', 'Validation failed'),
        status_code=400
    )


def create_not_found_response(resource: str) -> Dict[str, Any]:
    """
    Create a standardized not found response.
    
    Args:
        resource: Name of the resource that was not found
        
    Returns:
        JSON response
    """
    return create_error_response(
        error=f'{resource} not found',
        status_code=404
    )


def create_unauthorized_response(message: str = 'Unauthorized access') -> Dict[str, Any]:
    """
    Create a standardized unauthorized response.
    
    Args:
        message: Unauthorized message
        
    Returns:
        JSON response
    """
    return create_error_response(
        error=message,
        status_code=401
    )


def create_forbidden_response(message: str = 'Access forbidden') -> Dict[str, Any]:
    """
    Create a standardized forbidden response.
    
    Args:
        message: Forbidden message
        
    Returns:
        JSON response
    """
    return create_error_response(
        error=message,
        status_code=403
    )


def create_server_error_response(message: str = 'Internal server error') -> Dict[str, Any]:
    """
    Create a standardized server error response.
    
    Args:
        message: Server error message
        
    Returns:
        JSON response
    """
    return create_error_response(
        error=message,
        status_code=500
    )


def create_rate_limit_response(message: str = 'Rate limit exceeded') -> Dict[str, Any]:
    """
    Create a standardized rate limit response.
    
    Args:
        message: Rate limit message
        
    Returns:
        JSON response
    """
    return create_error_response(
        error=message,
        status_code=429
    )


def create_pagination_response(data: list, page: int, per_page: int, total: int, 
                             base_url: str) -> Dict[str, Any]:
    """
    Create a standardized pagination response.
    
    Args:
        data: List of data items
        page: Current page number
        per_page: Items per page
        total: Total number of items
        base_url: Base URL for pagination links
        
    Returns:
        JSON response with pagination metadata
    """
    total_pages = (total + per_page - 1) // per_page
    
    pagination_info = {
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1
    }
    
    # Add pagination links
    if pagination_info['has_prev']:
        pagination_info['prev_url'] = f"{base_url}?page={page-1}&per_page={per_page}"
    
    if pagination_info['has_next']:
        pagination_info['next_url'] = f"{base_url}?page={page+1}&per_page={per_page}"
    
    return create_success_response({
        'items': data,
        'pagination': pagination_info
    }) 
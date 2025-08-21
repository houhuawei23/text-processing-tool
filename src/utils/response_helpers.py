#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Response Helpers Module
======================

This module provides utility functions for creating standardized API responses 
throughout the application. All response functions return consistent JSON structures
that follow REST API best practices.

The module ensures:
- Consistent response format across all endpoints
- Proper HTTP status codes for different scenarios
- Type safety with optional parameters
- Easy integration with Flask's jsonify function

Standard Response Format:
------------------------
Success responses:
    {
        "success": true,
        "data": <response_data>,
        "message": "<optional_message>"
    }

Error responses:
    {
        "success": false,
        "error": "<error_message>",
        "details": <optional_error_details>
    }

Functions:
---------
Core Response Functions:
    create_success_response: Create standardized success responses
    create_error_response: Create standardized error responses

HTTP Status-Specific Functions:
    create_validation_error_response: 400 Bad Request for validation errors
    create_unauthorized_response: 401 Unauthorized access
    create_forbidden_response: 403 Forbidden access
    create_not_found_response: 404 Not Found
    create_server_error_response: 500 Internal Server Error
    create_rate_limit_response: 429 Too Many Requests

Specialized Functions:
    create_pagination_response: Paginated data with metadata

Example Usage:
-------------
.. code-block:: python

    from src.utils.response_helpers import create_success_response, create_error_response
    
    # Success response
    return create_success_response({'result': 'processed text'})
    
    # Error response  
    return create_error_response('Invalid input', 400)
    
    # Validation error
    validation_result = {'error': 'Text too long'}
    return create_validation_error_response(validation_result)
"""

from typing import Dict, Any, Optional
from flask import jsonify


def create_success_response(data: Any, message: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Creates a consistent success response format with optional success message.
    The response includes a success flag set to True and the provided data.
    
    Args:
        data (Any): The response data to include. Can be any JSON-serializable type
            including dictionaries, lists, strings, numbers, or None.
        message (Optional[str]): Optional success message to include in the response.
            If provided, adds a "message" field to the response.
    
    Returns:
        Dict[str, Any]: Flask JSON response object with the following structure:
            {
                "success": true,
                "data": <provided_data>,
                "message": "<optional_message>"  // Only if message is provided
            }
    
    Example:
        Basic success response:
        
        >>> create_success_response({'result': 'Hello World'})
        <Response: {"success": true, "data": {"result": "Hello World"}}>
        
        With success message:
        
        >>> create_success_response({'count': 42}, 'Processing completed')
        <Response: {"success": true, "data": {"count": 42}, "message": "Processing completed"}>
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
    
    Creates a consistent error response format with proper HTTP status code.
    The response includes a success flag set to False and the error message.
    
    Args:
        error (str): The error message to include in the response. Should be
            descriptive and user-friendly when possible.
        status_code (int, optional): HTTP status code for the error. Defaults to 400
            (Bad Request). Common codes: 400 (Bad Request), 401 (Unauthorized),
            403 (Forbidden), 404 (Not Found), 500 (Internal Server Error).
        details (Optional[Dict]): Optional dictionary containing additional error
            details such as field-specific validation errors or debugging information.
    
    Returns:
        Tuple[Dict[str, Any], int]: Flask JSON response tuple containing the response
            object and status code with the following structure:
            {
                "success": false,
                "error": "<error_message>",
                "details": <optional_details>  // Only if details are provided
            }
    
    Example:
        Basic error response:
        
        >>> create_error_response('Invalid input data')
        (<Response: {"success": false, "error": "Invalid input data"}>, 400)
        
        With custom status code:
        
        >>> create_error_response('Resource not found', 404)
        (<Response: {"success": false, "error": "Resource not found"}>, 404)
        
        With error details:
        
        >>> create_error_response('Validation failed', 400, {'field': 'email', 'issue': 'invalid format'})
        (<Response: {"success": false, "error": "Validation failed", "details": {"field": "email", "issue": "invalid format"}}>, 400)
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
    Create a standardized pagination response with metadata and navigation links.
    
    Creates a success response containing paginated data along with comprehensive
    pagination metadata including navigation URLs for easy client-side pagination.
    
    Args:
        data (list): List of data items for the current page. Should contain only
            the items that belong to the requested page.
        page (int): Current page number (1-based indexing).
        per_page (int): Number of items per page.
        total (int): Total number of items across all pages.
        base_url (str): Base URL for generating pagination navigation links.
            Should not include query parameters.
    
    Returns:
        Dict[str, Any]: Flask JSON response object containing paginated data and metadata:
            {
                "success": true,
                "data": {
                    "items": <data_list>,
                    "pagination": {
                        "page": <current_page>,
                        "per_page": <items_per_page>,
                        "total": <total_items>,
                        "total_pages": <calculated_total_pages>,
                        "has_next": <boolean>,
                        "has_prev": <boolean>,
                        "next_url": "<next_page_url>",  // Only if has_next is true
                        "prev_url": "<prev_page_url>"   // Only if has_prev is true
                    }
                }
            }
    
    Example:
        >>> create_pagination_response(
        ...     data=[{'id': 1, 'name': 'Item 1'}, {'id': 2, 'name': 'Item 2'}],
        ...     page=2,
        ...     per_page=2,
        ...     total=10,
        ...     base_url='https://api.example.com/items'
        ... )
        <Response: {
            "success": true,
            "data": {
                "items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}],
                "pagination": {
                    "page": 2,
                    "per_page": 2,
                    "total": 10,
                    "total_pages": 5,
                    "has_next": true,
                    "has_prev": true,
                    "next_url": "https://api.example.com/items?page=3&per_page=2",
                    "prev_url": "https://api.example.com/items?page=1&per_page=2"
                }
            }
        }>
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
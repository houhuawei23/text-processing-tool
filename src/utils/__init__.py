"""
Utilities Package
================

This package contains utility functions and helpers used throughout the text processing
framework. It provides common functionality for response formatting, input validation,
and other shared operations.

Modules:
--------
- :mod:`response_helpers`: Standardized API response creation functions
- :mod:`validators`: Input validation functions for API endpoints

The utilities are designed to be:
- Reusable across different parts of the application
- Consistent in their interfaces and return formats
- Well-tested and reliable
- Type-annotated for better development experience

Example Usage:
--------------
.. code-block:: python

    from src.utils.response_helpers import create_success_response, create_error_response
    from src.utils.validators import validate_text_input
    
    # Validate input
    validation_result = validate_text_input(user_input)
    if not validation_result['valid']:
        return create_error_response(validation_result['error'], 400)
    
    # Return success response
    return create_success_response({'processed': True})
"""

# Import commonly used functions for convenience
from .response_helpers import (
    create_success_response,
    create_error_response,
    create_validation_error_response,
    create_not_found_response,
    create_server_error_response
)
from .validators import (
    validate_text_input,
    validate_regex_rules,
    validate_operations
)

# Public API
__all__ = [
    # Response helpers
    'create_success_response',
    'create_error_response', 
    'create_validation_error_response',
    'create_not_found_response',
    'create_server_error_response',
    
    # Validators
    'validate_text_input',
    'validate_regex_rules',
    'validate_operations',
]
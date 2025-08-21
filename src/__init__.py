"""
Text Processing Framework
========================

A comprehensive text processing web application framework with formatting, analysis, 
and translation capabilities built on Flask.

This package provides:
- Text processing and analysis tools
- Translation services with multiple providers
- Regex-based text transformation
- REST API endpoints
- Web interface for text processing

Main Components:
---------------
- :mod:`src.app_factory`: Application factory for creating Flask apps
- :mod:`src.api`: REST API endpoints and route handlers
- :mod:`src.core`: Core text processing components
- :mod:`src.services`: External service integrations (translation)
- :mod:`src.utils`: Utility functions and helpers
- :mod:`src.config`: Configuration management

Quick Start:
-----------
.. code-block:: python

    from src import create_app
    
    # Create application instance
    app = create_app()
    
    # Run the application
    if __name__ == '__main__':
        app.run(debug=True)

API Usage:
----------
.. code-block:: python

    import requests
    
    # Process text via API
    response = requests.post('http://localhost:5000/api/process', 
                           json={'text': 'Hello world!', 
                                'operations': ['format', 'statistics']})
    result = response.json()

Version: 2.0.0
License: MIT
"""

from .app_factory import create_app

# Public API
__all__ = [
    'create_app',
]

# Package metadata
__version__ = '2.0.0'
__author__ = 'Your Name'
__license__ = 'MIT'
__description__ = 'A comprehensive text processing web application framework' 
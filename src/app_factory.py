#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Factory Module
Creates and configures the Flask application with all necessary components.
"""

import os
import logging
from flask import Flask, render_template
from .config.app_config import AppConfig
from .api.routes import api_bp
from .utils.response_helpers import create_error_response


def create_app(config_class=None):
    """
    Application factory function.
    
    Args:
        config_class: Configuration class to use (optional)
        
    Returns:
        Configured Flask application
    """
    # Get the root directory (where the app.py file is located)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create Flask app with correct template and static folder paths
    app = Flask(__name__,
                template_folder=os.path.join(root_dir, 'templates'),
                static_folder=os.path.join(root_dir, 'static'))
    
    # Configure app
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object(AppConfig)
    
    # Setup logging
    _setup_logging(app)
    
    # Validate configuration
    _validate_app_config(app)
    
    # Register blueprints
    _register_blueprints(app)
    
    # Register error handlers
    _register_error_handlers(app)
    
    # Register routes
    _register_routes(app)
    
    # Ensure upload directory exists
    os.makedirs(AppConfig.UPLOAD_FOLDER, exist_ok=True)
    
    return app


def _setup_logging(app):
    """Setup application logging."""
    if not app.debug:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(AppConfig.LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # Configure file logging
        logging.basicConfig(
            level=getattr(logging, AppConfig.LOG_LEVEL.upper()),
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
            handlers=[
                logging.FileHandler(AppConfig.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        
        app.logger.info('Text Processing Tool startup')


def _validate_app_config(app):
    """Validate application configuration."""
    validation_result = AppConfig.validate_config()
    
    if not validation_result['valid']:
        app.logger.error('Configuration validation failed:')
        for error in validation_result['errors']:
            app.logger.error(f'  - {error}')
    
    if validation_result['warnings']:
        app.logger.warning('Configuration warnings:')
        for warning in validation_result['warnings']:
            app.logger.warning(f'  - {warning}')


def _register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(api_bp)


def _register_error_handlers(app):
    """Register error handlers."""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return create_error_response('Page not found', 404)
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        app.logger.error(f'Server error: {error}')
        return create_error_response('Internal server error', 500)
    
    @app.errorhandler(413)
    def too_large(error):
        """Handle file too large errors."""
        return create_error_response('File too large', 413)
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors."""
        return create_error_response('Bad request', 400)
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle method not allowed errors."""
        return create_error_response('Method not allowed', 405)


def _register_routes(app):
    """Register main application routes."""
    
    @app.route('/')
    def index():
        """Main application page."""
        return render_template('index.html')
    
    @app.route('/test')
    def test_frontend():
        """Test frontend page for debugging."""
        return app.send_static_file('test_frontend.html')
    
    @app.route('/health')
    def health():
        """Simple health check endpoint."""
        return {'status': 'healthy', 'app': AppConfig.APP_NAME} 
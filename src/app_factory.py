#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Factory Module
==========================

This module implements the Flask application factory pattern, providing a clean and
configurable way to create Flask application instances with all necessary components.

The factory pattern allows for:
- Multiple application instances with different configurations
- Easy testing with different configurations
- Proper separation of concerns
- Deferred initialization of components

Key Features:
- Automatic configuration loading and validation
- Comprehensive error handling setup
- Blueprint registration for modular routing
- Logging configuration with file and console output
- Static file and template directory configuration

Example Usage:
    Basic application creation:

    .. code-block:: python

        from src.app_factory import create_app

        # Create app with default configuration
        app = create_app()

        # Create app with custom configuration
        from src.config.app_config import TestConfig
        test_app = create_app(TestConfig)

    Custom configuration:

    .. code-block:: python

        class CustomConfig:
            DEBUG = True
            TESTING = True
            SECRET_KEY = 'custom-secret-key'

        app = create_app(CustomConfig)

Functions:
    create_app: Main factory function for creating Flask applications

Internal Functions:
    _setup_logging: Configure application logging
    _validate_app_config: Validate application configuration
    _register_blueprints: Register Flask blueprints
    _register_error_handlers: Setup error handlers
    _register_routes: Register main application routes
"""

import os
import logging
from flask import Flask, render_template
from .config.app_config import AppConfig
from .api.routes import api_bp
from .utils.response_helpers import create_error_response
from dotenv import load_dotenv


def create_app(config_class=None):
    """
    Create and configure a Flask application instance.

    This is the main application factory function that creates a Flask application
    with all necessary components configured and initialized. The function follows
    the factory pattern to allow for multiple application instances with different
    configurations.

    The function performs the following initialization steps:
    1. Creates Flask application with proper template/static paths
    2. Loads configuration from the provided class or default AppConfig
    3. Sets up logging with file and console handlers
    4. Validates the configuration and logs any issues
    5. Registers blueprints for modular routing
    6. Sets up comprehensive error handlers
    7. Registers main application routes
    8. Creates necessary directories (uploads, logs)

    Args:
        config_class (class, optional): Configuration class to use for the application.
            If None, uses the default AppConfig. The class should contain Flask
            configuration variables as class attributes.

            Example:
                class MyConfig:
                    DEBUG = True
                    SECRET_KEY = 'my-secret'
                    DATABASE_URL = 'sqlite:///app.db'

    Returns:
        Flask: A fully configured Flask application instance ready to run.

    Raises:
        OSError: If required directories cannot be created
        ImportError: If configuration class cannot be imported

    Example:
        Basic usage:

        >>> from src.app_factory import create_app
        >>> app = create_app()
        >>> app.run(debug=True)

        With custom configuration:

        >>> class TestConfig:
        ...     TESTING = True
        ...     DEBUG = True
        >>> test_app = create_app(TestConfig)

    Note:
        The application will automatically create necessary directories such as
        the upload folder and log directory if they don't exist.
    """
    # Get the root directory (where the app.py file is located)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Create Flask app with correct template and static folder paths
    app = Flask(
        __name__,
        template_folder=os.path.join(root_dir, "templates"),
        static_folder=os.path.join(root_dir, "static"),
    )
    load_dotenv()  # 默认会读取当前目录下的 .env

    print(os.getenv("MICROSOFT_API_KEY"))
    print(os.getenv("MICROSOFT_REGION"))
    print(os.getenv("MICROSOFT_API_URL"))
    print(os.getenv("DEEPSEEK_API_KEY"))
    print(os.getenv("OPENAI_API_KEY"))
    print(os.getenv("DEEPSEEK_API_URL"))
    print(os.getenv("OPENAI_API_URL"))

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
    """
    Configure application logging with file and console handlers.

    Sets up comprehensive logging for the application with both file and console
    output. In production mode (non-debug), creates log files and configures
    appropriate log levels and formatting.

    Args:
        app (Flask): The Flask application instance to configure logging for.

    Note:
        - Only sets up file logging when app.debug is False
        - Creates log directory if it doesn't exist
        - Uses log level and file path from AppConfig
        - Logs both to file and console for production
    """
    if not app.debug:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(AppConfig.LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Configure file logging
        logging.basicConfig(
            level=getattr(logging, AppConfig.LOG_LEVEL.upper()),
            format="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
            handlers=[logging.FileHandler(AppConfig.LOG_FILE), logging.StreamHandler()],
        )

        app.logger.info("Text Processing Tool startup")


def _validate_app_config(app):
    """
    Validate the application configuration and log any issues.

    Performs validation of the current application configuration using the
    AppConfig.validate_config() method and logs any validation errors or
    warnings found.

    Args:
        app (Flask): The Flask application instance with loaded configuration.

    Note:
        - Logs validation errors at ERROR level
        - Logs validation warnings at WARNING level
        - Does not raise exceptions, only logs issues
    """
    validation_result = AppConfig.validate_config()

    if not validation_result["valid"]:
        app.logger.error("Configuration validation failed:")
        for error in validation_result["errors"]:
            app.logger.error(f"  - {error}")

    if validation_result["warnings"]:
        app.logger.warning("Configuration warnings:")
        for warning in validation_result["warnings"]:
            app.logger.warning(f"  - {warning}")


def _register_blueprints(app):
    """
    Register Flask blueprints for modular routing.

    Registers all application blueprints with the Flask application instance.
    Currently registers the API blueprint which contains all REST API endpoints.

    Args:
        app (Flask): The Flask application instance to register blueprints with.

    Blueprints Registered:
        - api_bp: REST API endpoints (mounted at /api)
    """
    app.register_blueprint(api_bp)


def _register_error_handlers(app):
    """
    Register comprehensive error handlers for the application.

    Sets up error handlers for common HTTP status codes to provide consistent
    error responses across the application. All error responses use the
    standardized format from response_helpers.

    Args:
        app (Flask): The Flask application instance to register error handlers with.

    Error Handlers:
        - 400: Bad Request
        - 404: Not Found
        - 405: Method Not Allowed
        - 413: Request Entity Too Large
        - 500: Internal Server Error

    Note:
        All error handlers return JSON responses using create_error_response()
        for consistency with the REST API.
    """

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return create_error_response("Page not found", 404)

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        app.logger.error(f"Server error: {error}")
        return create_error_response("Internal server error", 500)

    @app.errorhandler(413)
    def too_large(error):
        """Handle file too large errors."""
        return create_error_response("File too large", 413)

    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors."""
        return create_error_response("Bad request", 400)

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle method not allowed errors."""
        return create_error_response("Method not allowed", 405)


def _register_routes(app):
    """
    Register main application routes.

    Registers the core application routes that are not part of blueprints.
    These include the main web interface routes and utility endpoints.

    Args:
        app (Flask): The Flask application instance to register routes with.

    Routes:
        - /: Main application page (renders index.html template)
        - /test: Test frontend page for debugging
        - /health: Health check endpoint returning application status
    """

    @app.route("/")
    def index():
        """
        Main application page.

        Renders the main web interface for the text processing application.

        Returns:
            str: Rendered HTML template for the main application interface.
        """
        return render_template("index.html")

    @app.route("/test")
    def test_frontend():
        """
        Test frontend page for debugging.

        Serves a static test page for frontend debugging and development.
        Useful for testing API endpoints and frontend functionality.

        Returns:
            str: Static HTML file for testing frontend components.
        """
        return app.send_static_file("test_frontend.html")

    @app.route("/health")
    def health():
        """
        Health check endpoint.

        Provides a simple health check endpoint for monitoring and load balancers.
        Returns basic application status information.

        Returns:
            dict: JSON response with status and application name.
                Format: {'status': 'healthy', 'app': '<app_name>'}
        """
        return {"status": "healthy", "app": AppConfig.APP_NAME}

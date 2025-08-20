#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Application Entry Point
Text Processing Web Application
"""

import argparse
import sys
from src import create_app
from src.config.app_config import AppConfig


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Text Processing Web Application')
    parser.add_argument('--host', default=AppConfig.DEFAULT_HOST, 
                       help=f'Host address (default: {AppConfig.DEFAULT_HOST})')
    parser.add_argument('--port', type=int, default=AppConfig.DEFAULT_PORT, 
                       help=f'Port number (default: {AppConfig.DEFAULT_PORT})')
    parser.add_argument('--debug', action='store_true', 
                       help='Enable debug mode')
    parser.add_argument('--config', help='Configuration file path')
    
    return parser.parse_args()


def main():
    """Main application function."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Create application
    app = create_app()
    
    # Set debug mode
    if args.debug:
        app.config['DEBUG'] = True
    
    # Run application
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=app.config.get('DEBUG', False),
            threaded=True
        )
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 
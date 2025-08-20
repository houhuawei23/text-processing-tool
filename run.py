#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Application Startup Script
Provides better startup experience with dependency checking and configuration validation.
"""

import os
import sys
import argparse
import webbrowser
import time
import threading
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")


def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'flask',
        'requests',
        'werkzeug',
        'jinja2'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            os.system(f"{sys.executable} -m pip install -r requirements.txt")
            print("✅ Dependencies installed successfully")
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)


def create_directories():
    """Create necessary directories."""
    directories = [
        'uploads',
        'logs',
        'static/assets'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")


def validate_configuration():
    """Validate application configuration."""
    try:
        from src.config.app_config import AppConfig
        validation_result = AppConfig.validate_config()
        
        if not validation_result['valid']:
            print("❌ Configuration validation failed:")
            for error in validation_result['errors']:
                print(f"   - {error}")
            return False
        
        if validation_result['warnings']:
            print("⚠️  Configuration warnings:")
            for warning in validation_result['warnings']:
                print(f"   - {warning}")
        
        print("✅ Configuration validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation error: {e}")
        return False


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Text Processing Web Application')
    parser.add_argument('--host', default='127.0.0.1', help='Host address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5009, help='Port number (default: 5009)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')
    parser.add_argument('--skip-checks', action='store_true', help='Skip dependency and configuration checks')
    
    return parser.parse_args()


def open_browser(host, port, delay=2):
    """Open browser after a delay."""
    time.sleep(delay)
    url = f"http://{host}:{port}"
    
    try:
        webbrowser.open(url)
        print(f"🌐 Browser opened: {url}")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print(f"   Please manually visit: {url}")


def main():
    """Main startup function."""
    print("🚀 Starting Text Processing Web Application...")
    print("=" * 60)
    
    # Parse arguments
    args = parse_arguments()
    
    if not args.skip_checks:
        # Check Python version
        check_python_version()
        
        # Check dependencies
        check_dependencies()
        
        # Create directories
        create_directories()
        
        # Validate configuration
        if not validate_configuration():
            print("❌ Configuration validation failed. Please fix the issues above.")
            sys.exit(1)
    
    print("\n📋 Configuration:")
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   Debug: {'Yes' if args.debug else 'No'}")
    print("=" * 60)
    
    # Set environment variables
    if args.debug:
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = '1'
    
    # Import and create application
    try:
        from src import create_app
        app = create_app()
        print("✅ Application created successfully")
    except ImportError as e:
        print(f"❌ Failed to import application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to create application: {e}")
        sys.exit(1)
    
    # Start browser in background thread
    if not args.no_browser:
        browser_thread = threading.Thread(
            target=open_browser, 
            args=(args.host, args.port),
            daemon=True
        )
        browser_thread.start()
    
    # Start application
    try:
        print("🌐 Starting web server...")
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 
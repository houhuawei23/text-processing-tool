# Text Processing Web Application (Restructured)

A modern, well-structured text processing web application built with Python Flask. This application provides comprehensive text analysis, formatting, regex processing, and translation capabilities through a clean, modular architecture.

## 🚀 Features

### Core Functionality
- **Text Processing**: Format, analyze, and transform text with multiple operations
- **Statistical Analysis**: Detailed text statistics including character counts, word frequency, and readability metrics
- **Regex Processing**: Advanced regex pattern matching and replacement with custom rules
- **Translation Services**: Multi-service translation support (DeepSeek, OpenAI)
- **Prompt Management**: Add, save, select, export, and import translation prompts
- **Real-time Processing**: Fast, responsive text processing with progress indicators

### Technical Features
- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **RESTful API**: Comprehensive API endpoints for all functionality
- **Error Handling**: Robust error handling and validation
- **Configuration Management**: Centralized configuration with environment variable support
- **Logging**: Comprehensive logging system for debugging and monitoring
- **Session Management**: User session handling with processing history

## 📁 Project Structure

```
restructured_app/
├── src/                          # Main source code
│   ├── core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── text_processor.py     # Main text processing orchestrator
│   │   ├── text_analyzer.py      # Text analysis and statistics
│   │   └── text_formatter.py     # Text formatting and regex operations
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   └── routes.py             # API route handlers
│   ├── services/                 # External service integrations
│   │   ├── __init__.py
│   │   └── translation_service.py # Translation service implementations
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   ├── app_config.py         # Main application configuration
│   │   └── translation_config.py # Translation service configuration
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py         # Input validation functions
│   │   └── response_helpers.py   # API response helpers
│   ├── __init__.py
│   └── app_factory.py            # Flask application factory
├── static/                       # Static assets
│   ├── css/
│   │   └── style.css             # Application styles
│   ├── js/
│   │   └── app.js                # Frontend JavaScript
│   └── assets/                   # Additional assets
├── templates/                    # HTML templates
│   └── index.html                # Main application interface
├── tests/                        # Test files
├── docs/                         # Documentation
├── logs/                         # Application logs
├── uploads/                      # File upload directory
├── app.py                        # Main application entry point
├── run.py                        # Enhanced startup script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Quick Start

1. **Clone or download the project**
   ```bash
   cd restructured_app
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   # Using the enhanced startup script (recommended)
   python run.py
   
   # Or using the basic entry point
   python app.py
   ```

5. **Access the application**
   Open your browser and visit: http://localhost:5009

### Advanced Startup Options

```bash
# Run with custom host and port
python run.py --host 0.0.0.0 --port 8080

# Run in debug mode
python run.py --debug

# Run without automatic browser opening
python run.py --no-browser

# Skip dependency checks (for faster startup)
python run.py --skip-checks
```

## ⚙️ Configuration

### Environment Variables

Set these environment variables for production use:

```bash
# Application
export SECRET_KEY="your-secret-key-here"
export FLASK_ENV="production"
export LOG_LEVEL="INFO"

# Translation Services
export DEEPSEEK_API_KEY="your-deepseek-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

### Configuration Files

The application uses centralized configuration classes:
- `AppConfig`: Main application settings
- `TranslationConfig`: Translation service settings

## 🔧 API Reference

### Text Processing

**POST** `/api/process`
```json
{
    "text": "Text to process",
    "operations": ["format", "statistics", "analysis"]
}
```

### Regex Processing

**POST** `/api/regex`
```json
{
    "text": "Text to process",
    "regex_rules": [
        ["pattern", "replacement"],
        ["\\s+", " "]
    ]
}
```

### Translation

**POST** `/api/translate`
```json
{
    "text": "Text to translate",
    "prompt": "Translate to Chinese",
    "service_name": "deepseek"
}
```

### Other Endpoints

- **GET** `/api/health` - Health check
- **GET** `/api/config` - Application configuration
- **GET** `/api/translation-services` - Available translation services
- **GET** `/api/history` - Processing history
- **POST** `/api/clear` - Clear history

## 🧪 Testing

Run tests to verify functionality:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_text_processor.py

# Run with coverage
python -m pytest --cov=src tests/
```

## 📊 Features in Detail

### Text Processing Operations

1. **Format**: Clean and normalize text
   - Remove extra whitespace
   - Normalize sentence endings
   - Apply default regex rules

2. **Statistics**: Comprehensive text analysis
   - Character, word, line, and sentence counts
   - Character type distribution
   - Word frequency analysis
   - Average word and sentence lengths

3. **Analysis**: Advanced text analysis
   - Readability metrics (Flesch Reading Ease)
   - Sentiment analysis
   - Language feature detection
   - Content type identification

### Regex Processing

- Support for multiple rule formats
- Pattern validation
- Error handling for invalid patterns
- Batch processing of multiple rules

### Translation Services

- **DeepSeek**: Fast, reliable translation
- **OpenAI**: High-quality translation with GPT models
- **Long Text Support**: Automatic text chunking for large documents
- **Retry Mechanism**: Automatic retry on failures
- **Progress Tracking**: Real-time progress for long translations

### Prompt Management

- **Custom Prompts**: Create and save personalized translation prompts
- **Prompt Categories**: Organize prompts by type (translation, polish, summary, custom)
- **Quick Selection**: Fast access to saved prompts through modal interface
- **Import/Export**: Backup and restore prompt configurations via JSON files
- **Default Prompts**: Pre-configured prompts for common translation tasks

## 🔒 Security Features

- Input validation and sanitization
- XSS protection
- CSRF protection
- File upload restrictions
- Rate limiting support
- Secure session management

## 📈 Performance Optimizations

- Efficient text processing algorithms
- Memory-optimized operations
- Asynchronous processing for long operations
- Caching for repeated operations
- Optimized regex pattern matching

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the correct directory
   cd restructured_app
   
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

2. **Port Already in Use**
   ```bash
   # Use a different port
   python run.py --port 5008
   ```

3. **Translation Service Errors**
   - Check API key configuration
   - Verify internet connection
   - Check service availability

4. **Permission Errors**
   ```bash
   # Ensure write permissions
   chmod +x run.py
   chmod +x app.py
   ```

### Logs

Check application logs for detailed error information:
```bash
tail -f logs/app.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 src/

# Run type checking
mypy src/

# Run tests with coverage
pytest --cov=src --cov-report=html
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆕 Changelog

### Version 2.0.0 (Restructured)
- Complete code restructuring with modular architecture
- Improved error handling and validation
- Enhanced API design with standardized responses
- Better configuration management
- Comprehensive logging system
- Improved startup script with dependency checking
- Better separation of concerns
- Enhanced documentation

### Version 1.0.0 (Original)
- Initial release with basic text processing
- Web interface implementation
- Basic API endpoints
- Translation service integration

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review the logs for error details
- Open an issue on the project repository

---

**Enjoy using the Text Processing Tool!** 🚀 
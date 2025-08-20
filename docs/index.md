# Text Processing Tool Documentation

Welcome to the comprehensive documentation for the Text Processing Tool, a powerful web application for text analysis, formatting, and translation.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/text-processing-tool.git
cd text-processing-tool

# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt

# Run the application
python run.py
```

### Basic Usage

1. Open your browser and navigate to `http://localhost:5009`
2. Enter your text in the input area
3. Select processing options (format, statistics, analysis)
4. Click "处理文本" to process your text
5. View results in the output area

## 📚 Documentation Sections

### User Guide
- [Getting Started](user-guide/getting-started.md)
- [Text Processing](user-guide/text-processing.md)
- [Regex Operations](user-guide/regex-operations.md)
- [Translation Features](user-guide/translation.md)
- [Advanced Features](user-guide/advanced-features.md)

### Developer Guide
- [Installation](developer-guide/installation.md)
- [Architecture](developer-guide/architecture.md)
- [API Reference](developer-guide/api-reference.md)
- [Testing](developer-guide/testing.md)
- [Deployment](developer-guide/deployment.md)

### Configuration
- [Environment Variables](configuration/environment.md)
- [API Keys Setup](configuration/api-keys.md)
- [Security Settings](configuration/security.md)

## 🛠️ Features

### Core Functionality
- **Text Formatting**: Normalize whitespace, fix punctuation, improve readability
- **Statistical Analysis**: Character count, word frequency, sentence analysis
- **Content Analysis**: Sentiment analysis, readability scores, language detection
- **Regex Processing**: Advanced pattern matching and replacement
- **Translation**: Multi-language translation using AI services

### Advanced Features
- **Batch Processing**: Handle multiple texts efficiently
- **Custom Rules**: Create and save regex patterns
- **History Tracking**: Monitor processing history
- **Export Options**: Save results in various formats
- **API Access**: RESTful API for integration

## 🔧 Development

### Prerequisites
- Python 3.8 or higher
- Flask 2.3.0 or higher
- Modern web browser

### Development Setup
```bash
# Install development dependencies
make install-dev

# Run tests
make test

# Format code
make format

# Start development server
make serve
```

### Testing
```bash
# Run all tests
python tests/run_all_tests.py

# Run quick tests
python tests/run_all_tests.py --quick

# Run with coverage
make test-coverage
```

## 📊 Project Structure

```
text-processing-tool/
├── src/                    # Source code
│   ├── core/              # Core processing modules
│   ├── api/               # API endpoints
│   ├── services/          # External services
│   ├── config/            # Configuration
│   └── utils/             # Utility functions
├── tests/                 # Test suite
├── docs/                  # Documentation
├── static/                # Static files
├── templates/             # HTML templates
└── requirements.txt       # Dependencies
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/text-processing-tool/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/text-processing-tool/discussions)
- **Documentation**: [Read the Docs](https://text-processing-tool.readthedocs.io/)

## 🔗 Links

- **Repository**: [GitHub](https://github.com/yourusername/text-processing-tool)
- **Live Demo**: [Demo Site](https://text-processing-tool.herokuapp.com)
- **PyPI Package**: [PyPI](https://pypi.org/project/text-processing-tool/)

---

**Note**: This documentation is continuously updated. For the latest information, please check the [GitHub repository](https://github.com/yourusername/text-processing-tool). 
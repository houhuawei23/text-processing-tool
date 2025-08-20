# Contributing to Text Processing Tool

Thank you for your interest in contributing to the Text Processing Tool! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Reports**: Report bugs and issues
- **Feature Requests**: Suggest new features
- **Code Contributions**: Submit code improvements
- **Documentation**: Improve or add documentation
- **Testing**: Help with testing and quality assurance
- **Translation**: Help translate the application

### Before You Start

1. **Check Existing Issues**: Search existing issues to avoid duplicates
2. **Read Documentation**: Familiarize yourself with the project structure
3. **Set Up Development Environment**: Follow the installation guide

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A code editor (VS Code, PyCharm, etc.)

### Installation

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/text-processing-tool.git
cd text-processing-tool

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests to ensure everything works
python tests/run_all_tests.py
```

## 📝 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clean, well-documented code
- Follow the existing code style
- Add tests for new functionality
- Update documentation if needed

### 3. Run Tests and Checks

```bash
# Run all tests
make test

# Run linting
make lint

# Format code
make format

# Run security checks
make security

# Run all checks
make check-all
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific test file
python -m pytest tests/test_core_modules.py -v

# Run with coverage
make test-coverage

# Run quick tests
python tests/run_all_tests.py --quick
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Include edge cases and boundary conditions
- Mock external dependencies

### Test Structure

```python
def test_feature_name():
    """Test description of what is being tested."""
    # Arrange
    input_data = "test input"
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result == expected_output
```

## 📋 Code Style Guidelines

### Python Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Use isort for import sorting
- Maximum line length: 88 characters
- Use type hints where appropriate

### Documentation

- Use docstrings for all functions and classes
- Follow Google docstring format
- Include examples in docstrings
- Update README.md for user-facing changes

### Example Code Style

```python
from typing import Dict, List, Optional

def process_text(text: str, options: Optional[List[str]] = None) -> Dict[str, any]:
    """Process text with specified options.
    
    Args:
        text: The text to process
        options: List of processing options
        
    Returns:
        Dictionary containing processing results
        
    Raises:
        ValueError: If text is empty or invalid
        
    Example:
        >>> result = process_text("Hello world", ["format", "statistics"])
        >>> print(result["processed_text"])
        "Hello world."
    """
    if not text:
        raise ValueError("Text cannot be empty")
    
    # Process the text
    result = {
        "original_text": text,
        "processed_text": text.strip(),
        "options": options or []
    }
    
    return result
```

## 🔍 Code Review Process

### Pull Request Guidelines

1. **Title**: Use clear, descriptive titles
2. **Description**: Explain what and why, not how
3. **Tests**: Ensure all tests pass
4. **Documentation**: Update docs if needed
5. **Screenshots**: Include screenshots for UI changes

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered
- [ ] Backward compatibility maintained

## 🐛 Bug Reports

### Bug Report Template

```markdown
**Bug Description**
A clear description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. Windows 10, macOS 12]
- Python Version: [e.g. 3.9.7]
- Browser: [e.g. Chrome 96]

**Additional Context**
Any other context about the problem.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature.

**Use Case**
Why this feature would be useful.

**Proposed Implementation**
How you think it could be implemented.

**Alternatives Considered**
Other solutions you've considered.

**Additional Context**
Any other context or screenshots.
```

## 📚 Documentation Contributions

### Documentation Guidelines

- Use clear, concise language
- Include code examples
- Add screenshots for UI features
- Keep documentation up to date
- Use proper markdown formatting

### Documentation Structure

```
docs/
├── index.md              # Main documentation
├── user-guide/           # User documentation
├── developer-guide/      # Developer documentation
├── configuration/        # Configuration docs
└── api/                 # API documentation
```

## 🔒 Security

### Security Guidelines

- Never commit sensitive information (API keys, passwords)
- Use environment variables for configuration
- Validate all user inputs
- Follow security best practices
- Report security issues privately

### Reporting Security Issues

If you discover a security vulnerability, please report it privately:

1. **Don't create a public issue**
2. Email: security@yourdomain.com
3. Include detailed description and steps to reproduce
4. We'll respond within 48 hours

## 🏷️ Release Process

### Version Numbers

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version number updated
- [ ] Security review completed
- [ ] Release notes prepared

## 🎉 Recognition

### Contributors

All contributors will be recognized in:

- Project README
- Release notes
- Contributor hall of fame
- GitHub contributors page

### Types of Recognition

- **Code Contributors**: Listed in contributors file
- **Documentation Contributors**: Acknowledged in docs
- **Bug Reporters**: Thanked in issue resolution
- **Feature Requesters**: Credited in feature implementation

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and discussions
- **Email**: For security issues or private matters

### Before Asking for Help

1. Check existing documentation
2. Search existing issues
3. Try to reproduce the problem
4. Provide detailed information

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Text Processing Tool! 🚀 
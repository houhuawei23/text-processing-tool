# Test Suite Documentation

This directory contains comprehensive tests for the restructured text processing application. The test suite is designed to verify the correctness of all components and ensure the application works correctly after modifications.

## 📁 Test Files Overview

### Core Tests
- **`test_basic_functionality.py`** - Basic functionality tests for core modules
- **`test_core_modules.py`** - Comprehensive tests for text processor, analyzer, and formatter
- **`test_api_endpoints.py`** - API endpoint tests including validation and response formats
- **`test_configuration.py`** - Configuration management tests
- **`test_integration.py`** - Full application integration tests

### Test Runner
- **`run_all_tests.py`** - Comprehensive test runner with detailed reporting

## 🚀 Running Tests

### Quick Start
```bash
# Run all tests
python tests/run_all_tests.py

# Run quick tests only (for development)
python tests/run_all_tests.py --quick

# Show help
python tests/run_all_tests.py --help
```

### Individual Test Files
```bash
# Run specific test file
python -m unittest tests.test_core_modules
python -m unittest tests.test_api_endpoints
python -m unittest tests.test_configuration
python -m unittest tests.test_integration

# Run with verbose output
python -m unittest tests.test_core_modules -v
```

### Using Python's unittest
```bash
# Discover and run all tests
python -m unittest discover tests

# Run with coverage (if coverage is installed)
python -m coverage run -m unittest discover tests
python -m coverage report
```

## 📊 Test Coverage

### Core Modules (`test_core_modules.py`)
- **TextProcessor**: Initialization, text processing, regex processing, input validation, history management
- **TextAnalyzer**: Statistics generation, text analysis, language detection, sentiment analysis
- **TextFormatter**: Text formatting, regex replacements, rule parsing, pattern validation
- **Integration**: Full processing pipeline, component interaction

### API Endpoints (`test_api_endpoints.py`)
- **Health Check**: `/api/health` endpoint
- **Configuration**: `/api/config` endpoint
- **Text Processing**: `/api/process` endpoint with various scenarios
- **Regex Processing**: `/api/regex` endpoint with validation
- **Translation**: `/api/translate` endpoint with mocking
- **History & Clear**: `/api/history` and `/api/clear` endpoints
- **Error Handling**: Invalid requests, missing data, server errors
- **Validation**: Input validation functions
- **Response Helpers**: Response format helpers

### Configuration (`test_configuration.py`)
- **AppConfig**: Basic configuration, environment variables, validation
- **TranslationConfig**: Service configuration, API keys, service availability
- **Integration**: Configuration consistency and validation

### Integration (`test_integration.py`)
- **Full Workflow**: Complete text processing workflow
- **Regex Workflow**: Complete regex processing workflow
- **Translation Workflow**: Complete translation workflow
- **Error Handling**: Comprehensive error handling
- **Session Management**: Session handling and history
- **Static Files**: CSS and JavaScript serving
- **Template Rendering**: HTML template rendering
- **Performance**: Large text processing, multiple operations

## 🧪 Test Categories

### Unit Tests
- Individual component testing
- Isolated functionality verification
- Mock dependencies where appropriate

### Integration Tests
- Component interaction testing
- End-to-end workflow testing
- Real API endpoint testing

### Validation Tests
- Input validation testing
- Error handling verification
- Edge case testing

### Performance Tests
- Large text processing
- Multiple operations
- Memory usage verification

## 📋 Test Requirements

### Prerequisites
- Python 3.7 or higher
- All application dependencies installed
- Access to application source code

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up test environment (optional)
export FLASK_ENV=testing
export FLASK_DEBUG=false
```

## 🔧 Test Configuration

### Test Environment Variables
```bash
# For testing without external API calls
export TESTING_MODE=true

# For testing with specific configuration
export TEST_CONFIG_PATH=tests/test_config.json
```

### Mock Configuration
Tests use mocking for:
- External API calls (translation services)
- File system operations
- Network requests
- Environment variables

## 📈 Test Results

### Success Indicators
- All tests pass (0 failures, 0 errors)
- Success rate: 100%
- All test categories covered
- Performance within acceptable limits

### Common Issues
- **Import Errors**: Check Python path and module structure
- **Configuration Errors**: Verify environment variables and config files
- **API Errors**: Check external service availability or mocking
- **File System Errors**: Verify directory permissions and paths

## 🛠️ Adding New Tests

### Test File Structure
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test description for new functionality.
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from module_to_test import ClassToTest


class TestNewFunctionality(unittest.TestCase):
    """Test new functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def test_new_feature(self):
        """Test new feature functionality."""
        # Test implementation
        pass
    
    def tearDown(self):
        """Clean up test fixtures."""
        pass


if __name__ == '__main__':
    unittest.main()
```

### Test Naming Conventions
- Test classes: `Test[ComponentName]`
- Test methods: `test_[feature_name]`
- Descriptive names that explain what is being tested

### Test Best Practices
- Use descriptive test names
- Test both success and failure cases
- Include edge cases and boundary conditions
- Use appropriate assertions
- Clean up resources in tearDown
- Mock external dependencies
- Test one thing per test method

## 📊 Test Metrics

### Coverage Goals
- **Line Coverage**: >90%
- **Branch Coverage**: >85%
- **Function Coverage**: >95%

### Performance Benchmarks
- **Test Execution Time**: <30 seconds for full suite
- **Memory Usage**: <100MB for large text processing
- **Response Time**: <2 seconds for API endpoints

## 🔍 Debugging Tests

### Common Debugging Commands
```bash
# Run single test with verbose output
python -m unittest tests.test_core_modules.TestTextProcessor.test_process_text_basic -v

# Run tests with debugger
python -m pdb -m unittest tests.test_core_modules

# Run tests with specific pattern
python -m unittest discover tests -p "test_*processor*"
```

### Debugging Tips
- Use `print()` statements for debugging
- Check test output for detailed error messages
- Verify test data and expected results
- Check import paths and module structure
- Verify environment variables and configuration

## 📝 Test Maintenance

### Regular Tasks
- Update tests when adding new features
- Review and update test data
- Monitor test performance
- Update mocks for external dependencies
- Verify test coverage goals

### Test Review Checklist
- [ ] All new features have corresponding tests
- [ ] Tests cover both success and failure cases
- [ ] Edge cases are properly tested
- [ ] Performance tests are included where appropriate
- [ ] Tests are properly documented
- [ ] Test data is realistic and comprehensive

## 🎯 Continuous Integration

### CI/CD Integration
Tests are designed to run in CI/CD environments:
- Automated test execution
- Coverage reporting
- Performance monitoring
- Failure notifications

### Pre-commit Hooks
Consider adding pre-commit hooks to:
- Run quick tests before commits
- Check code coverage
- Validate test structure
- Ensure all tests pass

---

**Note**: This test suite is designed to be comprehensive and maintainable. Regular updates and maintenance are essential to ensure the application's reliability and correctness. 
.PHONY: help install install-dev test test-coverage lint format clean build docs serve check-all

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-coverage - Run tests with coverage"
	@echo "  lint         - Run linting checks"
	@echo "  format       - Format code with black and isort"
	@echo "  clean        - Clean build artifacts"
	@echo "  build        - Build package"
	@echo "  docs         - Build documentation"
	@echo "  serve        - Start development server"
	@echo "  check-all    - Run all checks (lint, test, security)"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

# Testing
test:
	python -m pytest tests/ -v

test-coverage:
	python -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

test-quick:
	python tests/run_all_tests.py --quick

# Code Quality
lint:
	flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	black --check --diff src/ tests/
	isort --check-only --diff src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

# Security
security:
	bandit -r src/ -f json -o bandit-report.json
	safety check

# Documentation
docs:
	sphinx-build -b html docs/ docs/_build/html

docs-serve:
	sphinx-build -b html docs/ docs/_build/html
	python -m http.server 8001 -d docs/_build/html

# Development
serve:
	python run.py --debug

serve-prod:
	python run.py --host 0.0.0.0 --port 5000

# Build and Clean
build:
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf docs/_build/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# All checks
check-all: lint test security

# Docker
docker-build:
	docker build -t text-processing-tool .

docker-run:
	docker run -p 5000:5000 text-processing-tool

# Database
db-migrate:
	@echo "No database migrations needed for this project"

# Environment setup
env-setup:
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source venv/bin/activate  # On Unix/macOS"
	@echo "  venv\\Scripts\\activate     # On Windows"

# Pre-commit
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

# Tox
tox-all:
	tox

tox-lint:
	tox -e lint

tox-security:
	tox -e security

# Performance
benchmark:
	python -m pytest tests/ -m "slow" -v

# Release
release-check:
	@echo "Checking release readiness..."
	python -c "import src; print('Version:', src.__version__)"
	check-manifest
	twine check dist/*

release-build:
	rm -rf dist/ build/
	python -m build
	twine check dist/*

# Development helpers
dev-setup: install-dev pre-commit-install
	@echo "Development environment setup complete!"

quick-test:
	python -m pytest tests/ -x -v --tb=short

watch-test:
	watchmedo auto-restart --patterns="*.py" --recursive -- python -m pytest tests/ -v

# Git helpers
git-hooks: pre-commit-install
	@echo "Git hooks installed!"

# Project info
info:
	@echo "Text Processing Tool - Development Commands"
	@echo "=========================================="
	@echo "Python version: $(shell python --version)"
	@echo "Pip version: $(shell pip --version)"
	@echo "Project root: $(PWD)"
	@echo ""
	@echo "Quick start:"
	@echo "  make install-dev    # Install all dependencies"
	@echo "  make serve          # Start development server"
	@echo "  make test           # Run tests"
	@echo "  make format         # Format code" 
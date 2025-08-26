"""
Configuration module for the application.
Contains all configuration classes and settings.
"""

from .app_config import AppConfig
from .translation_config import TranslationConfig
from .ocr_config import OCRConfig, ocr_config

__all__ = ['AppConfig', 'TranslationConfig', 'OCRConfig', 'ocr_config'] 
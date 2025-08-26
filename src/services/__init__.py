"""
Services module for external API integrations.
Contains translation services, OCR services and other external service integrations.
"""

from .translation_service import TranslationService
from .ocr_service import OCRService, ocr_service

__all__ = ['TranslationService', 'OCRService', 'ocr_service'] 
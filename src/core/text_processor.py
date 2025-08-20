#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Processor Core Module
Main text processing functionality with improved structure and error handling.
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from .text_analyzer import TextAnalyzer
from .text_formatter import TextFormatter


class TextProcessor:
    """
    Main text processor class that orchestrates all text processing operations.
    Provides a clean interface for text processing with improved error handling.
    """
    
    def __init__(self):
        """Initialize the text processor with required components."""
        self.analyzer = TextAnalyzer()
        self.formatter = TextFormatter()
        self.processing_history = []
    
    def process_text(self, text: str, operations: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Process text with specified operations.
        
        Args:
            text: Input text to process
            operations: List of operations to perform (format, statistics, analysis)
            
        Returns:
            Dictionary containing processing results
        """
        # Input validation
        validation_result = self._validate_input(text)
        if validation_result.get('error'):
            return validation_result
        
        # Set default operations if none specified
        if operations is None:
            operations = ['format', 'statistics', 'analysis']
        
        result = {
            'original_text': text,
            'processed_text': text,
            'statistics': {},
            'analysis': {},
            'operations': operations,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Execute requested operations
            if 'format' in operations:
                result['processed_text'] = self.formatter.format_text(text)
            
            if 'statistics' in operations:
                result['statistics'] = self.analyzer.generate_statistics(text)
            
            if 'analysis' in operations:
                result['analysis'] = self.analyzer.analyze_text(text)
            
            # Record processing history
            self._record_processing_history(operations, len(text))
            
        except Exception as e:
            result['error'] = f'Processing error: {str(e)}'
            result['processed_text'] = text  # Return original text on error
        
        return result
    
    def process_text_with_regex(self, text: str, regex_rules: List[tuple]) -> Dict[str, Any]:
        """
        Process text using custom regex rules.
        
        Args:
            text: Input text to process
            regex_rules: List of (pattern, replacement) tuples
            
        Returns:
            Dictionary containing regex processing results
        """
        # Input validation
        validation_result = self._validate_input(text)
        if validation_result.get('error'):
            return validation_result
        
        if not regex_rules:
            return {
                'error': 'Regex rules cannot be empty',
                'processed_text': '',
                'regex_rules': regex_rules
            }
        
        try:
            processed_text = self.formatter.apply_regex_replacements(text, regex_rules)
            
            result = {
                'original_text': text,
                'processed_text': processed_text,
                'regex_rules': regex_rules,
                'error': None,
                'timestamp': datetime.now().isoformat()
            }
            
            # Record processing history
            self._record_processing_history(['regex'], len(text), regex_rules_count=len(regex_rules))
            
            return result
            
        except Exception as e:
            return {
                'error': f'Regex processing error: {str(e)}',
                'processed_text': '',
                'regex_rules': regex_rules
            }
    
    def _validate_input(self, text: str) -> Dict[str, Any]:
        """
        Validate input text.
        
        Args:
            text: Text to validate
            
        Returns:
            Validation result dictionary
        """
        if text is None:
            return {'error': 'Input text cannot be None'}
        
        if not isinstance(text, str):
            try:
                text = str(text)
            except:
                return {'error': 'Input text must be a string'}
        
        if not text or not text.strip():
            return {'error': 'Input text cannot be empty'}
        
        return {'valid': True}
    
    def _record_processing_history(self, operations: List[str], text_length: int, **kwargs):
        """Record processing operation in history."""
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'operations': operations,
            'text_length': text_length,
            **kwargs
        }
        self.processing_history.append(history_entry)
    
    def get_processing_history(self) -> List[Dict[str, Any]]:
        """
        Get processing history.
        
        Returns:
            List of processing history entries
        """
        return self.processing_history.copy()
    
    def clear_history(self):
        """Clear processing history."""
        self.processing_history.clear()


# Global text processor instance
text_processor = TextProcessor() 
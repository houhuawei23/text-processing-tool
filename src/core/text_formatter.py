#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Formatter Module
Handles text formatting and regex replacement operations.
"""

import re
from typing import List, Tuple


class TextFormatter:
    """
    Text formatter class that provides text formatting and regex replacement capabilities.
    """
    
    def __init__(self):
        """Initialize the text formatter."""
        # Default regex rules for common formatting
        self.default_regex_rules = [
            (r"\\\(|\\\)", r"$"),  # Replace escaped parentheses with dollar signs
            (r"\*\*", r"*"),       # Replace double asterisks with single
            (r"\s+", r" "),        # Normalize whitespace
        ]
    
    def format_text(self, text: str) -> str:
        """
        Format text by cleaning up spacing and punctuation.
        
        Args:
            text: Text to format
            
        Returns:
            Formatted text
        """
        if not text or not text.strip():
            return text
        
        try:
            # Remove extra whitespace and normalize
            formatted_text = re.sub(r'\s+', ' ', text.strip())
            
            # Ensure proper sentence endings
            formatted_text = self._normalize_sentence_endings(formatted_text)
            
            # Apply default regex rules
            formatted_text = self.apply_regex_replacements(formatted_text, self.default_regex_rules)
            
            return formatted_text
            
        except Exception as e:
            # Return original text if formatting fails
            return text
    
    def apply_regex_replacements(self, text: str, regex_rules: List[Tuple[str, str]]) -> str:
        """
        Apply regex replacement rules to text.
        
        Args:
            text: Text to process
            regex_rules: List of (pattern, replacement) tuples
            
        Returns:
            Text with regex replacements applied
        """
        if not text or not regex_rules:
            return text
        
        processed_text = text
        
        for pattern, replacement in regex_rules:
            try:
                # Validate regex pattern
                re.compile(pattern)
                
                # Apply the replacement
                processed_text = re.sub(pattern, replacement, processed_text)
                
            except re.error as e:
                # Log regex error but continue with other rules
                print(f"Regex pattern error: {pattern} -> {replacement}, Error: {e}")
                continue
            except Exception as e:
                # Log other errors but continue
                print(f"Regex replacement error: {pattern} -> {replacement}, Error: {e}")
                continue
        
        return processed_text
    
    def parse_regex_rules_from_text(self, rules_text: str) -> List[Tuple[str, str]]:
        """
        Parse regex rules from text input.
        
        Args:
            rules_text: Text containing regex rules
            
        Returns:
            List of parsed (pattern, replacement) tuples
        """
        rules = []
        
        if not rules_text or not rules_text.strip():
            return rules
        
        try:
            # Split by lines and process each line
            lines = rules_text.strip().split('\n')
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):  # Skip empty lines and comments
                    continue
                
                # Try to parse as Python tuple format
                rule = self._parse_python_tuple(line)
                if rule:
                    rules.append(rule)
                    continue
                
                # Try to parse as "pattern -> replacement" format
                rule = self._parse_arrow_format(line)
                if rule:
                    rules.append(rule)
                    continue
                
                # Try to parse as simple string replacement
                rule = self._parse_simple_replacement(line)
                if rule:
                    rules.append(rule)
                    continue
        
        except Exception as e:
            print(f"Error parsing regex rules: {e}")
        
        return rules
    
    def _parse_python_tuple(self, line: str) -> Tuple[str, str]:
        """Parse Python tuple format: (pattern, replacement)."""
        try:
            # Remove outer parentheses and split by comma
            line = line.strip()
            if line.startswith('(') and line.endswith(')'):
                content = line[1:-1].strip()
                
                # Find the comma that separates pattern and replacement
                # Handle nested parentheses and quotes
                comma_pos = self._find_separator_comma(content)
                if comma_pos != -1:
                    pattern = content[:comma_pos].strip().strip('"\'')
                    replacement = content[comma_pos + 1:].strip().strip('"\'')
                    
                    # Remove 'r' prefix if present
                    if pattern.startswith('r"') or pattern.startswith("r'"):
                        pattern = pattern[2:-1]
                    elif pattern.startswith('"') or pattern.startswith("'"):
                        pattern = pattern[1:-1]
                    
                    if replacement.startswith('r"') or replacement.startswith("r'"):
                        replacement = replacement[2:-1]
                    elif replacement.startswith('"') or replacement.startswith("'"):
                        replacement = replacement[1:-1]
                    
                    return pattern, replacement
        except Exception:
            pass
        
        return None
    
    def _parse_arrow_format(self, line: str) -> Tuple[str, str]:
        """Parse arrow format: pattern -> replacement."""
        if " -> " in line:
            parts = line.split(" -> ", 1)
            if len(parts) == 2:
                pattern = parts[0].strip()
                replacement = parts[1].strip()
                return pattern, replacement
        
        return None
    
    def _parse_simple_replacement(self, line: str) -> Tuple[str, str]:
        """Parse simple replacement format: pattern=replacement."""
        if "=" in line:
            parts = line.split("=", 1)
            if len(parts) == 2:
                pattern = parts[0].strip()
                replacement = parts[1].strip()
                return pattern, replacement
        
        return None
    
    def _find_separator_comma(self, content: str) -> int:
        """Find the comma that separates pattern and replacement in a tuple."""
        paren_count = 0
        quote_char = None
        in_escape = False
        
        for i, char in enumerate(content):
            if in_escape:
                in_escape = False
                continue
            
            if char == '\\':
                in_escape = True
                continue
            
            if quote_char is None and char in '"\'':
                quote_char = char
                continue
            elif quote_char and char == quote_char:
                quote_char = None
                continue
            
            if quote_char is None:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == ',' and paren_count == 0:
                    return i
        
        return -1
    
    def _normalize_sentence_endings(self, text: str) -> str:
        """Normalize sentence endings to ensure proper punctuation."""
        # Split text into sentences while preserving punctuation
        sentences = re.split(r'([.!?]+)', text)
        formatted_sentences = []
        
        for i in range(0, len(sentences), 2):
            if i + 1 < len(sentences):
                sentence = sentences[i].strip()
                punctuation = sentences[i + 1]
                
                if sentence and not sentence.endswith(('.', '!', '?')):
                    sentence += '.'
                
                formatted_sentences.append(sentence + punctuation)
            else:
                sentence = sentences[i].strip()
                if sentence and not sentence.endswith(('.', '!', '?')):
                    sentence += '.'
                formatted_sentences.append(sentence)
        
        return ' '.join(formatted_sentences)
    
    def validate_regex_pattern(self, pattern: str) -> bool:
        """
        Validate a regex pattern.
        
        Args:
            pattern: Regex pattern to validate
            
        Returns:
            True if pattern is valid, False otherwise
        """
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False
    
    def escape_special_characters(self, text: str) -> str:
        """
        Escape special regex characters in text.
        
        Args:
            text: Text to escape
            
        Returns:
            Escaped text
        """
        special_chars = r'[\]{}()*+?|^$\.'
        escaped_text = ''
        
        for char in text:
            if char in special_chars:
                escaped_text += '\\' + char
            else:
                escaped_text += char
        
        return escaped_text 
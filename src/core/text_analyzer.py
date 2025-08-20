#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Analyzer Module
Handles text statistics generation and content analysis.
"""

import re
import string
from typing import Dict, Any, List
from collections import Counter


class TextAnalyzer:
    """
    Text analyzer class that provides comprehensive text analysis capabilities.
    """
    
    def __init__(self):
        """Initialize the text analyzer."""
        # Simple sentiment analysis word lists
        self.positive_words = [
            '好', '棒', '优秀', '喜欢', '爱', '开心', '快乐', '成功', '胜利', '美好',
            'good', 'great', 'excellent', 'love', 'happy', 'success', 'wonderful', 'amazing'
        ]
        self.negative_words = [
            '坏', '糟糕', '讨厌', '恨', '伤心', '痛苦', '失败', '失望', '可怕', '恐怖',
            'bad', 'terrible', 'hate', 'sad', 'pain', 'failure', 'disappointing', 'horrible'
        ]
    
    def generate_statistics(self, text: str) -> Dict[str, Any]:
        """
        Generate comprehensive text statistics.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing various statistics
        """
        if not text or not text.strip():
            return self._empty_statistics()
        
        try:
            # Basic statistics
            basic_stats = self._calculate_basic_statistics(text)
            
            # Character type statistics
            char_stats = self._calculate_character_statistics(text)
            
            # Word frequency analysis
            word_freq = self._calculate_word_frequency(text)
            
            # Calculate averages
            averages = self._calculate_averages(basic_stats, word_freq)
            
            return {
                'basic': basic_stats,
                'character_types': char_stats,
                'word_frequency': word_freq,
                'averages': averages
            }
            
        except Exception as e:
            return {
                'error': f'Statistics generation error: {str(e)}',
                'basic': self._empty_statistics()['basic']
            }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive text analysis.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        if not text or not text.strip():
            return self._empty_analysis()
        
        try:
            analysis = {
                'readability': self._calculate_readability(text),
                'sentiment': self._analyze_sentiment(text),
                'language_features': self._analyze_language_features(text)
            }
            
            return analysis
            
        except Exception as e:
            return {
                'error': f'Analysis error: {str(e)}',
                'readability': {},
                'sentiment': {},
                'language_features': {}
            }
    
    def _calculate_basic_statistics(self, text: str) -> Dict[str, int]:
        """Calculate basic text statistics."""
        char_count = len(text)
        word_count = len(text.split())
        line_count = len(text.splitlines())
        
        # Count sentences (improved sentence detection)
        sentences = re.split(r'[。！？.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        return {
            'characters': char_count,
            'words': word_count,
            'lines': line_count,
            'sentences': sentence_count
        }
    
    def _calculate_character_statistics(self, text: str) -> Dict[str, int]:
        """Calculate character type statistics."""
        letters = sum(c.isalpha() for c in text)
        digits = sum(c.isdigit() for c in text)
        spaces = sum(c.isspace() for c in text)
        punctuation = sum(c in string.punctuation for c in text)
        
        return {
            'letters': letters,
            'digits': digits,
            'spaces': spaces,
            'punctuation': punctuation
        }
    
    def _calculate_word_frequency(self, text: str) -> List[tuple]:
        """Calculate word frequency statistics."""
        # Extract words (improved word detection)
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out very short words and common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        filtered_words = [word for word in words if len(word) > 2 and word not in stop_words]
        
        # Get top 10 most common words
        word_freq = Counter(filtered_words).most_common(10)
        
        return word_freq
    
    def _calculate_averages(self, basic_stats: Dict[str, int], word_freq: List[tuple]) -> Dict[str, float]:
        """Calculate average values."""
        word_count = basic_stats['words']
        sentence_count = basic_stats['sentences']
        
        # Calculate average word length
        if word_freq:
            total_word_length = sum(len(word) * count for word, count in word_freq)
            total_words = sum(count for _, count in word_freq)
            avg_word_length = total_word_length / total_words if total_words > 0 else 0
        else:
            avg_word_length = 0
        
        # Calculate average sentence length
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        return {
            'average_word_length': round(avg_word_length, 2),
            'average_sentence_length': round(avg_sentence_length, 2)
        }
    
    def _calculate_readability(self, text: str) -> Dict[str, float]:
        """Calculate readability metrics."""
        sentences = re.split(r'[。！？.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = re.findall(r'\b\w+\b', text.lower())
        syllables = sum(self._count_syllables(word) for word in words)
        
        if not sentences or not words:
            return {'flesch_reading_ease': 0, 'average_sentence_length': 0}
        
        # Calculate Flesch Reading Ease
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        flesch_score = max(0, min(100, flesch_score))  # Clamp between 0-100
        
        return {
            'flesch_reading_ease': round(flesch_score, 2),
            'average_sentence_length': round(avg_sentence_length, 2),
            'average_syllables_per_word': round(avg_syllables_per_word, 2)
        }
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified version)."""
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        # Adjust for silent 'e' at the end
        if word.endswith("e"):
            count -= 1
        
        return max(1, count)
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Perform sentiment analysis."""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        total_words = len(text.split())
        if total_words == 0:
            return {'sentiment': 'neutral', 'positive_ratio': 0, 'negative_ratio': 0}
        
        positive_ratio = positive_count / total_words
        negative_ratio = negative_count / total_words
        
        # Determine sentiment
        if positive_ratio > negative_ratio:
            sentiment = 'positive'
        elif negative_ratio > positive_ratio:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'positive_ratio': round(positive_ratio, 3),
            'negative_ratio': round(negative_ratio, 3),
            'positive_count': positive_count,
            'negative_count': negative_count
        }
    
    def _analyze_language_features(self, text: str) -> Dict[str, Any]:
        """Analyze language features and content types."""
        # Detect language type
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        total_chars = len(text.replace(' ', ''))
        
        if total_chars == 0:
            language_type = 'unknown'
            chinese_ratio = 0
            english_ratio = 0
        else:
            chinese_ratio = chinese_chars / total_chars
            english_ratio = english_chars / total_chars
            
            if chinese_ratio > 0.3 and english_ratio > 0.3:
                language_type = 'mixed'
            elif chinese_ratio > english_ratio:
                language_type = 'chinese'
            elif english_ratio > chinese_ratio:
                language_type = 'english'
            else:
                language_type = 'mixed'
        
        # Detect content features
        has_numbers = bool(re.search(r'\d', text))
        has_urls = bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
        has_emails = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        has_phone_numbers = bool(re.search(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text))
        
        return {
            'language_type': language_type,
            'chinese_ratio': round(chinese_ratio, 3),
            'english_ratio': round(english_ratio, 3),
            'features': {
                'has_numbers': has_numbers,
                'has_urls': has_urls,
                'has_emails': has_emails,
                'has_phone_numbers': has_phone_numbers
            }
        }
    
    def _empty_statistics(self) -> Dict[str, Any]:
        """Return empty statistics structure."""
        return {
            'basic': {'characters': 0, 'words': 0, 'lines': 0, 'sentences': 0},
            'character_types': {'letters': 0, 'digits': 0, 'spaces': 0, 'punctuation': 0},
            'word_frequency': [],
            'averages': {'average_word_length': 0, 'average_sentence_length': 0}
        }
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis structure."""
        return {
            'readability': {'flesch_reading_ease': 0, 'average_sentence_length': 0},
            'sentiment': {'sentiment': 'neutral', 'positive_ratio': 0, 'negative_ratio': 0},
            'language_features': {'language_type': 'unknown', 'features': {}}
        } 
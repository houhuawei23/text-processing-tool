#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translation Service Module
Provides translation functionality using various AI services.
"""

import json
import requests
import time
import re
from typing import Dict, Any, Optional, List
from ..config.translation_config import TranslationConfig


class TranslationService:
    """
    Translation service that supports multiple AI translation providers.
    Handles long text segmentation and retry mechanisms.
    """
    
    def __init__(self):
        """Initialize the translation service."""
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'TextProcessor/1.0'
        })
        
        # Configuration parameters
        self.max_chunk_size = 3000  # Maximum characters per chunk
        self.timeout_short = 60     # Timeout for short texts (seconds)
        self.timeout_long = 180     # Timeout for long texts (seconds)
        self.max_retries = 3        # Maximum retry attempts
        self.retry_delay = 2        # Delay between retries (seconds)
    
    def translate_text(self, text: str, prompt: str, service_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Translate text using the specified service.
        
        Args:
            text: Text to translate
            prompt: Translation prompt/instructions
            service_name: Name of the translation service to use
            
        Returns:
            Dictionary containing translation results
        """
        # Input validation
        if not text or not text.strip():
            return {
                'error': 'Input text cannot be empty',
                'translated_text': '',
                'service_used': '',
                'prompt_used': prompt
            }
        
        if not prompt or not prompt.strip():
            return {
                'error': 'Translation prompt cannot be empty',
                'translated_text': '',
                'service_used': '',
                'prompt_used': ''
            }
        
        # Use default service if none specified
        if not service_name:
            service_name = TranslationConfig.DEFAULT_TRANSLATION_SERVICE
        
        # Check if service is available
        if not TranslationConfig.is_service_available(service_name):
            return {
                'error': f'Translation service {service_name} is not available. Please check API key configuration.',
                'translated_text': '',
                'service_used': service_name,
                'prompt_used': prompt
            }
        
        try:
            # Determine if text needs to be split into chunks
            if len(text) > self.max_chunk_size:
                return self._translate_long_text(text, prompt, service_name)
            else:
                return self._translate_short_text(text, prompt, service_name)
                
        except Exception as e:
            return {
                'error': f'Translation error: {str(e)}',
                'translated_text': '',
                'service_used': service_name,
                'prompt_used': prompt
            }
    
    def _translate_short_text(self, text: str, prompt: str, service_name: str) -> Dict[str, Any]:
        """
        Translate short text (single API call).
        
        Args:
            text: Text to translate
            prompt: Translation prompt
            service_name: Service name
            
        Returns:
            Translation result
        """
        for attempt in range(self.max_retries):
            try:
                if service_name == 'deepseek':
                    return self._translate_with_deepseek(text, prompt, service_name, self.timeout_short)
                elif service_name == 'openai':
                    return self._translate_with_openai(text, prompt, service_name, self.timeout_short)
                else:
                    return {
                        'error': f'Unsupported translation service: {service_name}',
                        'translated_text': '',
                        'service_used': service_name,
                        'prompt_used': prompt
                    }
                    
            except requests.exceptions.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                else:
                    return {
                        'error': 'Translation timeout. Please try again later or reduce text length.',
                        'translated_text': '',
                        'service_used': service_name,
                        'prompt_used': prompt
                    }
            except Exception as e:
                return {
                    'error': f'Translation failed: {str(e)}',
                    'translated_text': '',
                    'service_used': service_name,
                    'prompt_used': prompt
                }
    
    def _translate_long_text(self, text: str, prompt: str, service_name: str) -> Dict[str, Any]:
        """
        Translate long text by splitting into chunks.
        
        Args:
            text: Text to translate
            prompt: Translation prompt
            service_name: Service name
            
        Returns:
            Translation result
        """
        # Split text into chunks
        chunks = self._split_text(text)
        
        if len(chunks) == 1:
            # If only one chunk after splitting, use short text translation
            return self._translate_short_text(text, prompt, service_name)
        
        translated_chunks = []
        total_chunks = len(chunks)
        
        for i, chunk in enumerate(chunks, 1):
            try:
                # Add progress information to prompt
                chunk_prompt = f"{prompt}\n\n(Part {i}/{total_chunks})"
                
                if service_name == 'deepseek':
                    result = self._translate_with_deepseek(chunk, chunk_prompt, service_name, self.timeout_long)
                elif service_name == 'openai':
                    result = self._translate_with_openai(chunk, chunk_prompt, service_name, self.timeout_long)
                else:
                    return {
                        'error': f'Unsupported translation service: {service_name}',
                        'translated_text': '',
                        'service_used': service_name,
                        'prompt_used': prompt
                    }
                
                if result.get('error'):
                    return result
                
                translated_chunks.append(result['translated_text'])
                
            except requests.exceptions.Timeout:
                return {
                    'error': f'Translation timeout on part {i}. Please try again later or reduce text length.',
                    'translated_text': '',
                    'service_used': service_name,
                    'prompt_used': prompt
                }
            except Exception as e:
                return {
                    'error': f'Translation failed on part {i}: {str(e)}',
                    'translated_text': '',
                    'service_used': service_name,
                    'prompt_used': prompt
                }
        
        # Combine translation results
        translated_text = '\n\n'.join(translated_chunks)
        
        return {
            'translated_text': translated_text,
            'service_used': service_name,
            'prompt_used': prompt,
            'error': None,
            'chunks_translated': total_chunks
        }
    
    def _split_text(self, text: str) -> List[str]:
        """
        Intelligently split text into chunks for translation.
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        # If text is shorter than max chunk size, return as single chunk
        if len(text) <= self.max_chunk_size:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by sentences
        sentences = re.split(r'([。！？.!?]+)', text)
        
        for i in range(0, len(sentences), 2):
            sentence = sentences[i]
            punctuation = sentences[i + 1] if i + 1 < len(sentences) else ""
            full_sentence = sentence + punctuation
            
            # Start new chunk if adding this sentence would exceed limit
            if len(current_chunk + full_sentence) > self.max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = full_sentence
            else:
                current_chunk += full_sentence
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # If too many chunks, force split by character count
        if len(chunks) > 10:  # Maximum 10 chunks
            chunks = []
            for i in range(0, len(text), self.max_chunk_size):
                chunk = text[i:i + self.max_chunk_size]
                if chunk.strip():
                    chunks.append(chunk.strip())
        
        return chunks
    
    def _translate_with_deepseek(self, text: str, prompt: str, service_name: str, timeout: int) -> Dict[str, Any]:
        """
        Translate using DeepSeek API.
        
        Args:
            text: Text to translate
            prompt: Translation prompt
            service_name: Service name
            timeout: Request timeout
            
        Returns:
            Translation result
        """
        config = TranslationConfig.get_service_config(service_name)
        
        # Build complete prompt
        full_prompt = f"{prompt}\n\nText to translate:\n```{text}```"
        
        # Adjust max_tokens based on text length
        estimated_tokens = len(text) * 2  # Rough estimate
        max_tokens = min(max(estimated_tokens, 2000), 8000)  # Min 2000, max 8000
        
        payload = {
            "model": config['model'],
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens
        }
        
        headers = {
            "Authorization": f"Bearer {config['api_key']}"
        }
        
        response = self.session.post(
            config['api_url'],
            headers=headers,
            json=payload,
            timeout=timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result['choices'][0]['message']['content'].strip()
            
            return {
                'translated_text': translated_text,
                'service_used': service_name,
                'prompt_used': prompt,
                'error': None
            }
        else:
            return {
                'error': f'DeepSeek API error: {response.status_code} - {response.text}',
                'translated_text': '',
                'service_used': service_name,
                'prompt_used': prompt
            }
    
    def _translate_with_openai(self, text: str, prompt: str, service_name: str, timeout: int) -> Dict[str, Any]:
        """
        Translate using OpenAI API.
        
        Args:
            text: Text to translate
            prompt: Translation prompt
            service_name: Service name
            timeout: Request timeout
            
        Returns:
            Translation result
        """
        config = TranslationConfig.get_service_config(service_name)
        
        # Build complete prompt
        full_prompt = f"{prompt}\n\nText to translate:\n{text}"
        
        # Adjust max_tokens based on text length
        estimated_tokens = len(text) * 2  # Rough estimate
        max_tokens = min(max(estimated_tokens, 2000), 8000)  # Min 2000, max 8000
        
        payload = {
            "model": config['model'],
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens
        }
        
        headers = {
            "Authorization": f"Bearer {config['api_key']}"
        }
        
        response = self.session.post(
            config['api_url'],
            headers=headers,
            json=payload,
            timeout=timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            translated_text = result['choices'][0]['message']['content'].strip()
            
            return {
                'translated_text': translated_text,
                'service_used': service_name,
                'prompt_used': prompt,
                'error': None
            }
        else:
            return {
                'error': f'OpenAI API error: {response.status_code} - {response.text}',
                'translated_text': '',
                'service_used': service_name,
                'prompt_used': prompt
            }
    
    def get_available_services(self) -> Dict[str, Dict[str, Any]]:
        """
        Get list of available translation services.
        
        Returns:
            Dictionary of available services
        """
        return TranslationConfig.get_enabled_services()


# Global translation service instance
translation_service = TranslationService() 
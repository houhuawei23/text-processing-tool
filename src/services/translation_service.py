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
import uuid
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
                elif service_name == 'microsoft':
                    return self._translate_with_microsoft(text, prompt, service_name, self.timeout_short)
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
                elif service_name == 'microsoft':
                    result = self._translate_with_microsoft(chunk, chunk_prompt, service_name, self.timeout_long)
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
        
        # Check if API key is valid
        api_key = config.get('api_key', '')
        
        # Debug logging
        from flask import current_app
        current_app.logger.info(f"DEBUG: DeepSeek service config: {config}")
        current_app.logger.info(f"DEBUG: DeepSeek API key length: {len(api_key) if api_key else 0}")
        current_app.logger.info(f"DEBUG: DeepSeek API key starts with: {api_key[:10] if api_key else 'None'}")
        
        if not api_key or api_key == '••••••••••••••••':
            return {
                'error': 'API key not configured or invalid. Please configure your API key in the translation settings.',
                'translated_text': '',
                'service_used': service_name,
                'prompt_used': prompt
            }
        
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
            "Authorization": f"Bearer {api_key}"
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
            # Parse error response to provide better error message
            try:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Unknown error')
                if 'Authentication Fails' in error_message:
                    return {
                        'error': 'API密钥无效或已过期。请检查您的DeepSeek API密钥是否正确，并确保有足够的余额。',
                        'translated_text': '',
                        'service_used': service_name,
                        'prompt_used': prompt
                    }
                else:
                    return {
                        'error': f'DeepSeek API错误: {error_message}',
                        'translated_text': '',
                        'service_used': service_name,
                        'prompt_used': prompt
                    }
            except:
                return {
                    'error': f'DeepSeek API错误: {response.status_code} - {response.text}',
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
        
        # Check if API key is valid
        api_key = config.get('api_key', '')
        
        # Debug logging
        from flask import current_app
        current_app.logger.info(f"DEBUG: OpenAI service config: {config}")
        current_app.logger.info(f"DEBUG: OpenAI API key length: {len(api_key) if api_key else 0}")
        current_app.logger.info(f"DEBUG: OpenAI API key starts with: {api_key[:10] if api_key else 'None'}")
        
        if not api_key or api_key == '••••••••••••••••':
            return {
                'error': 'API key not configured or invalid. Please configure your API key in the translation settings.',
                'translated_text': '',
                'service_used': service_name,
                'prompt_used': prompt
            }
        
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
            "Authorization": f"Bearer {api_key}"
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
            # Parse error response to provide better error message
            try:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Unknown error')
                if 'Authentication Fails' in error_message or 'invalid_api_key' in error_message:
                    return {
                        'error': 'API密钥无效或已过期。请检查您的OpenAI API密钥是否正确，并确保有足够的余额。',
                        'translated_text': '',
                        'service_used': service_name,
                        'prompt_used': prompt
                    }
                else:
                    return {
                        'error': f'OpenAI API错误: {error_message}',
                        'translated_text': '',
                        'service_used': service_name,
                        'prompt_used': prompt
                    }
            except:
                return {
                    'error': f'OpenAI API错误: {response.status_code} - {response.text}',
                    'translated_text': '',
                    'service_used': service_name,
                    'prompt_used': prompt
                }
    
    def _translate_with_microsoft(self, text: str, prompt: str, service_name: str, timeout: int) -> Dict[str, Any]:
        """
        Translate using Microsoft Translator API.
        
        Args:
            text: Text to translate
            prompt: Translation prompt (used to determine target language)
            service_name: Service name
            timeout: Request timeout
            
        Returns:
            Translation result
        """
        config = TranslationConfig.get_service_config(service_name)
        
        # Check if API key is valid
        api_key = config.get('api_key', '')
        region = config.get('region', 'southeastasia')
        
        # Debug logging
        from flask import current_app
        current_app.logger.info(f"DEBUG: Microsoft service config: {config}")
        current_app.logger.info(f"DEBUG: Microsoft API key length: {len(api_key) if api_key else 0}")
        current_app.logger.info(f"DEBUG: Microsoft region: {region}")
        
        if not api_key or api_key == '••••••••••••••••':
            return {
                'error': 'API key not configured or invalid. Please configure your API key in the translation settings.',
                'translated_text': '',
                'service_used': service_name,
                'prompt_used': prompt
            }
        
        # Determine target language from prompt
        target_lang = self._extract_target_language_from_prompt(prompt)
        
        # Build API URL
        path = "/translate?api-version=3.0"
        params = f"&to={target_lang}"
        url = config['api_url'] + path + params
        
        headers = {
            "Ocp-Apim-Subscription-Key": api_key,
            "Ocp-Apim-Subscription-Region": region,
            "Content-Type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }
        
        # Prepare request body
        body = [{"text": text}]
        
        try:
            response = self.session.post(
                url,
                headers=headers,
                json=body,
                timeout=timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract translated text from response
                if result and len(result) > 0:
                    translations = result[0].get('translations', [])
                    if translations and len(translations) > 0:
                        translated_text = translations[0].get('text', '')
                        
                        return {
                            'translated_text': translated_text,
                            'service_used': service_name,
                            'prompt_used': prompt,
                            'error': None,
                            'target_language': target_lang
                        }
                
                return {
                    'error': 'No translation result received from Microsoft Translator',
                    'translated_text': '',
                    'service_used': service_name,
                    'prompt_used': prompt
                }
            else:
                # Parse error response
                try:
                    error_data = response.json()
                    error_message = error_data.get('error', {}).get('message', 'Unknown error')
                    return {
                        'error': f'Microsoft Translator API错误: {error_message}',
                        'translated_text': '',
                        'service_used': service_name,
                        'prompt_used': prompt
                    }
                except:
                    return {
                        'error': f'Microsoft Translator API错误: {response.status_code} - {response.text}',
                        'translated_text': '',
                        'service_used': service_name,
                        'prompt_used': prompt
                    }
                    
        except requests.exceptions.Timeout:
            return {
                'error': 'Microsoft Translator API请求超时，请稍后重试',
                'translated_text': '',
                'service_used': service_name,
                'prompt_used': prompt
            }
        except Exception as e:
            return {
                'error': f'Microsoft Translator API请求失败: {str(e)}',
                'translated_text': '',
                'service_used': service_name,
                'prompt_used': prompt
            }
    
    def _extract_target_language_from_prompt(self, prompt: str) -> str:
        """
        Extract target language from translation prompt.
        
        Args:
            prompt: Translation prompt
            
        Returns:
            Target language code (e.g., 'zh', 'en', 'ja')
        """
        prompt_lower = prompt.lower()
        
        # Common language mappings
        language_mappings = {
            '中文': 'zh',
            'chinese': 'zh',
            'china': 'zh',
            '英文': 'en',
            'english': 'en',
            '英语': 'en',
            '日文': 'ja',
            'japanese': 'ja',
            '日语': 'ja',
            '韩文': 'ko',
            'korean': 'ko',
            '韩语': 'ko',
            '法文': 'fr',
            'french': 'fr',
            '法语': 'fr',
            '德文': 'de',
            'german': 'de',
            '德语': 'de',
            '西班牙文': 'es',
            'spanish': 'es',
            '西班牙语': 'es',
            '俄文': 'ru',
            'russian': 'ru',
            '俄语': 'ru',
            '阿拉伯文': 'ar',
            'arabic': 'ar',
            '阿拉伯语': 'ar',
        }
        
        # Check for language keywords in prompt
        for keyword, lang_code in language_mappings.items():
            if keyword in prompt_lower:
                return lang_code
        
        # Default to Chinese if no specific language is mentioned
        return 'zh'
    
    def get_available_services(self) -> Dict[str, Dict[str, Any]]:
        """
        Get list of available translation services.
        
        Returns:
            Dictionary of available services
        """
        return TranslationConfig.get_all_services()


# Global translation service instance
translation_service = TranslationService() 
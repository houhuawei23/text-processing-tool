#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translation Configuration Module
Contains translation service settings and API configurations.
"""

import os
import json
from typing import Dict, Any, List
from flask import session

from dotenv import load_dotenv

load_dotenv()


class TranslationConfig:
    """Translation service configuration class."""

    # DeepSeek API configuration
    DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    DEEPSEEK_MODEL = "deepseek-chat"

    # OpenAI ChatGPT API configuration
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    OPENAI_MODEL = "gpt-3.5-turbo"

    # Microsoft Translator API configuration
    MICROSOFT_API_KEY = os.environ.get("MICROSOFT_API_KEY", "")
    MICROSOFT_API_URL = "https://api.cognitive.microsofttranslator.com"
    MICROSOFT_REGION = os.environ.get("MICROSOFT_REGION", "southeastasia")

    # Default translation service
    DEFAULT_TRANSLATION_SERVICE = "deepseek"

    # Available models for each service
    AVAILABLE_MODELS = {
        "deepseek": ["deepseek-chat", "deepseek-coder", "deepseek-chat-33b"],
        "openai": ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-turbo", "gpt-4-32k"],
        "microsoft": ["api-version-3.0"],  # Microsoft Translator uses API version instead of models
    }

    # Available translation services
    AVAILABLE_SERVICES = {
        "deepseek": {
            "name": "DeepSeek",
            "api_key": DEEPSEEK_API_KEY,
            "api_url": DEEPSEEK_API_URL,
            "model": DEEPSEEK_MODEL,
            "enabled": bool(DEEPSEEK_API_KEY),
        },
        "openai": {
            "name": "OpenAI ChatGPT",
            "api_key": OPENAI_API_KEY,
            "api_url": OPENAI_API_URL,
            "model": OPENAI_MODEL,
            "enabled": bool(OPENAI_API_KEY),
        },
        "microsoft": {
            "name": "Microsoft Translator",
            "api_key": MICROSOFT_API_KEY,
            "api_url": MICROSOFT_API_URL,
            "region": MICROSOFT_REGION,
            "model": "api-version-3.0",
            "enabled": bool(MICROSOFT_API_KEY),
        },
    }

    # Default prompts
    DEFAULT_PROMPTS = [
        {
            "id": "translate_to_chinese_1",
            "name": "翻译成中文",
            "content": """
将所给的文本内容完整准确地翻译成流畅的中文，要求：\n\
- 保留重要术语的英文，如 “领域无关规划器（Domain-independent planners）”\n\
- 完整准确地翻译原文，不要遗漏任何信息，包引用和注释等\n\
- 只输出翻译好的结果""",
            "category": "translation",
        },
        {
            "id": "translate_to_chinese_2",
            "name": "翻译成中文",
            "content": "请将以下文本翻译成中文，保持原文的语气和风格：",
            "category": "translation",
        },
        {
            "id": "translate_to_english",
            "name": "翻译成英文",
            "content": "Please translate the following text to English, maintaining the original tone and style:",
            "category": "translation",
        },
        {
            "id": "polish_text",
            "name": "润色文本",
            "content": "请对以下文本进行润色，使其更加流畅自然，保持原意不变：",
            "category": "polish",
        },
        {
            "id": "summarize_text",
            "name": "总结文本",
            "content": "请对以下文本进行总结，提取主要观点和关键信息：",
            "category": "summary",
        },
    ]

    @classmethod
    def get_user_config(cls, service_name: str) -> Dict[str, Any]:
        """
        Get user-provided configuration for a specific service.

        Args:
            service_name: Name of the service

        Returns:
            User configuration dictionary
        """
        try:
            user_configs = session.get("user_translation_configs", {})
            return user_configs.get(service_name, {})
        except RuntimeError:
            # Handle case when running outside of request context (e.g., in tests)
            return {}

    @classmethod
    def set_user_config(cls, service_name: str, api_key: str, model: str = None) -> None:
        """
        Set user-provided configuration for a specific service.

        Args:
            service_name: Name of the service
            api_key: User-provided API key
            model: User-selected model (optional)
        """
        try:
            # Ensure base container exists
            if "user_translation_configs" not in session:
                session["user_translation_configs"] = {}

            # Build the user config
            user_config = {"api_key": api_key, "enabled": bool(api_key.strip())}

            if model:
                user_config["model"] = model

            # Update via reassignment so Flask detects the change
            configs = dict(session.get("user_translation_configs", {}))
            configs[service_name] = user_config
            session["user_translation_configs"] = configs
            session.modified = True
        except RuntimeError:
            # Handle case when running outside of request context (e.g., in tests)
            pass

    @classmethod
    def clear_user_config(cls, service_name: str) -> None:
        """
        Clear user-provided configuration for a specific service.

        Args:
            service_name: Name of the service
        """
        try:
            if "user_translation_configs" in session:
                configs = dict(session.get("user_translation_configs", {}))
                configs.pop(service_name, None)
                session["user_translation_configs"] = configs
                session.modified = True
        except RuntimeError:
            # Handle case when running outside of request context (e.g., in tests)
            pass

    @classmethod
    def get_service_config(cls, service_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific service.
        Prioritizes user-provided configuration over environment variables.

        Args:
            service_name: Name of the service

        Returns:
            Service configuration dictionary
        """
        # First check for user-provided configuration
        user_config = cls.get_user_config(service_name)
        if user_config and user_config.get("api_key"):  # Check for API key instead of enabled
            base_config = cls.AVAILABLE_SERVICES.get(service_name, {}).copy()
            # Only override specific user-provided fields, keep base config intact
            if user_config.get("api_key"):
                base_config["api_key"] = user_config["api_key"]
            if user_config.get("model"):
                base_config["model"] = user_config["model"]
            base_config["enabled"] = user_config.get("enabled", False)
            return base_config

        # Fall back to environment-based configuration
        return cls.AVAILABLE_SERVICES.get(service_name, {})

    @classmethod
    def get_all_services(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get all available services (enabled and disabled).

        Returns:
            Dictionary of all available services
        """
        all_services = {}

        # Add all available services
        for name, config in cls.AVAILABLE_SERVICES.items():
            service_config = config.copy()

            # Check if user has configured this service
            user_config = cls.get_user_config(name)
            if user_config:
                # Only override specific user-provided fields, keep base config intact
                if user_config.get("api_key"):
                    service_config["api_key"] = user_config["api_key"]
                if user_config.get("model"):
                    service_config["model"] = user_config["model"]
                service_config["enabled"] = user_config.get("enabled", False)
                service_config["is_user_configured"] = True
            else:
                service_config["is_user_configured"] = False

            all_services[name] = service_config

        return all_services

    @classmethod
    def get_enabled_services(cls) -> Dict[str, Dict[str, Any]]:
        """
        Get all enabled services (including user-provided ones).

        Returns:
            Dictionary of enabled services
        """
        enabled_services = {}

        # Check environment-based services
        for name, config in cls.AVAILABLE_SERVICES.items():
            if config.get("enabled", False):
                enabled_services[name] = config.copy()

        # Check user-provided services
        try:
            user_configs = session.get("user_translation_configs", {})
            for name, user_config in user_configs.items():
                if user_config.get("enabled", False):
                    base_config = cls.AVAILABLE_SERVICES.get(name, {}).copy()
                    # Only override specific user-provided fields, keep base config intact
                    if user_config.get("api_key"):
                        base_config["api_key"] = user_config["api_key"]
                    if user_config.get("model"):
                        base_config["model"] = user_config["model"]
                    base_config["enabled"] = user_config.get("enabled", False)
                    enabled_services[name] = base_config
        except RuntimeError:
            # Handle case when running outside of request context (e.g., in tests)
            pass

        return enabled_services

    @classmethod
    def is_service_available(cls, service_name: str) -> bool:
        """
        Check if a service is available.

        Args:
            service_name: Name of the service

        Returns:
            True if service is available, False otherwise
        """
        config = cls.get_service_config(service_name)
        return config.get("enabled", False)

    @classmethod
    def get_service_names(cls) -> list:
        """
        Get list of all service names.

        Returns:
            List of service names
        """
        return list(cls.AVAILABLE_SERVICES.keys())

    @classmethod
    def get_available_models_for_service(cls, service_name: str) -> list:
        """
        Get available models for a specific service.

        Args:
            service_name: Name of the service

        Returns:
            List of available models
        """
        return cls.AVAILABLE_MODELS.get(service_name, [])

    @classmethod
    def validate_service_config(cls, service_name: str) -> Dict[str, Any]:
        """
        Validate configuration for a specific service.

        Args:
            service_name: Name of the service

        Returns:
            Validation results
        """
        config = cls.get_service_config(service_name)

        validation = {"valid": True, "errors": [], "warnings": []}

        if not config:
            validation["valid"] = False
            validation["errors"].append(f"Service {service_name} not found")
            return validation

        # Check API key
        if not config.get("api_key"):
            validation["valid"] = False
            validation["errors"].append(f"API key not configured for {service_name}")

        # Check API URL
        if not config.get("api_url"):
            validation["valid"] = False
            validation["errors"].append(f"API URL not configured for {service_name}")

        # Check model
        if not config.get("model"):
            validation["warnings"].append(f"Model not specified for {service_name}")

        return validation

    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """
        Get configuration summary.

        Returns:
            Configuration summary
        """
        enabled_services = cls.get_enabled_services()

        return {
            "total_services": len(cls.AVAILABLE_SERVICES),
            "enabled_services": len(enabled_services),
            "default_service": cls.DEFAULT_TRANSLATION_SERVICE,
            "enabled_service_names": list(enabled_services.keys()),
            "all_service_names": cls.get_service_names(),
        }

    # Prompt management methods
    @classmethod
    def get_user_prompts(cls) -> List[Dict[str, Any]]:
        """
        Get user's saved prompts.

        Returns:
            List of user prompts
        """
        try:
            user_prompts = session.get("user_translation_prompts", [])
            return user_prompts
        except RuntimeError:
            # Handle case when running outside of request context (e.g., in tests)
            return []

    @classmethod
    def get_all_prompts(cls) -> List[Dict[str, Any]]:
        """
        Get all prompts (default + user prompts).

        Returns:
            List of all prompts
        """
        user_prompts = cls.get_user_prompts()
        all_prompts = cls.DEFAULT_PROMPTS + user_prompts
        return all_prompts

    @classmethod
    def add_user_prompt(cls, name: str, content: str, category: str = "custom") -> Dict[str, Any]:
        """
        Add a new user prompt.

        Args:
            name: Prompt name
            content: Prompt content
            category: Prompt category

        Returns:
            Created prompt dictionary
        """
        # Generate unique ID
        import uuid

        prompt_id = f"user_{uuid.uuid4().hex[:8]}"

        new_prompt = {
            "id": prompt_id,
            "name": name,
            "content": content,
            "category": category,
            "is_user_created": True,
            "created_at": cls._get_current_timestamp(),
        }

        # Get current user prompts
        user_prompts = cls.get_user_prompts()
        user_prompts.append(new_prompt)

        # Save to session
        try:
            session["user_translation_prompts"] = user_prompts
            session.modified = True
        except RuntimeError:
            # Handle case when running outside of request context (e.g., in tests)
            pass

        return new_prompt

    @classmethod
    def update_user_prompt(
        cls, prompt_id: str, name: str = None, content: str = None, category: str = None
    ) -> Dict[str, Any]:
        """
        Update an existing user prompt.

        Args:
            prompt_id: Prompt ID to update
            name: New prompt name (optional)
            content: New prompt content (optional)
            category: New prompt category (optional)

        Returns:
            Updated prompt dictionary
        """
        user_prompts = cls.get_user_prompts()

        # Find the prompt to update
        for prompt in user_prompts:
            if prompt["id"] == prompt_id:
                if name is not None:
                    prompt["name"] = name
                if content is not None:
                    prompt["content"] = content
                if category is not None:
                    prompt["category"] = category

                prompt["updated_at"] = cls._get_current_timestamp()

                # Save to session
                try:
                    session["user_translation_prompts"] = user_prompts
                    session.modified = True
                except RuntimeError:
                    # Handle case when running outside of request context (e.g., in tests)
                    pass

                return prompt

        raise ValueError(f"Prompt with ID {prompt_id} not found")

    @classmethod
    def delete_user_prompt(cls, prompt_id: str) -> bool:
        """
        Delete a user prompt.

        Args:
            prompt_id: Prompt ID to delete

        Returns:
            True if deleted, False if not found
        """
        user_prompts = cls.get_user_prompts()

        # Find and remove the prompt
        for i, prompt in enumerate(user_prompts):
            if prompt["id"] == prompt_id:
                user_prompts.pop(i)

                # Save to session
                try:
                    session["user_translation_prompts"] = user_prompts
                    session.modified = True
                except RuntimeError:
                    # Handle case when running outside of request context (e.g., in tests)
                    pass

                return True

        return False

    @classmethod
    def get_prompt_by_id(cls, prompt_id: str) -> Dict[str, Any]:
        """
        Get a specific prompt by ID.

        Args:
            prompt_id: Prompt ID

        Returns:
            Prompt dictionary or None if not found
        """
        # Check default prompts first
        for prompt in cls.DEFAULT_PROMPTS:
            if prompt["id"] == prompt_id:
                return prompt

        # Check user prompts
        user_prompts = cls.get_user_prompts()
        for prompt in user_prompts:
            if prompt["id"] == prompt_id:
                return prompt

        return None

    @classmethod
    def get_prompts_by_category(cls, category: str) -> List[Dict[str, Any]]:
        """
        Get prompts by category.

        Args:
            category: Category name

        Returns:
            List of prompts in the category
        """
        all_prompts = cls.get_all_prompts()
        return [prompt for prompt in all_prompts if prompt.get("category") == category]

    @classmethod
    def export_prompts(cls) -> str:
        """
        Export all user prompts to JSON string.

        Returns:
            JSON string containing user prompts
        """
        user_prompts = cls.get_user_prompts()
        export_data = {
            "version": "1.0",
            "exported_at": cls._get_current_timestamp(),
            "prompts": user_prompts,
        }
        return json.dumps(export_data, ensure_ascii=False, indent=2)

    @classmethod
    def import_prompts(cls, json_data: str) -> Dict[str, Any]:
        """
        Import prompts from JSON string.

        Args:
            json_data: JSON string containing prompts

        Returns:
            Import result dictionary
        """
        try:
            data = json.loads(json_data)

            # Validate structure
            if not isinstance(data, dict) or "prompts" not in data:
                raise ValueError("Invalid import format: missing 'prompts' field")

            prompts = data["prompts"]
            if not isinstance(prompts, list):
                raise ValueError("Invalid import format: 'prompts' must be a list")

            # Validate each prompt
            imported_count = 0
            skipped_count = 0
            errors = []

            for prompt in prompts:
                try:
                    # Validate required fields
                    if not all(key in prompt for key in ["name", "content"]):
                        errors.append(
                            f"Prompt missing required fields: {prompt.get('name', 'Unknown')}"
                        )
                        continue

                    # Check for duplicate names
                    existing_prompts = cls.get_user_prompts()
                    if any(p["name"] == prompt["name"] for p in existing_prompts):
                        skipped_count += 1
                        continue

                    # Add the prompt
                    cls.add_user_prompt(
                        name=prompt["name"],
                        content=prompt["content"],
                        category=prompt.get("category", "imported"),
                    )
                    imported_count += 1

                except Exception as e:
                    errors.append(
                        f"Error importing prompt '{prompt.get('name', 'Unknown')}': {str(e)}"
                    )

            return {
                "success": True,
                "imported_count": imported_count,
                "skipped_count": skipped_count,
                "errors": errors,
            }

        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON format: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Import failed: {str(e)}"}

    @classmethod
    def clear_all_user_prompts(cls) -> None:
        """
        Clear all user prompts.
        """
        try:
            session["user_translation_prompts"] = []
            session.modified = True
        except RuntimeError:
            # Handle case when running outside of request context (e.g., in tests)
            pass

    @classmethod
    def _get_current_timestamp(cls) -> str:
        """
        Get current timestamp in ISO format.

        Returns:
            Current timestamp string
        """
        from datetime import datetime

        return datetime.now().isoformat()

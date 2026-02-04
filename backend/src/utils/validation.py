"""
Validation utilities for the Todo AI Chatbot.
Provides common validation functions for input data.
"""

import re
from typing import Optional, Union
from datetime import datetime


def validate_user_id(user_id: str) -> bool:
    """
    Validate user ID format.

    Args:
        user_id: User ID string to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not user_id or len(user_id.strip()) == 0:
        return False

    # Basic validation: alphanumeric, underscore, hyphen, dots, length 1-50
    pattern = r'^[a-zA-Z0-9_.-]{1,50}$'
    return bool(re.match(pattern, user_id))


def validate_task_title(title: str) -> tuple[bool, Optional[str]]:
    """
    Validate task title.

    Args:
        title: Task title to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not title or len(title.strip()) == 0:
        return False, "Task title cannot be empty"

    if len(title) > 255:
        return False, "Task title must be 255 characters or less"

    return True, None


def validate_task_description(description: Optional[str]) -> tuple[bool, Optional[str]]:
    """
    Validate task description.

    Args:
        description: Task description to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if description is None:
        return True, None

    if len(description) > 1000:
        return False, "Task description must be 1000 characters or less"

    return True, None


def validate_message_content(content: str) -> tuple[bool, Optional[str]]:
    """
    Validate message content.

    Args:
        content: Message content to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not content or len(content.strip()) == 0:
        return False, "Message content cannot be empty"

    if len(content) > 10000:  # 10k characters max
        return False, "Message content must be 10000 characters or less"

    return True, None


def validate_conversation_id(conversation_id: Union[int, None]) -> bool:
    """
    Validate conversation ID.

    Args:
        conversation_id: Conversation ID to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if conversation_id is None:
        return True  # Optional field

    if isinstance(conversation_id, int) and conversation_id > 0:
        return True

    return False


def sanitize_input(text: str) -> str:
    """
    Sanitize input text by removing potentially harmful characters.

    Args:
        text: Input text to sanitize

    Returns:
        str: Sanitized text
    """
    if not text:
        return ""

    # Remove potentially dangerous characters
    # This is a basic example - you might want to use a more sophisticated sanitizer
    sanitized = text.replace('\0', '')  # Remove null bytes
    return sanitized


def validate_role(role: str) -> bool:
    """
    Validate message role.

    Args:
        role: Role to validate ('user' or 'assistant')

    Returns:
        bool: True if valid, False otherwise
    """
    return role in ['user', 'assistant']


def validate_task_status(status: str) -> bool:
    """
    Validate task status filter.

    Args:
        status: Status to validate ('all', 'pending', 'completed')

    Returns:
        bool: True if valid, False otherwise
    """
    return status in ['all', 'pending', 'completed']
"""
Logging configuration for the Todo AI Chatbot.
Sets up structured logging for the application.
"""

import logging
import sys
from datetime import datetime
from typing import Any, Dict
import json


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as JSON."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id

        return json.dumps(log_entry)


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Set up logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Logger instance
    """
    # Create logger
    logger = logging.getLogger("todo_ai_chatbot")
    logger.setLevel(getattr(logging, level.upper()))

    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))

    # Create JSON formatter
    formatter = JSONFormatter()
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger instance.

    Args:
        name: Name of the logger

    Returns:
        Named logger instance
    """
    return logging.getLogger(f"todo_ai_chatbot.{name}")


# Global logger instance
app_logger = setup_logging()
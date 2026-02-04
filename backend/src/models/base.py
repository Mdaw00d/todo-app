"""
Base model for the Todo AI Chatbot.
Provides common functionality for all models.
"""

from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models."""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


class BaseSQLModel(SQLModel):
    """Base SQLModel with common functionality."""
    pass
"""
Message model for the Todo AI Chatbot.
Represents individual exchanges in a conversation, including user input and AI responses.
"""

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String
from typing import Optional
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Enum for message roles."""
    USER = "user"
    ASSISTANT = "assistant"


class MessageBase(SQLModel):
    """Base class for Message model with common fields."""
    user_id: str = Field(index=True)  # Foreign key reference to user, indexed
    conversation_id: int = Field(index=True)  # Foreign key reference to conversation, indexed
    role: MessageRole = Field(sa_column=Column("role", String(20)))  # Role: user or assistant
    content: str = Field(min_length=1)  # Message content


class Message(MessageBase, table=True):
    """Message model representing individual exchanges in a conversation."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    user_id: str = Field(min_length=1)
    conversation_id: int = Field(gt=0)
    role: MessageRole
    content: str = Field(min_length=1, max_length=10000)


class MessageRead(MessageBase):
    """Schema for reading a message with its ID."""
    id: int
    created_at: datetime


class MessageUpdate(SQLModel):
    """Schema for updating an existing message."""
    # Messages are immutable once created, so no updatable fields
    pass
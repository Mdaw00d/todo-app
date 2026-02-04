"""
Conversation model for the Todo AI Chatbot.
Represents a logical grouping of messages between a user and the AI assistant.
"""

from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import json


class ConversationBase(SQLModel):
    """Base class for Conversation model with common fields."""
    user_id: str = Field(index=True)  # Foreign key reference to user, indexed


class Conversation(ConversationBase, table=True):
    """Conversation model representing a logical grouping of messages."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Context tracking fields
    context_data: Optional[str] = Field(default=None)  # JSON string to store conversation context

    def get_context(self) -> Dict[str, Any]:
        """Get the conversation context as a dictionary."""
        if self.context_data:
            try:
                return json.loads(self.context_data)
            except json.JSONDecodeError:
                return {}
        return {}

    def set_context(self, context: Dict[str, Any]) -> None:
        """Set the conversation context from a dictionary."""
        self.context_data = json.dumps(context)


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    user_id: str = Field(min_length=1)


class ConversationRead(ConversationBase):
    """Schema for reading a conversation with its ID."""
    id: int
    created_at: datetime
    updated_at: datetime
    context_data: Optional[str] = None


class ConversationUpdate(SQLModel):
    """Schema for updating an existing conversation."""
    context_data: Optional[str] = None
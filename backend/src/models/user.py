"""User model and DTOs."""

from datetime import datetime
from typing import Optional, List
import uuid

from sqlmodel import Field, SQLModel, Relationship


class UserBase(SQLModel):
    """Base user attributes shared by all user models."""

    email: str = Field(unique=True, nullable=False, max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=100)


class User(UserBase, table=True):
    """User database model."""

    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str = Field(nullable=False, max_length=255)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """DTO for creating a new user."""

    password: str = Field(min_length=8, max_length=128)
    password_confirm: str = Field(min_length=8, max_length=128)


class UserUpdate(SQLModel):
    """DTO for updating an existing user."""

    full_name: Optional[str] = Field(default=None, max_length=100)


class UserPublic(UserBase):
    """DTO for user API responses."""

    id: str
    created_at: datetime
    updated_at: datetime
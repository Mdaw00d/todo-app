"""Task model and DTOs."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
import uuid

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .user import User


class TaskBase(SQLModel):
    """Base task attributes shared by all task models."""

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)


class Task(TaskBase, table=True):
    """Task database model."""

    __tablename__ = "tasks"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False)
    completed: bool = Field(default=False, nullable=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """DTO for creating a new task."""
    pass


class TaskUpdate(SQLModel):
    """DTO for updating an existing task."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskPublic(TaskBase):
    """DTO for task API responses."""

    id: str
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime

"""
Unit tests for the models in the Todo AI Chatbot.
Tests for all model classes.
"""

import pytest
from datetime import datetime
from src.models.task import Task, TaskCreate, TaskUpdate, TaskRead
from src.models.conversation import Conversation, ConversationCreate, ConversationRead
from src.models.message import Message, MessageCreate, MessageRead, MessageRole


def test_task_model_creation():
    """Test creating a Task model instance."""
    task = Task(
        id=1,
        title="Test task",
        description="Test description",
        completed=False,
        user_id="user123"
    )

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed is False
    assert task.user_id == "user123"
    assert task.created_at is not None
    assert task.updated_at is not None


def test_task_create_schema():
    """Test TaskCreate schema."""
    task_create = TaskCreate(
        title="Test task",
        description="Test description",
        user_id="user123"
    )

    assert task_create.title == "Test task"
    assert task_create.description == "Test description"
    assert task_create.user_id == "user123"


def test_task_update_schema():
    """Test TaskUpdate schema."""
    task_update = TaskUpdate(
        title="Updated task",
        description="Updated description",
        completed=True
    )

    assert task_update.title == "Updated task"
    assert task_update.description == "Updated description"
    assert task_update.completed is True


def test_task_read_schema():
    """Test TaskRead schema."""
    now = datetime.utcnow()
    task_read = TaskRead(
        id=1,
        title="Test task",
        description="Test description",
        completed=False,
        user_id="user123",
        created_at=now,
        updated_at=now
    )

    assert task_read.id == 1
    assert task_read.title == "Test task"
    assert task_read.description == "Test description"
    assert task_read.completed is False
    assert task_read.user_id == "user123"
    assert task_read.created_at == now
    assert task_read.updated_at == now


def test_conversation_model_creation():
    """Test creating a Conversation model instance."""
    conversation = Conversation(
        id=1,
        user_id="user123"
    )

    assert conversation.id == 1
    assert conversation.user_id == "user123"
    assert conversation.created_at is not None
    assert conversation.updated_at is not None


def test_conversation_create_schema():
    """Test ConversationCreate schema."""
    conversation_create = ConversationCreate(
        user_id="user123"
    )

    assert conversation_create.user_id == "user123"


def test_conversation_read_schema():
    """Test ConversationRead schema."""
    now = datetime.utcnow()
    conversation_read = ConversationRead(
        id=1,
        user_id="user123",
        created_at=now,
        updated_at=now
    )

    assert conversation_read.id == 1
    assert conversation_read.user_id == "user123"
    assert conversation_read.created_at == now
    assert conversation_read.updated_at == now


def test_message_model_creation():
    """Test creating a Message model instance."""
    message = Message(
        id=1,
        user_id="user123",
        conversation_id=1,
        role=MessageRole.USER,
        content="Test message content"
    )

    assert message.id == 1
    assert message.user_id == "user123"
    assert message.conversation_id == 1
    assert message.role == MessageRole.USER
    assert message.content == "Test message content"
    assert message.created_at is not None


def test_message_create_schema():
    """Test MessageCreate schema."""
    message_create = MessageCreate(
        user_id="user123",
        conversation_id=1,
        role=MessageRole.ASSISTANT,
        content="Test message content"
    )

    assert message_create.user_id == "user123"
    assert message_create.conversation_id == 1
    assert message_create.role == MessageRole.ASSISTANT
    assert message_create.content == "Test message content"


def test_message_read_schema():
    """Test MessageRead schema."""
    now = datetime.utcnow()
    message_read = MessageRead(
        id=1,
        user_id="user123",
        conversation_id=1,
        role=MessageRole.USER,
        content="Test message content",
        created_at=now
    )

    assert message_read.id == 1
    assert message_read.user_id == "user123"
    assert message_read.conversation_id == 1
    assert message_read.role == MessageRole.USER
    assert message_read.content == "Test message content"
    assert message_read.created_at == now


def test_message_role_enum():
    """Test MessageRole enum values."""
    assert MessageRole.USER.value == "user"
    assert MessageRole.ASSISTANT.value == "assistant"

    # Verify we can create from string values
    assert MessageRole("user") == MessageRole.USER
    assert MessageRole("assistant") == MessageRole.ASSISTANT


def test_task_validation_minimal():
    """Test creating a task with minimal required fields."""
    task_create = TaskCreate(
        title="Minimal task",
        user_id="user123"
    )

    assert task_create.title == "Minimal task"
    assert task_create.user_id == "user123"
    assert task_create.description is None


def test_conversation_context_storage():
    """Test conversation context storage and retrieval."""
    conversation = Conversation(
        id=1,
        user_id="user123"
    )

    # Initially should have empty context
    assert conversation.get_context() == {}

    # Set some context
    test_context = {
        "current_task_list": [{"id": 1, "title": "Test task"}],
        "last_interaction": "2026-01-28T10:00:00Z"
    }
    conversation.set_context(test_context)

    # Get the context back
    retrieved_context = conversation.get_context()
    assert retrieved_context == test_context


def test_invalid_context_json():
    """Test handling invalid JSON in context_data."""
    conversation = Conversation(
        id=1,
        user_id="user123",
        context_data="{invalid json"
    )

    # Should return empty dict for invalid JSON
    assert conversation.get_context() == {}

    # Test setting and getting context normally
    test_context = {"valid": "json"}
    conversation.set_context(test_context)
    assert conversation.get_context() == test_context
"""
Unit tests for the services in the Todo AI Chatbot.
Tests for all service classes.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.conversation import Conversation, ConversationCreate
from src.models.message import Message, MessageCreate
from src.services.task_service import TaskService
from src.services.conversation_service import ConversationService
from src.services.message_service import MessageService
from src.exceptions.handlers import (
    TaskNotFoundException,
    ConversationNotFoundException,
    InvalidTaskOperationError
)


@pytest.mark.asyncio
async def test_task_service_create_task():
    """Test creating a task using TaskService."""
    # Create a mock session
    session = AsyncMock(spec=AsyncSession)

    # Create task creation data
    task_create = TaskCreate(
        title="Test task",
        description="Test description",
        user_id="test_user_123"
    )

    # Create a mock task instance
    mock_task = Task(
        id=1,
        title="Test task",
        description="Test description",
        user_id="test_user_123",
        completed=False
    )

    # Configure the session mock
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    # Patch the model validation to return our mock task
    original_validate = Task.model_validate
    Task.model_validate = MagicMock(return_value=mock_task)

    # Call the service method
    result = await TaskService.create_task(session, task_create)

    # Verify the result
    assert result.id == 1
    assert result.title == "Test task"
    assert result.user_id == "test_user_123"

    # Restore original method
    Task.model_validate = original_validate


@pytest.mark.asyncio
async def test_task_service_get_task_by_id():
    """Test getting a task by ID using TaskService."""
    # Create a mock session
    session = AsyncMock(spec=AsyncSession)

    # Create a mock task
    mock_task = Task(
        id=1,
        title="Test task",
        description="Test description",
        user_id="test_user_123",
        completed=False
    )

    # Configure the session mock to return the task
    execute_mock = AsyncMock()
    execute_mock.first.return_value = mock_task
    session.execute.return_value = execute_mock

    # Call the service method
    result = await TaskService.get_task_by_id(session, 1, "test_user_123")

    # Verify the result
    assert result.id == 1
    assert result.title == "Test task"
    assert result.user_id == "test_user_123"


@pytest.mark.asyncio
async def test_task_service_get_task_by_id_not_found():
    """Test getting a non-existent task raises TaskNotFoundException."""
    # Create a mock session
    session = AsyncMock(spec=AsyncSession)

    # Configure the session mock to return None
    execute_mock = AsyncMock()
    execute_mock.first.return_value = None
    session.execute.return_value = execute_mock

    # Call the service method and expect an exception
    with pytest.raises(TaskNotFoundException):
        await TaskService.get_task_by_id(session, 999, "test_user_123")


@pytest.mark.asyncio
async def test_conversation_service_create_conversation():
    """Test creating a conversation using ConversationService."""
    # Create a mock session
    session = AsyncMock(spec=AsyncSession)

    # Create conversation creation data
    conversation_create = ConversationCreate(
        user_id="test_user_123"
    )

    # Create a mock conversation instance
    mock_conversation = Conversation(
        id=1,
        user_id="test_user_123"
    )

    # Configure the session mock
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    # Patch the model validation to return our mock conversation
    original_validate = Conversation.model_validate
    Conversation.model_validate = MagicMock(return_value=mock_conversation)

    # Call the service method
    result = await ConversationService.create_conversation(session, conversation_create)

    # Verify the result
    assert result.id == 1
    assert result.user_id == "test_user_123"

    # Restore original method
    Conversation.model_validate = original_validate


@pytest.mark.asyncio
async def test_message_service_create_message():
    """Test creating a message using MessageService."""
    # Create a mock session
    session = AsyncMock(spec=AsyncSession)

    # Create message creation data
    message_create = MessageCreate(
        user_id="test_user_123",
        conversation_id=1,
        role="user",
        content="Test message content"
    )

    # Create a mock message instance
    mock_message = Message(
        id=1,
        user_id="test_user_123",
        conversation_id=1,
        role="user",
        content="Test message content"
    )

    # Configure the session mock
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    # Patch the model validation to return our mock message
    original_validate = Message.model_validate
    Message.model_validate = MagicMock(return_value=mock_message)

    # Call the service method
    result = await MessageService.create_message(session, message_create)

    # Verify the result
    assert result.id == 1
    assert result.user_id == "test_user_123"
    assert result.content == "Test message content"

    # Restore original method
    Message.model_validate = original_validate


@pytest.mark.asyncio
async def test_task_service_update_task():
    """Test updating a task using TaskService."""
    # Create a mock session
    session = AsyncMock(spec=AsyncSession)

    # Create an existing task
    existing_task = Task(
        id=1,
        title="Old title",
        description="Old description",
        user_id="test_user_123",
        completed=False
    )

    # Configure the session mock to return the existing task
    execute_mock = AsyncMock()
    execute_mock.first.return_value = existing_task
    session.execute.return_value = execute_mock

    # Create update data
    task_update = TaskUpdate(
        title="New title",
        description="New description"
    )

    # Call the service method
    result = await TaskService.update_task(session, 1, "test_user_123", task_update)

    # Verify the result
    assert result.title == "New title"
    assert result.description == "New description"


@pytest.mark.asyncio
async def test_task_service_delete_task():
    """Test deleting a task using TaskService."""
    # Create a mock session
    session = AsyncMock(spec=AsyncSession)

    # Create an existing task
    existing_task = Task(
        id=1,
        title="Test task",
        description="Test description",
        user_id="test_user_123",
        completed=False
    )

    # Configure the session mock to return the existing task
    execute_mock = AsyncMock()
    execute_mock.first.return_value = existing_task
    session.execute.return_value = execute_mock

    # Configure the session mock for delete operations
    session.delete = MagicMock()
    session.commit = AsyncMock()

    # Call the service method
    result = await TaskService.delete_task(session, 1, "test_user_123")

    # Verify the result
    assert result is True


@pytest.mark.asyncio
async def test_task_service_complete_task():
    """Test completing a task using TaskService."""
    # Create a mock session
    session = AsyncMock(spec=AsyncSession)

    # Create an existing task
    existing_task = Task(
        id=1,
        title="Test task",
        description="Test description",
        user_id="test_user_123",
        completed=False
    )

    # Configure the session mock to return the existing task
    execute_mock = AsyncMock()
    execute_mock.first.return_value = existing_task
    session.execute.return_value = execute_mock

    # Call the service method
    result = await TaskService.complete_task(session, 1, "test_user_123")

    # Verify the result
    assert result.id == 1
    assert result.completed is True
"""
Unit tests for the MCP tools in the Todo AI Chatbot.
Tests for all MCP tool classes.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.mcp_tools.task_mcp_tools import TaskMCPTools
from src.mcp_tools.conversation_mcp_tools import ConversationMCPTools
from src.services.task_service import TaskService
from src.services.conversation_service import ConversationService
from src.models.task import TaskRead


@pytest.mark.asyncio
async def test_task_mcp_tools_add_task():
    """Test the add_task MCP tool."""
    with patch('src.mcp_tools.task_mcp_tools.get_async_session') as mock_session_context:
        # Create mock session
        mock_session = AsyncMock()
        mock_session_context.return_value.__aenter__.return_value = mock_session

        # Mock the TaskService.create_task method
        with patch.object(TaskService, 'create_task') as mock_create_task:
            # Create a mock task to return
            mock_task = TaskRead(
                id=1,
                title="Test task",
                description="Test description",
                completed=False,
                user_id="test_user_123",
                created_at=None,
                updated_at=None
            )
            mock_create_task.return_value = mock_task

            # Call the MCP tool
            result = await TaskMCPTools.add_task(
                user_id="test_user_123",
                title="Test task",
                description="Test description"
            )

            # Verify the result
            assert result["success"] is True
            assert result["task_id"] == 1
            assert "Task 'Test task' created successfully" in result["message"]

            # Verify that create_task was called with correct parameters
            mock_create_task.assert_called_once()


@pytest.mark.asyncio
async def test_task_mcp_tools_add_task_invalid_user_id():
    """Test the add_task MCP tool with invalid user ID."""
    result = await TaskMCPTools.add_task(
        user_id="",  # Invalid user ID
        title="Test task"
    )

    assert result["success"] is False
    assert "Invalid user ID format" in result["error"]


@pytest.mark.asyncio
async def test_task_mcp_tools_list_tasks():
    """Test the list_tasks MCP tool."""
    with patch('src.mcp_tools.task_mcp_tools.get_async_session') as mock_session_context:
        # Create mock session
        mock_session = AsyncMock()
        mock_session_context.return_value.__aenter__.return_value = mock_session

        # Mock the TaskService.get_tasks_by_user method
        with patch.object(TaskService, 'get_tasks_by_user') as mock_get_tasks:
            # Create mock tasks to return
            mock_tasks = [
                TaskRead(
                    id=1,
                    title="Task 1",
                    description="Description 1",
                    completed=False,
                    user_id="test_user_123",
                    created_at=None,
                    updated_at=None
                ),
                TaskRead(
                    id=2,
                    title="Task 2",
                    description="Description 2",
                    completed=True,
                    user_id="test_user_123",
                    created_at=None,
                    updated_at=None
                )
            ]
            mock_get_tasks.return_value = mock_tasks

            # Call the MCP tool
            result = await TaskMCPTools.list_tasks(
                user_id="test_user_123",
                status="all"
            )

            # Verify the result
            assert result["success"] is True
            assert result["count"] == 2
            assert len(result["tasks"]) == 2


@pytest.mark.asyncio
async def test_task_mcp_tools_list_tasks_invalid_status():
    """Test the list_tasks MCP tool with invalid status."""
    result = await TaskMCPTools.list_tasks(
        user_id="test_user_123",
        status="invalid_status"
    )

    assert result["success"] is False
    assert "Invalid status parameter" in result["error"]


@pytest.mark.asyncio
async def test_task_mcp_tools_complete_task():
    """Test the complete_task MCP tool."""
    with patch('src.mcp_tools.task_mcp_tools.get_async_session') as mock_session_context:
        # Create mock session
        mock_session = AsyncMock()
        mock_session_context.return_value.__aenter__.return_value = mock_session

        # Mock the TaskService.complete_task method
        with patch.object(TaskService, 'complete_task') as mock_complete_task:
            # Create a mock task to return
            mock_task = TaskRead(
                id=1,
                title="Test task",
                description="Test description",
                completed=True,
                user_id="test_user_123",
                created_at=None,
                updated_at=None
            )
            mock_complete_task.return_value = mock_task

            # Call the MCP tool
            result = await TaskMCPTools.complete_task(
                user_id="test_user_123",
                task_id=1
            )

            # Verify the result
            assert result["success"] is True
            assert "marked as completed" in result["message"]


@pytest.mark.asyncio
async def test_task_mcp_tools_complete_task_invalid_task_id():
    """Test the complete_task MCP tool with invalid task ID."""
    result = await TaskMCPTools.complete_task(
        user_id="test_user_123",
        task_id=-1  # Invalid task ID
    )

    assert result["success"] is False
    assert "Invalid task ID" in result["error"]


@pytest.mark.asyncio
async def test_conversation_mcp_tools_create_conversation():
    """Test the create_conversation MCP tool."""
    with patch('src.mcp_tools.conversation_mcp_tools.get_async_session') as mock_session_context:
        # Create mock session
        mock_session = AsyncMock()
        mock_session_context.return_value.__aenter__.return_value = mock_session

        # Mock the ConversationService.create_conversation method
        with patch.object(ConversationService, 'create_conversation') as mock_create_conversation:
            # Create a mock conversation to return
            from src.models.conversation import ConversationRead
            mock_conversation = ConversationRead(
                id=1,
                user_id="test_user_123",
                created_at=None,
                updated_at=None
            )
            mock_create_conversation.return_value = mock_conversation

            # Call the MCP tool
            result = await ConversationMCPTools.create_conversation(
                user_id="test_user_123"
            )

            # Verify the result
            assert result["success"] is True
            assert result["conversation_id"] == 1
            assert "Conversation created successfully" in result["message"]


@pytest.mark.asyncio
async def test_conversation_mcp_tools_create_conversation_invalid_user():
    """Test the create_conversation MCP tool with invalid user ID."""
    result = await ConversationMCPTools.create_conversation(
        user_id=""  # Invalid user ID
    )

    assert result["success"] is False
    assert "Invalid user ID format" in result["error"]


@pytest.mark.asyncio
async def test_task_mcp_tools_get_task_by_id():
    """Test the get_task_by_id MCP tool."""
    with patch('src.mcp_tools.task_mcp_tools.get_async_session') as mock_session_context:
        # Create mock session
        mock_session = AsyncMock()
        mock_session_context.return_value.__aenter__.return_value = mock_session

        # Mock the TaskService.get_task_by_id method
        with patch.object(TaskService, 'get_task_by_id') as mock_get_task:
            # Create a mock task to return
            mock_task = TaskRead(
                id=1,
                title="Test task",
                description="Test description",
                completed=False,
                user_id="test_user_123",
                created_at=None,
                updated_at=None
            )
            mock_get_task.return_value = mock_task

            # Call the MCP tool
            result = await TaskMCPTools.get_task_by_id(
                user_id="test_user_123",
                task_id=1
            )

            # Verify the result
            assert result["success"] is True
            assert result["task"]["id"] == 1
            assert result["task"]["title"] == "Test task"


@pytest.mark.asyncio
async def test_task_mcp_tools_get_recent_tasks():
    """Test the get_recent_tasks MCP tool."""
    with patch('src.mcp_tools.task_mcp_tools.get_async_session') as mock_session_context:
        # Create mock session
        mock_session = AsyncMock()
        mock_session_context.return_value.__aenter__.return_value = mock_session

        # Mock the TaskService.get_tasks_by_user method
        with patch.object(TaskService, 'get_tasks_by_user') as mock_get_tasks:
            # Create mock tasks to return
            mock_tasks = [
                TaskRead(
                    id=1,
                    title="Recent task 1",
                    description="Description 1",
                    completed=False,
                    user_id="test_user_123",
                    created_at=None,
                    updated_at=None
                ),
                TaskRead(
                    id=2,
                    title="Recent task 2",
                    description="Description 2",
                    completed=True,
                    user_id="test_user_123",
                    created_at=None,
                    updated_at=None
                )
            ]
            mock_get_tasks.return_value = mock_tasks

            # Call the MCP tool
            result = await TaskMCPTools.get_recent_tasks(
                user_id="test_user_123",
                limit=10
            )

            # Verify the result
            assert result["success"] is True
            assert result["count"] >= 0  # Count should be non-negative


@pytest.mark.asyncio
async def test_conversation_mcp_tools_update_conversation_context():
    """Test the update_conversation_context MCP tool."""
    with patch('src.mcp_tools.conversation_mcp_tools.get_async_session') as mock_session_context:
        # Create mock session
        mock_session = AsyncMock()
        mock_session_context.return_value.__aenter__.return_value = mock_session

        # Mock the ConversationService.update_conversation_context method
        with patch.object(ConversationService, 'update_conversation_context') as mock_update_context:
            # Create a mock conversation to return
            from src.models.conversation import ConversationRead
            mock_conversation = ConversationRead(
                id=1,
                user_id="test_user_123",
                created_at=None,
                updated_at=None
            )
            mock_update_context.return_value = mock_conversation

            # Call the MCP tool
            result = await ConversationMCPTools.update_conversation_context(
                user_id="test_user_123",
                conversation_id=1,
                context_updates={"key": "value"}
            )

            # Verify the result
            assert result["success"] is True
            assert result["conversation_id"] == 1
            assert "Conversation context updated successfully" in result["message"]
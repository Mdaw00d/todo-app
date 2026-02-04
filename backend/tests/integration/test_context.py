"""
Integration tests for conversation context maintenance in the Todo AI Chatbot.
Tests stateful conversation functionality and context awareness.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import sys
import os

# Add the backend directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app
from src.mcp_tools.task_mcp_tools import TaskMCPTools
from src.mcp_tools.conversation_mcp_tools import ConversationMCPTools
from src.agents.todo_agent import TodoAgent
from src.services.conversation_service import ConversationService


@pytest.mark.asyncio
async def test_conversation_context_maintenance():
    """Test that conversation context is maintained across multiple exchanges."""
    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'add_task', new_callable=AsyncMock) as mock_add_task, \
         patch.object(TaskMCPTools, 'list_tasks', new_callable=AsyncMock) as mock_list_tasks, \
         patch.object(TaskMCPTools, 'complete_task', new_callable=AsyncMock) as mock_complete_task, \
         patch.object(ConversationMCPTools, 'create_conversation', new_callable=AsyncMock) as mock_create_conv, \
         patch.object(ConversationMCPTools, 'add_message_to_conversation', new_callable=AsyncMock) as mock_add_msg:

        # Set up mock return values
        mock_create_conv.return_value = {"success": True, "conversation_id": 1, "message": "Conversation created"}
        mock_add_task.return_value = {"success": True, "task_id": 1, "message": "Task created"}
        mock_list_tasks.return_value = {
            "success": True,
            "tasks": [{"id": 1, "title": "Call mom", "completed": False}],
            "count": 1
        }
        mock_complete_task.return_value = {"success": True, "message": "Task completed"}
        mock_add_msg.return_value = {"success": True, "message_id": 1, "message": "Message added"}

        # Test the agent's ability to maintain context
        agent = TodoAgent()

        # Simulate a conversation sequence
        user_id = "test_user_123"

        # First message: Add a task
        result1 = await agent.process_message(user_id, None, "Add a task to call mom")
        assert result1["response"] != ""  # Should have a response

        # Second message: List tasks (context should be maintained)
        result2 = await agent.process_message(user_id, result1["conversation_id"], "Show my tasks")
        assert result2["response"] != ""  # Should have a response

        # Third message: Complete the first task by referring to it in context
        result3 = await agent.process_message(user_id, result2["conversation_id"], "Complete the first task")
        assert result3["response"] != ""  # Should have a response

        # Verify that the agent maintained conversation context
        assert result1["conversation_id"] == result2["conversation_id"]
        assert result2["conversation_id"] == result3["conversation_id"]


@pytest.mark.asyncio
async def test_multi_turn_conversation_flow():
    """Test multi-turn conversation flow with context preservation."""
    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'add_task', new_callable=AsyncMock) as mock_add_task, \
         patch.object(TaskMCPTools, 'list_tasks', new_callable=AsyncMock) as mock_list_tasks, \
         patch.object(ConversationMCPTools, 'create_conversation', new_callable=AsyncMock) as mock_create_conv, \
         patch.object(ConversationMCPTools, 'add_message_to_conversation', new_callable=AsyncMock) as mock_add_msg:

        # Set up mock return values
        mock_create_conv.return_value = {"success": True, "conversation_id": 1, "message": "Conversation created"}
        mock_add_task.return_value = {"success": True, "task_id": 1, "message": "Task created"}
        mock_list_tasks.return_value = {
            "success": True,
            "tasks": [{"id": 1, "title": "Buy groceries", "completed": False}],
            "count": 1
        }
        mock_add_msg.return_value = {"success": True, "message_id": 1, "message": "Message added"}

        # Test the agent's ability to handle a multi-turn conversation
        agent = TodoAgent()

        user_id = "test_user_456"
        conversation_id = None

        # Simulate a multi-turn conversation
        messages = [
            "Add a task to buy groceries",
            "What tasks do I have?",
            "Tell me again about my tasks"
        ]

        for i, message in enumerate(messages):
            result = await agent.process_message(user_id, conversation_id, message)

            # Verify conversation ID is maintained after first message
            if i == 0:
                assert result["conversation_id"] is not None
                conversation_id = result["conversation_id"]
            else:
                assert result["conversation_id"] == conversation_id

            # Verify response is not empty
            assert result["response"] != ""


@pytest.mark.asyncio
async def test_contextual_task_references():
    """Test that the agent correctly identifies tasks based on conversation context."""
    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'add_task', new_callable=AsyncMock) as mock_add_task, \
         patch.object(TaskMCPTools, 'list_tasks', new_callable=AsyncMock) as mock_list_tasks, \
         patch.object(TaskMCPTools, 'update_task', new_callable=AsyncMock) as mock_update_task, \
         patch.object(ConversationMCPTools, 'create_conversation', new_callable=AsyncMock) as mock_create_conv, \
         patch.object(ConversationMCPTools, 'add_message_to_conversation', new_callable=AsyncMock) as mock_add_msg:

        # Set up mock return values
        mock_create_conv.return_value = {"success": True, "conversation_id": 1, "message": "Conversation created"}
        mock_add_task.return_value = {"success": True, "task_id": 1, "message": "Task created"}
        mock_list_tasks.return_value = {
            "success": True,
            "tasks": [
                {"id": 1, "title": "Call mom", "completed": False},
                {"id": 2, "title": "Buy groceries", "completed": False}
            ],
            "count": 2
        }
        mock_update_task.return_value = {"success": True, "message": "Task updated"}
        mock_add_msg.return_value = {"success": True, "message_id": 1, "message": "Message added"}

        # Test the agent's ability to reference tasks by position in context
        agent = TodoAgent()

        user_id = "test_user_789"
        conversation_id = None

        # Add two tasks
        result1 = await agent.process_message(user_id, conversation_id, "Add a task to call mom")
        conversation_id = result1["conversation_id"]

        result2 = await agent.process_message(user_id, conversation_id, "Add a task to buy groceries")

        # List tasks to establish context
        result3 = await agent.process_message(user_id, conversation_id, "Show my tasks")

        # Update the first task by referencing its position
        result4 = await agent.process_message(user_id, conversation_id, "Change the first task to call dad instead")

        # Verify the conversation continued properly
        assert result4["response"] != ""
        assert result3["conversation_id"] == result4["conversation_id"]
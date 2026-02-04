"""
Integration tests for the chat functionality of the Todo AI Chatbot.
Tests natural language processing for task operations.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import AsyncMock, patch
import sys
import os

# Add the backend directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from main import app
from src.mcp_tools.task_mcp_tools import TaskMCPTools
from src.mcp_tools.conversation_mcp_tools import ConversationMCPTools
from src.agents.todo_agent import TodoAgent


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.asyncio
async def test_natural_language_processing_for_task_creation():
    """Test natural language processing for task creation."""
    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'add_task', new_callable=AsyncMock) as mock_add_task:
        mock_add_task.return_value = {"success": True, "task_id": 1, "message": "Task created successfully"}

        # Test that the agent correctly identifies task creation intent
        agent = TodoAgent()

        result = await agent._determine_intent("Add a task to call mom")
        assert result["intent"] == "create_task"
        assert "call mom" in result["params"]["title"].lower()


@pytest.mark.asyncio
async def test_natural_language_processing_for_task_listing():
    """Test natural language processing for task listing."""
    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'list_tasks', new_callable=AsyncMock) as mock_list_tasks:
        mock_list_tasks.return_value = {"success": True, "tasks": [], "count": 0}

        # Test that the agent correctly identifies task listing intent
        agent = TodoAgent()

        result = await agent._determine_intent("Show me my tasks")
        assert result["intent"] == "list_tasks"


@pytest.mark.asyncio
async def test_natural_language_processing_for_task_completion():
    """Test natural language processing for task completion."""
    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'complete_task', new_callable=AsyncMock) as mock_complete_task:
        mock_complete_task.return_value = {"success": True, "message": "Task completed successfully"}

        # Test that the agent correctly identifies task completion intent
        agent = TodoAgent()

        result = await agent._determine_intent("Complete the first task")
        assert result["intent"] == "complete_task"
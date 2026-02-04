"""
Performance tests for the chat endpoint in the Todo AI Chatbot.
Tests to ensure the chat endpoint meets performance requirements.
"""

import pytest
import time
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.mcp_tools.task_mcp_tools import TaskMCPTools
from src.mcp_tools.conversation_mcp_tools import ConversationMCPTools
from src.agents.todo_agent import TodoAgent

# Import the main app for testing
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from main import app


def test_single_chat_request_performance():
    """Test the performance of a single chat request."""
    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'add_task', new_callable=AsyncMock) as mock_add_task, \
         patch.object(ConversationMCPTools, 'create_conversation', new_callable=AsyncMock) as mock_create_conv, \
         patch.object(ConversationMCPTools, 'add_message_to_conversation', new_callable=AsyncMock) as mock_add_msg:

        # Set up mock return values
        mock_add_task.return_value = {"success": True, "task_id": 1, "message": "Task created"}
        mock_create_conv.return_value = {"success": True, "conversation_id": 1, "message": "Conversation created"}
        mock_add_msg.return_value = {"success": True, "message_id": 1, "message": "Message added"}

        # Create a test client
        client = TestClient(app)

        # Measure the time to process a request
        start_time = time.time()

        # Simulate a simple chat request using the agent directly
        agent = TodoAgent()
        user_id = "test_user_123"

        # Process a simple request
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                agent.process_message(user_id, None, "Add a task to buy groceries")
            )
        finally:
            loop.close()

        end_time = time.time()
        duration = end_time - start_time

        # Assert that the request completed within acceptable time (e.g., 3 seconds)
        assert duration < 3.0, f"Request took {duration:.2f}s, which is too slow"

        # Verify that we got a response
        assert result is not None
        assert "response" in result


@pytest.mark.asyncio
async def test_multiple_concurrent_requests_performance():
    """Test performance under concurrent requests."""
    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'add_task', new_callable=AsyncMock) as mock_add_task, \
         patch.object(ConversationMCPTools, 'create_conversation', new_callable=AsyncMock) as mock_create_conv, \
         patch.object(ConversationMCPTools, 'add_message_to_conversation', new_callable=AsyncMock) as mock_add_msg:

        # Set up mock return values
        mock_add_task.return_value = {"success": True, "task_id": 1, "message": "Task created"}
        mock_create_conv.return_value = {"success": True, "conversation_id": 1, "message": "Conversation created"}
        mock_add_msg.return_value = {"success": True, "message_id": 1, "message": "Message added"}

        # Create an agent instance
        agent = TodoAgent()

        # Define the number of concurrent requests to test
        num_requests = 10
        user_ids = [f"test_user_{i}" for i in range(num_requests)]
        messages = [f"Add task {i} for user {i}" for i in range(num_requests)]

        # Record start time
        start_time = time.time()

        # Create tasks for concurrent execution
        tasks = [
            agent.process_message(user_ids[i], None, messages[i])
            for i in range(num_requests)
        ]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks)

        # Record end time
        end_time = time.time()
        duration = end_time - start_time

        # Verify that all requests succeeded
        assert len(results) == num_requests
        for result in results:
            assert result is not None
            assert "response" in result

        # Assert that all requests completed within a reasonable time
        # For 10 concurrent requests, allow slightly more time
        assert duration < 10.0, f"All {num_requests} requests took {duration:.2f}s, which is too slow"


def test_agent_processing_performance():
    """Test the performance of the AI agent processing."""
    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'list_tasks', new_callable=AsyncMock) as mock_list_tasks, \
         patch.object(ConversationMCPTools, 'create_conversation', new_callable=AsyncMock) as mock_create_conv, \
         patch.object(ConversationMCPTools, 'add_message_to_conversation', new_callable=AsyncMock) as mock_add_msg:

        # Set up mock return values with multiple tasks
        mock_list_tasks.return_value = {
            "success": True,
            "tasks": [
                {"id": i, "title": f"Task {i}", "completed": i % 2 == 0}
                for i in range(1, 21)  # 20 tasks
            ],
            "count": 20
        }
        mock_create_conv.return_value = {"success": True, "conversation_id": 1, "message": "Conversation created"}
        mock_add_msg.return_value = {"success": True, "message_id": 1, "message": "Message added"}

        # Create an agent instance
        agent = TodoAgent()

        # Record start time
        start_time = time.time()

        # Process a request that requires handling multiple tasks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                agent.process_message("test_user_456", None, "Show me all my tasks")
            )
        finally:
            loop.close()

        # Record end time
        end_time = time.time()
        duration = end_time - start_time

        # Verify the result
        assert result is not None
        assert "response" in result
        assert len(result["response"]) > 0  # Should have a response with task list

        # Assert that the processing completed within acceptable time
        assert duration < 2.0, f"Processing with 20 tasks took {duration:.2f}s, which is too slow"


@pytest.mark.asyncio
async def test_determine_intent_performance():
    """Test the performance of intent determination."""
    agent = TodoAgent()

    # Test various types of messages
    test_messages = [
        "Add a task to call mom",
        "Show me my tasks",
        "Complete the first task",
        "Update task 1 to call dad instead",
        "Delete the second task from my list",
        "What are my pending tasks?",
        "Mark task 5 as done",
        "I need to remember to buy groceries"
    ]

    # Record start time
    start_time = time.time()

    # Process all messages
    for message in test_messages:
        intent_result = await agent._determine_intent(message)
        assert "intent" in intent_result
        assert "params" in intent_result

    # Record end time
    end_time = time.time()
    duration = end_time - start_time

    # Assert that processing all intents was fast
    assert duration < 0.5, f"Processing {len(test_messages)} intents took {duration:.2f}s, which is too slow"


def test_agent_context_handling_performance():
    """Test the performance of context handling in the agent."""
    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'add_task', new_callable=AsyncMock) as mock_add_task, \
         patch.object(TaskMCPTools, 'list_tasks', new_callable=AsyncMock) as mock_list_tasks, \
         patch.object(TaskMCPTools, 'complete_task', new_callable=AsyncMock) as mock_complete_task, \
         patch.object(ConversationMCPTools, 'create_conversation', new_callable=AsyncMock) as mock_create_conv, \
         patch.object(ConversationMCPTools, 'add_message_to_conversation', new_callable=AsyncMock) as mock_add_msg:

        # Set up mock return values
        mock_add_task.return_value = {"success": True, "task_id": 1, "message": "Task created"}
        mock_list_tasks.return_value = {
            "success": True,
            "tasks": [{"id": 1, "title": "Test task", "completed": False}],
            "count": 1
        }
        mock_complete_task.return_value = {"success": True, "message": "Task completed"}
        mock_create_conv.return_value = {"success": True, "conversation_id": 1, "message": "Conversation created"}
        mock_add_msg.return_value = {"success": True, "message_id": 1, "message": "Message added"}

        # Create an agent instance
        agent = TodoAgent()

        # Record start time
        start_time = time.time()

        # Simulate a conversation sequence that requires context handling
        user_id = "test_user_789"

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Add a task
            result1 = loop.run_until_complete(
                agent.process_message(user_id, None, "Add a task to schedule dentist appointment")
            )

            # List tasks to establish context
            result2 = loop.run_until_complete(
                agent.process_message(user_id, result1["conversation_id"], "Show my tasks")
            )

            # Complete the task by referencing it in context
            result3 = loop.run_until_complete(
                agent.process_message(user_id, result2["conversation_id"], "Complete the first task")
            )
        finally:
            loop.close()

        # Record end time
        end_time = time.time()
        duration = end_time - start_time

        # Verify results
        assert result1 is not None
        assert result2 is not None
        assert result3 is not None

        # Verify conversation continuity
        assert result1["conversation_id"] == result2["conversation_id"]
        assert result2["conversation_id"] == result3["conversation_id"]

        # Assert that the conversation with context handling was fast
        assert duration < 3.0, f"Context-aware conversation took {duration:.2f}s, which is too slow"


# Additional performance test for measuring p95 response time
def test_p95_response_time_simulation():
    """Simulate measuring p95 response time for the chat endpoint."""
    # This is a simplified simulation of p95 measurement
    # In a real system, you would collect actual response times over time

    # Mock the MCP tools to avoid actual database calls
    with patch.object(TaskMCPTools, 'add_task', new_callable=AsyncMock) as mock_add_task, \
         patch.object(ConversationMCPTools, 'create_conversation', new_callable=AsyncMock) as mock_create_conv, \
         patch.object(ConversationMCPTools, 'add_message_to_conversation', new_callable=AsyncMock) as mock_add_msg:

        # Set up mock return values
        mock_add_task.return_value = {"success": True, "task_id": 1, "message": "Task created"}
        mock_create_conv.return_value = {"success": True, "conversation_id": 1, "message": "Conversation created"}
        mock_add_msg.return_value = {"success": True, "message_id": 1, "message": "Message added"}

        # Simulate multiple requests and measure response times
        response_times = []
        agent = TodoAgent()
        num_samples = 100

        for i in range(num_samples):
            start_time = time.time()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    agent.process_message(f"user_{i}", None, f"Add task {i} for testing")
                )
            finally:
                loop.close()

            end_time = time.time()
            response_times.append(end_time - start_time)

        # Calculate approximate p95 (95th percentile)
        # Sort the response times and get the 95th percentile value
        sorted_times = sorted(response_times)
        p95_index = int(0.95 * len(sorted_times))
        p95_time = sorted_times[p95_index] if p95_index < len(sorted_times) else sorted_times[-1]

        # Assert that p95 response time meets the requirement (e.g., < 3 seconds)
        assert p95_time < 3.0, f"P95 response time is {p95_time:.2f}s, which exceeds the 3s requirement"
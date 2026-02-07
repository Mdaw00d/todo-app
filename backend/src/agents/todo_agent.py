"""
Todo AI Agent for the Todo AI Chatbot.
Manages AI interactions and reasoning for todo management.
"""

import asyncio
from typing import Dict, Any, Optional, List
from ..mcp_tools.task_mcp_tools import TaskMCPTools
from ..mcp_tools.conversation_mcp_tools import ConversationMCPTools
from ..utils.logging import get_logger


logger = get_logger("todo_agent")


class TodoAgent:
    """
    AI Agent for handling todo management through natural language.
    Uses MCP tools to perform operations on tasks and conversations.
    """

    def __init__(self):
        """Initialize the Todo Agent with MCP tools."""
        try:
            self.task_tools = TaskMCPTools()
            self.conversation_tools = ConversationMCPTools()
        except Exception as e:
            print(f"Error initializing MCP tools: {str(e)}")
            # Create dummy tools that return error responses
            class DummyTools:
                async def add_task(self, **kwargs):
                    return {"success": False, "error": "MCP tools not available"}
                
                async def list_tasks(self, **kwargs):
                    return {"success": False, "error": "MCP tools not available", "tasks": []}
                
                async def complete_task(self, **kwargs):
                    return {"success": False, "error": "MCP tools not available"}
                
                async def update_task(self, **kwargs):
                    return {"success": False, "error": "MCP tools not available"}
                
                async def delete_task(self, **kwargs):
                    return {"success": False, "error": "MCP tools not available"}
                
                async def create_conversation(self, **kwargs):
                    return {"success": False, "error": "MCP tools not available"}
                
                async def add_message_to_conversation(self, **kwargs):
                    return {"success": False, "error": "MCP tools not available"}

            self.task_tools = DummyTools()
            self.conversation_tools = DummyTools()
        
        self.logger = logger

    async def process_message(self, user_id: str, conversation_id: Optional[int], message: str) -> Dict[str, Any]:
        """
        Process a user message and return an appropriate response.

        Args:
            user_id: ID of the user sending the message
            conversation_id: ID of the conversation (None for new conversation)
            message: The user's message

        Returns:
            Dict containing response and any tool calls made
        """
        self.logger.info(f"Processing message for user {user_id}: {message}")

        # Determine intent from the message
        intent_result = await self._determine_intent(message)
        intent = intent_result["intent"]
        params = intent_result["params"]

        # Add user ID to params
        params["user_id"] = user_id

        response = ""
        tool_calls = []

        try:
            if intent == "create_task":
                # Create a new conversation if needed
                if conversation_id is None:
                    conv_result = await self.conversation_tools.create_conversation(user_id)
                    if conv_result["success"]:
                        conversation_id = conv_result["conversation_id"]

                # Add the user message to the conversation
                await self.conversation_tools.add_message_to_conversation(
                    user_id, conversation_id, "user", message
                )

                # Create the task
                task_result = await self.task_tools.add_task(
                    user_id=user_id,
                    title=params.get("title", ""),
                    description=params.get("description", "")
                )

                if task_result["success"]:
                    response = f"I've added the task '{params.get('title', '')}' to your list."
                    tool_calls.append({
                        "name": "add_task",
                        "arguments": {
                            "user_id": user_id,
                            "title": params.get("title", ""),
                            "description": params.get("description", "")
                        }
                    })

                    # Add the assistant's response to the conversation
                    await self.conversation_tools.add_message_to_conversation(
                        user_id, conversation_id, "assistant", response
                    )
                else:
                    response = f"Sorry, I couldn't add the task: {task_result.get('error', 'Unknown error')}"

            elif intent == "list_tasks":
                # Create a new conversation if needed
                if conversation_id is None:
                    conv_result = await self.conversation_tools.create_conversation(user_id)
                    if conv_result["success"]:
                        conversation_id = conv_result["conversation_id"]

                # Add the user message to the conversation
                await self.conversation_tools.add_message_to_conversation(
                    user_id, conversation_id, "user", message
                )

                # Get the user's tasks
                status = params.get("status", "all")
                tasks_result = await self.task_tools.list_tasks(user_id, status)

                if tasks_result["success"]:
                    tasks = tasks_result["tasks"]
                    if tasks:
                        task_list_str = "\n".join([f"- {task['title']} ({'completed' if task['completed'] else 'pending'})" for task in tasks])
                        response = f"Here are your tasks:\n{task_list_str}"
                    else:
                        response = "You don't have any tasks at the moment."

                    tool_calls.append({
                        "name": "list_tasks",
                        "arguments": {
                            "user_id": user_id,
                            "status": status
                        }
                    })

                    # Add the assistant's response to the conversation
                    await self.conversation_tools.add_message_to_conversation(
                        user_id, conversation_id, "assistant", response
                    )
                else:
                    response = f"Sorry, I couldn't retrieve your tasks: {tasks_result.get('error', 'Unknown error')}"

            elif intent == "complete_task":
                # Create a new conversation if needed
                if conversation_id is None:
                    conv_result = await self.conversation_tools.create_conversation(user_id)
                    if conv_result["success"]:
                        conversation_id = conv_result["conversation_id"]

                # Add the user message to the conversation
                await self.conversation_tools.add_message_to_conversation(
                    user_id, conversation_id, "user", message
                )

                # Complete the task
                task_id = params.get("task_id")
                if task_id:
                    task_result = await self.task_tools.complete_task(user_id, task_id)

                    if task_result["success"]:
                        response = f"I've marked the task as completed."
                        tool_calls.append({
                            "name": "complete_task",
                            "arguments": {
                                "user_id": user_id,
                                "task_id": task_id
                            }
                        })

                        # Add the assistant's response to the conversation
                        await self.conversation_tools.add_message_to_conversation(
                            user_id, conversation_id, "assistant", response
                        )
                    else:
                        response = f"Sorry, I couldn't complete the task: {task_result.get('error', 'Unknown error')}"
                else:
                    response = "I couldn't identify which task to complete."

            elif intent == "update_task":
                # Create a new conversation if needed
                if conversation_id is None:
                    conv_result = await self.conversation_tools.create_conversation(user_id)
                    if conv_result["success"]:
                        conversation_id = conv_result["conversation_id"]

                # Add the user message to the conversation
                await self.conversation_tools.add_message_to_conversation(
                    user_id, conversation_id, "user", message
                )

                # Update the task
                task_id = params.get("task_id")
                if task_id:
                    task_result = await self.task_tools.update_task(
                        user_id, task_id,
                        title=params.get("title"),
                        description=params.get("description")
                    )

                    if task_result["success"]:
                        response = f"I've updated the task."
                        tool_calls.append({
                            "name": "update_task",
                            "arguments": {
                                "user_id": user_id,
                                "task_id": task_id,
                                "title": params.get("title"),
                                "description": params.get("description")
                            }
                        })

                        # Add the assistant's response to the conversation
                        await self.conversation_tools.add_message_to_conversation(
                            user_id, conversation_id, "assistant", response
                        )
                    else:
                        response = f"Sorry, I couldn't update the task: {task_result.get('error', 'Unknown error')}"
                else:
                    response = "I couldn't identify which task to update."

            elif intent == "delete_task":
                # Create a new conversation if needed
                if conversation_id is None:
                    conv_result = await self.conversation_tools.create_conversation(user_id)
                    if conv_result["success"]:
                        conversation_id = conv_result["conversation_id"]

                # Add the user message to the conversation
                await self.conversation_tools.add_message_to_conversation(
                    user_id, conversation_id, "user", message
                )

                # Delete the task
                task_id = params.get("task_id")
                if task_id:
                    task_result = await self.task_tools.delete_task(user_id, task_id)

                    if task_result["success"]:
                        response = f"I've deleted the task."
                        tool_calls.append({
                            "name": "delete_task",
                            "arguments": {
                                "user_id": user_id,
                                "task_id": task_id
                            }
                        })

                        # Add the assistant's response to the conversation
                        await self.conversation_tools.add_message_to_conversation(
                            user_id, conversation_id, "assistant", response
                        )
                    else:
                        response = f"Sorry, I couldn't delete the task: {task_result.get('error', 'Unknown error')}"
                else:
                    response = "I couldn't identify which task to delete."

            else:
                # Unknown intent - create a new conversation if needed
                if conversation_id is None:
                    conv_result = await self.conversation_tools.create_conversation(user_id)
                    if conv_result["success"]:
                        conversation_id = conv_result["conversation_id"]

                # Add the user message to the conversation
                await self.conversation_tools.add_message_to_conversation(
                    user_id, conversation_id, "user", message
                )

                response = "I'm sorry, I didn't understand that. Could you please rephrase or try commands like 'add task', 'list tasks', 'complete task', etc.?"

                # Add the assistant's response to the conversation
                await self.conversation_tools.add_message_to_conversation(
                    user_id, conversation_id, "assistant", response
                )

        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            response = "Sorry, I encountered an error processing your request."

        return {
            "conversation_id": conversation_id,
            "response": response,
            "tool_calls": tool_calls
        }

    async def _determine_intent(self, message: str) -> Dict[str, Any]:
        """
        Determine the intent from a user message using simple keyword matching.
        In a real implementation, this would use NLP or an AI model.

        Args:
            message: The user's message

        Returns:
            Dict containing the intent and extracted parameters
        """
        message_lower = message.lower().strip()

        # Intent: Create task
        if any(keyword in message_lower for keyword in ["add task", "create task", "new task", "add a task", "remember to", "remind me to"]):
            # Extract task title from message
            title = ""
            if "add task" in message_lower:
                title = message_lower.split("add task", 1)[1].strip()
            elif "create task" in message_lower:
                title = message_lower.split("create task", 1)[1].strip()
            elif "new task" in message_lower:
                title = message_lower.split("new task", 1)[1].strip()
            elif "add a task" in message_lower:
                title = message_lower.split("add a task", 1)[1].strip()
            elif "remember to" in message_lower:
                title = message_lower.split("remember to", 1)[1].strip()
            elif "remind me to" in message_lower:
                title = message_lower.split("remind me to", 1)[1].strip()

            # Clean up the title
            title = title.strip().strip('"').strip("'").strip()

            return {
                "intent": "create_task",
                "params": {
                    "title": title or "Untitled task",
                    "description": ""
                }
            }

        # Intent: List tasks
        elif any(keyword in message_lower for keyword in ["list tasks", "show tasks", "my tasks", "show me", "list my", "what are my", "show my"]):
            status = "all"
            if "pending" in message_lower or "incomplete" in message_lower:
                status = "pending"
            elif "completed" in message_lower or "done" in message_lower:
                status = "completed"

            return {
                "intent": "list_tasks",
                "params": {
                    "status": status
                }
            }

        # Intent: Complete task
        elif any(keyword in message_lower for keyword in ["complete task", "finish task", "done with", "mark as done", "complete the"]):
            # Try to extract task ID or title
            task_id = None
            if "task" in message_lower and any(c.isdigit() for c in message_lower):
                # Look for digits that might represent a task ID
                import re
                matches = re.findall(r'\d+', message_lower)
                if matches:
                    try:
                        task_id = int(matches[0])
                    except ValueError:
                        pass

            return {
                "intent": "complete_task",
                "params": {
                    "task_id": task_id
                }
            }

        # Intent: Update task
        elif any(keyword in message_lower for keyword in ["update task", "change task", "edit task", "modify task"]):
            # Try to extract task ID and new details
            task_id = None
            title = None
            description = None

            if "task" in message_lower and any(c.isdigit() for c in message_lower):
                import re
                matches = re.findall(r'\d+', message_lower)
                if matches:
                    try:
                        task_id = int(matches[0])
                    except ValueError:
                        pass

            return {
                "intent": "update_task",
                "params": {
                    "task_id": task_id,
                    "title": title,
                    "description": description
                }
            }

        # Intent: Delete task
        elif any(keyword in message_lower for keyword in ["delete task", "remove task", "cancel task", "get rid of"]):
            # Try to extract task ID
            task_id = None
            if "task" in message_lower and any(c.isdigit() for c in message_lower):
                import re
                matches = re.findall(r'\d+', message_lower)
                if matches:
                    try:
                        task_id = int(matches[0])
                    except ValueError:
                        pass

            return {
                "intent": "delete_task",
                "params": {
                    "task_id": task_id
                }
            }

        # Default: Unknown intent
        else:
            return {
                "intent": "unknown",
                "params": {}
            }
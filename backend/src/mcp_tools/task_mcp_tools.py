"""
MCP tools for task operations in the Todo AI Chatbot.
These tools allow the AI agent to perform task operations through MCP.
"""

import asyncio
from typing import Optional, List, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from ..services.task_service import TaskService
from ..models.task import TaskCreate, TaskUpdate
from ..database import get_async_session
from ..utils.validation import validate_user_id, validate_task_title, validate_task_description


class TaskMCPTools:
    """Class containing MCP tools for task operations."""

    @staticmethod
    async def add_task(
        user_id: str,
        title: str,
        description: Optional[str] = None
    ) -> dict:
        """
        Add a new task for a user.

        Args:
            user_id: ID of the user creating the task
            title: Title of the task
            description: Optional description of the task

        Returns:
            dict: Result of the operation
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        is_valid, error_msg = validate_task_title(title)
        if not is_valid:
            return {"success": False, "error": error_msg}

        if description:
            is_valid, error_msg = validate_task_description(description)
            if not is_valid:
                return {"success": False, "error": error_msg}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Prepare the task creation data
                task_create = TaskCreate(
                    user_id=user_id,
                    title=title,
                    description=description
                )

                # Call the service to create the task
                created_task = await TaskService.create_task(session, task_create)

                return {
                    "success": True,
                    "task_id": created_task.id,
                    "message": f"Task '{title}' created successfully"
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to create task: {str(e)}"}

    @staticmethod
    async def list_tasks(
        user_id: str,
        status: str = "all"
    ) -> dict:
        """
        List tasks for a user, optionally filtered by status.

        Args:
            user_id: ID of the user whose tasks to list
            status: Filter by status ('all', 'pending', 'completed')

        Returns:
            dict: Result of the operation with task list
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        # Validate status parameter
        if status not in ["all", "pending", "completed"]:
            return {"success": False, "error": "Invalid status parameter. Use 'all', 'pending', or 'completed'"}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Call the service to get tasks
                tasks = await TaskService.get_tasks_by_user(session, user_id, status)

                # Format the result
                task_list = []
                for task in tasks:
                    task_dict = {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat() if task.created_at else None
                    }
                    task_list.append(task_dict)

                return {
                    "success": True,
                    "tasks": task_list,
                    "count": len(task_list)
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to list tasks: {str(e)}"}

    @staticmethod
    async def complete_task(
        user_id: str,
        task_id: int
    ) -> dict:
        """
        Mark a task as completed.

        Args:
            user_id: ID of the user who owns the task
            task_id: ID of the task to complete

        Returns:
            dict: Result of the operation
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(task_id, int) or task_id <= 0:
            return {"success": False, "error": "Invalid task ID"}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Call the service to complete the task
                updated_task = await TaskService.complete_task(session, task_id, user_id)

                return {
                    "success": True,
                    "message": f"Task '{updated_task.title}' marked as completed"
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to complete task: {str(e)}"}

    @staticmethod
    async def update_task(
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> dict:
        """
        Update a task.

        Args:
            user_id: ID of the user who owns the task
            task_id: ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)

        Returns:
            dict: Result of the operation
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(task_id, int) or task_id <= 0:
            return {"success": False, "error": "Invalid task ID"}

        if title is not None:
            is_valid, error_msg = validate_task_title(title)
            if not is_valid:
                return {"success": False, "error": error_msg}

        if description is not None:
            is_valid, error_msg = validate_task_description(description)
            if not is_valid:
                return {"success": False, "error": error_msg}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Prepare the task update data
                task_update = TaskUpdate(
                    title=title,
                    description=description
                )

                # Call the service to update the task
                updated_task = await TaskService.update_task(session, task_id, user_id, task_update)

                return {
                    "success": True,
                    "message": f"Task updated successfully"
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to update task: {str(e)}"}

    @staticmethod
    async def delete_task(
        user_id: str,
        task_id: int
    ) -> dict:
        """
        Delete a task.

        Args:
            user_id: ID of the user who owns the task
            task_id: ID of the task to delete

        Returns:
            dict: Result of the operation
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(task_id, int) or task_id <= 0:
            return {"success": False, "error": "Invalid task ID"}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Call the service to delete the task
                success = await TaskService.delete_task(session, task_id, user_id)

                if success:
                    return {
                        "success": True,
                        "message": f"Task deleted successfully"
                    }
                else:
                    return {
                        "success": False,
                        "error": "Failed to delete task"
                    }

        except Exception as e:
            return {"success": False, "error": f"Failed to delete task: {str(e)}"}

    @staticmethod
    async def get_task_by_id(
        user_id: str,
        task_id: int
    ) -> dict:
        """
        Get a specific task by its ID.

        Args:
            user_id: ID of the user who owns the task
            task_id: ID of the task to retrieve

        Returns:
            dict: Result of the operation with task details
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(task_id, int) or task_id <= 0:
            return {"success": False, "error": "Invalid task ID"}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Call the service to get the task
                task = await TaskService.get_task_by_id(session, task_id, user_id)

                # Format the result
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                    "user_id": task.user_id
                }

                return {
                    "success": True,
                    "task": task_dict
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to get task: {str(e)}"}

    @staticmethod
    async def get_recent_tasks(
        user_id: str,
        limit: int = 10
    ) -> dict:
        """
        Get the most recent tasks for a user.

        Args:
            user_id: ID of the user whose tasks to retrieve
            limit: Maximum number of tasks to return

        Returns:
            dict: Result of the operation with recent tasks
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(limit, int) or limit <= 0:
            return {"success": False, "error": "Invalid limit"}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Call the service to get all tasks for the user
                all_tasks = await TaskService.get_tasks_by_user(session, user_id, "all")

                # Sort by creation date descending and take the limit
                sorted_tasks = sorted(all_tasks, key=lambda x: x.created_at, reverse=True)[:limit]

                # Format the result
                task_list = []
                for task in sorted_tasks:
                    task_dict = {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat() if task.created_at else None
                    }
                    task_list.append(task_dict)

                return {
                    "success": True,
                    "tasks": task_list,
                    "count": len(task_list)
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to get recent tasks: {str(e)}"}
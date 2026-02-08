"""
MCP tools for task operations in the Todo AI Chatbot.
These tools allow the AI agent to perform task operations through MCP.
"""

from typing import Optional
from ..services.task_service import TaskService
from ..models.task import TaskCreate, TaskUpdate
from ..database import get_async_session
from ..utils.validation import (
    validate_user_id,
    validate_task_title,
    validate_task_description,
)


class TaskMCPTools:
    """Class containing MCP tools for task operations."""

    @staticmethod
    async def add_task(
        user_id: str,
        title: str,
        description: Optional[str] = None,
    ) -> dict:
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
            async with get_async_session() as session:
                task_create = TaskCreate(
                    title=title,
                    description=description,
                )
                service = TaskService(session)
                created_task = await service.create_task(user_id, task_create)

                return {
                    "success": True,
                    "task_id": created_task.id,
                    "message": f"Task '{title}' created successfully",
                }
        except Exception as e:
            return {"success": False, "error": f"Failed to create task: {str(e)}"}

    @staticmethod
    async def list_tasks(
        user_id: str,
        status: str = "all",
    ) -> dict:
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if status not in ["all", "pending", "completed"]:
            return {
                "success": False,
                "error": "Invalid status parameter. Use 'all', 'pending', or 'completed'",
            }

        try:
            async with get_async_session() as session:
                service = TaskService(session)
                tasks = await service.list_tasks(user_id)

                if status == "pending":
                    tasks = [t for t in tasks if not t.completed]
                elif status == "completed":
                    tasks = [t for t in tasks if t.completed]

                task_list = [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed,
                        "created_at": t.created_at.isoformat()
                        if t.created_at
                        else None,
                    }
                    for t in tasks
                ]

                return {
                    "success": True,
                    "tasks": task_list,
                    "count": len(task_list),
                }
        except Exception as e:
            return {"success": False, "error": f"Failed to list tasks: {str(e)}"}

    @staticmethod
    async def complete_task(
        user_id: str,
        task_id: int,
    ) -> dict:
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(task_id, int) or task_id <= 0:
            return {"success": False, "error": "Invalid task ID"}

        try:
            async with get_async_session() as session:
                service = TaskService(session)
                updated_task = await service.toggle_complete(
                    user_id, str(task_id)
                )

                if updated_task:
                    return {
                        "success": True,
                        "message": f"Task '{updated_task.title}' marked as completed",
                    }
                return {
                    "success": False,
                    "error": "Task not found or access denied",
                }
        except Exception as e:
            return {"success": False, "error": f"Failed to complete task: {str(e)}"}

    @staticmethod
    async def update_task(
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> dict:
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
            async with get_async_session() as session:
                task_update = TaskUpdate(
                    title=title,
                    description=description,
                )
                service = TaskService(session)
                updated_task = await service.update_task(
                    user_id, str(task_id), task_update
                )

                if updated_task:
                    return {"success": True, "message": "Task updated successfully"}
                return {
                    "success": False,
                    "error": "Task not found or access denied",
                }
        except Exception as e:
            return {"success": False, "error": f"Failed to update task: {str(e)}"}

    @staticmethod
    async def delete_task(
        user_id: str,
        task_id: int,
    ) -> dict:
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(task_id, int) or task_id <= 0:
            return {"success": False, "error": "Invalid task ID"}

        try:
            async with get_async_session() as session:
                service = TaskService(session)
                success = await service.delete_task(
                    user_id, str(task_id)
                )

                if success:
                    return {"success": True, "message": "Task deleted successfully"}
                return {
                    "success": False,
                    "error": "Task not found or access denied",
                }
        except Exception as e:
            return {"success": False, "error": f"Failed to delete task: {str(e)}"}

    @staticmethod
    async def get_task_by_id(
        user_id: str,
        task_id: int,
    ) -> dict:
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(task_id, int) or task_id <= 0:
            return {"success": False, "error": "Invalid task ID"}

        try:
            async with get_async_session() as session:
                service = TaskService(session)
                task = await service.get_task(user_id, str(task_id))

                if not task:
                    return {
                        "success": False,
                        "error": "Task not found or access denied",
                    }

                return {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat()
                        if task.created_at
                        else None,
                        "updated_at": task.updated_at.isoformat()
                        if task.updated_at
                        else None,
                        "user_id": task.user_id,
                    },
                }
        except Exception as e:
            return {"success": False, "error": f"Failed to get task: {str(e)}"}

    @staticmethod
    async def get_recent_tasks(
        user_id: str,
        limit: int = 10,
    ) -> dict:
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(limit, int) or limit <= 0:
            return {"success": False, "error": "Invalid limit"}

        try:
            async with get_async_session() as session:
                service = TaskService(session)
                tasks = await service.list_tasks(user_id)

                tasks = sorted(
                    tasks,
                    key=lambda t: t.created_at,
                    reverse=True,
                )[:limit]

                task_list = [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed,
                        "created_at": t.created_at.isoformat()
                        if t.created_at
                        else None,
                    }
                    for t in tasks
                ]

                return {
                    "success": True,
                    "tasks": task_list,
                    "count": len(task_list),
                }
        except Exception as e:
            return {"success": False, "error": f"Failed to get recent tasks: {str(e)}"}

"""Task API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, verify_user_access
from src.auth.middleware import JWTUser
from src.database import get_session
from src.models.task import Task, TaskCreate, TaskPublic as TaskResponse, TaskUpdate
from src.services.task_service import TaskService

router = APIRouter(prefix="/api/users/{user_id}/tasks", tags=["tasks"])




@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    user_id: str,  # This is ignored, we use the authenticated user's ID
    current_user: JWTUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[Task]:
    """Get all tasks for the specified user.

    Returns a list of tasks belonging to the authenticated user,
    ordered by creation date (newest first).
    """
    service = TaskService(session)
    return await service.list_tasks(current_user.user_id)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,  # This is ignored, we use the authenticated user's ID
    task_id: str,
    current_user: JWTUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Task:
    """Get a specific task by ID.

    Returns the task if found and owned by the authenticated user.
    """
    service = TaskService(session)
    task = await service.get_task(current_user.user_id, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    return task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,  # This is ignored, we use the authenticated user's ID
    data: TaskCreate,
    current_user: JWTUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Task:
    """Create a new task for the authenticated user.

    The task title is required and must be between 1-200 characters.
    The description is optional.
    """
    service = TaskService(session)

    try:
        return await service.create_task(current_user.user_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,  # This is ignored, we use the authenticated user's ID
    task_id: str,
    data: TaskUpdate,
    current_user: JWTUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Task:
    """Update an existing task.

    Both title and description can be updated.
    Title must be between 1-200 characters if provided.
    """
    service = TaskService(session)

    try:
        task = await service.update_task(current_user.user_id, task_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,  # This is ignored, we use the authenticated user's ID
    task_id: str,
    current_user: JWTUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a task.

    Returns 204 No Content on success, 404 if task not found.
    """
    service = TaskService(session)
    deleted = await service.delete_task(current_user.user_id, task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,  # This is ignored, we use the authenticated user's ID
    task_id: str,
    current_user: JWTUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Task:
    """Toggle the completion status of a task.

    If the task is incomplete, it will be marked as complete.
    If the task is complete, it will be marked as incomplete.
    """
    service = TaskService(session)
    task = await service.toggle_complete(current_user.user_id, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    return task

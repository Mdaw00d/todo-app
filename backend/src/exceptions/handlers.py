"""
Custom exception handlers for the Todo AI Chatbot.
Defines application-specific exceptions and error responses.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Union
from pydantic import ValidationError
from sqlmodel import SQLModel


class TodoException(Exception):
    """Base exception for todo-related errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class TaskNotFoundException(TodoException):
    """Raised when a task is not found."""
    def __init__(self, task_id: int):
        super().__init__(f"Task with ID {task_id} not found", 404)


class ConversationNotFoundException(TodoException):
    """Raised when a conversation is not found."""
    def __init__(self, conversation_id: int):
        super().__init__(f"Conversation with ID {conversation_id} not found", 404)


class UnauthorizedAccessException(TodoException):
    """Raised when a user tries to access another user's data."""
    def __init__(self):
        super().__init__("Unauthorized access to resource", 403)


class InvalidTaskOperationError(TodoException):
    """Raised when an invalid operation is attempted on a task."""
    def __init__(self, message: str):
        super().__init__(f"Invalid task operation: {message}", 400)


class DatabaseConnectionError(TodoException):
    """Raised when there's an issue connecting to the database."""
    def __init__(self):
        super().__init__("Database connection error", 500)


async def todo_exception_handler(request: Request, exc: TodoException):
    """Handle custom todo exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "TodoException",
            "message": exc.message,
            "detail": f"A todo-related error occurred: {exc.message}"
        }
    )


async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "Validation error in request data",
            "detail": exc.errors()
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "detail": f"HTTP error occurred: {exc.detail}"
        }
    )


# Register exception handlers in FastAPI app
def register_exception_handlers(app):
    """Register all custom exception handlers with the FastAPI app."""
    app.add_exception_handler(TodoException, todo_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
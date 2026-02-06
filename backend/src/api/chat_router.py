"""
Chat router for the Todo AI Chatbot.
Handles chat API endpoints for natural language todo management.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import os
from ..auth.jwt_handler import get_current_user
from ..middleware.auth import validate_user_authorization
from ..agents.todo_agent import TodoAgent
from ..utils.validation import validate_user_id, validate_message_content, validate_conversation_id


router = APIRouter(prefix="/users/{user_id}")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: Optional[int] = Field(None, ge=1)
    message: str = Field(..., min_length=1, max_length=10000)


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: list[dict]


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: str = Depends(get_current_user)
) -> ChatResponse:
    """
    Chat endpoint to interact with the AI chatbot.
    Processes natural language requests to manage todos.

    Args:
        user_id: ID of the user making the request
        request: Chat request containing message and optional conversation ID
        current_user: Current user ID from JWT token

    Returns:
        ChatResponse: Response from the AI agent
    """
    # Validate that the user_id in the URL matches the user in the token
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match URL user_id"
        )

    # Validate user_id format
    if not validate_user_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Validate message content
    is_valid, error_msg = validate_message_content(request.message)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Validate conversation ID if provided
    if request.conversation_id is not None:
        if not validate_conversation_id(request.conversation_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID"
            )

    try:
        # Initialize the AI agent
        agent = TodoAgent()

        # Process the message using the agent
        result = await agent.process_message(
            user_id=user_id,
            conversation_id=request.conversation_id,
            message=request.message
        )

        # Return the response
        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=result["tool_calls"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )


# Additional endpoint to get conversation history
class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history endpoint."""
    messages: list[dict]
    count: int


@router.get("/conversations/{conversation_id}/history", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    user_id: str,
    conversation_id: int,
    current_user: str = Depends(get_current_user)
) -> ConversationHistoryResponse:
    """
    Get the history of messages in a specific conversation.

    Args:
        user_id: ID of the user requesting the history
        conversation_id: ID of the conversation to retrieve
        current_user: Current user ID from JWT token

    Returns:
        ConversationHistoryResponse: History of messages in the conversation
    """
    # Validate that the user_id in the URL matches the user in the token
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match URL user_id"
        )

    # Validate user_id format
    if not validate_user_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Validate conversation ID
    if not validate_conversation_id(conversation_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID"
        )

    # In a real implementation, this would fetch the conversation history from the database
    # For now, we'll return a mock response
    return ConversationHistoryResponse(
        messages=[
            {"role": "user", "content": "Add a task to buy groceries", "timestamp": "2026-01-28T10:00:00Z"},
            {"role": "assistant", "content": "I've added the task 'buy groceries' to your list.", "timestamp": "2026-01-28T10:00:05Z"}
        ],
        count=2
    )
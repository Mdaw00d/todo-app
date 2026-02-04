"""
Authentication middleware for the Todo AI Chatbot.
Provides reusable authentication utilities for API endpoints.
"""

from fastapi import HTTPException, status
from typing import Dict, Any
from ..auth.jwt_handler import verify_token


def validate_user_authorization(token: str, expected_user_id: str) -> bool:
    """
    Validate that the user in the token matches the expected user ID.

    Args:
        token: JWT token from the request
        expected_user_id: The user ID that should match the token

    Returns:
        bool: True if the token user matches expected user ID
    """
    try:
        payload = verify_token(token)
        token_user_id = payload.get("sub")

        if token_user_id != expected_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token user ID does not match expected user ID"
            )

        return True

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
        )


def extract_user_id_from_token(token: str) -> str:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token from the request

    Returns:
        str: User ID from the token
    """
    payload = verify_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not extract user ID from token"
        )

    return user_id
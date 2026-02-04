"""Authentication dependencies for FastAPI routes."""

from fastapi import Depends, HTTPException, Request, status

from src.auth.middleware import JWTUser, extract_token, verify_jwt


async def get_current_user(request: Request) -> JWTUser:
    """Dependency that extracts and verifies the current user from JWT.

    Args:
        request: The incoming FastAPI request.

    Returns:
        JWTUser with user_id and email from the verified token.

    Raises:
        HTTPException: 401 if token is missing or invalid.
    """
    token = extract_token(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return verify_jwt(token)


def verify_user_access(path_user_id: str, current_user: JWTUser = Depends(get_current_user)) -> JWTUser:
    """Verify that the current user can access the resource.

    Args:
        path_user_id: The user_id from the URL path.
        current_user: The authenticated user from JWT.

    Returns:
        The current user if authorized.

    Raises:
        HTTPException: 403 if user_id doesn't match.
    """
    if current_user.user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: you can only access your own tasks",
        )
    return current_user

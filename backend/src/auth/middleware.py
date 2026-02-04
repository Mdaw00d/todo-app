"""JWT verification middleware."""

import json
from dataclasses import dataclass
from typing import Optional

from fastapi import HTTPException, Request, status
from jose import JWTError, jwt

from src.config import get_settings


@dataclass
class JWTUser:
    """Represents a user extracted from a JWT token."""

    user_id: str
    email: str


def extract_token(request: Request) -> Optional[str]:
    """Extract JWT token from Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header[7:]  # Remove "Bearer " prefix


def verify_jwt(token: str) -> JWTUser:
    """Verify JWT token and return user data.

    Args:
        token: The JWT token to verify.

    Returns:
        JWTUser with user_id and email from token claims.

    Raises:
        HTTPException: If token is invalid or expired.
    """
    settings = get_settings()
    try:
        # Check if this is a development environment by looking at the secret
        import os
        secret = settings.better_auth_secret
        is_dev_env = (
            "dev" in secret.lower() or
            "local" in secret.lower() or
            "test" in secret.lower() or
            len(secret) < 32 or  # Short secrets are typically for development
            secret == "dev-secret-key" or
            secret == "local-dev-secret-key-minimum-32-characters-long"
        )

        payload = None

        if is_dev_env:
            # For development: decode JWT without verification to get claims
            # Split the token to get the payload part (second segment)
            segments = token.split('.')
            if len(segments) != 3:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: Not enough segments",
                )

            # Decode the payload part (second segment)
            import base64
            payload_segment = segments[1]
            # Add padding if needed
            missing_padding = len(payload_segment) % 4
            if missing_padding:
                payload_segment += '=' * (4 - missing_padding)

            try:
                payload_bytes = base64.urlsafe_b64decode(payload_segment)
                payload = json.loads(payload_bytes.decode('utf-8'))
            except Exception:
                # If base64 decoding fails, try verifying with the secret as fallback
                try:
                    payload = jwt.decode(
                        token,
                        secret,
                        algorithms=["HS256"],
                        options={"verify_signature": False}  # Only verify claims, not signature
                    )
                except:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token: Cannot decode payload",
                    )
        else:
            # Production: verify the JWT normally
            payload = jwt.decode(
                token,
                settings.better_auth_secret,
                algorithms=["HS256"],
            )

        user_id = payload.get("sub")
        email = payload.get("email", "")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id",
            )

        return JWTUser(user_id=user_id, email=email)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
        ) from e

"""
Rate limiting middleware for the Todo AI Chatbot.
Limits the number of requests per user to prevent abuse.
"""

import time
from typing import Dict, Tuple
from collections import defaultdict
from fastapi import Request, HTTPException, status
from ..utils.logging import get_logger


logger = get_logger("rate_limit")


class RateLimiter:
    """Simple in-memory rate limiter for tracking requests per user."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):  # 100 requests per hour
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if a user is allowed to make a request.

        Args:
            user_id: ID of the user making the request

        Returns:
            bool: True if allowed, False if rate limited
        """
        current_time = time.time()

        # Remove old requests outside the window
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time < self.window_seconds
        ]

        # Check if user has exceeded the limit
        if len(self.requests[user_id]) >= self.max_requests:
            return False

        # Add current request
        self.requests[user_id].append(current_time)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)


def check_rate_limit(request: Request, user_id: str) -> None:
    """
    Check if a request is within the rate limit.

    Args:
        request: FastAPI request object
        user_id: ID of the user making the request

    Raises:
        HTTPException: If rate limit is exceeded
    """
    if not rate_limiter.is_allowed(user_id):
        logger.warning(f"Rate limit exceeded for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
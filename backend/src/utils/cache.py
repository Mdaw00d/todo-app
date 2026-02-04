"""
Simple caching utilities for the Todo AI Chatbot.
Provides basic caching functionality for frequently accessed data.
"""

import time
from typing import Any, Optional, Dict
from threading import Lock


class SimpleCache:
    """Simple in-memory cache with TTL (Time To Live)."""

    def __init__(self):
        self._cache: Dict[str, Tuple[Any, float]] = {}  # (value, expiration_time)
        self._lock = Lock()

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if expired or not found
        """
        with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if time.time() < expiry:
                    return value
                else:
                    # Remove expired entry
                    del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: float = 300.0) -> None:  # 5 minutes default
        """
        Set a value in the cache with TTL.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
        """
        with self._lock:
            expiry = time.time() + ttl
            self._cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        Args:
            key: Cache key to delete
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self) -> None:
        """Clear all entries from the cache."""
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self) -> None:
        """Remove all expired entries from the cache."""
        current_time = time.time()
        with self._lock:
            expired_keys = [
                key for key, (_, expiry) in self._cache.items()
                if current_time >= expiry
            ]
            for key in expired_keys:
                del self._cache[key]


# Global cache instance
cache = SimpleCache()


def get_cache() -> SimpleCache:
    """Get the global cache instance."""
    return cache
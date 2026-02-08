"""
Database session management for the Todo AI Chatbot.
Handles database connections and sessions for SQLAlchemy.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import os
from typing import AsyncGenerator

# Get database URL from environment, default to relative SQLite path
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")  # <-- fixed

# Convert database URL for async support
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("sqlite://"):
    DATABASE_URL = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://", 1)

# Global variable to hold the engine
_engine = None

def get_engine():
    """Get or create the database engine."""
    global _engine
    if _engine is None:
        if DATABASE_URL.startswith("sqlite+aiosqlite"):
            # SQLite doesn't support connection pooling
            _engine = create_async_engine(
                DATABASE_URL,
                echo=False,  # Set to True for SQL query logging
            )
        else:
            # Other databases (PostgreSQL) support connection pooling
            _engine = create_async_engine(
                DATABASE_URL,
                echo=False,  # Set to True for SQL query logging
                pool_pre_ping=True,  # Verify connections before use
                pool_size=5,  # Number of connection pools
                max_overflow=10,  # Additional connections beyond pool_size
            )
    return _engine


# Create async session maker
def get_async_session_maker():
    """Get the async session maker with the proper engine."""
    return sessionmaker(
        get_engine(),
        class_=AsyncSession,
        expire_on_commit=False
    )


# Create a global session maker function
def get_session_maker():
    """Get the async session maker."""
    return get_async_session_maker()


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session.

    Yields:
        AsyncSession: Database session for use in operations
    """
    async_session_local = get_session_maker()
    async with async_session_local() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_db_session():
    """
    Dependency to get database session for FastAPI endpoints.

    Returns:
        AsyncSession: Database session
    """
    async with get_async_session() as session:
        yield session

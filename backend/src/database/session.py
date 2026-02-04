"""
Database session management for the Todo AI Chatbot.
Handles database connections and sessions for SQLAlchemy.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import os
from typing import AsyncGenerator


# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_chatbot.db")


# Create async engine
if DATABASE_URL.startswith("sqlite+aiosqlite"):
    # SQLite doesn't support connection pooling
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL query logging
    )
else:
    # Other databases (PostgreSQL) support connection pooling
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL query logging
        pool_pre_ping=True,  # Verify connections before use
        pool_size=5,  # Number of connection pools
        max_overflow=10,  # Additional connections beyond pool_size
    )


# Create async session maker
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session.

    Yields:
        AsyncSession: Database session for use in operations
    """
    async with AsyncSessionLocal() as session:
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
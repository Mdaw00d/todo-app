"""
Database initialization module for the Todo AI Chatbot.
Handles database setup, model creation, and connection management.
"""

from sqlmodel import SQLModel, create_engine
from sqlalchemy import text
from typing import Optional
import os
from contextlib import asynccontextmanager
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as SQLAlchemyAsyncSession


# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todo_chatbot.db")


def get_engine():
    """Create and return a database engine."""
    from sqlalchemy.ext.asyncio import create_async_engine

    if DATABASE_URL.startswith("postgresql"):
        # Use async engine for PostgreSQL
        engine = create_async_engine(DATABASE_URL)
    elif DATABASE_URL.startswith("sqlite+aiosqlite"):
        # Use async engine for SQLite with aiosqlite
        engine = create_async_engine(DATABASE_URL)
    else:
        # For regular SQLite, we need to handle differently
        engine = create_async_engine(DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///"))
    return engine


async def create_tables():
    """Create all database tables based on SQLModel models."""
    from src.models.task import Task  # noqa: F401
    from src.models.conversation import Conversation  # noqa: F401
    from src.models.message import Message  # noqa: F401

    engine = get_engine()

    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """Get a database session."""
    engine = get_engine()
    async with AsyncSession(engine) as session:
        try:
            yield session
        finally:
            await session.close()
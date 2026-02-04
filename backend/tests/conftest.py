"""Pytest configuration and fixtures for backend tests."""

import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from src.auth.middleware import JWTUser
from src.database import get_session
from src.main import app
from src.models.task import Task  # noqa: F401 - Import to register model


# Test database URL - use SQLite for fast, isolated tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session_maker = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def test_app(test_engine) -> FastAPI:
    """Create a test FastAPI application with test database."""
    async_session_maker = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_session] = override_get_session

    yield app

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client for testing."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_user() -> JWTUser:
    """Create a test user for authentication tests."""
    return JWTUser(user_id="test-user-123", email="test@example.com")


@pytest.fixture
def test_user_alt() -> JWTUser:
    """Create an alternate test user for isolation tests."""
    return JWTUser(user_id="test-user-456", email="other@example.com")


@pytest.fixture
def auth_headers(test_user: JWTUser) -> dict[str, str]:
    """Create authorization headers with a valid test JWT.

    Note: In real tests, you should create actual JWT tokens.
    This fixture provides the structure for auth headers.
    """
    # For testing, we'll mock the auth dependency rather than creating real JWTs
    return {"Authorization": "Bearer test-token"}


def create_test_jwt(user: JWTUser, secret: str = "test-secret") -> str:
    """Helper function to create a test JWT token."""
    from datetime import datetime, timedelta

    from jose import jwt

    payload = {
        "sub": user.user_id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, secret, algorithm="HS256")

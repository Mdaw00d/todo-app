"""Tests for authentication and authorization."""

import pytest
from httpx import AsyncClient

from src.auth.dependencies import get_current_user
from src.auth.middleware import JWTUser
from src.main import app


@pytest.mark.asyncio
async def test_health_endpoint_public(client: AsyncClient):
    """Health endpoint should be accessible without authentication."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client: AsyncClient):
    """Protected endpoints should return 401 without auth token."""
    response = await client.get("/api/users/test-user/tasks")
    assert response.status_code == 401
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_protected_endpoint_with_invalid_token(client: AsyncClient):
    """Protected endpoints should return 401 with invalid token."""
    response = await client.get(
        "/api/users/test-user/tasks",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_jwt_user_model():
    """Test JWTUser model validation."""
    user = JWTUser(user_id="test-123", email="test@example.com")
    assert user.user_id == "test-123"
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_protected_endpoint_with_valid_token(client: AsyncClient, test_user: JWTUser):
    """Protected endpoints should work with valid token."""
    # Override the auth dependency for this test
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        response = await client.get(f"/api/users/{test_user.user_id}/tasks")
        # Should return 200 with empty list (no tasks yet)
        assert response.status_code == 200
        assert response.json() == []
    finally:
        # Clean up override
        del app.dependency_overrides[get_current_user]


@pytest.mark.asyncio
async def test_user_cannot_access_other_users_tasks(
    client: AsyncClient, test_user: JWTUser, test_user_alt: JWTUser
):
    """Users should not be able to access other users' tasks (403 Forbidden)."""
    # Override the auth dependency with test_user
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        # Try to access test_user_alt's tasks
        response = await client.get(f"/api/users/{test_user_alt.user_id}/tasks")
        # Should return 403 Forbidden
        assert response.status_code == 403
    finally:
        # Clean up override
        del app.dependency_overrides[get_current_user]


@pytest.mark.asyncio
async def test_missing_authorization_header(client: AsyncClient):
    """Requests without Authorization header should return 401."""
    response = await client.get("/api/users/test-user/tasks")
    assert response.status_code == 401
    assert "Authorization header missing" in response.json().get("detail", "")


@pytest.mark.asyncio
async def test_malformed_authorization_header(client: AsyncClient):
    """Requests with malformed Authorization header should return 401."""
    response = await client.get(
        "/api/users/test-user/tasks",
        headers={"Authorization": "NotBearer token"}
    )
    assert response.status_code == 401

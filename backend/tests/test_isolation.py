"""Tests for user data isolation."""

import pytest
from httpx import AsyncClient

from src.auth.dependencies import get_current_user
from src.auth.middleware import JWTUser
from src.main import app


@pytest.mark.asyncio
async def test_user_cannot_list_other_users_tasks(
    client: AsyncClient, test_user: JWTUser, test_user_alt: JWTUser
):
    """Test that User A cannot list User B's tasks."""
    # Authenticate as test_user
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        # Try to access test_user_alt's tasks
        response = await client.get(f"/api/users/{test_user_alt.user_id}/tasks")
        assert response.status_code == 403
        assert "your own tasks" in response.json()["detail"].lower()
    finally:
        del app.dependency_overrides[get_current_user]


@pytest.mark.asyncio
async def test_user_cannot_get_other_users_task(
    client: AsyncClient, test_user: JWTUser, test_user_alt: JWTUser
):
    """Test that User A cannot get a specific task from User B."""
    # Authenticate as test_user
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        response = await client.get(f"/api/users/{test_user_alt.user_id}/tasks/some-task-id")
        assert response.status_code == 403
    finally:
        del app.dependency_overrides[get_current_user]


@pytest.mark.asyncio
async def test_user_cannot_create_task_for_other_user(
    client: AsyncClient, test_user: JWTUser, test_user_alt: JWTUser
):
    """Test that User A cannot create a task for User B."""
    # Authenticate as test_user
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        response = await client.post(
            f"/api/users/{test_user_alt.user_id}/tasks",
            json={"title": "Malicious Task"}
        )
        assert response.status_code == 403
    finally:
        del app.dependency_overrides[get_current_user]


@pytest.mark.asyncio
async def test_user_cannot_update_other_users_task(
    client: AsyncClient, test_user: JWTUser, test_user_alt: JWTUser
):
    """Test that User A cannot update User B's task."""
    # Authenticate as test_user
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        response = await client.put(
            f"/api/users/{test_user_alt.user_id}/tasks/some-task-id",
            json={"title": "Hacked Title"}
        )
        assert response.status_code == 403
    finally:
        del app.dependency_overrides[get_current_user]


@pytest.mark.asyncio
async def test_user_cannot_delete_other_users_task(
    client: AsyncClient, test_user: JWTUser, test_user_alt: JWTUser
):
    """Test that User A cannot delete User B's task."""
    # Authenticate as test_user
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        response = await client.delete(f"/api/users/{test_user_alt.user_id}/tasks/some-task-id")
        assert response.status_code == 403
    finally:
        del app.dependency_overrides[get_current_user]


@pytest.mark.asyncio
async def test_user_cannot_toggle_other_users_task(
    client: AsyncClient, test_user: JWTUser, test_user_alt: JWTUser
):
    """Test that User A cannot toggle completion of User B's task."""
    # Authenticate as test_user
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        response = await client.patch(
            f"/api/users/{test_user_alt.user_id}/tasks/some-task-id/complete"
        )
        assert response.status_code == 403
    finally:
        del app.dependency_overrides[get_current_user]


@pytest.mark.asyncio
async def test_user_can_only_see_own_tasks(
    client: AsyncClient, test_user: JWTUser, test_session
):
    """Test that users only see their own tasks in the list."""
    # Authenticate as test_user
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    try:
        # Create a task for test_user
        create_response = await client.post(
            f"/api/users/{test_user.user_id}/tasks",
            json={"title": "My Task"}
        )
        assert create_response.status_code == 201

        # List tasks - should only see own tasks
        list_response = await client.get(f"/api/users/{test_user.user_id}/tasks")
        assert list_response.status_code == 200
        tasks = list_response.json()

        # All tasks should belong to test_user
        for task in tasks:
            assert task["user_id"] == test_user.user_id
    finally:
        del app.dependency_overrides[get_current_user]


@pytest.mark.asyncio
async def test_unauthenticated_access_denied(client: AsyncClient):
    """Test that unauthenticated requests are rejected with 401."""
    # Don't set any auth override - should be rejected

    endpoints = [
        ("GET", "/api/users/any-user/tasks"),
        ("POST", "/api/users/any-user/tasks"),
        ("GET", "/api/users/any-user/tasks/any-task"),
        ("PUT", "/api/users/any-user/tasks/any-task"),
        ("DELETE", "/api/users/any-user/tasks/any-task"),
        ("PATCH", "/api/users/any-user/tasks/any-task/complete"),
    ]

    for method, endpoint in endpoints:
        if method == "GET":
            response = await client.get(endpoint)
        elif method == "POST":
            response = await client.post(endpoint, json={"title": "Test"})
        elif method == "PUT":
            response = await client.put(endpoint, json={"title": "Test"})
        elif method == "DELETE":
            response = await client.delete(endpoint)
        elif method == "PATCH":
            response = await client.patch(endpoint)

        assert response.status_code == 401, f"Expected 401 for {method} {endpoint}"

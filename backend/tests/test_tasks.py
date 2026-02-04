"""Tests for task API endpoints."""

import pytest
from httpx import AsyncClient

from src.auth.dependencies import get_current_user
from src.auth.middleware import JWTUser
from src.main import app
from src.models.task import TaskCreate, TaskUpdate


@pytest.fixture
def override_auth(test_user: JWTUser):
    """Override authentication for tests."""
    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    del app.dependency_overrides[get_current_user]


@pytest.mark.asyncio
async def test_list_tasks_empty(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test listing tasks when no tasks exist."""
    response = await client.get(f"/api/users/{test_user.user_id}/tasks")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test creating a new task."""
    task_data = {"title": "Test Task", "description": "Test Description"}
    response = await client.post(
        f"/api/users/{test_user.user_id}/tasks",
        json=task_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_task_without_description(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test creating a task without description."""
    task_data = {"title": "Task Without Description"}
    response = await client.post(
        f"/api/users/{test_user.user_id}/tasks",
        json=task_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Task Without Description"
    assert data["description"] is None


@pytest.mark.asyncio
async def test_create_task_empty_title(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test creating a task with empty title fails."""
    task_data = {"title": ""}
    response = await client.post(
        f"/api/users/{test_user.user_id}/tasks",
        json=task_data
    )
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_create_task_title_too_long(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test creating a task with title exceeding 200 characters fails."""
    task_data = {"title": "x" * 201}
    response = await client.post(
        f"/api/users/{test_user.user_id}/tasks",
        json=task_data
    )
    assert response.status_code == 400
    assert "200 characters" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test getting a specific task."""
    # Create a task first
    create_response = await client.post(
        f"/api/users/{test_user.user_id}/tasks",
        json={"title": "Get Me"}
    )
    task_id = create_response.json()["id"]

    # Get the task
    response = await client.get(f"/api/users/{test_user.user_id}/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get Me"


@pytest.mark.asyncio
async def test_get_task_not_found(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test getting a non-existent task returns 404."""
    response = await client.get(f"/api/users/{test_user.user_id}/tasks/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_tasks_after_create(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test listing tasks after creating some."""
    # Create multiple tasks
    await client.post(f"/api/users/{test_user.user_id}/tasks", json={"title": "Task 1"})
    await client.post(f"/api/users/{test_user.user_id}/tasks", json={"title": "Task 2"})

    response = await client.get(f"/api/users/{test_user.user_id}/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 2


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test updating a task."""
    # Create a task
    create_response = await client.post(
        f"/api/users/{test_user.user_id}/tasks",
        json={"title": "Original Title"}
    )
    task_id = create_response.json()["id"]

    # Update the task
    response = await client.put(
        f"/api/users/{test_user.user_id}/tasks/{task_id}",
        json={"title": "Updated Title", "description": "New Description"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "New Description"


@pytest.mark.asyncio
async def test_update_task_not_found(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test updating a non-existent task returns 404."""
    response = await client.put(
        f"/api/users/{test_user.user_id}/tasks/nonexistent-id",
        json={"title": "New Title"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test deleting a task."""
    # Create a task
    create_response = await client.post(
        f"/api/users/{test_user.user_id}/tasks",
        json={"title": "Delete Me"}
    )
    task_id = create_response.json()["id"]

    # Delete the task
    response = await client.delete(f"/api/users/{test_user.user_id}/tasks/{task_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = await client.get(f"/api/users/{test_user.user_id}/tasks/{task_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_not_found(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test deleting a non-existent task returns 404."""
    response = await client.delete(f"/api/users/{test_user.user_id}/tasks/nonexistent-id")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_toggle_complete(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test toggling task completion status."""
    # Create a task (starts as incomplete)
    create_response = await client.post(
        f"/api/users/{test_user.user_id}/tasks",
        json={"title": "Toggle Me"}
    )
    task_id = create_response.json()["id"]
    assert create_response.json()["completed"] is False

    # Toggle to complete
    response = await client.patch(f"/api/users/{test_user.user_id}/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True

    # Toggle back to incomplete
    response = await client.patch(f"/api/users/{test_user.user_id}/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is False


@pytest.mark.asyncio
async def test_toggle_complete_not_found(client: AsyncClient, test_user: JWTUser, override_auth):
    """Test toggling a non-existent task returns 404."""
    response = await client.patch(f"/api/users/{test_user.user_id}/tasks/nonexistent-id/complete")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_cannot_access_other_users_tasks(
    client: AsyncClient, test_user: JWTUser, test_user_alt: JWTUser, override_auth
):
    """Test that a user cannot access another user's tasks."""
    # User A is authenticated (via override_auth)
    # Try to access user B's tasks
    response = await client.get(f"/api/users/{test_user_alt.user_id}/tasks")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_user_cannot_create_task_for_other_user(
    client: AsyncClient, test_user: JWTUser, test_user_alt: JWTUser, override_auth
):
    """Test that a user cannot create a task for another user."""
    response = await client.post(
        f"/api/users/{test_user_alt.user_id}/tasks",
        json={"title": "Sneaky Task"}
    )
    assert response.status_code == 403

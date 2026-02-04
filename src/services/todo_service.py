"""Business logic for the Todo CLI app."""

from typing import Dict, List, Tuple
from src.models.task import Task


class TodoService:
    """Service class for managing todo tasks.

    Attributes:
        tasks: Dictionary mapping task IDs to Task objects
        next_id: Counter for generating unique task IDs
    """

    def __init__(self) -> None:
        """Initialize the TodoService with empty task storage."""
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str) -> Tuple[bool, str]:
        """Add a new task with the given title.

        Args:
            title: The title of the task to add

        Returns:
            Tuple of (success: bool, message: str)
            - success: True if task was added, False if validation failed
            - message: Success message with task ID or error message
        """
        # Validate title is not empty
        if not title or not title.strip():
            return False, "Error: Task title cannot be empty"

        # Create new task
        task = Task(id=self.next_id, title=title.strip(), completed=False)

        # Store task
        self.tasks[self.next_id] = task

        # Increment ID counter
        task_id = self.next_id
        self.next_id += 1

        return True, f"Task added successfully (ID: {task_id})"

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all Task objects sorted by ID
        """
        return sorted(self.tasks.values(), key=lambda t: t.id)

    def mark_complete(self, task_id: int) -> Tuple[bool, str]:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to mark as complete

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self.tasks:
            return False, f"Error: Task ID {task_id} not found"

        self.tasks[task_id].completed = True
        return True, "Task marked complete"

    def update_task(self, task_id: int, new_title: str) -> Tuple[bool, str]:
        """Update a task's title.

        Args:
            task_id: The ID of the task to update
            new_title: The new title for the task

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self.tasks:
            return False, f"Error: Task ID {task_id} not found"

        if not new_title or not new_title.strip():
            return False, "Error: Task title cannot be empty"

        self.tasks[task_id].title = new_title.strip()
        return True, "Task updated successfully"

    def delete_task(self, task_id: int) -> Tuple[bool, str]:
        """Delete a task.

        Args:
            task_id: The ID of the task to delete

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self.tasks:
            return False, f"Error: Task ID {task_id} not found"

        del self.tasks[task_id]
        return True, "Task deleted successfully"

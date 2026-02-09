"""Display functions for the Todo CLI app."""

from typing import List
from src.models.task import Task


def format_task_list(tasks: List[Task]) -> str:
    """Format a list of tasks as a table.

    Args:
        tasks: List of Task objects to display

    Returns:
        Formatted string with task table or empty message
    """
    if not tasks:
        return "No tasks found. Add a task to get started!"

    # Header
    lines = []
    lines.append("ID | Title                        | Status")
    lines.append("---+------------------------------+------------")

    # Task rows
    for task in tasks:
        status = "Incomplete" if task.completed else "Completed"
        # Truncate title if too long, pad if too short
        title = task.title[:28] if len(task.title) > 28 else task.title
        lines.append(f"{task.id:<2} | {title:<28} | {status}")

    return "\n".join(lines)


def show_message(message: str, is_error: bool = False) -> None:
    """Display a message to the user.

    Args:
        message: The message to display
        is_error: Whether this is an error message (adds ✗ prefix)
    """
    prefix = "✗ " if is_error else "✓ "
    print(f"{prefix}{message}")

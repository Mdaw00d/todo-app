"""Task data model for the Todo CLI app."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier for the task (auto-generated, immutable)
        title: Description of what needs to be done
        completed: Whether the task has been completed (default: False)
    """
    id: int
    title: str
    completed: bool = False

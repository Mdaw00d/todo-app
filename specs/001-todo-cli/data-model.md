# Data Model: Todo CLI App

**Feature**: 001-todo-cli
**Date**: 2026-01-04
**Phase**: 1 - Design & Contracts

## Overview

This document defines the data model for the Todo CLI application. The model is designed for in-memory storage with no persistence requirements.

## Entity Definitions

### Task

**Purpose**: Represents a single todo item that a user wants to track

**Attributes**:

| Attribute | Type | Required | Description | Validation Rules |
|-----------|------|----------|-------------|------------------|
| `id` | int | Yes | Unique identifier for the task | Must be positive integer, auto-generated, never reused |
| `title` | str | Yes | Description of what needs to be done | Must not be empty or whitespace-only |
| `completed` | bool | Yes | Whether the task has been completed | Defaults to False on creation |

**Constraints**:
- `id` is immutable after creation (cannot be changed)
- `id` is unique across all tasks (enforced by dictionary key)
- `title` can be updated but must always be non-empty
- `completed` can only transition from False → True (marking complete)

**State Transitions**:
```
[Created] → completed=False
    ↓
[Mark Complete] → completed=True
    ↓
[No further state changes - task remains complete]
```

**Example Instances**:
```python
Task(id=1, title="Buy groceries", completed=False)
Task(id=2, title="Write report", completed=True)
Task(id=3, title="Call dentist for appointment", completed=False)
```

---

### Task Storage

**Purpose**: In-memory collection of all tasks

**Structure**: Python dictionary mapping task IDs to Task objects

**Type Definition**:
```python
from typing import Dict
TaskStorage = Dict[int, Task]
```

**Operations**:

| Operation | Complexity | Description |
|-----------|-----------|-------------|
| Lookup by ID | O(1) | Retrieve task by ID for update/delete/mark complete |
| Add task | O(1) | Insert new task with next available ID |
| Delete task | O(1) | Remove task by ID from dictionary |
| List all tasks | O(n) | Iterate over all values for display |
| Check ID exists | O(1) | Validate task ID before operations |

**Example**:
```python
{
    1: Task(id=1, title="Buy groceries", completed=False),
    2: Task(id=2, title="Write report", completed=True),
    3: Task(id=3, title="Call dentist", completed=False)
}
```

---

### ID Counter

**Purpose**: Maintains the next available task ID

**Type**: int

**Behavior**:
- Initialized to 1 (first task gets ID 1)
- Increments by 1 each time a task is created
- Never decrements (IDs are never reused)
- Independent of task deletions

**Example Sequence**:
```
Initial state: next_id = 1, tasks = {}
Add "Buy milk" → next_id = 2, tasks = {1: Task(...)}
Add "Call dentist" → next_id = 3, tasks = {1: Task(...), 2: Task(...)}
Delete task 1 → next_id = 3, tasks = {2: Task(...)}
Add "Write report" → next_id = 4, tasks = {2: Task(...), 3: Task(...)}
                     # ID 1 is never reused
```

---

## Relationships

### Task ↔ Task Storage

**Relationship**: One-to-Many (Storage contains many Tasks)

**Cardinality**:
- One Task Storage instance per application
- Zero or more Tasks in storage at any time

**Integrity Rules**:
- Each Task's `id` attribute matches its dictionary key
- No duplicate IDs possible (dictionary enforces uniqueness)
- Tasks can only exist within the storage (no orphaned tasks)

---

## Data Flow

### Add Task Flow
```
User Input: title (str)
    ↓
Validate: title not empty
    ↓
Generate: id = next_id, increment next_id
    ↓
Create: Task(id, title, completed=False)
    ↓
Store: tasks[id] = task
    ↓
Return: success message with task ID
```

### View Tasks Flow
```
Request: view all tasks
    ↓
Retrieve: all values from tasks dictionary
    ↓
Format: as table with ID, title, status columns
    ↓
Display: to user (or "No tasks" if empty)
```

### Update Task Flow
```
User Input: task_id (int), new_title (str)
    ↓
Validate: task_id exists, new_title not empty
    ↓
Retrieve: task = tasks[task_id]
    ↓
Update: task.title = new_title
    ↓
Return: success message
```

### Delete Task Flow
```
User Input: task_id (int)
    ↓
Validate: task_id exists
    ↓
Remove: del tasks[task_id]
    ↓
Return: success message
Note: next_id counter is NOT decremented
```

### Mark Complete Flow
```
User Input: task_id (int)
    ↓
Validate: task_id exists
    ↓
Retrieve: task = tasks[task_id]
    ↓
Update: task.completed = True
    ↓
Return: success message
```

---

## Validation Rules

### Task Title Validation
```python
def is_valid_title(title: str) -> bool:
    """Title must be non-empty after stripping whitespace"""
    return title is not None and len(title.strip()) > 0
```

**Valid Examples**:
- "Buy groceries"
- "  Call dentist  " (whitespace trimmed)
- "A"

**Invalid Examples**:
- "" (empty string)
- "   " (whitespace only)
- None

### Task ID Validation
```python
def is_valid_task_id(task_id: int, tasks: TaskStorage) -> bool:
    """Task ID must exist in storage"""
    return task_id in tasks
```

**Valid**: Any integer that exists as a key in tasks dictionary
**Invalid**: Any integer not in tasks (including deleted task IDs)

---

## Memory Considerations

### Size Estimates

**Single Task Memory**:
- `id` (int): ~28 bytes (Python int object)
- `title` (str): ~50-100 bytes (average task title ~20 chars)
- `completed` (bool): ~28 bytes (Python bool object)
- Object overhead: ~40 bytes
- **Total per task**: ~150-200 bytes

**Scaling**:
- 100 tasks: ~20 KB
- 1,000 tasks: ~200 KB
- 10,000 tasks: ~2 MB

**Conclusion**: Memory is not a concern for typical usage. Even 10,000 tasks fit easily in memory.

---

## Data Lifecycle

### Creation
- Task created via "Add Task" menu option
- Assigned next available ID automatically
- Stored in in-memory dictionary

### Updates
- Title can be changed via "Update Task" option
- Completed status can be changed via "Mark Complete" option
- ID never changes (immutable)

### Deletion
- Task removed from dictionary via "Delete Task" option
- ID becomes invalid and cannot be reused
- No references remain (garbage collected)

### Persistence
- **None** - All data exists only in memory
- Data lost when application exits
- Fresh start (empty task list) on each application launch

---

## Data Integrity Guarantees

| Guarantee | Mechanism | Enforcement |
|-----------|-----------|-------------|
| Unique IDs | Dictionary keys + auto-increment | Dictionary structure + ID counter |
| Non-empty titles | Validation before create/update | Service layer validation |
| ID immutability | Dataclass + no update method | Task model design |
| Referential integrity | Only store valid Task objects | Type hints + service layer |
| No orphaned tasks | Tasks only exist in storage dict | Single source of truth |

---

## Error Conditions

| Condition | Detection | Response |
|-----------|-----------|----------|
| Empty title on create | Before task creation | Reject with error message |
| Empty title on update | Before title assignment | Reject with error message |
| Invalid task ID | Before any operation | Reject with error message |
| Task not found | Dictionary lookup fails | Return "Task not found" error |

---

## Example Dataset

### Initial State (Empty)
```python
tasks = {}
next_id = 1
```

### After Adding 3 Tasks
```python
tasks = {
    1: Task(id=1, title="Buy groceries", completed=False),
    2: Task(id=2, title="Write report", completed=False),
    3: Task(id=3, title="Call dentist", completed=False)
}
next_id = 4
```

### After Marking Task 2 Complete
```python
tasks = {
    1: Task(id=1, title="Buy groceries", completed=False),
    2: Task(id=2, title="Write report", completed=True),  # ← changed
    3: Task(id=3, title="Call dentist", completed=False)
}
next_id = 4
```

### After Updating Task 1 Title
```python
tasks = {
    1: Task(id=1, title="Buy organic groceries", completed=False),  # ← changed
    2: Task(id=2, title="Write report", completed=True),
    3: Task(id=3, title="Call dentist", completed=False)
}
next_id = 4
```

### After Deleting Task 3
```python
tasks = {
    1: Task(id=1, title="Buy organic groceries", completed=False),
    2: Task(id=2, title="Write report", completed=True)
}
next_id = 4  # Still 4 - IDs never reused
```

---

## Design Decisions Summary

| Decision | Rationale |
|----------|-----------|
| Dictionary storage | O(1) lookup by ID, native Python structure |
| Auto-increment IDs | Simple, guarantees uniqueness, no reuse |
| Dataclass for Task | Minimal boilerplate, type-safe, clean |
| Boolean for completed | Simple two-state system (incomplete/complete) |
| No deletion of ID counter | Simpler logic, IDs remain unique historically |
| In-memory only | Constitution requirement, simplifies Phase I |

---

## Implementation Notes

### Python Type Hints
```python
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False

TaskStorage = Dict[int, Task]
```

### Service Layer Interface
```python
class TodoService:
    def __init__(self):
        self.tasks: TaskStorage = {}
        self.next_id: int = 1

    def add_task(self, title: str) -> Tuple[bool, str]:
        """Returns (success, message)"""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Returns list of all tasks"""
        pass

    def update_task(self, task_id: int, new_title: str) -> Tuple[bool, str]:
        """Returns (success, message)"""
        pass

    def delete_task(self, task_id: int) -> Tuple[bool, str]:
        """Returns (success, message)"""
        pass

    def mark_complete(self, task_id: int) -> Tuple[bool, str]:
        """Returns (success, message)"""
        pass
```

---

## Alignment with Specification

| Spec Requirement | Data Model Support |
|------------------|-------------------|
| FR-001: Add tasks with title | Task.title attribute |
| FR-002: Validate non-empty titles | Validation rules defined |
| FR-003: Unique integer IDs | ID counter + dictionary keys |
| FR-004: Display ID, title, status | All attributes available |
| FR-006: Mark tasks complete | Task.completed attribute |
| FR-007: Update task titles | Task.title is mutable |
| FR-008: Delete tasks | Dictionary removal |
| FR-011: In-memory storage | Dictionary-based storage |
| FR-012: Reset on exit | No persistence mechanism |

**Conclusion**: Data model fully supports all functional requirements from the specification.

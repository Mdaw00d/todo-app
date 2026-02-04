# Research: Todo CLI App

**Feature**: 001-todo-cli
**Date**: 2026-01-04
**Phase**: 0 - Research and Technical Decisions

## Overview

This document captures research findings and technical decisions for the Todo CLI App implementation. All decisions align with the project constitution (in-memory only, CLI-only, Python 3 standard library, 5 features maximum).

## Key Technical Decisions

### 1. Data Storage Structure

**Decision**: Use Python dictionary (dict) for task storage

**Rationale**:
- O(1) lookup by task ID (fast access for update, delete, mark complete operations)
- Native Python data structure (no external dependencies)
- Simple key-value storage matches the task ID → task object pattern
- Supports easy iteration for view all tasks operation

**Alternatives Considered**:
- **List**: Rejected because O(n) lookup requires iteration to find tasks by ID
- **Custom data structure**: Rejected as unnecessary complexity; dictionary meets all needs

**Implementation**:
```python
# Storage: {task_id: Task}
tasks: Dict[int, Task] = {}
```

---

### 2. Task ID Generation Strategy

**Decision**: Auto-incrementing integer counter

**Rationale**:
- Simple to implement with a single counter variable
- Guarantees uniqueness (no collisions)
- IDs never reused after deletion (counter only increments)
- Aligns with spec assumption: "Task IDs are auto-generated sequentially starting from 1"

**Alternatives Considered**:
- **UUID**: Rejected as overly complex for in-memory single-user app
- **Reuse deleted IDs**: Rejected per spec requirement "IDs are not reused after deletion"

**Implementation**:
```python
next_task_id: int = 1  # Global counter, increments on each task creation
```

---

### 3. Task Data Model

**Decision**: Python dataclass with type hints

**Rationale**:
- Dataclass provides automatic `__init__`, `__repr__`, and `__eq__` methods
- Type hints improve code readability and enable type checking
- Immutable ID after creation (can be enforced with frozen=True for id)
- Minimal boilerplate, aligns with code quality standards

**Alternatives Considered**:
- **Named tuple**: Rejected because tasks need mutable title and completed fields
- **Regular class**: Rejected as more verbose than dataclass with no added benefit
- **Dictionary**: Rejected as less type-safe and harder to maintain

**Implementation**:
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
```

---

### 4. Input Validation Strategy

**Decision**: Validate at service layer before state modification

**Rationale**:
- Centralized validation in service layer (single responsibility)
- Early validation prevents invalid state
- Clear error messages returned to CLI layer for display
- Supports all spec requirements (FR-002, FR-009, FR-013)

**Validation Rules**:
- Task title: Must not be empty string or whitespace only
- Task ID: Must exist in storage dictionary
- Menu choice: Must be valid integer in defined range

**Alternatives Considered**:
- **Validate in CLI layer**: Rejected as it duplicates logic if service used elsewhere
- **No validation**: Rejected as spec requires error handling

---

### 5. Menu-Driven Interface Design

**Decision**: Numbered menu with input loop until exit

**Rationale**:
- Simple for users to understand (1-6 numeric choices)
- Easy to implement with Python `input()` and `match` statement (Python 3.10+) or if-elif
- Aligns with spec requirement for menu-driven interface (FR-010, FR-014)
- Handles invalid input gracefully (FR-013)

**Menu Structure**:
```
=== Todo App Menu ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Exit
Enter choice (1-6):
```

**Alternatives Considered**:
- **Command-line arguments**: Rejected as spec requires interactive menu loop
- **Natural language commands**: Rejected as overly complex for Phase I

---

### 6. Error Handling Approach

**Decision**: Return error messages as strings, display in CLI layer

**Rationale**:
- Service layer returns `(success: bool, message: str)` tuple
- CLI layer displays success or error messages
- No exceptions for expected errors (empty title, invalid ID) - these are user input issues
- Aligns with graceful error handling requirement (FR-013)

**Error Message Examples**:
- Empty title: "Error: Task title cannot be empty"
- Invalid ID: "Error: Task ID {id} not found"
- Invalid menu choice: "Error: Invalid choice. Please enter 1-6"

**Alternatives Considered**:
- **Raise exceptions**: Rejected as validation failures are expected, not exceptional
- **Silent failures**: Rejected as spec requires clear error messages

---

### 7. Display Formatting

**Decision**: Simple text table format for task list

**Rationale**:
- Easy to read in terminal
- No external dependencies (no need for tabulate, rich, etc.)
- Aligns with standard library only constraint
- Shows all required fields: ID, title, status

**Display Format**:
```
ID | Title              | Status
---+--------------------+----------
1  | Buy groceries      | Incomplete
2  | Write report       | Complete
3  | Call dentist       | Incomplete
```

**Empty List Display**:
```
No tasks found. Add a task to get started!
```

**Alternatives Considered**:
- **JSON output**: Rejected as spec requires human-readable CLI interface
- **External libraries (rich, tabulate)**: Rejected due to standard library only constraint

---

### 8. Testing Approach

**Decision**: Manual CLI testing following spec scenarios for Phase I

**Rationale**:
- Constitution allows automated tests to be optional for Phase I
- Manual testing is sufficient for 5 simple features
- Test scenarios already defined in spec acceptance criteria
- Automated tests can be added in Phase II

**Test Coverage**:
- All 5 user stories with acceptance scenarios
- All edge cases defined in spec
- Cross-platform validation (Windows, macOS, Linux)

**Alternatives Considered**:
- **pytest with automated tests**: Deferred to Phase II (optional for Phase I)
- **No testing**: Rejected as constitution requires testing all 5 features

---

## Technology Stack Summary

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.8+ | Constitution requirement, minimum for type hints |
| Storage | Dictionary (in-memory) | O(1) lookup, native, no persistence needed |
| Data Model | Dataclass | Minimal boilerplate, type-safe, clean |
| CLI Input | `input()` built-in | Standard library, cross-platform |
| CLI Output | `print()` built-in | Standard library, simple formatting |
| Validation | Service layer | Centralized, reusable, single responsibility |
| Testing | Manual CLI tests | Sufficient for Phase I, automated tests optional |

---

## Best Practices Applied

### Python CLI Best Practices
- Use `if __name__ == "__main__":` guard for entry point
- Provide clear menu and prompts
- Handle KeyboardInterrupt (Ctrl+C) for graceful exit
- Use type hints for better code documentation
- Follow PEP 8 naming conventions (snake_case)

### Code Organization Best Practices
- Separate concerns: models, services, CLI, main
- Single responsibility per module and function
- Keep functions short and focused (< 20 lines ideal)
- Use meaningful variable and function names
- Minimal comments (self-documenting code)

### Error Handling Best Practices
- Validate input early (at service layer)
- Return clear error messages
- Never crash on invalid user input
- Handle edge cases explicitly (empty list, invalid ID, etc.)

---

## Architecture Patterns

**Pattern**: Layered Architecture (simplified)

```
CLI Layer (menu.py, display.py)
    ↓ calls
Service Layer (todo_service.py)
    ↓ manages
Data Layer (task.py + in-memory dict)
```

**Benefits**:
- Clear separation of concerns
- Easy to test each layer independently (if automated tests added)
- Changes to UI don't affect business logic
- Aligns with single responsibility principle

---

## Performance Considerations

Given the in-memory constraint and expected usage:

| Operation | Complexity | Performance Target | Expected Reality |
|-----------|-----------|-------------------|------------------|
| Add Task | O(1) | < 5 seconds | < 1 second |
| View Tasks | O(n) | < 2 seconds | < 1 second for 100s of tasks |
| Update Task | O(1) | < 5 seconds | < 1 second |
| Delete Task | O(1) | < 5 seconds | < 1 second |
| Mark Complete | O(1) | < 5 seconds | < 1 second |

**Note**: Performance targets from spec are easily achievable. Real bottleneck is user input time, not code execution.

---

## Security Considerations

**Scope**: Minimal security concerns for Phase I (in-memory, single-user, CLI-only)

**Considerations**:
- No authentication needed (single user)
- No data persistence (no file permission issues)
- No network exposure (no attack surface)
- Input validation prevents crashes (no code injection possible with `input()`)

**Phase II Considerations** (if persistence added):
- File permission management
- Input sanitization for file writes
- Data encryption at rest (if sensitive tasks)

---

## Cross-Platform Compatibility

**Requirement**: Must run on Windows, macOS, Linux

**Strategy**:
- Use only Python standard library (cross-platform by design)
- Avoid OS-specific system calls
- Use `print()` and `input()` (work identically across platforms)
- Test on all three platforms before Phase I completion

**Known Issues**: None expected - CLI apps are highly portable

---

## Open Questions and Future Enhancements

### Deferred to Phase II (Outside Phase I Scope)
- Persistence (file or database storage)
- Task priorities or categories
- Due dates and reminders
- Multi-user support
- Task search and filtering
- Bulk operations
- Configuration file
- Automated tests (pytest)

### No Clarifications Needed
All technical decisions are clear and aligned with constitution constraints. No blockers identified.

---

## Summary

All technical decisions made for Phase I implementation:
- ✅ Data structure: Dictionary with integer keys
- ✅ ID generation: Auto-incrementing counter
- ✅ Task model: Python dataclass
- ✅ Validation: Service layer with clear error messages
- ✅ Interface: Numbered menu with input loop
- ✅ Display: Simple text table format
- ✅ Testing: Manual CLI testing per spec scenarios
- ✅ Architecture: Layered (CLI → Service → Data)

**Ready to proceed to Phase 1: Design & Contracts**

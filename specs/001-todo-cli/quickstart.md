# Quickstart Guide: Todo CLI App

**Feature**: 001-todo-cli
**Date**: 2026-01-04
**Audience**: Developers and testers

## Overview

This quickstart guide provides step-by-step instructions for setting up, running, and testing the Todo CLI application.

## Prerequisites

**Required**:
- Python 3.8 or higher

**How to check**:
```bash
python --version
# or
python3 --version
```

Expected output: `Python 3.8.x` or higher

**If Python not installed**:
- Windows: Download from [python.org](https://python.org)
- macOS: `brew install python3` or download from python.org
- Linux: `sudo apt install python3` (Debian/Ubuntu) or `sudo yum install python3` (RHEL/CentOS)

---

## Installation

### Step 1: Clone or Download Repository

```bash
# If using git
git clone <repository-url>
cd to-do-app

# Or download and extract ZIP
# cd to-do-app
```

### Step 2: Verify Project Structure

```bash
# Check that you have the src directory
ls src/

# Expected output:
# main.py  models/  services/  cli/
```

**No dependencies to install** - the application uses Python standard library only.

---

## Running the Application

### Option 1: Run Directly

```bash
python src/main.py
```

### Option 2: Run as Module (from repository root)

```bash
python -m src.main
```

### Expected Output

```
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Exit

Enter choice (1-6):
```

---

## Basic Usage

### 1. Add a Task

```
Enter choice (1-6): 1
Enter task title: Buy groceries

✓ Task added successfully (ID: 1)
```

### 2. View All Tasks

```
Enter choice (1-6): 2

ID | Title              | Status
---+--------------------+----------
1  | Buy groceries      | Incomplete
```

### 3. Add More Tasks

```
Enter choice (1-6): 1
Enter task title: Write report

✓ Task added successfully (ID: 2)

Enter choice (1-6): 1
Enter task title: Call dentist

✓ Task added successfully (ID: 3)
```

### 4. Mark a Task Complete

```
Enter choice (1-6): 5
Enter task ID: 2

✓ Task marked complete
```

### 5. Update a Task Title

```
Enter choice (1-6): 3
Enter task ID: 1
Enter new title: Buy organic groceries

✓ Task updated successfully
```

### 6. Delete a Task

```
Enter choice (1-6): 4
Enter task ID: 3

✓ Task deleted successfully
```

### 7. View Updated List

```
Enter choice (1-6): 2

ID | Title                   | Status
---+-------------------------+----------
1  | Buy organic groceries   | Incomplete
2  | Write report            | Complete
```

### 8. Exit Application

```
Enter choice (1-6): 6

Goodbye!
```

---

## Common Scenarios

### Scenario 1: Empty Task List

```
Enter choice (1-6): 2

No tasks found. Add a task to get started!
```

### Scenario 2: Invalid Task Title

```
Enter choice (1-6): 1
Enter task title:

✗ Error: Task title cannot be empty
```

### Scenario 3: Invalid Task ID

```
Enter choice (1-6): 5
Enter task ID: 999

✗ Error: Task ID 999 not found
```

### Scenario 4: Invalid Menu Choice

```
Enter choice (1-6): 10

✗ Error: Invalid choice. Please enter 1-6
```

### Scenario 5: Non-Numeric Input for ID

```
Enter choice (1-6): 5
Enter task ID: abc

✗ Error: Please enter a valid number
```

---

## Testing the Application

### Manual Test Checklist

Follow the test scenarios from the specification:

#### Test 1: Add and View Tasks (User Story 1)
- [ ] Start application with empty list
- [ ] Add task "Buy groceries"
- [ ] Verify task appears with ID 1 and status Incomplete
- [ ] Add two more tasks
- [ ] View all tasks - verify all 3 appear
- [ ] Attempt to add task with empty title - verify error message
- [ ] View tasks when list is empty - verify appropriate message

#### Test 2: Mark Tasks Complete (User Story 2)
- [ ] Add 3 tasks
- [ ] Mark task ID 2 as complete
- [ ] View tasks - verify only task 2 shows Complete
- [ ] Attempt to mark invalid ID (999) - verify error message
- [ ] Mark same task complete again - verify no error

#### Test 3: Update Task Titles (User Story 3)
- [ ] Add task "Buy milk"
- [ ] Update task title to "Buy almond milk"
- [ ] View tasks - verify title changed
- [ ] Attempt to update with invalid ID - verify error
- [ ] Attempt to update with empty title - verify error

#### Test 4: Delete Tasks (User Story 4)
- [ ] Add 5 tasks
- [ ] Delete task ID 3
- [ ] View tasks - verify task 3 gone, others remain
- [ ] Attempt to delete invalid ID - verify error
- [ ] Verify IDs are not reassigned after deletion

#### Test 5: Exit Application (User Story 5)
- [ ] Add several tasks
- [ ] Exit application
- [ ] Restart application
- [ ] View tasks - verify list is empty

### Cross-Platform Testing

Test on each target platform:

**Windows**:
```powershell
python src\main.py
```

**macOS/Linux**:
```bash
python3 src/main.py
```

Verify all features work identically on all platforms.

### Edge Case Testing

- [ ] Add 100+ tasks - verify all display correctly
- [ ] Add task with very long title (500+ characters) - verify accepted
- [ ] Rapid task creation (add 10 tasks quickly) - verify IDs increment correctly
- [ ] Alternate between all operations - verify no state corruption

---

## Troubleshooting

### Issue: `python: command not found`

**Solution**: Use `python3` instead of `python`:
```bash
python3 src/main.py
```

### Issue: `ModuleNotFoundError: No module named 'src'`

**Solution**: Run from repository root directory:
```bash
cd path/to/to-do-app
python src/main.py
```

### Issue: Application doesn't exit with Ctrl+C

**Solution**: This is expected behavior. Use menu option 6 to exit properly.

### Issue: Tasks disappear after restart

**Solution**: This is expected - the app is in-memory only. Tasks are not saved.

---

## Development Workflow

### Project Structure

```
to-do-app/
├── src/
│   ├── main.py              # Entry point
│   ├── models/
│   │   └── task.py          # Task data class
│   ├── services/
│   │   └── todo_service.py  # Business logic
│   └── cli/
│       ├── menu.py          # Menu and input handling
│       └── display.py       # Output formatting
├── tests/
│   └── manual/
│       └── test_scenarios.md
└── specs/
    └── 001-todo-cli/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        └── quickstart.md    # This file
```

### Code Style

- Follow PEP 8 conventions
- Use type hints for function parameters and return values
- Keep functions small (< 20 lines ideal)
- Use descriptive variable names
- Minimal comments (code should be self-documenting)

### Making Changes

1. Update the relevant module (models, services, or CLI)
2. Test manually using the scenarios above
3. Verify all 5 features still work correctly
4. Check cross-platform compatibility if changing I/O

---

## Performance Benchmarks

Expected performance (from specification success criteria):

| Operation | Target | Typical Performance |
|-----------|--------|---------------------|
| Add Task | < 5 seconds | < 1 second |
| View Tasks | < 2 seconds | < 1 second |
| Update Task | < 5 seconds | < 1 second |
| Delete Task | < 5 seconds | < 1 second |
| Mark Complete | < 5 seconds | < 1 second |

**Note**: Actual time includes user input. Pure code execution is sub-millisecond.

---

## Workflow Examples

### Quick Task Management Session

```bash
# Start app
python src/main.py

# Add 3 tasks
1 → Buy groceries
1 → Write report
1 → Call dentist

# View list
2 → (shows 3 tasks)

# Complete first task
5 → 1

# Update second task
3 → 2 → Finish quarterly report

# Delete third task
4 → 3

# View final state
2 → (shows 2 tasks: 1 complete, 1 incomplete)

# Exit
6
```

### Testing Complete Feature Set

```bash
# Start fresh
python src/main.py

# Add tasks
1 → Task A
1 → Task B
1 → Task C

# Try all operations
2 → View (verify 3 tasks)
5 → 2 → Mark B complete
3 → 1 → Updated Task A → Update A's title
4 → 3 → Delete C
2 → View final (verify changes)

# Test error handling
1 → (empty) → Verify error
5 → 999 → Verify error
3 → 999 → Verify error
4 → 999 → Verify error

# Exit
6
```

---

## Next Steps

After completing the quickstart:

1. **For Testers**: Run through all test scenarios in the Manual Test Checklist
2. **For Developers**: Review code in `src/` directory to understand implementation
3. **For Users**: Start using the app for real todo management (remember: data doesn't persist!)

---

## Support

**Issues**: Report bugs or issues via project issue tracker

**Questions**: Refer to specification documents in `specs/001-todo-cli/`

**Contributing**: Follow the Spec → Plan → Tasks → Implement workflow

---

## Appendix: Complete Feature List

| Feature | Menu Option | Description |
|---------|-------------|-------------|
| Add Task | 1 | Create new task with title |
| View Tasks | 2 | Display all tasks with ID, title, status |
| Update Task | 3 | Change task title by ID |
| Delete Task | 4 | Remove task by ID |
| Mark Complete | 5 | Set task status to complete by ID |
| Exit | 6 | Close application (data lost) |

**Remember**: All data is in-memory only. Tasks are lost when the application exits.

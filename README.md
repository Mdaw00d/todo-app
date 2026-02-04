# Todo CLI App

A simple command-line todo list application built with Python. Manage your tasks entirely in-memory with a clean, user-friendly interface.

## Features

- **Add Tasks**: Create new todo items with descriptive titles
- **View Tasks**: Display all tasks in a formatted table showing ID, title, and status
- **Update Tasks**: Modify task titles by ID
- **Delete Tasks**: Remove tasks from your list
- **Mark Complete**: Toggle tasks as complete or incomplete
- **Exit**: Clean exit with Ctrl+C support

## Requirements

- Python 3.8 or higher
- No external dependencies (uses Python standard library only)

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd to-do-app
   ```

## Usage

### Starting the Application

Run the application as a Python module:

```bash
python -m src.main
```

### Menu Options

Once started, you'll see the main menu:

```
=== Todo App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Exit
```

Enter a number (1-6) to select an option.

### Example Workflow

1. **Add your first task**:
   - Select option `1`
   - Enter: `Buy groceries`
   - Result: Task created with ID 1

2. **Add more tasks**:
   - Select option `1`
   - Enter: `Finish report`
   - Result: Task created with ID 2

3. **View all tasks**:
   - Select option `2`
   - See your task list:
     ```
     ID | Title                        | Status
     ---+------------------------------+------------
     1  | Buy groceries                | Incomplete
     2  | Finish report                | Incomplete
     ```

4. **Mark a task complete**:
   - Select option `5`
   - Enter task ID: `1`
   - Result: Task 1 marked as complete

5. **Update a task**:
   - Select option `3`
   - Enter task ID: `2`
   - Enter new title: `Finish quarterly report`
   - Result: Task 2 title updated

6. **Delete a task**:
   - Select option `4`
   - Enter task ID: `1`
   - Result: Task 1 removed from list

7. **Exit**:
   - Select option `6`
   - Or press `Ctrl+C` at any time

## Project Structure

```
to-do-app/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task data model
│   ├── services/
│   │   ├── __init__.py
│   │   └── todo_service.py  # Business logic
│   └── cli/
│       ├── __init__.py
│       ├── display.py       # Output formatting
│       └── menu.py          # Menu and input handling
├── tests/
│   └── manual/
│       └── test_scenarios.md
├── specs/
│   └── 001-todo-cli/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── research.md
│       ├── data-model.md
│       └── quickstart.md
└── README.md
```

## Data Model

Each task contains:
- **id** (int): Unique identifier, auto-generated
- **title** (str): Task description
- **completed** (bool): Completion status (default: False)

## Technical Details

- **Storage**: In-memory only (data resets on application exit)
- **Language**: Python 3.8+
- **Dependencies**: Python standard library only
- **Architecture**: Layered design (CLI → Service → Data)
- **Type Safety**: Full type hints throughout codebase

## Input Validation

The application handles common errors gracefully:
- Empty task titles are rejected
- Invalid task IDs show error messages
- Non-numeric ID inputs are caught and handled
- Invalid menu choices show helpful error messages

## Limitations

- **No Persistence**: All data is stored in-memory and will be lost when the application exits
- **No Multi-User Support**: Designed for single-user local use only
- **CLI Only**: No graphical or web interface

## Development

Built using Spec-Driven Development (SDD) workflow:
1. Specification (`specs/001-todo-cli/spec.md`)
2. Implementation Plan (`specs/001-todo-cli/plan.md`)
3. Task Breakdown (`specs/001-todo-cli/tasks.md`)
4. Implementation (with Claude Code + Spec-Kit Plus)

For more details, see the specification files in the `specs/001-todo-cli/` directory.

## License

This project is for educational purposes.

## Contributing

This is a Phase I implementation focused on core functionality. Future phases may include:
- File-based persistence (JSON, CSV)
- Task priorities and due dates
- Task categories or tags
- Search and filter capabilities
- Data export/import

However, these features are explicitly out of scope for Phase I per the constitution.

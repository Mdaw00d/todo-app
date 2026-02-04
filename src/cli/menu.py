"""Menu and input handling for the Todo CLI app."""


def display_menu() -> None:
    """Display the main menu options."""
    print("\n=== Todo App ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Exit")


def get_user_choice() -> str:
    """Get the user's menu choice.

    Returns:
        The user's input as a string
    """
    return input("\nEnter choice (1-6): ").strip()


def get_task_title() -> str:
    """Prompt user for a task title.

    Returns:
        The task title entered by the user
    """
    return input("Enter task title: ").strip()


def get_task_id() -> int:
    """Prompt user for a task ID.

    Returns:
        The task ID as an integer

    Raises:
        ValueError: If input is not a valid integer
    """
    id_input = input("Enter task ID: ").strip()
    return int(id_input)


def handle_add_task(service) -> None:
    """Handle the 'Add Task' menu option.

    Args:
        service: TodoService instance
    """
    from src.cli.display import show_message

    title = get_task_title()
    success, message = service.add_task(title)
    show_message(message, is_error=not success)


def handle_view_tasks(service) -> None:
    """Handle the 'View Tasks' menu option.

    Args:
        service: TodoService instance
    """
    from src.cli.display import format_task_list

    tasks = service.get_all_tasks()
    print("\n" + format_task_list(tasks))


def handle_update_task(service) -> None:
    """Handle the 'Update Task' menu option.

    Args:
        service: TodoService instance
    """
    from src.cli.display import show_message

    try:
        task_id = get_task_id()
        new_title = input("Enter new title: ").strip()
        success, message = service.update_task(task_id, new_title)
        show_message(message, is_error=not success)
    except ValueError:
        show_message("Error: Please enter a valid number", is_error=True)


def handle_delete_task(service) -> None:
    """Handle the 'Delete Task' menu option.

    Args:
        service: TodoService instance
    """
    from src.cli.display import show_message

    try:
        task_id = get_task_id()
        success, message = service.delete_task(task_id)
        show_message(message, is_error=not success)
    except ValueError:
        show_message("Error: Please enter a valid number", is_error=True)


def handle_mark_complete(service) -> None:
    """Handle the 'Mark Task Complete' menu option.

    Args:
        service: TodoService instance
    """
    from src.cli.display import show_message

    try:
        task_id = get_task_id()
        success, message = service.mark_complete(task_id)
        show_message(message, is_error=not success)
    except ValueError:
        show_message("Error: Please enter a valid number", is_error=True)

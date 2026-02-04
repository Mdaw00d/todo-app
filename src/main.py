"""Main entry point for the Todo CLI app."""

from src.services.todo_service import TodoService
from src.cli.menu import (
    display_menu,
    get_user_choice,
    handle_add_task,
    handle_view_tasks,
    handle_update_task,
    handle_delete_task,
    handle_mark_complete
)
from src.cli.display import show_message


def main() -> None:
    """Main application loop."""
    service = TodoService()

    print("Welcome to Todo CLI App!")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            handle_add_task(service)
        elif choice == "2":
            handle_view_tasks(service)
        elif choice == "3":
            handle_update_task(service)
        elif choice == "4":
            handle_delete_task(service)
        elif choice == "5":
            handle_mark_complete(service)
        elif choice == "6":
            print("\nGoodbye!")
            break
        else:
            show_message("Error: Invalid choice. Please enter 1-6", is_error=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

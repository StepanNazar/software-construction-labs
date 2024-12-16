import sys
from datetime import datetime
from uuid import UUID

from tabulate import tabulate

from models import Status


class View:
    """View class for the To-Do List App."""

    def welcome_message(self):
        """Show a welcome message to the user."""
        print("\nWelcome to the To-Do List App!\n")

    def exit_message(self):
        """Show an exit message to the user."""
        print("\nThank you for using the To-Do List App!\n")

    def error_message(self, error):
        """Show an error message to the user in the standard error stream."""
        print(f"Unexpected error: {error}", file=sys.stderr)

    def message(self, message):
        """Show a message to the user."""
        print(message)

    def show_tasks(self, tasks):
        """Show a tasks in a table."""
        if not tasks:
            print("No tasks found.")
            return

        table = [
            (
                task.id,
                task.description,
                task.schedule_for or "No deadline",
                task.status.value,
                task.created_at,
            )
            for task in tasks
        ]
        headers = ["ID", "Description", "Schedule For", "Status", "Created At"]
        print(
            tabulate(
                table,
                headers,
                tablefmt="grid",
                colalign=("center", "left", "center", "center", "center"),
                maxcolwidths=[36, 36, 36, 12, 36],
            )
        )

    def get_menu_choice(self):
        """Get a menu choice from the user."""
        print("\nPlease select an option:")
        print("1. Add a task")
        print("2. Change task status")
        print("3. Remove a task")
        print("4. Edit task")
        print("5. List tasks")
        print("6. Filter tasks")
        print("7. Show task by ID")
        print("8. Exit")
        return self.get_choice(1, 8)

    def get_id(self) -> UUID:
        """Get a task UUID from the user."""
        id_ = None
        while id_ is None:
            try:
                id_ = UUID(input("Enter task ID: "))
            except ValueError:
                pass
        return id_

    def get_description(self) -> str:
        """Get a description from the user. Can be an empty string."""
        return input("Enter task description: ")

    def get_schedule_for(self) -> datetime | None:
        """Get a deadline from the user. Return None if the user enters an empty string."""
        schedule_for = None
        while schedule_for is None:
            try:
                string = input("Enter task deadline (YYYY-MM-DD HH:MM:SS): ")
                if not string:
                    break
                schedule_for = datetime.fromisoformat(string)
            except ValueError:
                pass
        return schedule_for

    def get_status(self) -> Status:
        """Get a status from the user."""
        status = None
        while status not in Status:
            status = input("Enter task status (ToDo, InProgress, Done): ")
        return Status(status)

    def get_choice(self, min_: int, max_: int) -> int:
        """Get an integer choice between min_ and max_."""
        choice = None
        while choice is None or (choice < min_ or choice > max_):
            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                pass
        return choice

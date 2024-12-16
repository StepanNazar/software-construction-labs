import sys

from view import View
from models import Task


class Controller:
    """Controller class for the To-Do List App."""

    def __init__(self, view: View):
        self.view = view

    def run(self) -> None:
        """Run the To-Do List App."""
        self.view.welcome_message()
        while True:
            try:
                choice = self.view.get_menu_choice()
                self.process_choice(choice)
            except KeyboardInterrupt:
                self.exit()
            except Exception as e:
                self.view.error_message(e)

    def process_choice(self, choice: int) -> None:
        """Process the user's menu choice."""
        match choice:
            case 1:
                self.add_task()
            case 2:
                self.change_task_status()
            case 3:
                self.remove_task()
            case 4:
                self.edit_task()
            case 5:
                self.list_tasks()
            case 6:
                self.filter_tasks()
            case 7:
                self.show_task_by_id()
            case 8:
                self.exit()

    def add_task(self) -> None:
        """Add a new task to the to-do list.
        Ask the user for a description and a schedule for the task."""
        description = self.view.get_description()
        schedule_for = self.view.get_schedule_for()
        if schedule_for is None:
            self.view.message("Please enter a schedule for the task.")
            return
        task = Task(description, schedule_for)
        self.view.message(f"Task {task.id} added.")

    def change_task_status(self) -> None:
        """Change the status of a task in the to-do list.
        Ask the user for the task ID and the new status."""
        id_ = self.view.get_id()
        status = self.view.get_status()
        if not status:
            return
        task = Task.get_task(id_)
        if task is None:
            self.view.message(f"Task {id_} not found.")
            return
        task.status = status
        self.view.message(f"Task {id_} status changed to {status.value}.")

    def remove_task(self) -> None:
        """Remove a task from the to-do list. Ask the user for the task ID."""
        id_ = self.view.get_id()
        task = Task.remove_task(id_)
        if task is None:
            self.view.message(f"Task {id_} not found.")
            return
        self.view.message(f"Task {id_} removed.")

    def edit_task(self) -> None:
        """Edit a task in the to-do list. Ask the user for the task ID and the new task details."""
        id_ = self.view.get_id()
        self.view.message("Enter new task details(leave blank to keep the same):")
        description = self.view.get_description()
        schedule_for = self.view.get_schedule_for()
        task = Task.get_task(id_)
        if task is None:
            self.view.message(f"Task {id_} not found.")
            return
        if description:
            task.description = description
        if schedule_for:
            task.schedule_for = schedule_for
        self.view.message(f"Task {id_} edited.")

    def list_tasks(self) -> None:
        """List all tasks in the to-do list."""
        tasks = Task.list_tasks()
        self.view.show_tasks(tasks)

    def filter_tasks(self) -> None:
        """Filter tasks by status. Ask the user for a status."""
        status = self.view.get_status()
        tasks = Task.filter_tasks_by_status(status)
        self.view.show_tasks(tasks)

    def show_task_by_id(self) -> None:
        """Show a task by its unique identifier. Ask the user for the task ID."""
        id_ = self.view.get_id()
        task = Task.get_task(id_)
        if task is None:
            self.view.message(f"Task {id_} not found.")
            return
        self.view.show_tasks([task])

    def exit(self) -> None:
        """Exit the To-Do List App."""
        self.view.exit_message()
        sys.exit(0)

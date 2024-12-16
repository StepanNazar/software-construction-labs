from datetime import datetime
from uuid import UUID

from tabulate import tabulate

from models import Status


class View:
    def __init__(self, controller=None):
        self.controller = controller

    def welcome_message(self):
        print("\nWelcome to the To-Do List App!\n")

    def exit_message(self):
        print("\nThank you for using the To-Do List App!\n")

    def error_message(self, error):
        print(f"Unexpected error: {error}")

    def message(self, message):
        print(message)

    def show_tasks(self, tasks):
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

    def menu(self):
        print("\nPlease select an option:")
        print("1. Add a task")
        print("2. Change task status")
        print("3. Remove a task")
        print("4. Edit task")
        print("5. List tasks")
        print("6. Filter tasks")
        print("7. Show task by ID")
        print("8. Exit")
        match input("Enter your choice: "):
            case "1":
                self.add_task()
            case "2":
                self.change_task_status()
            case "3":
                self.remove_task()
            case "4":
                self.edit_task()
            case "5":
                self.list_tasks()
            case "6":
                self.filter_tasks()
            case "7":
                self.show_task_by_id()
            case "8":
                self.controller.exit()
            case _:
                print("Invalid option. Please try again.")
                self.menu()

    def get_id(self):
        id_ = None
        while id_ is None:
            try:
                id_ = UUID(input("Enter task ID: "))
            except ValueError:
                pass
        return id_

    def get_description(self):
        return input("Enter task description: ")

    def get_schedule_for(self):
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

    def get_status(self):
        status = None
        while status not in Status:
            status = input("Enter task status (ToDo, InProgress, Done): ")
        return Status(status)

    def add_task(self):
        description = self.get_description()
        schedule_for = self.get_schedule_for()
        self.controller.add_task(description, schedule_for)

    def change_task_status(self):
        id_ = self.get_id()
        status = self.get_status()
        self.controller.edit_task(id_, status=status)

    def remove_task(self):
        id_ = self.get_id()
        self.controller.remove_task(id_)

    def edit_task(self):
        id_ = self.get_id()
        print("Enter new task details(leave blank to keep the same):")
        description = self.get_description()
        schedule_for = self.get_schedule_for()
        self.controller.edit_task(
            id_, description=description, schedule_for=schedule_for
        )

    def show_task_by_id(self):
        id_ = self.get_id()
        task = self.controller.get_task(id_)
        if task:
            self.show_tasks([task])
        else:
            self.message(f"Task {id_} not found.")

    def filter_tasks(self):
        status = self.get_status()
        self.show_tasks(self.controller.filter_tasks(status))

    def list_tasks(self):
        self.show_tasks(self.controller.list_tasks())

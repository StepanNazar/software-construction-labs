import sys

from models import Task, Status


class Controller:
    def __init__(self, view):
        self.view = view
        view.controller = self

    def run(self):
        self.view.welcome_message()
        while True:
            try:
                self.view.menu()
            except KeyboardInterrupt:
                self.exit()
            except Exception as e:
                self.view.error_message(e)

    def add_task(self, description: str, schedule_for):
        task = Task(description, schedule_for)
        self.view.message(f"Task {task.id} added.")

    def remove_task(self, id_):
        task = Task.remove_task(id_)
        if task is None:
            self.view.message(f"Task {id_} not found.")
            return
        self.view.message(f"Task {id_} removed.")

    def edit_task(self, id_, status=None, description=None, schedule_for=None):
        task = Task.get_task(id_)
        if task is None:
            self.view.message(f"Task {id_} not found.")
            return
        if status:
            task.status = status
        if description:
            task.description = description
        if schedule_for:
            task.schedule_for = schedule_for
        self.view.message(f"Task {id_} edited.")

    def list_tasks(self):
        return Task.list_tasks()

    def filter_tasks(self, status):
        return Task.filter_tasks_by_status(status)

    def get_task(self, id_):
        return Task.get_task(id_)

    def exit(self):
        self.view.exit_message()
        sys.exit(0)

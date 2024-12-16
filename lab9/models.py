from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class Status(Enum):
    """An enumeration to represent the status of a task."""

    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class _ConstantAttribute:
    """A descriptor to create constant attributes."""

    def __set_name__(self, owner, name):
        self.name = "__" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if hasattr(instance, self.name):
            raise AttributeError(f"{self.name} is read-only")
        setattr(instance, self.name, value)


class Task:
    """A class to represent a task in a to-do list.

    Attributes:
        description (str): A description of the task.
        schedule_for (datetime): The date and time the task is scheduled for.
        status (Status): The status of the task(to do, in progress, done).
        id (UUID): The unique identifier of the task.
        created_at (datetime): The date and time the task was created.
    """

    __tasks = {}
    id = _ConstantAttribute()
    created_at = _ConstantAttribute()

    def __init__(
        self,
        description: str,
        schedule_for: datetime,
        status: Status = Status.TODO,
        created_at: datetime = None,
        id_: UUID = None,
    ):
        self.description = description
        self.schedule_for = schedule_for
        self.status = status
        self.created_at = created_at or datetime.now().replace(microsecond=0)
        if id_ in self.__tasks:
            raise ValueError("Task ID already exists")
        self.id = id_ or uuid4()
        self.__tasks[self.id] = self

    @classmethod
    def get_task(cls, id_: UUID):
        """Get a task by its unique identifier."""
        return cls.__tasks.get(id_)

    @classmethod
    def remove_task(cls, id_: UUID):
        """Remove a task from memory by its unique identifier."""
        return cls.__tasks.pop(id_, None)

    @classmethod
    def list_tasks(cls):
        """List all tasks."""
        return list(cls.__tasks.values())

    @classmethod
    def filter_tasks_by_status(cls, status: Status):
        """List tasks by status."""
        return list(task for task in cls.__tasks.values() if task.status == status)

    def __repr__(self):
        return f"Task {self.id}"

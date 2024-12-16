from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from models import Status, Task


def test_task_model():
    # test creation
    current_datetime = datetime.now().replace(microsecond=0)
    task = Task(description="Test Task", schedule_for=datetime(2023, 10, 30))
    assert task.description == "Test Task"
    assert task.schedule_for == datetime(2023, 10, 30)
    assert task.status == Status.TODO
    assert isinstance(task.id, uuid4().__class__)
    assert isinstance(task.created_at, datetime)
    assert (task.created_at - current_datetime) < timedelta(seconds=1)

    # test constant attributes
    with pytest.raises(AttributeError):
        task.id = uuid4()
    with pytest.raises(AttributeError):
        task.created_at = datetime.now().replace(microsecond=0)
    # test non-constant attributes
    task.description = "New Task"
    task.schedule_for = datetime(2023, 10, 31)
    task.status = Status.TODO

    # test id uniqueness
    with pytest.raises(ValueError):
        Task(description="Test Task", schedule_for=datetime(2023, 10, 30), id_=task.id)
    Task(description="Test Task", schedule_for=datetime(2023, 10, 30), id_=uuid4())

    # test class methods
    assert task in Task.list_tasks()
    assert task in Task.filter_tasks_by_status(Status.TODO)
    assert task not in Task.filter_tasks_by_status(Status.DONE)
    assert task not in Task.filter_tasks_by_status(Status.IN_PROGRESS)
    task.status = Status.DONE
    assert task in Task.filter_tasks_by_status(Status.DONE)
    assert Task.get_task(task.id) == task
    Task.remove_task(task.id)
    assert Task.get_task(task.id) is None
    assert task not in Task.list_tasks()
    assert task not in Task.filter_tasks_by_status(Status.DONE)

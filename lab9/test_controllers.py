from datetime import datetime
from unittest.mock import MagicMock

import pytest

from controllers import Controller
from models import Status, Task


@pytest.fixture(autouse=True)
def clear_tasks():
    """Fixture to clear tasks before each test."""
    yield
    for task in Task.list_tasks():
        Task.remove_task(task.id)


@pytest.fixture
def setup_controller():
    """Fixture to create the controller and mock view."""
    view = MagicMock()
    controller = Controller(view)
    sample_task = Task(description="Sample Task", schedule_for=datetime(2023, 10, 31))
    yield controller, view, sample_task


def test_controller_run(setup_controller):
    """Test running the controller."""
    controller, view, _ = setup_controller
    view.get_menu_choice.side_effect = [8]
    with pytest.raises(SystemExit):
        controller.run()
    view.welcome_message.assert_called_once()
    view.get_menu_choice.assert_called_once()
    view.exit_message.assert_called_once()


def test_controller_process_choice():
    """Test processing the user's menu choice."""
    controller = MagicMock()
    methods = {
        1: "add_task",
        2: "change_task_status",
        3: "remove_task",
        4: "edit_task",
        5: "list_tasks",
        6: "filter_tasks",
        7: "show_task_by_id",
        8: "exit",
    }
    for choice, method in methods.items():
        Controller.process_choice(controller, choice)
        getattr(controller, method).assert_called_once()


def test_controller_add_task(setup_controller):
    """Test adding a task."""
    controller, view, _ = setup_controller
    view.get_description.return_value = "New Task"
    view.get_schedule_for.return_value = datetime(2023, 11, 1)

    controller.add_task()

    tasks = Task.list_tasks()
    assert len(tasks) == 2  # Includes the sample task from the fixture
    assert tasks[1].description == "New Task"
    view.message.assert_called_with(f"Task {tasks[1].id} added.")


def test_controller_change_task_status(setup_controller):
    """Test changing the status of a task."""
    controller, view, sample_task = setup_controller
    view.get_id.return_value = sample_task.id
    view.get_status.return_value = Status.DONE

    controller.change_task_status()
    assert sample_task.status == Status.DONE
    view.message.assert_called_with(f"Task {sample_task.id} status changed to Done.")


def test_controller_remove_task(setup_controller):
    """Test removing a task."""
    controller, view, sample_task = setup_controller
    view.get_id.return_value = sample_task.id

    controller.remove_task()
    assert Task.get_task(sample_task.id) is None
    view.message.assert_called_with(f"Task {sample_task.id} removed.")


def test_controller_edit_task(setup_controller):
    """Test editing a task."""
    controller, view, sample_task = setup_controller
    view.get_id.return_value = sample_task.id
    view.get_description.return_value = "Updated Task"
    view.get_schedule_for.return_value = datetime(2025, 11, 2)

    controller.edit_task()

    assert sample_task.description == "Updated Task"
    assert sample_task.schedule_for == datetime(2025, 11, 2)
    view.message.assert_called_with(f"Task {sample_task.id} edited.")


def test_controller_list_tasks(setup_controller):
    """Test listing tasks."""
    controller, view, sample_task = setup_controller
    task2 = Task(description="Task 2", schedule_for=datetime(2023, 11, 1))
    controller.list_tasks()
    view.show_tasks.assert_called_with([sample_task, task2])


def test_controller_filter_tasks(setup_controller):
    """Test filtering tasks by status."""
    controller, view, sample_task = setup_controller
    view.get_status.return_value = Status.TODO
    task2 = Task(
        description="Task 2",
        schedule_for=datetime(2023, 11, 1),
        status=Status.IN_PROGRESS,
    )

    controller.filter_tasks()
    view.show_tasks.assert_called_with([sample_task])

    view.get_status.return_value = Status.IN_PROGRESS
    controller.filter_tasks()
    view.show_tasks.assert_called_with([task2])


def test_controller_show_task_by_id(setup_controller):
    """Test showing a task by ID."""
    controller, view, sample_task = setup_controller
    view.get_id.return_value = sample_task.id

    controller.show_task_by_id()
    view.show_tasks.assert_called_with([sample_task])


def test_controller_exit(setup_controller):
    """Test exiting the application."""
    controller, view, _ = setup_controller
    with pytest.raises(SystemExit):
        controller.exit()
    view.exit_message.assert_called_once()

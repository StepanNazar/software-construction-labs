from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import patch
from uuid import UUID

import pytest

from models import Status, Task
from view import View


@pytest.fixture
def view():
    """Fixture to create a View instance."""
    return View()


@patch("sys.stdout", new_callable=StringIO)
def test_welcome_message(mock_stdout, view):
    """Test welcome message."""
    view.welcome_message()
    assert "Welcome to the To-Do List App!" in mock_stdout.getvalue()


@patch("sys.stdout", new_callable=StringIO)
def test_exit_message(mock_stdout, view):
    """Test exit message."""
    view.exit_message()
    assert "Thank you for using the To-Do List App!" in mock_stdout.getvalue()


@patch("sys.stderr", new_callable=StringIO)
def test_error_message(mock_stderr, view):
    """Test error message."""
    view.error_message("Error message")
    assert "Unexpected error: Error message" in mock_stderr.getvalue()


@patch("sys.stdout", new_callable=StringIO)
def test_message(mock_stdout, view):
    """Test message."""
    view.message("Message")
    assert "Message" in mock_stdout.getvalue()


@patch("builtins.input", lambda _: "Sample Task")
def test_get_description(view):
    """Test getting a description."""
    description = view.get_description()
    assert description == "Sample Task"


@patch("builtins.input", side_effect=["invalid", "2023-10-31 12:00:00"])
def test_get_schedule_for(mock_input, view):  # noqa
    """Test retrying an invalid schedule."""
    schedule = view.get_schedule_for()
    assert schedule == datetime(2023, 10, 31, 12, 0)


@patch("builtins.input", side_effect=["to", "ToDo"])
def test_get_status(mock_input, view):  # noqa
    """Test getting task status."""
    status = view.get_status()
    assert status == Status.TODO


@patch(
    "builtins.input",
    side_effect=["123e4567-e89b-12d3", "123e4567-e89b-12d3-a456-426614174000"],
)
def test_get_id(mock_input, view):  # noqa
    """Test getting a task ID."""
    id_ = view.get_id()
    assert id_ == UUID("123e4567-e89b-12d3-a456-426614174000")


@patch("builtins.input", side_effect=["a", "0", "10", "1"])
def test_get_menu_choice(mock_input, view):  # noqa
    """Test getting a menu choice."""
    choice = view.get_menu_choice()
    assert choice == 1


@patch("sys.stdout", new_callable=StringIO)
def test_show_tasks_no_tasks(mock_stdout, view):
    """Test showing tasks when there are no tasks."""
    view.show_tasks([])
    assert "No tasks found." in mock_stdout.getvalue()


@patch("sys.stdout", new_callable=StringIO)
def test_show_tasks(mock_stdout, view):
    """Test showing tasks."""
    current_time = datetime.now().replace(microsecond=0)
    task = Task("Sample Task", datetime(2023, 10, 31, 12, 0))
    view.show_tasks([task])
    output = mock_stdout.getvalue().strip()
    header = output.splitlines()[1]
    print(output.splitlines())
    data = "\n".join(output.splitlines()[3:-1])
    assert "ID" in header
    assert "Description" in header
    assert "Schedule For" in header
    assert "Status" in header
    assert "Created At" in header
    assert str(task.id) in data
    assert task.description in data
    assert "2023-10-31 12:00:00" in data
    assert "ToDo" in data
    assert str(current_time) in data or str(current_time + timedelta(seconds=1)) in data

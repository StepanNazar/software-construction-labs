"""Test the main function of the program and run all doctests."""

import doctest
import unittest
from io import StringIO
from unittest.mock import patch

import string_utils
from main import main


class TestMainFunction(unittest.TestCase):
    """Test the main function of the program."""

    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.argv", ["main.py", " #$@!%  !%1 !ab$  "])
    def test_main_with_arg(self, mock_stdout: StringIO) -> None:
        """Test main function with command line argument."""
        main()
        output = mock_stdout.getvalue()
        self.assertEqual(output, " #$@!%  !%1 !ba$  \n")

    @patch("sys.argv", ["main.py", "Hello", "World"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_with_args(self, mock_stdout: StringIO) -> None:
        """Test main function with several command line arguments."""
        main()
        output = mock_stdout.getvalue()
        self.assertEqual(output, "olleH\ndlroW\n")

    @patch("sys.argv", ["main.py"])
    @patch("builtins.input", return_value="Hello World", spec=input)
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_without_args(self, mock_stdout: StringIO, mock_input: str) -> None:
        """Test main function without command line arguments."""
        main()
        output = mock_stdout.getvalue()
        self.assertEqual(output, "olleH dlroW\n")

    @patch("sys.argv", ["main.py", "-h"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_main_help(self, mock_stdout: StringIO) -> None:
        """Test main function with help option."""
        with self.assertRaises(SystemExit):
            main()
        output = mock_stdout.getvalue()
        self.assertIn("usage: ", output)

    @patch("sys.argv", ["main.py", "-f"])
    @patch("sys.stderr", new_callable=StringIO)
    def test_main_invalid_args(self, mock_stderr: StringIO) -> None:
        """Test main function with invalid option."""
        with self.assertRaises(SystemExit):
            main()
        output = mock_stderr.getvalue()
        self.assertIn("error: unrecognized arguments:", output)


def load_tests(loader, tests, ignore):
    """Load the doctests from other modules."""
    tests.addTests(doctest.DocTestSuite(string_utils))
    return tests


if __name__ == "__main__":
    unittest.main()

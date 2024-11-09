import re
import sys
from io import StringIO

import pytest
from main import main


@pytest.mark.parametrize(
    "amount, stdout",
    [
        ("1234.56", "Одна тисяча двісті тридцять чотири гривні 56 копійок.\n"),
    ],
)
def test_correct_amount(amount: str, stdout: str, mocker) -> None:
    mocker.patch("sys.argv", ["main.py", amount])
    mocker.patch("sys.stdout", new_callable=StringIO)
    main()
    assert stdout == sys.stdout.getvalue()
    mocker.patch("sys.argv", ["main.py"])
    mocker.patch("sys.stdin", StringIO(amount))
    mocker.patch("sys.stdout", new_callable=StringIO)
    main()
    assert sys.stdout.getvalue().endswith(stdout)


@pytest.mark.parametrize(
    "amount",
    [
        "1234.5",
        "1234.567",
        "1234",
        "10.10.10",
        "10.1a",
        "ten",
        "ten.ten",
    ],
)
def test_incorrect_amount(amount: str, mocker) -> None:
    stderr_regex = r"usage: .*\n.*error: Неправильний формат грошової суми\. Введіть у форматі x\.yy"
    mocker.patch("sys.argv", ["main.py", amount])
    mocker.patch("sys.stderr", new_callable=StringIO)
    with pytest.raises(SystemExit):
        main()
    assert re.match(stderr_regex, sys.stderr.getvalue())
    mocker.patch("sys.argv", ["main.py"])
    mocker.patch("sys.stdin", StringIO(amount))
    mocker.patch("sys.stderr", new_callable=StringIO)
    with pytest.raises(SystemExit):
        main()
    assert re.match(stderr_regex, sys.stderr.getvalue())


def test_help(mocker) -> None:
    mocker.patch("sys.argv", ["main.py", "-h"])
    mocker.patch("sys.stdout", new_callable=StringIO)
    with pytest.raises(SystemExit):
        main()
    assert sys.stdout.getvalue().startswith("usage: ")


@pytest.mark.parametrize(
    "argv",
    [
        ["main.py", "-f"],
        ["main.py", "-f", "1234.56"],
        ["main.py", "1234.56", "-f"],
        ["main.py", "1234.56", "1234.56"],
        ["main.py", "1234.56", "-f", "1234.56"],
        ["main.py", "-f", "1234.56", "1234.56"],
    ],
)
def test_invalid_args(argv: list[str], mocker) -> None:
    stderr_regex = r"usage: .*\n.*error: unrecognized arguments:"
    mocker.patch("sys.argv", argv)
    mocker.patch("sys.stderr", new_callable=StringIO)
    with pytest.raises(SystemExit):
        main()
    assert re.match(stderr_regex, sys.stderr.getvalue())

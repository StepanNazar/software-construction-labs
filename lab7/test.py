import pytest

from main import extract_bytes, sum_bytes_sent_and_received

test_data = [
    """213.109.238.193 - - [07/May/2017:00:08:35 +0300] "GET /question/edit.php?cmid=1&cat=1%2C18&qpage=0&category=7%2C131&qbshowtext=0&recurse=0&recurse=1&showhidden=0&showhidden=1 HTTP/1.0" 303 440 "http://learn.topnode.if.ua/question/edit.php" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0""",
    """213.109.238.193 - - [07/May/2017:01:16:47 +0300] "POST /lib/editor/atto/autosave-ajax.php HTTP/1.0" 200 0 "http://learn.topnode.if.ua/question/question.php?returnurl=%2Fmod%2Fquiz%2Fedit.php%3Fcmid%3D32%26amp%3Bcat%3D7%252C131%26amp%3Bqpage%3D0%26amp%3Brecurse%3D1%26amp%3Bshowhidden%3D1&cmid=32&id=20" "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0""",
    """91.243.6.52 - - [07/May/2017:08:15:31 +0300] "GET /grade/report/user/index.php?id=3 HTTP/1.0" 200 60640 "http://learn.topnode.if.ua/course/view.php?id=3" "Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0""",
]


@pytest.mark.parametrize(
    "entry, bytes_",
    [
        (test_data[0], 440),
        (test_data[1], 0),
        (test_data[2], 60640),
    ],
)
def test_extract_bytes(entry: str, bytes_) -> None:
    assert extract_bytes(entry) == bytes_


@pytest.fixture
def nginx_log_file(mocker) -> None:
    mocker.patch("main.open", mocker.mock_open(read_data="\n".join(test_data)))


def test_sum_bytes_sent_and_received(nginx_log_file) -> None:
    assert sum_bytes_sent_and_received("some_file.txt") == 61080

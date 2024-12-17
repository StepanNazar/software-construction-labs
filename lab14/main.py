from dateutil.parser import parse
import re


def extract_datetime(string : str) -> str:
    """
    Extracts the date and time in format YYYY-MM-DDTH:M:SZ from a string.

    :param string: The string to extract the date and time from.
    :return: A string in the format YYYY-MM-DDTH:M:SZ.

    >>> extract_datetime("On Sun, 13 Oct 2024 19:01:18 +0800, Test User <test@test.me> wrote:")
    '2024-10-13T19:01:18Z'
    >>> extract_datetime("On Tue, Oct 1, 2024 at 19:23 Test User <test@test.me> wrote:")
    '2024-10-01T19:23:00Z'
    >>> extract_datetime("On Mon, Oct 14, 2024, 8:06 PM Test User <test@test.me> wrote:")
    '2024-10-14T20:06:00Z'
    >>> extract_datetime("On Wed, 9 Oct 2024, 2:04 am Test User, <test@test.me> wrote:")
    '2024-10-09T02:04:00Z'
    >>> extract_datetime("On 25-Sep-2024 3:37 am, Test User <test@test.me> wrote:")
    '2024-09-25T03:37:00Z'
    >>> extract_datetime("On Fri, 27 Sept 2024, 17:32 Test User, <test@test.me> wrote:")
    '2024-09-27T17:32:00Z'
    """
    datetime_string = re.match(r'(?i)On ([\w\s,:+-]*[\dm]),? \w* \w*', string).group(1)
    datetime = parse(datetime_string)
    return datetime.strftime("%Y-%m-%dT%H:%M:%SZ")



if __name__ == "__main__":
    import doctest

    doctest.testmod()

"""Set of functions for reversing words."""


def reverse_word(word: str) -> str:
    r"""Reverses a word.

    Returns a reversed word. Non-alphabetic characters remain in place. Leading and
    trailing whitespaces are removed. If there are whitespaces in the middle of the
    word, raises ValueError.
    :param word: Word to reverse.
    :return: Reversed word.
    :raises TypeError: if word argument is not str.
    :raises ValueError: if there are whitespaces in the middle of the word.

    Usage:

    >>> reverse_word("string")
    'gnirts'
    >>> reverse_word("a1bcd")
    'd1cba'
    >>> reverse_word("к!ири")
    'и!рик'
    >>> reverse_word("")
    ''
    >>> reverse_word(" ab \t")
    'ba'
    >>> reverse_word("ab cd")
    Traceback (most recent call last):
        ...
    ValueError: You passed several words. Use reverse_words_in_string instead.
    >>> reverse_word(1)
    Traceback (most recent call last):
        ...
    TypeError: word argument must be str, not int
    >>> reverse_word(None)
    Traceback (most recent call last):
        ...
    TypeError: word argument must be str, not NoneType
    """
    if not isinstance(word, str):
        msg = f"word argument must be str, not {type(word).__name__}"
        raise TypeError(msg)
    word = word.strip()
    result = ""
    ptr = len(word) - 1
    for char in word:
        if char.isalpha():
            while not word[ptr].isalpha():
                ptr -= 1
            result += word[ptr]
            ptr -= 1
        elif char.isspace():
            msg = "You passed several words. Use reverse_words_in_string instead."
            raise ValueError(msg)
        else:
            result += char
    return result


def reverse_words_in_string(string: str) -> str:
    r"""Reverses each word in string.

    Returns a string with reversed words. Non-alphabetic characters remain in place.
    Words can be separated by any whitespace character.
    :param string: String to process.
    :return: String with reversed words.
    :raises TypeError: if string argument is not str.

    Usage:

    >>> reverse_words_in_string("string")
    'gnirts'
    >>> reverse_words_in_string("Hello World")
    'olleH dlroW'
    >>> reverse_words_in_string("Hello, World! 123")
    'olleH, dlroW! 123'
    >>> reverse_words_in_string("a1bcd efg!h")
    'd1cba hgf!e'
    >>> reverse_words_in_string("ки!ри 1иця")
    'ир!ик 1яци'
    >>> reverse_words_in_string("")
    ''
    >>> reverse_words_in_string("   ")
    '   '
    >>> reverse_words_in_string(" #$@!%  !%1 !ab$  ")
    ' #$@!%  !%1 !ba$  '
    >>> reverse_words_in_string("Hello\tWorld")
    'olleH\tdlroW'
    >>> reverse_words_in_string(1)
    Traceback (most recent call last):
        ...
    TypeError: string argument must be str, not int
    >>> reverse_words_in_string(None)
    Traceback (most recent call last):
        ...
    TypeError: string argument must be str, not NoneType
    """
    if not isinstance(string, str):
        msg = f"string argument must be str, not {type(string).__name__}"
        raise TypeError(msg)
    result = ""
    word = ""
    for char in string:
        if char.isspace():
            result += reverse_word(word)
            result += char
            word = ""
        else:
            word += char
    result += reverse_word(word)
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()

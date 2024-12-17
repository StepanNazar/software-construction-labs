"""Command line tool for reversing words in a string."""

import argparse

from .string_utils import reverse_words_in_string


def main() -> None:
    """Command line tool for reversing words in a string."""
    arg_parser = argparse.ArgumentParser(
        description="Reverse words in strings. No arguments will read from stdin.",
    )
    arg_parser.add_argument("strings", type=str, help="Strings to reverse.", nargs="*")
    args = arg_parser.parse_args()
    if args.strings:
        for string in args.strings:
            print(reverse_words_in_string(string))
    else:
        string = input("Enter a string: ")
        print(reverse_words_in_string(string))


if __name__ == "__main__":
    main()

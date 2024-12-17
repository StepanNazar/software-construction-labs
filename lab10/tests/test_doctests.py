"""Run the doctests from the other modules."""

import doctest
import unittest

from pnu_2024_kpz_lab10_stepan_nazar import string_utils


def load_tests(loader, tests, ignore):
    """Load the doctests from other modules."""
    tests.addTests(doctest.DocTestSuite(string_utils))
    return tests


if __name__ == "__main__":
    unittest.main()

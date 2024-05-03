"""Provide global variables and functions.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
prefs = {}


def to_string(text):
    """Return text, converted to a string."""
    if text is None:
        return ''

    return str(text)

"""Provide global variables and functions.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
import sys

from nvlib.model.data.py_calendar import PyCalendar

prefs = {}
launchers = {}
# launchers for opening linked non-standard filetypes.
# key: extension, value: path to application
# this dictionary is populated by novelibre.py after reading the configuration file

HOME_URL = 'https://github.com/peter88213/novelibre/'

HOME_DIR = str(Path.home()).replace('\\', '/')
INSTALL_DIR = f'{HOME_DIR}/.novx'
PROGRAM_DIR = os.path.dirname(sys.argv[0])
if not PROGRAM_DIR:
    PROGRAM_DIR = '.'
USER_STYLES_DIR = f'{INSTALL_DIR}/styles'
USER_STYLES_XML = f'{USER_STYLES_DIR}/styles.xml'


def datestr(dateIso):
    """Return a localized date string, if the localize_date option is set.
    
    Otherwise return the input unchanged.
    """
    if prefs['localize_date']:
        return PyCalendar.locale_date(dateIso)
    else:
        return dateIso


def get_section_date_str(section):
    """Return a localized date string, if the localize_date option is set.
    
    Otherwise return the section's date in ISO format.
    """
    if prefs['localize_date']:
        return section.localeDate
    else:
        return section.date


def to_string(text):
    """Return text, converted to a string."""
    if text is None:
        return ''

    return str(text)


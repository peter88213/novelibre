"""Provide global variables and functions.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
import webbrowser

from novxlib.novx_globals import _

prefs = {}

HELP_URL = f'https://peter88213.github.io/{_("nvhelp-en")}/'
HOME_URL = 'https://github.com/peter88213/novelibre/'


def to_string(text):
    """Return text, converted to a string."""
    if text is None:
        return ''

    return str(text)


def open_help(page):
    """Show the online help page specified by page."""
    webbrowser.open(f'{HELP_URL}{page}')


def datestr(isoDate):
    """Return a localized date string, if the localize_date option is set.
    
    Otherwise return the input unchanged.
    """
    if prefs['localize_date']:
        return date.fromisoformat(isoDate).strftime("%x")
    else:
        return isoDate


def get_section_date_str(section):
    """Return a localized date string, if the localize_date option is set.
    
    Otherwise return the section's date in ISO format.
    """
    if prefs['localize_date']:
        return section.localeDate
    else:
        return section.date

"""Provide global variables and functions.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from datetime import time
import os

ROOT_PREFIX = 'rt'
CHAPTER_PREFIX = 'ch'
PLOT_LINE_PREFIX = 'ac'
SECTION_PREFIX = 'sc'
PLOT_POINT_PREFIX = 'ap'
CHARACTER_PREFIX = 'cr'
LOCATION_PREFIX = 'lc'
ITEM_PREFIX = 'it'
PRJ_NOTE_PREFIX = 'pn'
CH_ROOT = f'{ROOT_PREFIX}{CHAPTER_PREFIX}'
PL_ROOT = f'{ROOT_PREFIX}{PLOT_LINE_PREFIX}'
CR_ROOT = f'{ROOT_PREFIX}{CHARACTER_PREFIX}'
LC_ROOT = f'{ROOT_PREFIX}{LOCATION_PREFIX}'
IT_ROOT = f'{ROOT_PREFIX}{ITEM_PREFIX}'
PN_ROOT = f'{ROOT_PREFIX}{PRJ_NOTE_PREFIX}'

BRF_SYNOPSIS_SUFFIX = '_brf_synopsis'
CHAPTERS_SUFFIX = '_chapters_tmp'
CHARACTER_REPORT_SUFFIX = '_character_report'
CHARACTERS_SUFFIX = '_characters_tmp'
CHARLIST_SUFFIX = '_charlist_tmp'
DATA_SUFFIX = '_data'
GRID_SUFFIX = '_grid_tmp'
ITEM_REPORT_SUFFIX = '_item_report'
ITEMLIST_SUFFIX = '_itemlist_tmp'
ITEMS_SUFFIX = '_items_tmp'
LOCATION_REPORT_SUFFIX = '_location_report'
LOCATIONS_SUFFIX = '_locations_tmp'
LOCLIST_SUFFIX = '_loclist_tmp'
MANUSCRIPT_SUFFIX = '_manuscript_tmp'
PARTS_SUFFIX = '_parts_tmp'
PLOTLIST_SUFFIX = '_plotlist'
PLOTLINES_SUFFIX = '_plotlines_tmp'
PROJECTNOTES_SUFFIX = '_projectnote_report'
PROOF_SUFFIX = '_proof_tmp'
SECTIONLIST_SUFFIX = '_sectionlist'
SECTIONS_SUFFIX = '_sections_tmp'
STAGES_SUFFIX = '_structure_tmp'
XREF_SUFFIX = '_xref'


class Error(Exception):
    """Base class for exceptions."""
    pass


class Notification(Error):
    pass


def norm_path(path):
    if path is None:
        path = ''
    return os.path.normpath(path)


def string_to_list(text, divider=';'):
    """Convert a string into a list with unique elements.
    
    Positional arguments:
        text -- string containing divider-separated substrings.
        
    Optional arguments:
        divider -- string that divides the substrings.
    
    Split a string into a list of strings. Retain the order, but discard duplicates.
    Remove leading and trailing spaces, if any.
    Return a list of strings.
    If an error occurs, return an empty list.
    """
    elements = []
    try:
        tempList = text.split(divider)
        for element in tempList:
            element = element.strip()
            if element and not element in elements:
                elements.append(element)
        return elements

    except:
        return []


def list_to_string(elements, divider=';'):
    """Join strings from a list.
    
    Positional arguments:
        elements -- list of elements to be concatenated.
        
    Optional arguments:
        divider -- string that divides the substrings.
    
    Return a string which is the concatenation of the 
    members of the list of strings "elements", separated by 
    a comma plus a space. The space allows word wrap in 
    spreadsheet cells.
    If an error occurs, return an empty string.
    """
    try:
        text = divider.join(elements)
        return text

    except:
        return ''


def intersection(elemList, refList):
    """Return a list with the intersection of elemList and refList.

    Positional arguments:
        elemList: list -- List to verify.
        refList: list -- Reference list.
    
    The element order is from elemList.
    """
    return [elem for elem in elemList if elem in refList]


def verified_date(dateStr):
    """Return a verified iso dateStr or None."""
    if dateStr is not None:
        date.fromisoformat(dateStr)
        # raising an exception if dateStr is not an iso-formatted date
    return dateStr


def verified_int_string(intStr):
    """Return a string representing a number or None."""
    if intStr is not None:
        int(intStr)
        # raising an exception if intStr does not represent a number
    return intStr


def verified_time(timeStr):
    """Return a verified iso timeStr or None."""
    if  timeStr is not None:
        time.fromisoformat(timeStr)
        # raising an exception if timeStr is not an iso-formatted time
        while timeStr.count(':') < 2:
            timeStr = f'{timeStr}:00'
            # adding minutes or seconds, if missing
    return timeStr


"""Provide global variables and functions.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.nv_locale import _

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
CHAPTERLIST_SUFFIX = '_chapterlist_tmp'
CHAPTERS_SUFFIX = '_chapters_tmp'
CHARACTER_REPORT_SUFFIX = '_character_report'
CHARACTERS_SUFFIX = '_characters_tmp'
CHARLIST_SUFFIX = '_charlist_tmp'
DATA_SUFFIX = '_data'
ELEMENT_NOTES_SUFFIX = '_element_note_report',
GRID_SUFFIX = '_grid_tmp'
ITEM_REPORT_SUFFIX = '_item_report'
ITEMLIST_SUFFIX = '_itemlist_tmp'
ITEMS_SUFFIX = '_items_tmp'
LOCATION_REPORT_SUFFIX = '_location_report'
LOCATIONS_SUFFIX = '_locations_tmp'
LOCLIST_SUFFIX = '_loclist_tmp'
MAJOR_MARKER = _('Major Character')
MANUSCRIPT_SUFFIX = '_manuscript_tmp'
MINOR_MARKER = _('Minor Character')
PARTLIST_SUFFIX = '_partlist_tmp'
PARTS_SUFFIX = '_parts_tmp'
PLOTLIST_SUFFIX = '_plotlist'
PLOTLINES_SUFFIX = '_plotlines_tmp'
PROJECTNOTES_SUFFIX = '_projectnote_report'
PROOF_SUFFIX = '_proof_tmp'
SECTIONLIST_SUFFIX = '_sectionlist'
SECTIONS_SUFFIX = '_sections_tmp'
STAGES_SUFFIX = '_structure_tmp'
TIMETABLE_SUFFIX = '_tt_tmp'
XREF_SUFFIX = '_xref'

NO_SCENE_FIELD_1_DEFAULT = _('Plot progress')
NO_SCENE_FIELD_2_DEFAULT = _('Characterization')
NO_SCENE_FIELD_3_DEFAULT = _('World building')
OTHER_SCENE_FIELD_1_DEFAULT = _('Opening')
OTHER_SCENE_FIELD_2_DEFAULT = _('Peak emotional moment')
OTHER_SCENE_FIELD_3_DEFAULT = _('Ending')
CR_FIELD_1_DEFAULT = _('Bio')
CR_FIELD_2_DEFAULT = _('Goals')

STATUS = [
    None,
    _('Outline'),
    _('Draft'),
    _('1st Edit'),
    _('2nd Edit'),
    _('Done')
]
# emulating an enumeration for the section completion status

SCENE = ['-', 'A', 'R', 'x']
# emulating an enumeration for the scene Action/Reaction/Other type


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
    
    Split a string into a list of strings. Retain the order, 
    but discard duplicates.
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


def verified_int_string(intStr):
    """Return a string representing a number or None."""
    if intStr is not None:
        int(intStr)
        # raising an exception if intStr does not represent a number
    return intStr


"""Provide a base helper class for section and chapter splitting.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Splitter:
    """Base class for section and chapter splitting.
    
    When importing sections to novelibre, they may contain manually 
    inserted section and chapter dividers.
    The Splitter class updates a Novel instance by splitting such sections 
    and creating new chapters and sections. 
    
    Public class constants:
        PART_SEPARATOR -- marker indicating the beginning of a new part,
                          splitting a section.
        CHAPTER_SEPARATOR -- marker indicating the beginning of a new chapter,
                             splitting a section.
        SECTION_SEPARATOR -- marker indicating the beginning of a new section, 
                             splitting a section.
        APPENDED_SECTION_SEPARATOR -- marker indicating the beginning of a new 
                                      "appended" section, splitting a section.
        DESC_SEPARATOR -- marker separating title and description of 
                          a chapter or section.
    """
    PART_SEPARATOR = '#'
    CHAPTER_SEPARATOR = '##'
    SECTION_SEPARATOR = '###'
    APPENDED_SECTION_SEPARATOR = '####'
    DESC_SEPARATOR = '|'
    _CLIP_TITLE = 20
    # Maximum length of newly generated section titles.


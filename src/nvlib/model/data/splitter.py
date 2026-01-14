"""Provide a base helper class for section and chapter splitting.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC

from nvlib.model.data.chapter import Chapter
from nvlib.model.data.section import Section


class Splitter(ABC):
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

    def create_chapter(
            self,
            novel,
            chapterId,
            title,
            desc,
            level,
    ):
        """Create a new chapter and add it to the novel.
        
        Positional arguments:
            chapterId -- str: ID of the chapter to create.
            title -- str: title of the chapter to create.
            desc -- str: description of the chapter to create.
            level -- int: chapter level (part/chapter).
        """
        newChapter = Chapter()
        newChapter.title = title
        newChapter.desc = desc
        newChapter.chLevel = level
        newChapter.chType = 0
        novel.chapters[chapterId] = newChapter

    def new_section(
        self,
        parent,
        splitCount,
        title,
        appendToPrev,
    ):
        """Factory method, returning a new section instance.
        
        Positional arguments:
            sectionId -- str: ID of the section to create.
            parent -- Section instance: parent section.
            splitCount -- int: number of parent's splittings.
            title -- str: title of the section to create.
            appendToPrev -- boolean: when exporting, append the section
                            to the previous one without separator.
        """
        WARNING = '(!)'

        # Mark metadata of split sections.
        newSection = Section(appendToPrev=appendToPrev)
        if title:
            newSection.title = title
        elif parent.title:
            if len(parent.title) > self._CLIP_TITLE:
                title = f'{parent.title[:self._CLIP_TITLE]}...'
            else:
                title = parent.title
            newSection.title = f'{title} Split: {splitCount}'
        else:
            newSection.title = f'{_("New Section")} Split: {splitCount}'
        if parent.goal and not parent.goal.startswith(WARNING):
            parent.goal = f'{WARNING}{parent.goal}'
        if parent.conflict and not parent.conflict.startswith(WARNING):
            parent.conflict = f'{WARNING}{parent.conflict}'
        if parent.outcome and not parent.outcome.startswith(WARNING):
            parent.outcome = f'{WARNING}{parent.outcome}'

        newSection.scType = parent.scType
        newSection.scene = parent.scene
        newSection.date = parent.date
        newSection.time = parent.time
        newSection.day = parent.day
        newSection.lastsDays = parent.lastsDays
        newSection.lastsHours = parent.lastsHours
        newSection.lastsMinutes = parent.lastsMinutes
        return newSection


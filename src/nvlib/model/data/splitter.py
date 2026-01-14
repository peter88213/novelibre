"""Provide a base  class for section and chapter splitting.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod

from nvlib.model.data.chapter import Chapter
from nvlib.model.data.id_generator import new_id
from nvlib.model.data.section import Section
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


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

    def create_section(
        self,
        novel,
        sectionId,
        parent,
        splitCount,
        title,
        appendToPrev,
    ):
        """Create a new section and add it to the novel.
        
        Positional arguments:
            sectionId -- str: ID of the section to create.
            parent -- Section instance: parent section.
            splitCount -- int: number of parent's splittings.
            title -- str: title of the section to create.
            appendToPrev -- boolean: when exporting, append the section
                            to the previous one without separator.
        """

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
        newSection.scType = parent.scType
        newSection.scene = parent.scene
        newSection.date = parent.date
        newSection.time = parent.time
        newSection.day = parent.day
        newSection.lastsDays = parent.lastsDays
        newSection.lastsHours = parent.lastsHours
        newSection.lastsMinutes = parent.lastsMinutes
        novel.sections[sectionId] = newSection

    def split_sections(self, novel):
        """Split sections by inserted chapter and section dividers.
        
        Update a Novel instance by generating new chapters and sections 
        if there are dividers within the section content.
        
        Positional arguments: 
            novel -- Novel instance to update.
        
        Return True if the sructure has changed, 
        otherwise return False.        
        """

        # Process chapters and sections.
        sectionsSplit = False
        chIndex = 0
        newLines = []
        for scanChId in novel.tree.get_children(CH_ROOT):
            scList = novel.tree.get_children(scanChId)
            novel.tree.delete_children(scanChId)
            chId = scanChId
            for scanScId in scList:
                scId = scanScId
                novel.tree.append(chId, scId)
                if not self._contains_heading(novel, scId):
                    continue

                lines = self._get_lines(novel, scanScId)
                newLines.clear()
                inSection = True
                sectionSplitCount = 0

                # Search section content for dividers.
                for line in lines:
                    plainLine = self._stripped_line(line)

                    if '#' in plainLine:
                        heading = plainLine.strip('# ').split(
                            self.DESC_SEPARATOR)
                        title = heading[0]
                        if len(heading) > 1:
                            desc = heading[1].strip()
                        else:
                            desc = ''

                    if plainLine.startswith(self.SECTION_SEPARATOR):
                        # Split the section.
                        if inSection:
                            self._set_text(novel, scId, newLines)
                        newLines.clear()
                        sectionSplitCount += 1
                        newScId = new_id(
                            novel.sections,
                            prefix=SECTION_PREFIX,
                        )
                        self.create_section(
                            novel,
                            newScId,
                            novel.sections[scId],
                            sectionSplitCount,
                            title,
                            desc,
                            plainLine.startswith(
                                self.APPENDED_SECTION_SEPARATOR)
                        )
                        novel.tree.append(chId, newScId)
                        scId = newScId
                        sectionsSplit = True
                        inSection = True

                    elif plainLine.startswith(self.CHAPTER_SEPARATOR):
                        # Start a new chapter.
                        if inSection:
                            self._set_text(novel, scId, newLines)
                            newLines.clear()
                            inSection = False
                        newChId = new_id(
                            novel.chapters,
                            prefix=CHAPTER_PREFIX,
                        )
                        if not title:
                            title = _('New Chapter')
                        self.create_chapter(novel, newChId, title, desc, 2)
                        chIndex += 1
                        novel.tree.insert(CH_ROOT, chIndex, newChId)
                        chId = newChId
                        sectionsSplit = True

                    elif plainLine.startswith(self.PART_SEPARATOR):
                        # start a new part.
                        if inSection:
                            self._set_text(novel, scId, newLines)
                            newLines.clear()
                            inSection = False
                        newChId = new_id(
                            novel.chapters,
                            prefix=CHAPTER_PREFIX,
                        )
                        if not title:
                            title = _('New Part')
                        self.create_chapter(novel, newChId, title, desc, 1)
                        chIndex += 1
                        novel.tree.insert(CH_ROOT, chIndex, newChId)
                        chId = newChId

                    elif not inSection:
                        # Append a section without heading to
                        # a new chapter or part.
                        newLines.append(line)
                        sectionSplitCount += 1
                        newScId = new_id(
                            novel.sections,
                            prefix=SECTION_PREFIX,
                        )
                        self.create_section(
                            novel,
                            newScId,
                            novel.sections[scId],
                            sectionSplitCount,
                            '',
                            '',
                            False,
                        )
                        novel.tree.append(chId, newScId)
                        scId = newScId
                        sectionsSplit = True
                        inSection = True

                    else:
                        newLines.append(line)

                if inSection:
                    self._set_text(novel, scId, newLines)
            chIndex += 1
        return sectionsSplit

    def _contains_heading(self, novel, scId):
        return True

    @abstractmethod
    def _get_lines(self, novel, scanScId):
        pass

    @abstractmethod
    def _set_text(self, novel, scId, newLines):
        pass

    def _stripped_line(self, line):
        return line

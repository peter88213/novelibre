"""Provide a helper class for section and chapter splitting.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re

from nvlib.model.data.chapter import Chapter
from nvlib.model.data.id_generator import new_id
from nvlib.model.data.section import Section
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


class Splitter:
    """Helper class for section and chapter splitting.
    
    When importing sections to novelibre, they may contain manually inserted section and chapter dividers.
    The Splitter class updates a Novel instance by splitting such sections and creating new chapters and sections. 
    
    Public class constants:
        PART_SEPARATOR -- marker indicating the beginning of a new part, splitting a section.
        CHAPTER_SEPARATOR -- marker indicating the beginning of a new chapter, splitting a section.
        SCENE_SEPARATOR -- marker indicating the beginning of a new section, splitting a section.
        DESC_SEPARATOR -- marker separating title and description of a chapter or section.
    """
    PART_SEPARATOR = '#'
    CHAPTER_SEPARATOR = '##'
    SCENE_SEPARATOR = '###'
    APPENDED_SCENE_SEPARATOR = '####'
    DESC_SEPARATOR = '|'
    _CLIP_TITLE = 20
    # Maximum length of newly generated section titles.

    def split_sections(self, novel):
        """Split sections by inserted chapter and section dividers.
        
        Update a Novel instance by generating new chapters and sections 
        if there are dividers within the section content.
        
        Positional argument: 
            novel -- Novel instance to update.
        
        Return True if the sructure has changed, 
        otherwise return False.        
        """

        def create_chapter(chapterId, title, desc, level):
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

        def create_section(sectionId, parent, splitCount, title, desc, appendToPrev):
            """Create a new section and add it to the novel.
            
            Positional arguments:
                sectionId -- str: ID of the section to create.
                parent -- Section instance: parent section.
                splitCount -- int: number of parent's splittings.
                title -- str: title of the section to create.
                desc -- str: description of the section to create.
                appendToPrev -- boolean: when exporting, append the section to the previous one without separator.
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
            if desc:
                newSection.desc = desc
            if parent.desc and not parent.desc.startswith(WARNING):
                parent.desc = f'{WARNING}{parent.desc}'
            if parent.goal and not parent.goal.startswith(WARNING):
                parent.goal = f'{WARNING}{parent.goal}'
            if parent.conflict and not parent.conflict.startswith(WARNING):
                parent.conflict = f'{WARNING}{parent.conflict}'
            if parent.outcome and not parent.outcome.startswith(WARNING):
                parent.outcome = f'{WARNING}{parent.outcome}'

            # Reset the parent's status to Draft, if not Outline.
            if parent.status > 2:
                parent.status = 2
            newSection.status = parent.status
            newSection.scType = parent.scType
            newSection.scene = parent.scene
            newSection.date = parent.date
            newSection.time = parent.time
            newSection.day = parent.day
            newSection.lastsDays = parent.lastsDays
            newSection.lastsHours = parent.lastsHours
            newSection.lastsMinutes = parent.lastsMinutes
            novel.sections[sectionId] = newSection

        # Process chapters and sections.
        sectionsSplit = False
        chIndex = 0
        for scanChId in novel.tree.get_children(CH_ROOT):
            scList = novel.tree.get_children(scanChId)
            novel.tree.delete_children(scanChId)
            chId = scanChId
            for scanScId in scList:
                scId = scanScId
                novel.tree.append(chId, scId)
                if not novel.sections[scId].sectionContent:
                    continue

                if not '#' in novel.sections[scId].sectionContent:
                    continue

                sectionContent = novel.sections[scanScId].sectionContent.replace('</p>', '</p>\n')
                lines = sectionContent.split('\n')
                newLines = []
                inSection = True
                sectionSplitCount = 0

                # Search section content for dividers.
                for line in lines:
                    plainLine = re.sub(r'\<.*?\>', '', line)

                    if '#' in plainLine:
                        heading = plainLine.strip('# ').split(self.DESC_SEPARATOR)
                        title = heading[0]
                        desc = ''
                        if len(heading) > 1:
                            desc = heading[1]

                    if plainLine.startswith(self.SCENE_SEPARATOR):
                        # Split the section.
                        if inSection:
                            novel.sections[scId].sectionContent = ''.join(newLines)
                        newLines = []
                        sectionSplitCount += 1
                        newScId = new_id(novel.sections, prefix=SECTION_PREFIX)
                        create_section(
                            newScId,
                            novel.sections[scId],
                            sectionSplitCount,
                            title,
                            desc,
                            plainLine.startswith(self.APPENDED_SCENE_SEPARATOR)
                        )
                        novel.tree.append(chId, newScId)
                        scId = newScId
                        sectionsSplit = True
                        inSection = True

                    elif plainLine.startswith(self.CHAPTER_SEPARATOR):
                        # Start a new chapter.
                        if inSection:
                            novel.sections[scId].sectionContent = ''.join(newLines)
                            newLines = []
                            sectionSplitCount = 0
                            inSection = False
                        newChId = new_id(novel.chapters, prefix=CHAPTER_PREFIX)
                        if not title:
                            title = _('New Chapter')
                        create_chapter(newChId, title, desc, 2)
                        chIndex += 1
                        novel.tree.insert(CH_ROOT, chIndex, newChId)
                        chId = newChId
                        sectionsSplit = True

                    elif plainLine.startswith(self.PART_SEPARATOR):
                        # start a new part.
                        if inSection:
                            novel.sections[scId].sectionContent = ''.join(newLines)
                            newLines = []
                            sectionSplitCount = 0
                            inSection = False
                        newChId = new_id(novel.chapters, prefix=CHAPTER_PREFIX)
                        if not title:
                            title = _('New Part')
                        create_chapter(newChId, title, desc, 1)
                        chIndex += 1
                        novel.tree.insert(CH_ROOT, chIndex, newChId)
                        chId = newChId

                    elif not inSection:
                        # Append a section without heading to a new chapter or part.
                        newLines.append(line)
                        sectionSplitCount += 1
                        newScId = new_id(novel.sections, prefix=SECTION_PREFIX)
                        create_section(newScId, novel.sections[scId], sectionSplitCount, '', '', False)
                        novel.tree.append(chId, newScId)
                        scId = newScId
                        sectionsSplit = True
                        inSection = True

                    else:
                        newLines.append(line)

                if inSection:
                    novel.sections[scId].sectionContent = '\n'.join(newLines)
            chIndex += 1
        return sectionsSplit

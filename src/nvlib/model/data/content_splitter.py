"""Provide a helper class for section and chapter splitting.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re

from nvlib.model.data.id_generator import new_id
from nvlib.model.data.splitter import Splitter
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


class ContentSplitter(Splitter):
    """Helper class for section and chapter splitting.
    
    When importing sections to novelibre, they may contain manually 
    inserted section and chapter dividers.
    The Splitter class updates a Novel instance by splitting such sections 
    and creating new chapters and sections. 
    """

    def create_section(
        self,
        novel,
        sectionId,
        parent,
        splitCount,
        title,
        desc,
        appendToPrev,
    ):
        """Create a new section and add it to the novel.
        
        Positional arguments:
            sectionId -- str: ID of the section to create.
            parent -- Section instance: parent section.
            splitCount -- int: number of parent's splittings.
            title -- str: title of the section to create.
            desc -- str: description of the section to create.
            appendToPrev -- boolean: when exporting, append the section
                            to the previous one without separator.
        """
        super().create_section(
            novel,
            sectionId,
            parent,
            splitCount,
            title,
            appendToPrev,
        )
        if desc:
            novel.sections[sectionId].desc = desc
        if parent.desc and not parent.desc.startswith(self._WARNING):
            parent.desc = f'{self._WARNING}{parent.desc}'

        # Reset the parent's status to Draft, if not Outline.
        if parent.status > 2:
            parent.status = 2
        novel.sections[sectionId].status = parent.status

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
                if not novel.sections[scId].sectionContent:
                    continue

                if not '#' in novel.sections[scId].sectionContent:
                    continue

                sectionContent = novel.sections[scanScId].sectionContent
                sectionContent = sectionContent.replace('</p>', '</p>\n')
                lines = sectionContent.split('\n')
                newLines.clear()
                inSection = True
                sectionSplitCount = 0

                # Search section content for dividers.
                for line in lines:
                    plainLine = re.sub(r'\<.*?\>', '', line)

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
                            novel.sections[scId].sectionContent = ''.join(
                                newLines)
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
                            novel.sections[scId].sectionContent = ''.join(
                                newLines)
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
                            novel.sections[scId].sectionContent = ''.join(
                                newLines)
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
                    novel.sections[scId].sectionContent = '\n'.join(
                        newLines)
            chIndex += 1
        return sectionsSplit

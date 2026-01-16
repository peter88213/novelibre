"""Provide a helper class for section and chapter splitting.

Splitting sections by headings in the section content.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re

from nvlib.model.data.splitter import Splitter


class ContentSplitter(Splitter):
    """Helper class for section and chapter splitting by content.
    
    When importing sections to novelibre, the contents may contain manually 
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
                            
        Extends the superclass method.
        """
        super().create_section(
            novel,
            sectionId,
            parent,
            splitCount,
            title,
            appendToPrev,
        )
        WARNING = '(!)'
        if desc:
            novel.sections[sectionId].desc = desc

        # Reset the parent's status to Draft, if not Outline.
        if parent.status > 2:
            parent.status = 2
        novel.sections[sectionId].status = parent.status

        # Mark parent's metadata with a reminder.
        if parent.desc and not parent.desc.startswith(WARNING):
            parent.desc = f'{WARNING}{parent.desc}'
        if parent.goal and not parent.goal.startswith(WARNING):
            parent.goal = f'{WARNING}{parent.goal}'
        if parent.conflict and not parent.conflict.startswith(WARNING):
            parent.conflict = f'{WARNING}{parent.conflict}'
        if parent.outcome and not parent.outcome.startswith(WARNING):
            parent.outcome = f'{WARNING}{parent.outcome}'

    def _contains_heading(self, novel, scId):
        return (
            novel.sections[scId].sectionContent and
            '#' in novel.sections[scId].sectionContent
        )

    def _get_lines(self, novel, scanScId):
        sectionContent = novel.sections[scanScId].sectionContent
        sectionContent = sectionContent.replace('</p>', '</p>\n')
        return sectionContent.split('\n')

    def _set_text(self, novel, scId, newLines):
        novel.sections[scId].sectionContent = ''.join(newLines)

    def _stripped_line(self, line):
        return re.sub(r'\<.*?\>', '', line)

"""Provide a helper class for section and chapter splitting.

Splitting sections by headings in the descriptions.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.splitter import Splitter


class DescSplitter(Splitter):
    """Helper class for section and chapter splitting by description.
    
    When importing sections to novelibre, the descriptions may contain 
    manually inserted section and chapter dividers.
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
        novel.sections[sectionId].status = 0

    def _contains_heading(self, novel, scId):
        return (
            novel.sections[scId].desc and
            '#' in novel.sections[scId].desc
        )

    def _get_lines(self, novel, scanScId):
        return novel.sections[scanScId].desc.split('\n')

    def _set_text(self, novel, scId, newLines):
        novel.sections[scId].desc = '\n'.join(newLines)


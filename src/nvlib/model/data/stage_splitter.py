"""Provide a helper class for stage splitting.

Splitting sections by headings in the descriptions.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.desc_splitter import DescSplitter
from nvlib.model.data.id_generator import new_id
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import SECTION_PREFIX


class StageSplitter(DescSplitter):
    """Helper class for stage splitting by description.
    
    When importing stages to novelibre, the descriptions may contain 
    manually inserted stage headings.
    The Splitter class updates a Novel instance by splitting such sections 
    and creating new stages.    
    """

    def create_section(
        self,
        novel,
        sectionId,
        parent,
        splitCount,
        title,
        level,
    ):
        """Create a new section and add it to the novel.
        
        Positional arguments:
            sectionId -- str: ID of the section to create.
            parent -- Section instance: parent section.
            splitCount -- int: number of parent's splittings.
            title -- str: title of the section to create.
            level -- int: level of the stage to create.
        """
        super().create_section(
            novel,
            sectionId,
            parent,
            splitCount,
            title,
            '',
            False,
        )
        novel.sections[sectionId].scType = level + 1

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
                        title = plainLine.strip('# ')

                        # Split the section.
                        if plainLine.startswith(self.CHAPTER_SEPARATOR):
                            level = 2
                        elif plainLine.startswith(self.PART_SEPARATOR):
                            level = 1

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
                            level,
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

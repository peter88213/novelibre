"""Provide a helper class for chapter splitting.

Splitting sections by headings in the descriptions.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.splitter import Splitter
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.model.data.id_generator import new_id


class ChapterSplitter(Splitter):
    """Helper class for chapter splitting by description.
    
    When importing chapters to novelibre, the descriptions may contain 
    manually inserted section and chapter dividers.
    The Splitter class updates a Novel instance by splitting such chapters 
    and creating new chapters.    
    """

    def split_sections(self, novel):
        """Split chapters by inserted chapter dividers.
        
        Update a Novel instance by generating new chapters 
        if there are dividers within the chapter description.
        
        Positional arguments: 
            novel -- Novel instance to update.
        
        Return True if the sructure has changed, 
        otherwise return False.        
        """

        # Process chapters and sections.
        chaptersSplit = False
        chIndex = 0
        newLines = []
        for scanChId in novel.tree.get_children(CH_ROOT):
            chId = scanChId
            if self._contains_heading(novel, chId):
                lines = self._get_lines(novel, scanChId)
                newLines.clear()
                inChapter = True
                chapterSplitCount = 0

                # Search chapter desc for dividers.
                for line in lines:
                    plainLine = self._stripped_line(line)

                    if '#' in plainLine:
                        title = plainLine.strip('# ')

                        # Split the section.
                        if plainLine.startswith(self.CHAPTER_SEPARATOR):
                            level = 2
                        elif plainLine.startswith(self.PART_SEPARATOR):
                            level = 1

                        if inChapter:
                            self._set_text(novel, chId, newLines)

                        newLines.clear()
                        chapterSplitCount += 1
                        newChId = new_id(
                            novel.chapters,
                            prefix=CHAPTER_PREFIX,
                        )
                        self.create_chapter(
                            novel,
                            newChId,
                            title,
                            '',
                            level,
                        )
                        chIndex += 1
                        novel.tree.insert(CH_ROOT, chIndex, newChId)
                        chId = newChId
                        chaptersSplit = True
                        inChapter = True

                    else:
                        newLines.append(line)
                if inChapter:
                    self._set_text(novel, chId, newLines)
            chIndex += 1
        return chaptersSplit

    def _contains_heading(self, novel, chId):
        return (
            novel.chapters[chId].desc and
            '#' in novel.chapters[chId].desc
        )

    def _get_lines(self, novel, scanChId):
        return novel.chapters[scanChId].desc.split('\n')

    def _set_text(self, novel, chId, newLines):
        novel.chapters[chId].desc = '\n'.join(newLines)


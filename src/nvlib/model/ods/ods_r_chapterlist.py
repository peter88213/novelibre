"""Provide a class for ODS chapter list import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.chapter import Chapter
from nvlib.model.data.id_generator import new_id
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import CHAPTERLIST_SUFFIX
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.nv_locale import _


class OdsRChapterList(OdsReader):
    """ODS chapter list reader."""

    DESCRIPTION = _('Chapter table')
    SUFFIX = CHAPTERLIST_SUFFIX
    _columnTitles = [
        'ID',
        'Chapter',
        'Title',
        'Description',
        'Notes',
    ]
    _idPrefix = CHAPTER_PREFIX,

    def add_new_element(self, prevId, row, level=2):
        """Add a new chapter to the tree.
        
        Positional arguments:
            prevId : str -- previous tree element, 
                            None if the new element is at the first place.
            row : List of the new element's properties. 
                  Used to determine whether a title is given.
        
        If a title is given:
            Create a Chapter instance,
            place its ID it after prevId in the tree,
            Return the chapter ID.
        Otherwise, return an empty string.
        """
        if not row[2]:
            return ''

        newId = new_id(self.novel.chapters, prefix=CHAPTER_PREFIX)
        self.novel.chapters[newId] = Chapter(
            chLevel=level,
            chType=0,
            noNumber=False,
            isTrash=False,
            hasEpigraph=False,
        )
        if prevId:
            index = self.novel.tree.get_children(CH_ROOT).index(prevId) + 1
        else:
            index = 0
        self.novel.tree.insert(CH_ROOT, index, newId)
        self.projectStructureModified = True
        return newId

    def read(self):
        """Parse the ODS file located at filePath.
        
        Fetch the Chapter attributes contained.
        Extends the superclass method.
        """
        super().read()
        self._read_chapters()


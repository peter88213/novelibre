"""Provide a class for ODS chapter list import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHAPTERLIST_SUFFIX
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
    _idPrefix = CHAPTER_PREFIX

    def read(self):
        """Parse the ODS file located at filePath.
        
        Fetch the Chapter attributes contained.
        Extends the superclass method.
        """
        super().read()

        for chId in self.novel.chapters:

            #--- name
            try:
                title = self._columnDict['Title'][chId]
            except:
                pass
            else:
                self.novel.chapters[chId].title = title.rstrip()

            #--- desc
            try:
                desc = self._columnDict['Description'][chId]
            except:
                pass
            else:
                self.novel.chapters[chId].desc = desc.rstrip()

            #--- notes
            try:
                notes = self._columnDict['Notes'][chId]
            except:
                pass
            else:
                self.novel.chapters[chId].notes = notes.rstrip()


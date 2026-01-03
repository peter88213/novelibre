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
    _idPrefix = CHAPTER_PREFIX,

    def read(self):
        """Parse the ODS file located at filePath.
        
        Fetch the Chapter attributes contained.
        Extends the superclass method.
        """
        super().read()
        self._read_chapters()


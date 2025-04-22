"""Provide a class for ODS chapter list import.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHAPTERLIST_SUFFIX
from nvlib.nv_locale import _


class OdsRChapterList(OdsReader):
    """ODS chapter list reader."""

    DESCRIPTION = _('Chapter list')
    SUFFIX = CHAPTERLIST_SUFFIX
    _columnTitles = ['ID', 'Chapter', 'Title', 'Description', 'Epigraph', 'Source', 'Notes']
    _idPrefix = CHAPTER_PREFIX

    def read(self):
        """Parse the ODS file located at filePath, fetching the Chapter attributes contained.

        Extends the superclass method.
        """
        super().read()

        for chId in self.novel.chapters:

            #--- name
            try:
                title = self._columns['Title'][chId]
            except:
                pass
            else:
                self.novel.chapters[chId].title = title.rstrip()

            #--- desc
            try:
                desc = self._columns['Description'][chId]
            except:
                pass
            else:
                self.novel.chapters[chId].desc = desc.rstrip()

            #--- notes
            try:
                notes = self._columns['Notes'][chId]
            except:
                pass
            else:
                self.novel.chapters[chId].notes = notes.rstrip()

            #--- epigraph
            try:
                epigraph = self._columns['Epigraph'][chId]
            except:
                pass
            else:
                self.novel.chapters[chId].epigraph = epigraph.rstrip()

            #--- epigraphSrc
            try:
                epigraphSrc = self._columns['Source'][chId]
            except:
                pass
            else:
                self.novel.chapters[chId].epigraphSrc = epigraphSrc.rstrip()


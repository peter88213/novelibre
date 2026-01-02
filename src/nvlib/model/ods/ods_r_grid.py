"""Provide a class for ODS plot grid import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import GRID_SUFFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


class OdsRGrid(OdsReader):
    """ODS section list reader. """
    DESCRIPTION = _('Plot grid')
    SUFFIX = GRID_SUFFIX
    COLUMN_TITLES = [
        'ID',
        'Section',
        'Date',
        'Time',
        'Day',
        'Duration',
        'Title',
        'Description',
        'Viewpoint',
        'Tags',
        'Scene',
        'Goal',
        'Conflict',
        'Outcome',
        'Notes',
    ]
    _idPrefix = SECTION_PREFIX

    def read(self):
        """Parse the ODS file located at filePath.
        
        Fetch the Section attributes contained.
        Extends the superclass method.
        """
        self._columnTitles = self.COLUMN_TITLES[:]
        for plId in self.novel.plotLines:
            self._columnTitles.append(plId)
        super().read()
        self._read_sections()

        #--- plot line titles
        for i, column in enumerate(self._rows[0]):
            if column.startswith(PLOT_LINE_PREFIX):
                self.novel.plotLines[column].title = self._rows[1][i]


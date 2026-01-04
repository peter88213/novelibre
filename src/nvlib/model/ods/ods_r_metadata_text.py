"""Provide a class for ODS metadata text import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import METADATA_TEXT_SUFFIX, CHAPTER_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import PRJ_NOTE_PREFIX
from nvlib.novx_globals import ROOT_PREFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


class OdsRMetadataText(OdsReader):
    """ODS section list reader. """
    DESCRIPTION = _('Metadata text')
    SUFFIX = METADATA_TEXT_SUFFIX
    COLUMN_TITLES = [
        'ID',
        'Title',
        'Full name',
        'Aka',
        'Description',
        'Bio',
        'Goals',
        'Notes',
        'Tags',
        'Goal',
        'Conflict',
        'Outcome',
    ]
    _idPrefix = (
        CHARACTER_PREFIX,
        CHAPTER_PREFIX,
        ITEM_PREFIX,
        LOCATION_PREFIX,
        SECTION_PREFIX,
        PLOT_LINE_PREFIX,
        PLOT_POINT_PREFIX,
        PRJ_NOTE_PREFIX,
        ROOT_PREFIX,
    )

    def read(self):
        """Parse the ODS file located at filePath.
        
        Fetch the Section attributes contained.
        Extends the superclass method.
        """
        self._columnTitles = self.COLUMN_TITLES[:]
        for plId in self.novel.plotLines:
            self._columnTitles.append(plId)
        super().read()
        self._read_basic_element(self.novel, ROOT_PREFIX)
        self._read_chapters()
        self._read_characters()
        self._read_items()
        self._read_locations()
        self._read_sections()
        self._read_plotlines()
        self._read_plot_points()
        self._read_project_notes()


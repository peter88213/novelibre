"""Provide a class for ODS location list import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import LOCLIST_SUFFIX
from nvlib.nv_locale import _


class OdsRLocList(OdsReader):
    """ODS location list reader. """
    DESCRIPTION = _('Location table')
    SUFFIX = LOCLIST_SUFFIX
    _columnTitles = [
        'ID',
        'Name',
        'Description',
        'Aka',
        'Tags',
        'Notes',
    ]
    _idPrefix = LOCATION_PREFIX,

    def read(self):
        """Parse the ODS file located at filePath.
        
        Fetch the location attributes contained.
        Extends the superclass method.
        """
        super().read()
        self._read_locations()


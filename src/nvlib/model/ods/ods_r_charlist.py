"""Provide a class for ODS character list import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CHARLIST_SUFFIX
from nvlib.nv_locale import _


class OdsRCharList(OdsReader):
    """ODS character list reader."""
    DESCRIPTION = _('Character table')
    SUFFIX = CHARLIST_SUFFIX
    _columnTitles = [
        'ID',
        'Name',
        'Full name',
        'Aka',
        'Description',
        'Bio',
        'Goals',
        'Importance',
        'Tags',
        'Notes',
    ]
    _idPrefix = CHARACTER_PREFIX

    def read(self):
        """Parse the ODS file located at filePath. 
        
        Fetch the Character attributes contained.
        Extends the superclass method.
        """
        super().read()
        self._read_characters()


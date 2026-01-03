"""Provide a class for ODS item list import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import ITEMLIST_SUFFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.nv_locale import _


class OdsRItemList(OdsReader):
    """ODS item list reader."""
    DESCRIPTION = _('Item table')
    SUFFIX = ITEMLIST_SUFFIX
    _columnTitles = [
        'ID',
        'Name',
        'Description',
        'Aka',
        'Tags',
        'Notes',
    ]
    _idPrefix = ITEM_PREFIX,

    def read(self):
        """Parse the ODS file located at filePath.
        
        Fetch the item attributes contained.
        Extends the superclass method.
        """
        super().read()
        self._read_items()


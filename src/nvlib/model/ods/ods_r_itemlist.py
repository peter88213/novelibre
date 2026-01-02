"""Provide a class for ODS item list import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import ITEMLIST_SUFFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import string_to_list
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
    _idPrefix = ITEM_PREFIX

    def read(self):
        """Parse the ODS file located at filePath.
        
        Fetch the item attributes contained.
        Extends the superclass method.
        """
        super().read()
        for itId in self.novel.items:

            #--- name
            try:
                title = self._columnDict['Name'][itId]
            except:
                pass
            else:
                self.novel.items[itId].title = title.rstrip()

            #--- desc
            try:
                desc = self._columnDict['Description'][itId]
            except:
                pass
            else:
                self.novel.items[itId].desc = desc.rstrip()

            #--- aka
            try:
                aka = self._columnDict['Aka'][itId]
            except:
                pass
            else:
                self.novel.items[itId].aka = aka.rstrip()

            #--- tags
            try:
                tags = self._columnDict['Tags'][itId]
            except:
                pass
            else:
                if tags:
                    self.novel.items[itId].tags = string_to_list(
                        tags,
                        divider=self._DIVIDER,
                    )

            #--- notes
            try:
                notes = self._columnDict['Notes'][itId]
            except:
                pass
            else:
                self.novel.items[itId].notes = notes.rstrip()


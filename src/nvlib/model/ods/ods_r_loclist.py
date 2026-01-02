"""Provide a class for ODS location list import.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import LOCLIST_SUFFIX
from nvlib.novx_globals import string_to_list
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
    _idPrefix = LOCATION_PREFIX

    def read(self):
        """Parse the ODS file located at filePath.
        
        Fetch the location attributes contained.
        Extends the superclass method.
        """
        super().read()
        for lcId in self.novel.locations:

            #--- name
            try:
                title = self._columnDict['Name'][lcId]
            except:
                pass
            else:
                self.novel.locations[lcId].title = title.rstrip()

            #--- desc
            try:
                desc = self._columnDict['Description'][lcId]
            except:
                pass
            else:
                self.novel.locations[lcId].desc = desc.rstrip()

            #--- aka
            try:
                aka = self._columnDict['Aka'][lcId]
            except:
                pass
            else:
                self.novel.locations[lcId].aka = aka.rstrip()

            #--- tags
            try:
                tags = self._columnDict['Tags'][lcId]
            except:
                pass
            else:
                if tags:
                    self.novel.locations[lcId].tags = string_to_list(
                        tags,
                        divider=self._DIVIDER,
                    )

            #--- notes
            try:
                notes = self._columnDict['Notes'][lcId]
            except:
                pass
            else:
                self.novel.locations[lcId].notes = notes.rstrip()


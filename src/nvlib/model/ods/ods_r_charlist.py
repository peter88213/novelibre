"""Provide a class for ODS character list import.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.character import Character
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CHARLIST_SUFFIX
from nvlib.novx_globals import string_to_list
from nvlib.nv_locale import _


class OdsRCharList(OdsReader):
    """ODS character list reader."""
    DESCRIPTION = _('Character list')
    SUFFIX = CHARLIST_SUFFIX
    _columnTitles = ['ID', 'Name', 'Full name', 'Aka', 'Description', 'Bio', 'Goals', 'Importance', 'Tags', 'Notes']
    _idPrefix = CHARACTER_PREFIX

    def read(self):
        """Parse the ODS file located at filePath, fetching the Character attributes contained.

        Extends the superclass method.
        """
        super().read()

        for crId in self.novel.characters:

            #--- name
            try:
                title = self._columns['Name'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].title = title.rstrip()

            #--- fullName
            try:
                fullName = self._columns['Full name'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].fullName = fullName.rstrip()

            #--- desc
            try:
                desc = self._columns['Description'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].desc = desc.rstrip()

            #--- aka
            try:
                desc = self._columns['Aka'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].aka = desc.rstrip()

            #--- tags
            try:
                tags = self._columns['Tags'][crId]
            except:
                pass
            else:
                if tags:
                    self.novel.characters[crId].tags = string_to_list(tags, divider=self._DIVIDER)

            #--- notes
            try:
                notes = self._columns['Section notes'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].notes = notes.rstrip()

            #--- goals
            try:
                goals = self._columns['Goals'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].goals = goals.rstrip()

            #--- bio
            try:
                bio = self._columns['Bio'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].bio = bio.rstrip()

            #--- birthDate
            try:
                birthDate = self._columns['Birth date'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].birthDate = birthDate.rstrip()

            #--- deathDate
            try:
                deathDate = self._columns['Death date'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].deathDate = deathDate.rstrip()

            #--- importance
            try:
                importance = self._columns['Importance'][crId]
            except:
                pass
            else:
                if Character.MAJOR_MARKER in importance:
                    self.novel.characters[crId].isMajor = True
                else:
                    self.novel.characters[crId].isMajor = False


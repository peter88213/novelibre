"""Provide a class for ODS character list import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.character import Character
from nvlib.model.data.id_generator import new_id
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CHARLIST_SUFFIX
from nvlib.novx_globals import CR_ROOT
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
    _idPrefix = CHARACTER_PREFIX,

    def read(self):
        """Parse the ODS file located at filePath. 
        
        Fetch the Character attributes contained.
        Extends the superclass method.
        """
        super().read()
        self._read_characters()

    def add_new_element(self, prevId, row):
        """Add a new character to the tree.
        
        Positional arguments:
            prevId : str -- previous tree element, 
                            None if the new element is at the first place.
            row : List of the new element's properties. 
                  Used to determine whether a name is given.
        
        If a name is given:
            Create a Character instance,
            place its ID it after prevId in the tree,
            Return the character ID.
        Otherwise, return an empty string.
        """
        if not row[1]:
            return ''

        newId = new_id(self.novel.characters, prefix=CHARACTER_PREFIX)
        self.novel.characters[newId] = Character()
        if prevId is not None:
            index = self.novel.tree.get_children(CR_ROOT).index(prevId) + 1
        else:
            index = 0
        self.novel.tree.insert(CR_ROOT, index, newId)
        self.projectStructureModified = True
        return newId

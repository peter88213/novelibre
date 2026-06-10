"""Provide a class for ODS location list import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import LOCATION_PREFIX, ITEM_PREFIX, IT_ROOT
from nvlib.novx_globals import LOCLIST_SUFFIX
from nvlib.nv_locale import _
from nvlib.novx_globals import LC_ROOT
from nvlib.model.data.id_generator import new_id
from nvlib.model.data.world_element import WorldElement


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

    def add_new_element(self, prevId, row):
        """Add a new location to the tree.
        
        Positional arguments:
            prevId : str -- previous tree element, 
                            None if the new element is at the first place.
            row : List of the new element's properties. 
                  Used to determine whether a name is given.
        
        If a name is given:
            Create a location instance,
            place its ID it after prevId in the tree,
            Return the item ID.
        Otherwise, return an empty string.
        """
        if not row[1]:
            return ''

        newId = new_id(self.novel.locations, prefix=LOCATION_PREFIX)
        self.novel.locations[newId] = WorldElement()
        if prevId is not None:
            index = self.novel.tree.get_children(LC_ROOT).index(prevId) + 1
        else:
            index = 0
        self.novel.tree.insert(LC_ROOT, index, newId)
        self.projectStructureModified = True
        return newId

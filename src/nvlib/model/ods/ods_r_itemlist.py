"""Provide a class for ODS item list import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.id_generator import new_id
from nvlib.model.data.world_element import WorldElement
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import ITEMLIST_SUFFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
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

    def add_new_element(self, prevId, row):
        """Add a new item to the tree.
        
        Positional arguments:
            prevId : str -- previous tree element, 
                            None if the new element is at the first place.
            row : List of the new element's properties. 
                  Used to determine whether a name is given.
        
        If a name is given:
            Create an Item instance,
            place its ID it after prevId in the tree,
            Return the item ID.
        Otherwise, return an empty string.
        """
        if not row[1]:
            return ''

        newId = new_id(self.novel.items, prefix=ITEM_PREFIX)
        self.novel.items[newId] = WorldElement()
        if prevId is not None:
            index = self.novel.tree.get_children(IT_ROOT).index(prevId) + 1
        else:
            index = 0
        self.novel.tree.insert(IT_ROOT, index, newId)
        self.projectStructureModified = True
        return newId

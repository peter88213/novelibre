"""Provide a class for a characters/locations/items importer.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.widgets.pick_list import PickList
from novxlib.model.id_generator import create_id
from novxlib.novx.character_data_reader import CharacterDataReader
from novxlib.novx.item_data_reader import ItemDataReader
from novxlib.novx.location_data_reader import LocationDataReader
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import ITEM_PREFIX
from novxlib.novx_globals import IT_ROOT
from novxlib.novx_globals import LC_ROOT
from novxlib.novx_globals import LOCATION_PREFIX
from novxlib.novx_globals import _
from novxlib.novx_globals import norm_path


class NvDataImporter:
    """Characters/locations/items importer with a pick list."""

    def __init__(self, model, view, controller, filePath, elemPrefix):
        """Open a pick list with the elements of the XML data file specified by filePath.
        
        Positional arguments:
            view -- the caller.
            filePath: str -- Path of the XML data file.
            elemPrefix: str -- Prefix of the new element IDs.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        sources = {
            CHARACTER_PREFIX:CharacterDataReader,
            LOCATION_PREFIX:LocationDataReader,
            ITEM_PREFIX:ItemDataReader,
        }
        source = sources[elemPrefix](filePath)
        source.novel = self._mdl.nvService.make_novel()
        errorMessages = {
            CHARACTER_PREFIX:_('No character data found'),
            LOCATION_PREFIX:_('No location data found'),
            ITEM_PREFIX:_('No item data found'),
        }
        try:
            source.read()
        except:
            self._ui.set_status(f"!{errorMessages[elemPrefix]}: {norm_path(filePath)}")
            return

        sourceElements = {
            CHARACTER_PREFIX:source.novel.characters,
            LOCATION_PREFIX:source.novel.locations,
            ITEM_PREFIX:source.novel.items,
        }
        targetElements = {
            CHARACTER_PREFIX:self._mdl.novel.characters,
            LOCATION_PREFIX:self._mdl.novel.locations,
            ITEM_PREFIX:self._mdl.novel.items,
        }
        elemParents = {
            CHARACTER_PREFIX:CR_ROOT,
            LOCATION_PREFIX:LC_ROOT,
            ITEM_PREFIX:IT_ROOT,
        }
        windowTitles = {
            CHARACTER_PREFIX:_('Select characters'),
            LOCATION_PREFIX:_('Select locations'),
            ITEM_PREFIX:_('Select items'),
        }
        self._elemPrefix = elemPrefix
        self._sourceElements = sourceElements[elemPrefix]
        self._targetElements = targetElements[elemPrefix]
        self._elemParent = elemParents[elemPrefix]
        pickButtonLabel = _('Import selected elements')
        offset = 50
        size = '300x400'
        __, x, y = self._ui.root.geometry().split('+')
        windowGeometry = f'{size}+{int(x)+offset}+{int(y)+offset}'
        PickList(
            windowTitles[elemPrefix],
            windowGeometry,
            self._sourceElements,
            pickButtonLabel,
            self._pick_element
            )

    def _pick_element(self, elements):
        """Add the selected elements to the novel."""
        i = 0
        for  elemId in elements:
            newId = create_id(self._targetElements, prefix=self._elemPrefix)
            self._targetElements[newId] = self._sourceElements[elemId]
            self._mdl.novel.tree.append(self._elemParent, newId)
            i += 1
        if i > 0:
            self._ui.tv.go_to_node(newId)
            self._ui.set_status(f'{i} {_("elements imported")}')

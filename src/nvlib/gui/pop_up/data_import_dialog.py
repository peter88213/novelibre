"""Provide a class for a data import dialog.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.sub_controller import SubController
from nvlib.gui.widgets.pick_list import PickList
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.nv_locale import _


class DataImportDialog(SubController):
    """Elements importer with a pop-up pick list."""
    OFFSET = 50
    MIN_WIDTH = 300
    MIN_HEIGHT = 200

    def __init__(self, view, controller, sourceElements, prefix):
        """Open a pick list with source elements of type specified by prefix.
        
        The "Import selected elements" button is linked to the 
        _import_selected_elements() method.
        
        Positional arguments:
            sourceElements: dict (tag: element ID, value: element)
            prefix: str -- Prefix of the new element IDs.
        """
        if not sourceElements:
            return

        self._ui = view
        self._ctrl = controller

        __, x, y = self._ui.root.geometry().split('+')
        windowGeometry = f'+{int(x)+self.OFFSET}+{int(y)+self.OFFSET}'
        windowTitles = {
            CHARACTER_PREFIX:_('Select characters'),
            LOCATION_PREFIX:_('Select locations'),
            ITEM_PREFIX:_('Select items'),
            PLOT_LINE_PREFIX:_('Select plot lines'),
        }
        pickList = PickList(
            windowTitles[prefix],
            windowGeometry,
            sourceElements,
            _('Import selected elements'),
            self._import_selected_elements
            )
        pickList.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

    def _import_selected_elements(self, selectedIds):
        # Callback function for the data import pick list.
        self._ctrl.dataImporter.add_elements(selectedIds)

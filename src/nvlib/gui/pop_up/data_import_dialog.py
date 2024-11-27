"""Provide a class for a data import dialog.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.pop_up.data_import_ctrl import DataImportCtrl
from nvlib.gui.widgets.pick_list import PickList
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import _


class DataImportDialog(DataImportCtrl):
    """Elements importer with a pop-up pick list."""
    OFFSET = 50
    MIN_WIDTH = 300
    MIN_HEIGHT = 200

    def __init__(self, model, view, controller, sourceElements, prefix):
        """Open a pick list with the elements of the XML data file specified by filePath.
        
        Positional arguments:
            elemPrefix: str -- Prefix of the new element IDs.
        """
        if not sourceElements:
            return

        self.initialize_controller(model, view, controller)

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
            self.add_elements
            )
        pickList.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)


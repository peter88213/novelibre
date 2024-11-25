"""Provide a mixin class for controlling the location properties view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.properties_window.world_element_view_ctrl import WorldElementViewCtrl


class LocationViewCtrl(WorldElementViewCtrl):

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.locations[elementId]
        super().set_data(elementId)

"""Provide a class for viewing and editing location properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.properties_window.location_view_ctrl import LocationViewCtrl
from nvlib.gui.properties_window.world_element_view import WorldElementView


class LocationView(WorldElementView, LocationViewCtrl):
    """Class for viewing and editing location properties."""

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        self.prefsShowLinks = 'show_lc_links'


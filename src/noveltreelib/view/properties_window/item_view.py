"""Provide a class for viewing and editing item properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from noveltreelib.view.properties_window.world_element_view import WorldElementView


class ItemView(WorldElementView):
    """Class for viewing and editing item properties."""

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        self._prefsShowLinks = 'show_it_links'

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.items[elementId]
        super().set_data(elementId)

"""Provide a class for viewing and editing stage properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.properties_window.basic_view import BasicView


class StageView(BasicView):
    """Class for viewing and editing stage properties."""

    def __init__(self, parent, model, view, controller):
        super().__init__(parent, model, view, controller)
        self._prefsShowLinks = 'show_st_links'

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.sections[elementId]
        super().set_data(elementId)

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

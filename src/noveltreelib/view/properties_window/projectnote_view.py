"""Provide a class for viewing and editing project notes.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from noveltreelib.view.properties_window.basic_view import BasicView


class ProjectnoteView(BasicView):
    """Class for viewing and editing project notes."""

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.projectNotes[elementId]
        super().set_data(elementId)

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_button_bar()

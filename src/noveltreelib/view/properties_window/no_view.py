"""Provide a class for viewing nothing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from noveltreelib.view.properties_window.basic_view import BasicView


class NoView(BasicView):
    """Class for viewing and editing location properties."""

    def focus_title(self):
        """Do not try to give the focus to a non-existent entry.
        
        Overwrites the superclass method.
        """
        pass

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass constructor.
        """
        super().set_data(elementId)

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        pass

"""Provide a class for viewing nothing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.view.properties_window.basic_view import BasicView


class NoView(BasicView):
    """Class for viewing and editing location properties."""

    def focus_title(self):
        """Do not try to give the focus to a non-existent entry.
        
        Overwrites the superclass method.
        """
        pass

    def lock(self):
        """Inhibit element change.

        Overrides the superclass method.
        """

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Overrides the superclass method.
        """
        pass

    def unlock(self):
        """Enable element change.

        Overrides the superclass method.
        """

    def _create_frames(self):
        """Template method for creating the frames in the right pane.

        Overrides the superclass method.
        """
        pass


"""Provide a class for viewing nothing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.properties_window.basic_view import BasicView
from nvlib.gui.properties_window.no_view_ctrl import NoViewCtrl


class NoView(BasicView, NoViewCtrl):
    """Class for viewing nothing."""

    def focus_title(self):
        """Do not try to give the focus to a non-existent entry.
        
        Overrides the superclass method.
        """
        pass

    def _create_frames(self):
        """Template method for creating the frames in the right pane.

        Overrides the superclass method.
        """
        pass


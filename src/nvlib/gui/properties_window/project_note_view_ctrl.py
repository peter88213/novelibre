"""Provide a mixin class for controlling the project notes view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.properties_window.basic_view_ctrl import BasicViewCtrl


class ProjectNoteViewCtrl(BasicViewCtrl):
    """Class for viewing and editing project notes."""

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.projectNotes[elementId]
        super().set_data(elementId)


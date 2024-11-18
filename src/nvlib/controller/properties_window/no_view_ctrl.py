"""Provide a mixin class for controlling the empty view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController


class NoViewCtrl(SubController):

    def apply_changes(self, event=None):
        """Apply changes."""
        pass

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Overrides the superclass method.
        """
        pass


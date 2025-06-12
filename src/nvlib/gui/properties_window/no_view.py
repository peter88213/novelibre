"""Provide a class for viewing nothing.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.properties_window.basic_view import BasicView


class NoView(BasicView):
    """Class for viewing nothing."""

    def apply_changes(self, event=None):
        pass

    def focus_title(self):
        pass

    def lock(self):
        pass

    def set_data(self, elementId):
        pass

    def unlock(self):
        pass

    def _create_frames(self):
        pass


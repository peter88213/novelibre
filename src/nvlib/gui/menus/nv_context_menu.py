"""Provide a context menu base class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu


class NvContextMenu(NvMenu):
    """A popup menu that closes under Linux when losing the focus."""

    def __init__(self, view, controller):
        super().__init__(view, controller)
        self.bind('<FocusOut>', self._close)

    def open(self, event):
        try:
            self.tk_popup(event.x_root, event.y_root)
        finally:
            self.grab_release()

    def _close(self, event):
        self.unpost()

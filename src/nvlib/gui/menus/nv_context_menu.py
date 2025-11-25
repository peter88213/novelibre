"""Provide a basic context menu class for a tree view branch.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
import tkinter as tk


class NvContextMenu(tk.Menu, NvMenu):
    """A popup menu that closes under Linux when losing the focus."""

    def __init__(self, master, model, view, controller):
        tk.Menu.__init__(self, master, tearoff=0)
        NvMenu.__init__(self, master, model, view, controller)
        self.bind('<FocusOut>', self._close)

    def _close(self, event):
        self.unpost()

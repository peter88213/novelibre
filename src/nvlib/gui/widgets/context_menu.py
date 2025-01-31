"""Provide a context menu widget.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk


class ContextMenu(tk.Menu):
    """A popup menu that closes under Linux when losing the focus."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<FocusOut>', self._close)

    def _close(self, event):
        self.unpost()

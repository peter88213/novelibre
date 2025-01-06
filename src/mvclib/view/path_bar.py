"""Provide a class for the novelibre path bar.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.view.observer import Observer
import tkinter as tk


class PathBar(Observer, tk.Label):

    COLOR_MODIFIED_BG = 'goldenrod1'
    COLOR_MODIFIED_FG = 'maroon'
    COLOR_NORMAL_BG = 'light gray'
    COLOR_NORMAL_FG = 'black'
    COLOR_LOCKED_BG = 'dim gray'
    COLOR_LOCKED_FG = 'light gray'

    def __init__(self, master, model, **kw):
        tk.Label.__init__(self, master, **kw)
        self._mdl = model

    def refresh(self):
        """Update view components and path bar.
        
        Overrides the superclass method.
        """
        if self._mdl.isModified:
            self.set_modified()
        else:
            self.set_normal()

    def set_locked(self):
        self.config(bg=self.COLOR_LOCKED_BG)
        self.config(fg=self.COLOR_LOCKED_FG)

    def set_modified(self):
        self.config(bg=self.COLOR_MODIFIED_BG)
        self.config(fg=self.COLOR_MODIFIED_FG)

    def set_normal(self):
        self.config(bg=self.COLOR_NORMAL_BG)
        self.config(fg=self.COLOR_NORMAL_FG)

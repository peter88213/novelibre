"""Provide a class for the novelibre status bar.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.view.observer import Observer
import tkinter as tk


class StatusBar(Observer, tk.Label):

    COLOR_NORMAL_BG = 'light gray'
    COLOR_NORMAL_FG = 'black'

    def __init__(self, master, **kw):
        tk.Label.__init__(self, master, **kw)
        self._statusText = ''

    def restore_status(self, event=None):
        """Overwrite error message with the status before."""
        self.show_status(self._statusText)

    def show_status(self, message=''):
        """Display a message at the status bar.
        
        Optional arguments:
            message: str -- Message to be displayed instead of the status text.
        """
        self._statusText = message
        self.config(bg=self.COLOR_NORMAL_BG)
        self.config(fg=self.COLOR_NORMAL_FG)
        self.config(text=message)

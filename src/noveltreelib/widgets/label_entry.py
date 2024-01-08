"""Provide a tkinter based entry box with a label.

Copyright (c) 2024 Peter Triesberger
https://github.com/peter88213
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk


class LabelEntry(ttk.Frame):
    """Entry box with a label.
    
    Credit goes to user stovfl on stackoverflow
    https://stackoverflow.com/questions/54584673/how-to-keep-tkinter-button-on-same-row-as-label-and-entry-box
    """

    def __init__(self, parent, text, textvariable, lblWidth=10):
        super().__init__(parent)
        self.pack(fill='x')
        self._label = ttk.Label(self, text=text, anchor='w', width=lblWidth)
        self._label.pack(side='left')
        self.entry = ttk.Entry(self, textvariable=textvariable)
        self.entry.pack(side='left', fill='x', expand=True)

    def set(self, value):
        """Replace None by an empty string.
        
        Extends the superclass method.
        """
        if value is None:
            value = ''
        self.entry.set(value)

    def config(self, **kwargs):
        self.configure(**kwargs)

    def configure(self, text=None, state=None):
        """Configure internal widgets."""
        if text is not None:
            self._label['text'] = text
        if state is not None:
            self.entry.config(state=state)

"""Provide a tkinter based display box with a label.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import ttk


class LabelDisp(ttk.Frame):
    """Display box with a label."""

    def __init__(self, parent, text, textvariable, lblWidth=10):
        super().__init__(parent)
        self.pack(fill='x')
        self._leftLabel = ttk.Label(self, text=text, anchor='w', width=lblWidth)
        self._leftLabel.pack(side='left')
        self._rightLabel = ttk.Label(self, textvariable=textvariable, anchor='w')
        self._rightLabel.pack(side='left', fill='x', expand=True)

    def config(self, **kwargs):
        self.configure(**kwargs)

    def configure(self, text=None):
        """Configure internal widget."""
        if text is not None:
            self._leftLabel['text'] = text

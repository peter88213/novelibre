"""Provide a tkinter based folding frame with a "show/hide" button.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import ttk


class FoldingFrame(ttk.Frame):
    """Folding frame with a "show/hide" button."""
    _PREFIX_SHOW = '▽  '
    _PREFIX_HIDE = '▷  '

    def __init__(self, parent, buttonText, command, **kw):
        super().__init__(parent, **kw)
        self.buttonText = buttonText
        self.titleBar = ttk.Frame(parent)
        self.titleBar.pack(fill='x', expand=False)
        self._toggleButton = ttk.Label(self.titleBar)
        self._toggleButton['text'] = f'{self._PREFIX_HIDE}{self.buttonText}'
        self._toggleButton.pack(side='left', fill='x', expand=True, pady=2)
        self._toggleButton.bind('<Button-1>', command)

    def show(self, event=None):
        """Expand the frame."""
        self._toggleButton['text'] = f'{self._PREFIX_SHOW}{self.buttonText}'
        self.pack(after=self.titleBar, fill='x', pady=5)

    def hide(self, event=None):
        """Collapse the frame."""
        self._toggleButton['text'] = f'{self._PREFIX_HIDE}{self.buttonText}'
        self.pack_forget()


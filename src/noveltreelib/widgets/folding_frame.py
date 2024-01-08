"""Provide a tkinter based folding frame with a "show/hide" button.

Copyright (c) 2024 Peter Triesberger
https://github.com/peter88213
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
        self._toggleButton = ttk.Label(parent)
        self._toggleButton['text'] = f'{self._PREFIX_HIDE}{self.buttonText}'
        self._toggleButton.pack(fill='x', pady=2)
        self._toggleButton.bind('<Button-1>', command)

    def show(self, event=None):
        self._toggleButton['text'] = f'{self._PREFIX_SHOW}{self.buttonText}'
        self.pack(after=self._toggleButton, fill='x', pady=5)

    def hide(self, event=None):
        self._toggleButton['text'] = f'{self._PREFIX_HIDE}{self.buttonText}'
        self.pack_forget()


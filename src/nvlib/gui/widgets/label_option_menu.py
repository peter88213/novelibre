"""Provide a tkinter based OptionMenu with a label.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
Published under the MIT License 
(https://opensource.org/licenses/mit-license.php)
"""
from tkinter import ttk


class LabelOptionMenu(ttk.Frame):
    """OptionMenu with a label."""

    def __init__(
            self,
            parent,
            text,
            textvariable,
            default=None,
            values=None,
            lblWidth=10,
            command=None,
        ):
        super().__init__(parent)
        self.pack(fill='x')
        self._label = ttk.Label(
            self,
            text=text,
            anchor='w',
            width=lblWidth,
        )
        self._label.pack(side='left')
        self.menu = ttk.OptionMenu(
            self,
            textvariable,
            default,
            *values,
            command=command,
        )
        self.menu.pack(anchor='w')

    def config(self, **kwargs):
        self.configure(**kwargs)

    def configure(self, text=None, state=None):
        """Configure internal widgets."""
        if text is not None:
            self._label['text'] = text
        if state is not None:
            self.menu['state'] = state

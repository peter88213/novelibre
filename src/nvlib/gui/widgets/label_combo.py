"""Provide a tkinter based combobox with a label.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from tkinter import ttk


class LabelCombo(ttk.Frame):
    """Combobox with a label.
    
    Credit goes to user stovfl on stackoverflow
    https://stackoverflow.com/questions/54584673/how-to-keep-tkinter-button-on-same-row-as-label-and-entry-box
    """

    def __init__(self, parent, text, textvariable, values, lblWidth=10):
        super().__init__(parent)
        self.pack(fill='x')
        self._label = ttk.Label(self, text=text, anchor='w', width=lblWidth)
        self._label.pack(side='left')
        self.combo = ttk.Combobox(self, textvariable=textvariable, values=values)
        self.combo.pack(side='left', fill='x', expand=True)

    def current(self):
        """Return the combobox selection."""
        return self.combo.current()

    def config(self, **kwargs):
        self.configure(**kwargs)

    def configure(self, text=None, values=None, state=None):
        """Configure internal widgets."""
        if text is not None:
            self._label['text'] = text
        if values is not None:
            self.combo['values'] = values
        if state is not None:
            self.combo.config(state=state)

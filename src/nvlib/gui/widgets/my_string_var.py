"""Provide a custom variant of the tkinter StringVar class.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
Published under the MIT License 
(https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk


class MyStringVar(tk.StringVar):
    """A custom variant of the tkinter StringVar class, handling "None"."""

    def set(self, value):
        """Replace None with an empty string.
        
        Extends the superclass method.
        """
        if value is None:
            value = ''
        super().set(value)

    def get(self, default=None):
        """Replace an empty string with default.
        
        Extends the superclass method.
        """
        value = super().get()
        if value == '':
            value = default
            if default is not None:
                self.set(default)
        return value

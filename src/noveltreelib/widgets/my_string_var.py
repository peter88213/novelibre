"""Provide a custom variant of the tkinter StringVar class.

Copyright (c) 2024 Peter Triesberger
https://github.com/peter88213
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
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

    def get(self):
        """Replace an empty string with None.
        
        Extends the superclass method.
        """
        value = super().get()
        if value == '':
            value = None
        return value

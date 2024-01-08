"""Provide a tkinter Text box class with a ttk scrollbar and a change flag.

Copyright (c) 2024 Peter Triesberger
https://github.com/peter88213
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import tkinter as tk
from tkinter import ttk


class TextBox(tk.Text):
    """A text box with a ttk scrollbar and a change flag."""

    def __init__(self, master=None, scrollbar=True, **kw):
        """Initialize the change flag and add a vertical scrollbar.
        
        If no font is defined, set the default font (mainly for Linux).        
        Copied from tkinter.scrolledtext and modified (use ttk widgets).
        Extends the supeclass constructor.
        """
        if kw.get('font', None) is None:
            kw['font'] = 'Courier 10'
        if scrollbar:
            # Add a scrollbar:
            self.frame = ttk.Frame(master)
            self.vbar = ttk.Scrollbar(self.frame)
            self.vbar.pack(side='right', fill='y')

            kw.update({'yscrollcommand': self.vbar.set})
            tk.Text.__init__(self, self.frame, **kw)
            self.pack(side='left', fill='both', expand=True)
            self.vbar['command'] = self.yview

            # Copy geometry methods of self.frame without overriding Text
            # methods -- hack!
            text_meths = vars(tk.Text).keys()
            methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
            methods = methods.difference(text_meths)

            for m in methods:
                if m[0] != '_' and m != 'config' and m != 'configure':
                    setattr(self, m, getattr(self.frame, m))
        else:
            tk.Text.__init__(self, master, **kw)

        # This part is project-specific:
        self.hasChanged = False
        self.bind('<KeyRelease>', self._on_edit)

    def clear(self):
        """Clear the box and reset the change flag."""
        self.delete('1.0', 'end')
        self.hasChanged = False

    def get_text(self):
        """Return the whole text."""
        return self.get('1.0', 'end').strip(' \n')

    def set_text(self, text):
        """Clear the box, reset the change flag, and load text."""
        self.clear()
        if text:
            self.insert('end', text)
            self.edit_reset()
            # this is to prevent the user from clearing the box with Ctrl-Z

    def _on_edit(self, event=None):
        """Event handler to indicate changes."""
        self.hasChanged = True


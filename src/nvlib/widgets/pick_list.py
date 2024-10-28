"""Provide a class for a BasicElement pick list.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk


class PickList(tk.Toplevel):
    """Data import pick list."""

    def __init__(self, title, geometry, sourceElements, pickButtonLabel, command):
        """
        
        Positional arguments:
            title: str -- Window title.
            geometry: str -- Window geometry.
            sourceElements: dict -- Key=ID, value=BasicElement reference.
            pickButtonLabel: str -- Text to be displayed on the "Pick element" button.
            command -- External callback function on picking elements.
            
        public instance variables:
            targetElements: list of picked IDs.
       
        """
        super().__init__()
        self._command = command
        self.title(title)
        self.geometry(geometry)
        self.grab_set()
        self.focus()
        self.pickList = ttk.Treeview(self, selectmode='extended')
        scrollY = ttk.Scrollbar(self.pickList, orient='vertical', command=self.pickList.yview)
        self.pickList.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side='right', fill='y')
        self.pickList.pack(fill='both', expand=True)
        ttk.Button(self, text=pickButtonLabel, command=self._pick_element).pack()
        for elemId in sourceElements:
            self.pickList.insert('', 'end', elemId, text=sourceElements[elemId].title)

    def _pick_element(self):
        """Internal callback function on picking elements."""
        selection = self.pickList.selection()
        self.destroy()
        # first close the pop-up, because the command might raise an exception
        self._command(selection)

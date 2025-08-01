"""Provide a class for a BasicElement pick list.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

import tkinter as tk


class PickList(tk.Toplevel):
    """Data import pick list."""

    def __init__(
            self,
            title,
            geometry,
            sourceElements,
            pickButtonLabel,
            command
    ):
        """
        
        Positional arguments:
            title: str -- Window title.
            geometry: str -- Window geometry.
            sourceElements: dict -- Key=ID, value=BasicElement reference.
            pickButtonLabel: str -- Text to be displayed on the 
                                    "Pick element" button.
            command -- External callback function on picking elements.
        """
        super().__init__()
        self._command = command
        self.title(title)
        self.geometry(geometry)
        self.grab_set()
        self.focus()
        self.pickList = ttk.Treeview(
            self,
            selectmode='extended',
        )
        scrollY = ttk.Scrollbar(
            self.pickList,
            orient='vertical',
            command=self.pickList.yview,
        )
        self.pickList.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side='right', fill='y')
        self.pickList.pack(fill='both', expand=True)
        ttk.Button(
            self,
            text=pickButtonLabel,
            command=self._pick_elements
        ).pack()
        for elemId in sourceElements:
            self.pickList.insert(
                '',
                'end',
                elemId,
                text=sourceElements[elemId].title,
            )

    def _pick_elements(self):
        # Internal callback function on picking elements.
        selection = self.pickList.selection()
        self.destroy()
        # first close the pop-up, because the command
        # might raise an exception
        self._command(selection)

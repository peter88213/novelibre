"""Provide a class for a BasicElement pick list.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.nv_locale import _
import tkinter as tk


class PickList(tk.Toplevel):
    """Data import pick list."""

    def __init__(
        self,
        title,
        geometry,
        sourceElements,
        command,
        icon=None,
        selectmode='extended',
    ):
        """
        
        Positional arguments:
            title: str -- Window title.
            geometry: str -- Window geometry.
            sourceElements: dict -- Key=ID, value=BasicElement reference.
            command -- External callback function on picking elements.
        """
        super().__init__()
        self._command = command
        self.title(title)
        if icon is not None:
            self.iconphoto(False, icon)
        self.geometry(geometry)
        self.grab_set()
        self.focus()

        listFrame = ttk.Frame(self)
        listFrame.pack(
            fill='both',
            expand=True,
            padx=4,
            pady=4,
        )

        self._pickList = ttk.Treeview(
            listFrame,
            selectmode=selectmode,
        )
        vbar = ttk.Scrollbar(
            listFrame,
            orient='vertical',
            command=self._pickList.yview,
        )
        vbar.pack(side='right', fill='y')
        self._pickList.pack(
            side='left',
            fill='both',
            expand=True,
        )
        self._pickList.config(yscrollcommand=vbar.set)

        # "OK" button.
        ttk.Button(
            self,
            text=_('OK'),
            command=self._pick_elements,
        ).pack(padx=5, pady=5, side='left')

        # "Close" button.
        ttk.Button(
            self,
            text=_('Cancel'),
            command=self.destroy,
        ).pack(padx=5, pady=5, side='right')

        for elemId in sourceElements:
            self._pickList.insert(
                '',
                'end',
                elemId,
                text=sourceElements[elemId].title,
            )

    def _pick_elements(self):
        # Internal callback function on picking elements.
        selection = self._pickList.selection()
        self.destroy()
        # first close the pop-up, because the command
        # might raise an exception
        self._command(selection)

"""Provide a class for string selection.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.nv_locale import _
import tkinter as tk


class StrSelectionDialog(ModalDialog):

    def __init__(
        self,
        master,
        strList,
        callback,
        label,
        fg=None,
        bg=None,
    ):
        super().__init__(master)
        self.title(label)
        self._cb = callback
        self._strList = strList

        # Heading.
        ttk.Label(self, text=label).pack()

        # Listbox.
        listFrame = ttk.Frame(self)
        listFrame.pack(
            fill='both',
            expand=True,
            padx=4,
            pady=4,
        )
        strListVar = tk.StringVar(value=self._strList)
        self._listBox = tk.Listbox(
            listFrame,
            listvariable=strListVar,
            selectmode='single',
            fg=fg,
            bg=bg,
        )
        vbar = ttk.Scrollbar(
            listFrame,
            orient='vertical',
            command=self._listBox.yview,
        )
        vbar.pack(side='right', fill='y')
        self._listBox.pack(
            side='left',
            fill='both',
            expand=True,
        )
        self._listBox.config(yscrollcommand=vbar.set)
        self._listBox.bind('<Double-1>', self._select_string)
        self._listBox.bind('<Return>', self._select_string)

        # "OK" button.
        ttk.Button(
            self,
            text=_('OK'),
            command=self._select_string,
        ).pack(padx=5, pady=5, side='left')

        # "Close" button.
        ttk.Button(
            self,
            text=_('Cancel'),
            command=self.destroy,
        ).pack(padx=5, pady=5, side='right')

    def _select_string(self, event=None):
        # Pass the selected string as a parameter to the callback function.
        selection = self._listBox.curselection()
        self.destroy()
        if selection:
            option = selection[0]
            self._cb(self._strList[option])

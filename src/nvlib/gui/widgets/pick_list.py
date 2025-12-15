"""Provide a class for a BasicElement pick list.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.nv_locale import _
from nvlib.gui.widgets.modal_dialog import ModalDialog


class PickList(ModalDialog):
    """Data import pick list."""

    LIST_WIDTH = 300

    def __init__(
        self,
        master,
        title,
        valueDict,
        command,
        icon=None,
        multiple=True,
    ):
        """
        
        Positional arguments:
            title: str -- Window title.
            valueDict: dict -- Key=ID, value=string.
            command -- External callback function to be called 
                       with a list of picked keys as parameter.
            icon -- tk.PhotoImage instance for window decoration.
        
        Optional arguments:
            multiple: Bool -- If True, allow the selection 
                              of multiple list elements. "OK" picks. 
                              If False, "OK" or double click picks 
                              a single list element.
        """

        def pick_elements(event=None):
            # Internal callback function on picking elements.
            selection = pList.selection()
            self.destroy()
            # first close the pop-up, because
            # the command might raise an exception
            self._command(selection)
            # selection is a list of keys.

        super().__init__(master)
        self.title(title)
        if icon is not None:
            self.iconphoto(False, icon)
        self._command = command

        listFrame = ttk.Frame(self)
        listFrame.pack(
            fill='both',
            expand=True,
            padx=4,
            pady=4,
        )

        # Prepare the pick list with a vertical scrollbar.
        if multiple:
            selectmode = 'extended'
        else:
            selectmode = 'browse'

        pList = ttk.Treeview(
            listFrame,
            selectmode=selectmode,
            show='tree',
        )
        vbar = ttk.Scrollbar(
            listFrame,
            orient='vertical',
            command=pList.yview,
        )
        vbar.pack(side='right', fill='y')
        pList.pack(
            side='left',
            fill='both',
            expand=True,
        )
        pList.config(yscrollcommand=vbar.set)
        pList.column('#0', width=self.LIST_WIDTH)

        # "OK" button to pick single or multiple entries.
        ttk.Button(
            self,
            text=_('OK'),
            command=pick_elements,
        ).pack(padx=5, pady=5, side='left')

        # Mouse key binding to pick a single entry.
        if not multiple:
            pList.bind('<Double-1>', pick_elements)

        # "Cancel" button to close the window without picking.
        ttk.Button(
            self,
            text=_('Cancel'),
            command=self.destroy,
        ).pack(padx=5, pady=5, side='right')

        # Populate the pick list.
        for key in valueDict:
            pList.insert(
                '',
                'end',
                key,
                text=valueDict[key],
            )


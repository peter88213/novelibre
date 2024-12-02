"""Provide a widget for displaying and modifying a collection of list items.

Copyright (c) 2024 Peter Triesberger
https://github.com/peter88213
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.platform.platform_settings import KEYS
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class CollectionBox(ttk.Frame):
    """A frame with a listbox and control buttons.
    
    Public instance variables:
        cList: tk.strVar -- Holds a list representing the collection.
        cListbox: tk.Listbox -- Displays the collection.
        btnOpen: ttk.Button -- Activatable button, not intended to modify the collection.
        btnAdd: ttk.Button -- Input widget, always active by default.
        btnRemove: ttk.Button -- Activatable input widget.
        inputWidgets -- List with references to the input widgets.
        
    The inputWidgets list can be used to lock the application, deactivating the input widgets.
    The enable_buttons() and disable_buttons() methods are intended for setting the 
    buttons' status from outsides, dependent on the list content and selection. So "Add" is always 
    meant to be active, whereas "Open" and "Remove" is only to be active when a list item is selected.
    """

    def __init__(
            self,
            master,
            cmdAdd=None, lblAdd=None, iconAdd=None,
            cmdOpen=None, lblOpen=None, iconOpen=None,
            cmdRemove=None, lblRemove=None, iconRemove=None,
            cmdActivate=None, cmdSelect=None,
            **kw
            ):
        """Set up the listbox and the buttons.
        
        Optional arguments:
            cmdAdd -- Reference to the callback routine for the "Add" button.
                      If not set, the "Add" button is not available.
            lblAdd --  Optional alternative text on the "Add" button.
            iconAdd --  Optional icon on the "Add" button.
            cmdOpen -- Reference to the callback routine for the "Open" button.
                       Bound to the "Return" key and left mouse button doublecklick.
                       If not set, the "Add" button is not available.
            lblOpen -- Optional alternative text on the "Open" button.
            iconOpen -- Optional icon on the "Open" button.
            cmdRemove -- Reference to the callback routine for the "Remove" button.
                         Bound to the "Delete" key.
                         If not set, the "Remove" button is not available.
            lblRemove -- Optional alternative text on the "Remove" button.
            iconRemove -- Optional icon on the "Remove" button.
            cmdActivate -- Reference to an external callback routine (optional)
                           Bound to listbox focus and selection.
            cmdSelect -- Reference to the callback routine for list element 
                         selection (optional).
        
        Extends the superclass constructor.
        """
        super().__init__(master, **kw)
        if cmdActivate is None:
            cmdActivate = self.enable_buttons

        # Listbox.
        listFrame = ttk.Frame(self)
        listFrame.pack(side='left', fill='both', expand=True)
        self.cList = tk.StringVar()
        self.cListbox = tk.Listbox(listFrame, listvariable=self.cList, selectmode='single')
        vbar = ttk.Scrollbar(listFrame, orient='vertical', command=self.cListbox.yview)
        vbar.pack(side='right', fill='y')
        self.cListbox.pack(side='left', fill='both', expand=True)
        self.cListbox.config(yscrollcommand=vbar.set)

        self.cListbox.bind('<FocusIn>', cmdActivate)
        self.cListbox.bind('<<ListboxSelect>>', self._on_change_selection)

        # Buttons.
        buttonbar = ttk.Frame(self)
        buttonbar.pack(anchor='n', side='right', fill='x', padx=5)
        self.inputWidgets = []

        # "Select" command.
        self._cmdSelect = cmdSelect

        # "Open" command.
        kwargs = dict(
            command=cmdOpen,
            image=iconOpen,
            )
        if lblOpen is None:
            kwargs['text'] = _('Open')
        else:
            kwargs['text'] = lblOpen
        self.btnOpen = ttk.Button(buttonbar, **kwargs)
        if cmdOpen is not None:
            self.btnOpen.pack(fill='x', expand=True)
            self.cListbox.bind('<Double-1>', cmdOpen)
            self.cListbox.bind('<Return>', cmdOpen)

        # "Add" command.
        kwargs = dict(
            command=cmdAdd,
            image=iconAdd,
            )
        if lblAdd is None:
            kwargs['text'] = _('Add')
        else:
            kwargs['text'] = lblAdd
        self.btnAdd = ttk.Button(buttonbar, **kwargs)
        if cmdAdd is not None:
            self.btnAdd.pack(fill='x', expand=True)
            self.inputWidgets.append(self.btnAdd)

        # "Remove" command.
        kwargs = dict(
            command=cmdRemove,
            image=iconRemove,
            )
        if lblRemove is None:
            kwargs['text'] = _('Remove')
        else:
            kwargs['text'] = lblRemove
        self.btnRemove = ttk.Button(buttonbar, **kwargs)
        if cmdRemove is not None:
            self.btnRemove.pack(fill='x', expand=True)
            self.inputWidgets.append(self.btnRemove)
            self.cListbox.bind(KEYS.DELETE[0], cmdRemove)

        self._set_hovertips()

    def enable_buttons(self, event=None):
        """Activate the group of activatable buttons."""
        self.btnOpen.config(state='normal')
        self.btnRemove.config(state='normal')

    def disable_buttons(self, event=None):
        """Deactivate the group of activatable buttons."""
        self.btnOpen.config(state='disabled')
        self.btnRemove.config(state='disabled')

    def _on_change_selection(self, event=None):
        self.enable_buttons()
        if self._cmdSelect is not None:
            try:
                self._cmdSelect(self.cListbox.curselection()[0])
            except:
                pass

    def _set_hovertips(self):
        if not prefs['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(self.btnAdd, self.btnAdd['text'])
        Hovertip(self.btnOpen, self.btnOpen['text'])
        Hovertip(self.btnRemove, f"{self.btnRemove['text']} ({KEYS.DELETE[1]})")

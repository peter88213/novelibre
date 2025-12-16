"""Provide a widget for displaying and modifying a collection of list items.

Copyright (c) 2025 Peter Triesberger
https://github.com/peter88213
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.tooltip import Hovertip
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class CollectionBox(ttk.Frame):
    """A frame with a listbox and control buttons.
    
    Public instance variables:
        btnOpen: ttk.Button -- Activatable button, not intended to 
                               modify the collection.
        btnAdd: ttk.Button -- Input widget, always active by default.
        btnRemove: ttk.Button -- Activatable input widget.
        inputWidgets -- List with references to the input widgets.
        
    The inputWidgets list can be used to lock the application, 
    deactivating the input widgets.
    The enable_buttons() and disable_buttons() methods are 
    intended for setting the 
    buttons' status from outsides, dependent on the list content 
    and selection. So "Add" is always 
    meant to be active, whereas "Open" and "Remove" is only to be 
    active when a list item is selected.
    """

    def __init__(
        self,
        master,
        cmdAdd=None,
        lblAdd=None,
        iconAdd=None,
        cmdOpen=None,
        lblOpen=None,
        iconOpen=None,
        cmdRemove=None,
        lblRemove=None,
        iconRemove=None,
        cmdSelect=None,
        **kw
    ):
        """Set up the listbox and the buttons.
        
        Optional arguments:
            cmdAdd -- Reference to the callback routine for the "Add" button.
                      If not set, the "Add" button is not available.
            lblAdd -- Optional alternative text on the "Add" button.
            iconAdd -- Optional icon on the "Add" button.
            cmdOpen -- Reference to the callback routine for the 
                       "Open" button.
                       Bound to the "Return" key and left mouse button 
                       doublecklick.
                       If not set, the "Add" button is not available.
            lblOpen -- Optional alternative text on the "Open" button.
            iconOpen -- Optional icon on the "Open" button.
            cmdRemove -- Reference to the callback routine for the "Remove" 
                         button.
                         Bound to the "Delete" key.
                         If not set, the "Remove" button is not available.
            lblRemove -- Optional alternative text on the "Remove" button.
            iconRemove -- Optional icon on the "Remove" button.
            cmdSelect -- Reference to the callback routine for list element 
                         selection (optional).
        
        Extends the superclass constructor.
        """

        def on_change_selection(event=None):
            # Internal callback function on selecting elements.
            if cmdSelect is not None:
                try:
                    cmdSelect(self._cList.curselection()[0])
                except:
                    pass

        super().__init__(master, **kw)

        # Listbox.
        listFrame = ttk.Frame(self)
        listFrame.pack(side='left', fill='both', expand=True)

        self._cListVar = tk.StringVar()
        self._cList = tk.Listbox(
            listFrame,
            listvariable=self._cListVar,
            selectmode='single',
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
        )
        vbar = ttk.Scrollbar(
            listFrame,
            orient='vertical',
            command=self._cList.yview,
        )
        vbar.pack(side='right', fill='y')
        self._cList.pack(
            side='left',
            fill='both',
            expand=True,
        )
        self._cList.config(yscrollcommand=vbar.set)
        self._cList.bind('<<ListboxSelect>>', on_change_selection)
        self._cList.configure(exportselection=False)
        # keep selection when losing the focus

        # Buttons.
        buttonbar = ttk.Frame(self)
        buttonbar.pack(anchor='n', side='right', fill='x', padx=5)
        self.inputWidgets = []

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
            self._cList.bind('<Double-1>', cmdOpen)
            self._cList.bind('<Return>', cmdOpen)

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
            self._cList.bind(KEYS.DELETE[0], cmdRemove)

        self._set_hovertips()

    @property
    def selection(self):
        try:
            return self._cList.curselection()[0]

        except:
            return None

    @selection.setter
    def selection(self, listIndex):
        try:
            self._cList.selection_set(listIndex)
        except:
            pass

    def enable_buttons(self, event=None):
        """Activate the group of activatable buttons."""
        self.btnOpen.config(state='normal')
        self.btnRemove.config(state='normal')

    def disable_buttons(self, event=None):
        """Deactivate the group of activatable buttons."""
        self.btnOpen.config(state='disabled')
        self.btnRemove.config(state='disabled')

    def set(self, newList):
        # Populate the collection.
        self._cList.selection_clear(0, 'end')
        self._cListVar.set(newList)
        self.disable_buttons()

    def set_height(self, newVal):
        self._cList.config(height=newVal)

    def _set_hovertips(self):
        if not prefs['enable_hovertips']:
            return

        Hovertip(
            self.btnAdd,
            self.btnAdd['text']
        )
        Hovertip(
            self.btnOpen,
            self.btnOpen['text']
        )
        Hovertip(
            self.btnRemove,
            f"{self.btnRemove['text']} ({KEYS.DELETE[1]})"
        )

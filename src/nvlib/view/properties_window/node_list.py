"""Provide a tkinter frame with a node list and controls.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk
from tkinter import ttk


class NodeList(ttk.Frame):
    """A Frame containing a list and control elements for adding and removing items.
    
    Public instance variables:
        listbox: tk.Listbox
    """

    def __init__(self, master, view, pickBtnTxt, clearBtnTxt, **kw):
        """Set up listbox and controls. 
        
        Positional arguments:
            master -- Parent widget.
            view: NoveltreeUi -- Reference to the user interface.
            pickBtnTxt: str -- Text on the "Pick" button.
            clearBtnTxt: str -- Text on the "Clear" button.

        Extends the superclass constructor.
        """
        self._ui = view
        super().__init__(master, **kw)
        self.listbox = tk.Listbox(self)
        self.listbox.pack(anchor='w', fill='x')
        ttk.Button(self, text=pickBtnTxt, command=self._pick_node).pack(side='left', padx=1, pady=2)
        ttk.Button(self, text=clearBtnTxt, command=self._clear_assignment).pack(side='left', padx=1, pady=2)

    def _pick_node(self, command, subtree):
        """Enter the "pick node" selection mode.
        
        Change the mouse cursor to "+" and expand the subtree.
        Now the tree selection does not trigger the viewer, 
        but calls command on node selection.  
        
        To end the "pick node" selection mode, either select any node, 
        or press the Escape key.
        """
        self._lastSelected = self._ui.tv.tree.selection()[0]
        self._ui.tv.config(cursor='plus')
        self._ui.tv.open_children(subtree)
        self._ui.tv.tree.see(subtree)
        self._treeSelectBinding = self._ui.tv.tree.bind('<<TreeviewSelect>>')
        self._ui.tv.tree.bind('<<TreeviewSelect>>', self._add_node)
        self._uiEscBinding = self._ui.root.bind('<Esc>')
        self._ui.root.bind('<Escape>', self._add_node)

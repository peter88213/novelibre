"""Provide a class for a novelibre project tree.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import PN_ROOT


class NvTreeview(ttk.Treeview):
    """novelibre project tree, defining the novel structure."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_element_change = self.do_nothing

        #--- Build the toplevel  structure.
        self.append('', CH_ROOT)
        self.append('', CR_ROOT)
        self.append('', LC_ROOT)
        self.append('', IT_ROOT)
        self.append('', PL_ROOT)
        self.append('', PN_ROOT)

    def append(self, parent, iid, text=None):
        if text is None:
            text = iid
        self.insert(parent, 'end', iid, text=text)

    def delete(self, *items):
        super().delete(*items)
        self.on_element_change()

    def delete_children(self, parent):
        for child in self.get_children(parent):
            self.delete(child)

    def insert(self, parent, index, iid=None, **kw):
        super().insert(parent, index, iid, **kw)
        self.on_element_change()

    def move(self, item, parent, index):
        super().move(item, parent, index)
        self.on_element_change()

    def reset(self):
        """Clear the tree, keeping the root elements."""
        self.on_element_change = self.do_nothing
        for rootElement in self.get_children(''):
            for child in self.get_children(rootElement):
                self.delete(child)

    def do_nothing(self):
        pass

"""Provide a class for a novelibre project tree substitute.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import PN_ROOT


class NvTree:
    """novelibre project structure, emulating the ttk.Treeview interface.
    
    This allows independence from the tkinter library.
    """

    def __init__(self):
        self.roots = {
            CH_ROOT:[],
            CR_ROOT:[],
            LC_ROOT:[],
            IT_ROOT:[],
            PL_ROOT:[],
            PN_ROOT:[],
        }
        # values : listed children's IDs
        self.srtSections = {}
        # key: chapter ID
        # value : section ID
        self.srtTurningPoints = {}
        # key: plot line ID
        # value : plot point ID

    def append(self, parent, iid):
        """Creates a new item with identifier iid."""
        if parent in self.roots:
            self.roots[parent].append(iid)
            if parent == CH_ROOT:
                self.srtSections[iid] = []
            elif parent == PL_ROOT:
                self.srtTurningPoints[iid] = []
            return

        if parent.startswith(CHAPTER_PREFIX):
            if parent in self.srtSections:
                self.srtSections[parent].append(iid)
            else:
                self.srtSections[parent] = [iid]
            return

        if parent.startswith(PLOT_LINE_PREFIX):
            if parent in self.srtTurningPoints:
                self.srtTurningPoints[parent].append(iid)
            else:
                self.srtTurningPoints[parent] = [iid]

    def delete(self, *items):
        """Delete all specified items and all their descendants. The root
        item may not be deleted."""
        raise NotImplementedError

    def delete_children(self, parent):
        """Delete all parent's descendants."""
        if parent in self.roots:
            self.roots[parent] = []
            if parent == CH_ROOT:
                self.srtSections = {}
                return

            if parent == PL_ROOT:
                self.srtTurningPoints = {}
            return

        if parent.startswith(CHAPTER_PREFIX):
            self.srtSections[parent] = []
            return

        if parent.startswith(PLOT_LINE_PREFIX):
            self.srtTurningPoints[parent] = []

    def get_children(self, item):
        """Returns the list of children belonging to item."""
        if item in self.roots:
            return self.roots[item]

        if item.startswith(CHAPTER_PREFIX):
            return self.srtSections.get(item, [])

        if item.startswith(PLOT_LINE_PREFIX):
            return self.srtTurningPoints.get(item, [])

    def index(self, item):
        """Return the integer index of item within its parent's list
        of children."""
        raise NotImplementedError

    def insert(self, parent, index, iid):
        """Create a new item with identifier iid."""
        if parent in self.roots:
            self.roots[parent].insert(index, iid)
            if parent == CH_ROOT:
                self.srtSections[iid] = []
            elif parent == PL_ROOT:
                self.srtTurningPoints[iid] = []
            return

        if parent.startswith(CHAPTER_PREFIX):
            if parent in self.srtSections:
                self.srtSections[parent].insert(index, iid)
            else:
                self.srtSections[parent] = [iid]
            return

        if parent.startswith(PLOT_LINE_PREFIX):
            if parent in self.srtTurningPoints:
                self.srtTurningPoints[parent].insert(index, iid)
            else:
                self.srtTurningPoints[parent] = [iid]

    def move(self, item, parent, index):
        """Move item to position index in parent's list of children.

        It is illegal to move an item under one of its descendants. If
        index is less than or equal to zero, item is moved to the
        beginning, if greater than or equal to the number of children,
        it is moved to the end. If item was detached it is reattached.
        """
        raise NotImplementedError

    def next(self, item):
        """Return the identifier of item's next sibling, or '' if item
        is the last child of its parent."""
        raise NotImplementedError

    def parent(self, item):
        """Return the ID of the parent of item, or '' if item is at the
        top level of the hierarchy."""
        raise NotImplementedError

    def prev(self, item):
        """Return the identifier of item's previous sibling, or '' if
        item is the first child of its parent."""
        raise NotImplementedError

    def reset(self):
        """Clear the tree."""
        for item in self.roots:
            self.roots[item] = []
        self.srtSections = {}
        self.srtTurningPoints = {}

    def set_children(self, item, newchildren):
        """Replaces item’s child with newchildren."""
        if item in self.roots:
            self.roots[item] = newchildren[:]
            if item == CH_ROOT:
                self.srtSections = {}
                return

            if item == PL_ROOT:
                self.srtTurningPoints = {}
            return

        if item.startswith(CHAPTER_PREFIX):
            self.srtSections[item] = newchildren[:]
            return

        if item.startswith(PLOT_LINE_PREFIX):
            self.srtTurningPoints[item] = newchildren[:]


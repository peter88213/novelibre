"""Provide a context menu class for the novelibre tree view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import PN_ROOT
from nvlib.novx_globals import PRJ_NOTE_PREFIX
from nvlib.novx_globals import ROOT_PREFIX
from nvlib.novx_globals import SECTION_PREFIX


class TreeContextMenu:

    def __init__(self, model, view):
        self._mdl = model
        self._ui = view

    def open(self, event):
        # Event handler for the tree's context menu.
        if self._mdl.prjFile is None:
            return

        row = self._ui.tv.tree.identify_row(event.y)
        if not row:
            return

        self._ui.tv.go_to_node(row)
        if row.startswith(ROOT_PREFIX):
            prefix = row
        else:
            prefix = row[:2]

        if prefix == CH_ROOT:
            self._ui.bookContextMenu.open(event)
        elif prefix == CHAPTER_PREFIX:
            if row == self._mdl.trashBin:
                self._ui.trashContextMenu.open(event)
            else:
                self._ui.chapterContextMenu.open(event)
        elif prefix == SECTION_PREFIX:
            if self._mdl.novel.tree.parent(row) == self._mdl.trashBin:
                self._ui.trashContextMenu.open(event)
            elif self._mdl.novel.sections[row].scType < 2:
                self._ui.sectionContextMenu.open(event)
            else:
                self._ui.stageContextMenu.open(event)
        elif prefix in (
            LOCATION_PREFIX,
            ITEM_PREFIX,
            PLOT_POINT_PREFIX,
            PRJ_NOTE_PREFIX,
        ):
            self._ui.elementContextMenu.open(event)
        elif prefix in(
            LC_ROOT,
            IT_ROOT,
            PL_ROOT,
            PN_ROOT,
        ):
            self._ui.rootContextMenu.open(event)
        elif prefix == CR_ROOT:
            self._ui.crRootContextMenu.open(event)
        elif prefix == CHARACTER_PREFIX:
            self._ui.characterContextMenu.open(event)
        elif prefix == PLOT_LINE_PREFIX:
            self._ui.plotLineContextMenu.open(event)


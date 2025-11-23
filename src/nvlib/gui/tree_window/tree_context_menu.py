"""Provide a context menu class for the novelibre tree view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.sub_controller import SubController
from nvlib.gui.tree_window.book_context_menu import BookContextMenu
from nvlib.gui.tree_window.chapter_context_menu import ChapterContextMenu
from nvlib.gui.tree_window.character_context_menu import CharacterContextMenu
from nvlib.gui.tree_window.cr_root_context_menu import CrRootContextMenu
from nvlib.gui.tree_window.element_context_menu import ElementContextMenu
from nvlib.gui.tree_window.plot_line_context_menu import PlotLineContextMenu
from nvlib.gui.tree_window.root_context_menu import RootContextMenu
from nvlib.gui.tree_window.section_context_menu import SectionContextMenu
from nvlib.gui.tree_window.stage_context_menu import StageContextMenu
from nvlib.gui.tree_window.trash_context_menu import TrashContextMenu
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


class TreeContextMenu(SubController):

    def __init__(self, master, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        #--- Create local context menus.
        self._bookContextMenu = BookContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._bookContextMenu)

        self._chapterContextMenu = ChapterContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._chapterContextMenu)

        self._characterContextMenu = CharacterContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._characterContextMenu)

        self._crRootContextMenu = CrRootContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._crRootContextMenu)

        self._elementContextMenu = ElementContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._elementContextMenu)

        self._plotLineContextMenu = PlotLineContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._plotLineContextMenu)

        self._rootContextMenu = RootContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._rootContextMenu)

        self._sectionContextMenu = SectionContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._sectionContextMenu)

        self._stageContextMenu = StageContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._stageContextMenu)

        self._trashContextMenu = TrashContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._trashContextMenu)

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
            self._bookContextMenu.open(event)
        elif prefix == CHAPTER_PREFIX:
            if row == self._mdl.trashBin:
                self._trashContextMenu.open(event)
            else:
                self._chapterContextMenu.open(event)
        elif prefix == SECTION_PREFIX:
            if self._mdl.novel.tree.parent(row) == self._mdl.trashBin:
                self._trashContextMenu.open(event)
            elif self._mdl.novel.sections[row].scType < 2:
                self._sectionContextMenu.open(event)
            else:
                self._stageContextMenu.open(event)
        elif prefix in (
            LOCATION_PREFIX,
            ITEM_PREFIX,
            PLOT_POINT_PREFIX,
            PRJ_NOTE_PREFIX,
        ):
            self._elementContextMenu.open(event)
        elif prefix in(
            LC_ROOT,
            IT_ROOT,
            PL_ROOT,
            PN_ROOT,
        ):
            self._rootContextMenu.open(event)
        elif prefix == CR_ROOT:
            self._crRootContextMenu.open(event)
        elif prefix == CHARACTER_PREFIX:
            self._characterContextMenu.open(event)
        elif prefix == PLOT_LINE_PREFIX:
            self._plotLineContextMenu.open(event)


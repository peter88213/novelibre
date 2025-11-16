"""Provide a context menu class for the novelibre tree view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.sub_controller import SubController
from nvlib.gui.tree_window.book_context_menu import BookContextMenu
from nvlib.gui.tree_window.chapter_context_menu import ChapterContextMenu
from nvlib.gui.tree_window.character_context_menu import CharacterContextMenu
from nvlib.gui.tree_window.plot_context_menu import PlotContextMenu
from nvlib.gui.tree_window.projectnote_context_menu import ProjectnoteContextMenu
from nvlib.gui.tree_window.section_context_menu import SectionContextMenu
from nvlib.gui.tree_window.stage_context_menu import StageContextMenu
from nvlib.gui.tree_window.trash_context_menu import TrashContextMenu
from nvlib.gui.tree_window.world_context_menu import WorldContextMenu
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
from nvlib.nv_locale import _


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

        self._trashContextMenu = TrashContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._trashContextMenu)

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

        self._characterContextMenu = CharacterContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._characterContextMenu)
        self._worldContextMenu = WorldContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._worldContextMenu)

        self.plotContextMenu = PlotContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self.plotContextMenu)
        self._projectnoteContextMenu = ProjectnoteContextMenu(
            master,
            self._mdl,
            self._ui,
            self._ctrl
        )
        self._ctrl.register_client(self._projectnoteContextMenu)

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

    def _configure_book_context_menu(self, prefix, row):
        bookContextEntries = (
            _('Add Section'),
            _('Add Chapter'),
            _('Add Part'),
            _('Insert Stage'),
            _('Change Level'),
            _('Export this chapter'),
            _('Delete'),
            _('Cut'),
            _('Paste'),
            _('Set Type'),
            _('Set Status'),
            _('Set Viewpoint...'),
            _('Join with previous'),
        )
        if self._ctrl.isLocked:
            for label in bookContextEntries:
                self._bookContextMenu.entryconfig(label, state='disabled')
            return

        for label in bookContextEntries:
            self._bookContextMenu.entryconfig(label, state='normal')
        self._bookContextMenu.entryconfig(_('Copy'), state='normal')

        if prefix == CHAPTER_PREFIX:
            for label in (
                _('Join with previous'),
            ):
                self._bookContextMenu.entryconfig(label, state='disabled')
            if row == self._mdl.trashBin:
                # Context is the "Trash" chapter.
                for label in (
                    _('Set Type'),
                    _('Set Status'),
                    _('Change Level'),
                    _('Add Section'),
                    _('Add Chapter'),
                    _('Add Part'),
                    _('Insert Stage'),
                    _('Export this chapter'),
                ):
                    self._bookContextMenu.entryconfig(label, state='disabled')
            return

        if prefix == SECTION_PREFIX:
            if self._mdl.novel.sections[row].scType < 2:
                # Context is a section, not a stage.
                for label in (
                    _('Export this chapter'),
                    _('Change Level'),
                ):
                    self._bookContextMenu.entryconfig(label, state='disabled')
                return

            # Context is a stage, not a section.
            for label in (
                _('Export this chapter'),
                _('Set Type'),
                _('Set Status'),
                _('Join with previous'),
            ):
                self._bookContextMenu.entryconfig(label, state='disabled')
            return

        if prefix == CH_ROOT:
            for label in (
                _('Delete'),
                _('Cut'),
                _('Copy'),
                _('Paste'),
                _('Set Type'),
                _('Add Section'),
                _('Insert Stage'),
                _('Change Level'),
                _('Join with previous'),
                _('Export this chapter'),
            ):
                self._bookContextMenu.entryconfig(label, state='disabled')
            return

    def _configure_plot_context_menu(self, prefix):
        plotContextEntries = (
            _('Add Plot line'),
            _('Add Plot point'),
            _('Delete'),
            _('Cut'),
            _('Paste'),
            _('Export manuscript filtered by plot line'),
            _('Export synopsis filtered by plot line'),
            _('Change sections to Unused'),
            _('Change sections to Normal'),
        )
        self.plotContextMenu.entryconfig(_('Copy'), state='normal')
        if self._ctrl.isLocked:
            for label in plotContextEntries:
                self.plotContextMenu.entryconfig(label, state='disabled')
            return

        for label in plotContextEntries:
            self.plotContextMenu.entryconfig(label, state='normal')

        if prefix == PLOT_LINE_PREFIX:
            return

        if prefix == PLOT_POINT_PREFIX:
            for label in (
                _('Export manuscript filtered by plot line'),
                _('Export synopsis filtered by plot line'),
                _('Change sections to Unused'),
                _('Change sections to Normal'),
            ):
                self.plotContextMenu.entryconfig(label, state='disabled')
            return

        if prefix == PL_ROOT:
            for label in (
                _('Add Plot point'),
                _('Delete'),
                _('Cut'),
                _('Copy'),
                _('Paste'),
                _('Export manuscript filtered by plot line'),
                _('Export synopsis filtered by plot line'),
                _('Change sections to Unused'),
                _('Change sections to Normal'),
            ):
                self.plotContextMenu.entryconfig(label, state='disabled')
            return

    def _configure_project_note_context_menu(self, prefix):
        projectnoteContextEntries = (
            _('Add Project note'),
            _('Delete'),
            _('Cut'),
            _('Paste'),
        )
        self.projectnoteContextMenu.entryconfig(_('Copy'), state='normal')
        if self._ctrl.isLocked:
            # No changes allowed.
            for label in projectnoteContextEntries:
                self.projectnoteContextMenu.entryconfig(
                    label,
                    state='disabled',
                )
            return

        for label in projectnoteContextEntries:
            self.projectnoteContextMenu.entryconfig(
                label,
                state='normal',
            )

        if prefix == PRJ_NOTE_PREFIX:
            return

        if prefix == PN_ROOT:
            for label in (
                _('Delete'),
                _('Cut'),
                _('Copy'),
                _('Paste'),
            ):
                self.projectnoteContextMenu.entryconfig(
                    label,
                    state='disabled',
                )
            return

    def _configure_world_context_menu(self, prefix):
        worldContextEntries = (
            _('Add'),
            _('Delete'),
            _('Cut'),
            _('Paste'),
            _('Set Status'),
            _('Export manuscript filtered by viewpoint'),
            _('Export synopsis filtered by viewpoint'),
        )
        self.worldContextMenu.entryconfig(_('Copy'), state='normal')
        if self._ctrl.isLocked:
            # No changes allowed.
            for label in worldContextEntries:
                self.worldContextMenu.entryconfig(label, state='disabled')
            return

        for label in worldContextEntries:
            self.worldContextMenu.entryconfig(label, state='normal')

        if prefix == CHARACTER_PREFIX:
            return

        if prefix in (LOCATION_PREFIX, ITEM_PREFIX):
            # Context is not a character.
            for label in (
                _('Set Status'),
                _('Export manuscript filtered by viewpoint'),
                _('Export synopsis filtered by viewpoint'),
            ):
                self.worldContextMenu.entryconfig(label, state='disabled')
            return

        if prefix == CR_ROOT:
            for label in (
                _('Delete'),
                _('Cut'),
                _('Copy'),
                _('Paste'),
                _('Export manuscript filtered by viewpoint'),
                _('Export synopsis filtered by viewpoint'),
            ):
                self.worldContextMenu.entryconfig(label, state='disabled')
            return

        if prefix in (LC_ROOT, IT_ROOT):
            for label in(
                _('Delete'),
                _('Cut'),
                _('Copy'),
                _('Paste'),
                _('Export manuscript filtered by viewpoint'),
                _('Export synopsis filtered by viewpoint'),
                _('Set Status'),
            ):
                self.worldContextMenu.entryconfig(label, state='disabled')
            return


"""Provide a context menu class for the novelibre tree view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.sub_controller import SubController
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.widgets.context_menu import ContextMenu
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

    def __init__(self, model, treeView, controller):
        self._mdl = model
        self._tv = treeView
        self._ctrl = controller

        #--- Create local context menus.

        #--- Create a narrative context menu.
        self._bookContextMenu = ContextMenu(self._tv, tearoff=0)
        self._bookContextMenu.add_command(
            label=_('Add Section'),
            command=self._ctrl.add_new_section,
        )
        self._bookContextMenu.add_command(
            label=_('Add Chapter'),
            command=self._ctrl.add_new_chapter)
        self._bookContextMenu.add_command(
            label=_('Add Part'),
            command=self._ctrl.add_new_part,
        )
        self._bookContextMenu.add_command(
            label=_('Insert Stage'),
            command=self._ctrl.add_new_stage,
        )
        self._bookContextMenu.add_cascade(
            label=_('Change Level'),
            menu=self._tv.selectLevelMenu,
        )
        self._bookContextMenu.add_cascade(
            label=_('Export this chapter'),
            command=self._tv._export_manuscript,
        )
        self._bookContextMenu.add_separator()
        self._bookContextMenu.add_command(
            label=_('Delete'),
            accelerator=KEYS.DELETE[1],
            command=self._ctrl.delete_elements,
        )
        self._bookContextMenu.add_command(
            label=_('Cut'),
            accelerator=KEYS.CUT[1],
            command=self._ctrl.cut_element,
        )
        self._bookContextMenu.add_command(
            label=_('Copy'),
            accelerator=KEYS.COPY[1],
            command=self._ctrl.copy_element,
        )
        self._bookContextMenu.add_command(
            label=_('Paste'),
            accelerator=KEYS.PASTE[1],
            command=self._ctrl.paste_element,
        )
        self._bookContextMenu.add_separator()
        self._bookContextMenu.add_cascade(
            label=_('Set Type'),
            menu=self._tv.selectTypeMenu,
        )
        self._bookContextMenu.add_cascade(
            label=_('Set Status'),
            menu=self._tv.scStatusMenu,
        )
        self._bookContextMenu.add_command(
            label=_('Set Viewpoint...'),
            command=self._ctrl.set_viewpoint,
        )
        self._bookContextMenu.add_separator()
        self._bookContextMenu.add_command(
            label=_('Join with previous'),
            command=self._ctrl.join_sections,
        )
        self._bookContextMenu.add_separator()
        self._bookContextMenu.add_command(
            label=_('Chapter level'),
            command=self._tv.show_chapter_level,
        )
        self._bookContextMenu.add_command(
            label=_('Expand'),
            command=self._tv.expand_selected)
        self._bookContextMenu.add_command(
            label=_('Collapse'),
            command=self._tv.collapse_selected,
        )
        self._bookContextMenu.add_command(
            label=_('Expand all'),
            command=self._tv.expand_all,
        )
        self._bookContextMenu.add_command(
            label=_('Collapse all'),
            command=self._tv.collapse_all,
        )

        #--- Create a world element context menu.
        self.worldContextMenu = ContextMenu(self._tv, tearoff=0)
        self.worldContextMenu.add_command(
            label=_('Add'),
            command=self._ctrl.add_new_element,
        )
        self.worldContextMenu.add_separator()
        self.worldContextMenu.add_command(
            label=_('Export manuscript filtered by viewpoint'),
            command=self._tv._export_manuscript,
        )
        self.worldContextMenu.add_command(
            label=_('Export synopsis filtered by viewpoint'),
            command=self._tv._export_synopsis,
        )
        self.worldContextMenu.add_separator()
        self.worldContextMenu.add_command(
            label=_('Delete'), accelerator=KEYS.DELETE[1],
            command=self._ctrl.delete_elements,
        )
        self.worldContextMenu.add_command(
            label=_('Cut'),
            accelerator=KEYS.CUT[1],
            command=self._ctrl.cut_element,
        )
        self.worldContextMenu.add_command(
            label=_('Copy'),
            accelerator=KEYS.COPY[1],
            command=self._ctrl.copy_element,
        )
        self.worldContextMenu.add_command(
            label=_('Paste'),
            accelerator=KEYS.PASTE[1],
            command=self._ctrl.paste_element,
        )
        self.worldContextMenu.add_separator()
        self.worldContextMenu.add_cascade(
            label=_('Set Status'),
            menu=self._tv.crStatusMenu,
        )

        #--- Create a plot line context menu.
        self.plotContextMenu = ContextMenu(self._tv, tearoff=0)
        self.plotContextMenu.add_command(
            label=_('Add Plot line'),
            command=self._ctrl.add_new_plot_line,
        )
        self.plotContextMenu.add_command(
            label=_('Add Plot point'),
            command=self._ctrl.add_new_plot_point,
        )
        self.plotContextMenu.add_separator()
        self.plotContextMenu.add_command(
            label=_('Export manuscript filtered by plot line'),
            command=self._tv._export_manuscript,
        )
        self.plotContextMenu.add_command(
            label=_('Export synopsis filtered by plot line'),
            command=self._tv._export_synopsis,
        )
        self.plotContextMenu.add_separator()
        self.plotContextMenu.add_command(
            label=_('Change sections to Unused'),
            command=self._ctrl.exclude_plot_line,
        )
        self.plotContextMenu.add_command(
            label=_('Change sections to Normal'),
            command=self._ctrl.include_plot_line
        )
        self.plotContextMenu.add_separator()
        self.plotContextMenu.add_command(
            label=_('Delete'), accelerator=KEYS.DELETE[1],
            command=self._ctrl.delete_elements,
        )
        self.plotContextMenu.add_command(
            label=_('Cut'),
            accelerator=KEYS.CUT[1],
            command=self._ctrl.cut_element,
        )
        self.plotContextMenu.add_command(
            label=_('Copy'),
            accelerator=KEYS.COPY[1],
            command=self._ctrl.copy_element,
        )
        self.plotContextMenu.add_command(
            label=_('Paste'),
            accelerator=KEYS.PASTE[1],
            command=self._ctrl.paste_element,
        )

        #--- Create a project note context menu.
        self.projectnoteContextMenu = ContextMenu(self._tv, tearoff=0)
        self.projectnoteContextMenu.add_command(
            label=_('Add Project note'),
            command=self._ctrl.add_new_project_note,
        )
        self.projectnoteContextMenu.add_separator()
        self.projectnoteContextMenu.add_command(
            label=_('Delete'),
            accelerator=KEYS.DELETE[1],
            command=self._ctrl.delete_elements,
        )
        self.projectnoteContextMenu.add_command(
            label=_('Cut'),
            accelerator=KEYS.CUT[1],
            command=self._ctrl.cut_element,
        )
        self.projectnoteContextMenu.add_command(
            label=_('Copy'),
            accelerator=KEYS.COPY[1],
            command=self._ctrl.copy_element,
        )
        self.projectnoteContextMenu.add_command(
            label=_('Paste'),
            accelerator=KEYS.PASTE[1],
            command=self._ctrl.paste_element,
        )

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

    def open(self, event):
        # Event handler for the tree's context menu.
        # - Configure the context menu depending on
        #   the selected branch and the program state.
        # - Open it.
        if self._mdl.prjFile is None:
            return

        row = self._tv.tree.identify_row(event.y)
        if not row:
            return

        self._tv.go_to_node(row)
        if row.startswith(ROOT_PREFIX):
            prefix = row
        else:
            prefix = row[:2]

        if prefix in (
            CH_ROOT,
            CHAPTER_PREFIX,
            SECTION_PREFIX,
        ):
            self._configure_book_context_menu(prefix, row)
            try:
                self._bookContextMenu.tk_popup(event.x_root, event.y_root, 0)
            finally:
                self._bookContextMenu.grab_release()

        elif prefix in (
            CR_ROOT,
            CHARACTER_PREFIX,
            LC_ROOT,
            LOCATION_PREFIX,
            IT_ROOT,
            ITEM_PREFIX,
        ):
            self._configure_world_context_menu(prefix)
            try:
                self.worldContextMenu.tk_popup(event.x_root, event.y_root, 0)
            finally:
                self.worldContextMenu.grab_release()

        elif prefix in (
            PL_ROOT,
            PLOT_LINE_PREFIX,
            PLOT_POINT_PREFIX
        ):
            self._configure_plot_context_menu(prefix)
            try:
                self.plotContextMenu.tk_popup(event.x_root, event.y_root, 0)
            finally:
                self.plotContextMenu.grab_release()

        elif prefix in (
            PN_ROOT,
            PRJ_NOTE_PREFIX
        ):
            self._configure_project_note_context_menu(prefix)
            try:
                self.projectnoteContextMenu.tk_popup(
                    event.x_root,
                    event.y_root,
                    0
                )
            finally:
                self.projectnoteContextMenu.grab_release()

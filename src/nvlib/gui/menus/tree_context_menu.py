"""Provide a context menu class for the novelibre tree view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.sub_controller import SubController
from nvlib.gui.menus.nv_context_menu import NvContextMenu
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

    def __init__(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        #--- Book context menu.
        self._bookContextMenu = NvContextMenu()

        self._ui._add_chapter_part_commands(self._bookContextMenu)
        self._bookContextMenu.add_separator()
        self._ui._add_set_status_cascade(self._bookContextMenu)
        self._ui._add_set_viewpoint_command(self._bookContextMenu)
        self._bookContextMenu.add_separator()
        self._ui._add_view_commands(self._bookContextMenu)

        self._ctrl.register_client(self._bookContextMenu)

        #--- Chapter context menu.
        self._chapterContextMenu = NvContextMenu()

        self._ui._add_add_section_command(self._chapterContextMenu)
        self._ui._add_chapter_part_commands(self._chapterContextMenu)
        self._ui._add_insert_stage_command(self._chapterContextMenu)
        self._chapterContextMenu.add_separator()
        self._ui._add_delete_command(self._chapterContextMenu)
        self._chapterContextMenu.add_separator()
        self._ui._add_clipboard_commands(self._chapterContextMenu)
        self._chapterContextMenu.add_separator()
        self._ui._add_change_level_cascade(self._chapterContextMenu)
        self._ui._add_set_type_cascade(self._chapterContextMenu)
        self._ui._add_set_status_cascade(self._chapterContextMenu)
        self._ui._add_set_viewpoint_command(self._chapterContextMenu)
        self._chapterContextMenu.add_separator()

        label = _('Export this chapter')
        self._chapterContextMenu.add_cascade(
            label=label,
            command=self._ctrl.export_filtered_manuscript,
        )
        self._chapterContextMenu.disableOnLock.append(label)

        self._chapterContextMenu.add_separator()
        self._ui._add_view_commands(self._chapterContextMenu)

        self._ctrl.register_client(self._chapterContextMenu)

        #--- Character context menu.
        self._characterContextMenu = NvContextMenu()

        self._ui._add_add_command(self._characterContextMenu)
        self._characterContextMenu.add_separator()
        self._ui._add_delete_command(self._characterContextMenu)
        self._characterContextMenu.add_separator()
        self._ui._add_clipboard_commands(self._characterContextMenu)
        self._characterContextMenu.add_separator()
        self._ui._add_set_cr_status_cascade(self._characterContextMenu)
        self._characterContextMenu.add_separator()

        label = _('Export manuscript filtered by viewpoint')
        self._characterContextMenu.add_command(
            label=label,
            command=self._ctrl.export_filtered_manuscript,
        )
        self._characterContextMenu.disableOnLock.append(label)

        label = _('Export synopsis filtered by viewpoint')
        self._characterContextMenu.add_command(
            label=label,
            command=self._ctrl.export_filtered_synopsis,
        )
        self._characterContextMenu.disableOnLock.append(label)

        self._characterContextMenu.add_separator()
        self._ui._add_view_commands(self._characterContextMenu)

        self._ctrl.register_client(self._characterContextMenu)

        #--- Characters root context menu.
        self._crRootContextMenu = NvContextMenu()

        self._ui._add_add_command(self._crRootContextMenu)
        self._crRootContextMenu.add_separator()
        self._ui._add_set_cr_status_cascade(self._crRootContextMenu)
        self._crRootContextMenu.add_separator()
        self._ui._add_view_commands(self._crRootContextMenu)

        self._ctrl.register_client(self._crRootContextMenu)

        #--- Location/item/plot line/project note context menu.
        self._elementContextMenu = NvContextMenu()

        self._ui._add_add_command(self._elementContextMenu)
        self._elementContextMenu.add_separator()
        self._ui._add_delete_command(self._elementContextMenu)
        self._elementContextMenu.add_separator()
        self._ui._add_clipboard_commands(self._elementContextMenu)
        self._elementContextMenu.add_separator()
        self._ui._add_view_commands(self._elementContextMenu)

        self._ctrl.register_client(self._elementContextMenu)

        #--- Plot line context menu.
        self._plotLineContextMenu = NvContextMenu()

        label = _('Add Plot line')
        self._plotLineContextMenu.add_command(
            label=label,
            command=self._ctrl.add_new_plot_line,
        )
        self._plotLineContextMenu.disableOnLock.append(label)

        label = _('Add Plot point')
        self._plotLineContextMenu.add_command(
            label=label,
            command=self._ctrl.add_new_plot_point,
        )
        self._plotLineContextMenu.disableOnLock.append(label)

        self._plotLineContextMenu.add_separator()
        self._ui._add_delete_command(self._plotLineContextMenu)
        self._plotLineContextMenu.add_separator()
        self._ui._add_clipboard_commands(self._plotLineContextMenu)
        self._plotLineContextMenu.add_separator()

        label = _('Change sections to Unused')
        self._plotLineContextMenu.add_command(
            label=label,
            command=self._ctrl.exclude_plot_line,
        )
        self._plotLineContextMenu.disableOnLock.append(label)

        label = _('Change sections to Normal')
        self._plotLineContextMenu.add_command(
            label=label,
            command=self._ctrl.include_plot_line
        )
        self._plotLineContextMenu.disableOnLock.append(label)

        self._plotLineContextMenu.add_separator()

        label = _('Export manuscript filtered by plot line')
        self._plotLineContextMenu.add_command(
            label=label,
            command=self._ctrl.export_filtered_manuscript,
        )
        self._plotLineContextMenu.disableOnLock.append(label)

        label = _('Export synopsis filtered by plot line')
        self._plotLineContextMenu.add_command(
            label=label,
            command=self._ctrl.export_filtered_synopsis,
        )
        self._plotLineContextMenu.disableOnLock.append(label)

        self._plotLineContextMenu.add_separator()
        self._ui._add_view_commands(self._plotLineContextMenu)

        self._ctrl.register_client(self._plotLineContextMenu)

        #--- Locations/items/plot lines/project notes root menu.
        self._rootContextMenu = NvContextMenu()

        self._ui._add_add_command(self._rootContextMenu)
        self._rootContextMenu.add_separator()
        self._ui._add_view_commands(self._rootContextMenu)

        self._ctrl.register_client(self._rootContextMenu)

        #--- Section context menu.
        self._sectionContextMenu = NvContextMenu()

        self._ui._add_add_section_command(self._sectionContextMenu)
        self._ui._add_insert_stage_command(self._sectionContextMenu)
        self._sectionContextMenu.add_separator()
        self._ui._add_delete_command(self._sectionContextMenu)
        self._sectionContextMenu.add_separator()
        self._ui._add_clipboard_commands(self._sectionContextMenu)
        self._sectionContextMenu.add_separator()
        self._ui._add_set_type_cascade(self._sectionContextMenu)
        self._ui._add_set_status_cascade(self._sectionContextMenu)
        self._ui._add_set_viewpoint_command(self._sectionContextMenu)
        self._sectionContextMenu.add_separator()

        label = _('Join with previous')
        self._sectionContextMenu.add_command(
            label=label,
            command=self._ctrl.join_sections,
        )
        self._sectionContextMenu.disableOnLock.append(label)

        self._sectionContextMenu.add_separator()
        self._ui._add_view_commands(self._sectionContextMenu)

        self._ctrl.register_client(self._sectionContextMenu)

        #--- Stage context menu.
        self._stageContextMenu = NvContextMenu()

        self._ui._add_add_section_command(self._stageContextMenu)
        self._ui._add_insert_stage_command(self._stageContextMenu)
        self._stageContextMenu.add_separator()
        self._ui._add_delete_command(self._stageContextMenu)
        self._stageContextMenu.add_separator()
        self._ui._add_clipboard_commands(self._stageContextMenu)
        self._stageContextMenu.add_separator()
        self._ui._add_change_level_cascade(self._stageContextMenu)
        self._stageContextMenu.add_separator()
        self._ui._add_view_commands(self._stageContextMenu)

        self._ctrl.register_client(self._stageContextMenu)

        #--- Trash bin context menu.
        self._trashContextMenu = NvContextMenu()

        self._ui._add_delete_command(self._trashContextMenu)

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


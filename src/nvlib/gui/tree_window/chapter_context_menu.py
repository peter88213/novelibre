"""Provide a context menu class for the "Chapter" branch.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.tree_window.branch_context_menu import BranchContextMenu
from nvlib.nv_locale import _


class ChapterContextMenu(BranchContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self._add_add_section_command()
        self._add_chapter_part_commands()
        self._add_insert_stage_command()
        self._add_delete_command()
        self._add_clipboard_commands()
        self.add_separator()
        self._add_change_level_cascade(master)
        self._add_set_type_cascade(master)
        self._add_set_status_cascade(master)
        self._add_set_viewpoint_command()
        self.add_separator()

        label = _('Export this chapter')
        self.add_cascade(
            label=label,
            command=master._export_manuscript,
        )
        self._disableOnLock.append(label)

        self._add_view_commands(master)


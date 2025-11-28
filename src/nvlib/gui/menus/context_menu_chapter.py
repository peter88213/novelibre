"""Provide a context menu class for the "Chapter" branch.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_context_menu import NvContextMenu
from nvlib.nv_locale import _


class ContextMenuChapter(NvContextMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)

        self._add_add_section_command()
        self._add_chapter_part_commands()
        self._add_insert_stage_command()
        self.add_separator()
        self._add_delete_command()
        self.add_separator()
        self._add_clipboard_commands()
        self.add_separator()
        self._add_change_level_cascade()
        self._add_set_type_cascade()
        self._add_set_status_cascade()
        self._add_set_viewpoint_command()
        self.add_separator()

        label = _('Export this chapter')
        self.add_cascade(
            label=label,
            command=self._ctrl.export_filtered_manuscript,
        )
        self._disableOnLock.append(label)

        self.add_separator()
        self._add_view_commands()


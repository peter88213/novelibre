"""Provide a context menu class for stages.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_context_menu import NvContextMenu


class ContextMenuStage(NvContextMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)

        self._add_add_section_command()
        self._add_insert_stage_command()
        self._add_delete_command()
        self._add_clipboard_commands()
        self.add_separator()
        self._add_change_level_cascade()
        self._add_view_commands()


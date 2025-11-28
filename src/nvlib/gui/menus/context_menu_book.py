"""Provide a context menu class for the "Book" branch.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_context_menu import NvContextMenu


class ContextMenuBook(NvContextMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)

        self._add_chapter_part_commands()
        self.add_separator()
        self._add_set_status_cascade()
        self._add_set_viewpoint_command()
        self.add_separator()
        self._add_view_commands()


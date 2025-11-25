"""Provide a basic context menu class for branch elements.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_context_menu import NvContextMenu


class ContextMenuElement(NvContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self._add_add_command()
        self._add_delete_command()
        self._add_clipboard_commands()
        self._add_view_commands(master)


"""Provide a context menu class for the "Trash bin".

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_context_menu import NvContextMenu


class ContextMenuTrash(NvContextMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)
        self._add_delete_command()


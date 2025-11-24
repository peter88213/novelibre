"""Provide a context menu class for a "Characters" branch.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.tree_window.branch_context_menu import BranchContextMenu


class CrRootContextMenu(BranchContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self._add_add_command()
        self.add_separator()
        self._add_set_cr_status_cascade(master)
        self._add_view_commands(master)

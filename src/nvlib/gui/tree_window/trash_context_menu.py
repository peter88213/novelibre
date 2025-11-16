"""Provide a context menu class for the "Trash bin".

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.tree_window.branch_context_menu import BranchContextMenu
from nvlib.nv_locale import _


class TrashContextMenu(BranchContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self.add_command(
            label=_('Delete'),
            accelerator=KEYS.DELETE[1],
            command=self._ctrl.delete_elements,
        )
        self.add_separator()
        self.add_command(
            label=_('Chapter level'),
            command=master.show_chapter_level,
        )
        self.add_command(
            label=_('Expand'),
            command=master.expand_selected)
        self.add_command(
            label=_('Collapse'),
            command=master.collapse_selected,
        )
        self.add_command(
            label=_('Expand all'),
            command=master.expand_all,
        )
        self.add_command(
            label=_('Collapse all'),
            command=master.collapse_all,
        )
        self._disableOnLock = [
            _('Delete'),
        ]


"""Provide a context menu class for the "Project note" branch.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.tree_window.branch_context_menu import BranchContextMenu
from nvlib.nv_locale import _


class ProjectnoteContextMenu(BranchContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self.add_command(
            label=_('Add Project note'),
            command=self._ctrl.add_new_project_note,
        )
        self.add_separator()
        self.add_command(
            label=_('Delete'),
            accelerator=KEYS.DELETE[1],
            command=self._ctrl.delete_elements,
        )
        self.add_separator()
        self.add_command(
            label=_('Cut'),
            accelerator=KEYS.CUT[1],
            command=self._ctrl.cut_element,
        )
        self.add_command(
            label=_('Copy'),
            accelerator=KEYS.COPY[1],
            command=self._ctrl.copy_element,
        )
        self.add_command(
            label=_('Paste'),
            accelerator=KEYS.PASTE[1],
            command=self._ctrl.paste_element,
        )
        self._disableOnLock = [
            _('Add Project note'),
            _('Delete'),
            _('Cut'),
            _('Paste'),
        ]


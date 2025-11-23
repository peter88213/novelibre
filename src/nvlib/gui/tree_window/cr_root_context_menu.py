"""Provide a context menu class for the "Character" branch.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.tree_window.root_context_menu import RootContextMenu
from nvlib.nv_locale import _


class CrRootContextMenu(RootContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self.add_separator()
        self.add_cascade(
            label=_('Set Status'),
            menu=master.crStatusMenu,
        )
        self._disableOnLock.extend([
            _('Set Status'),
        ])

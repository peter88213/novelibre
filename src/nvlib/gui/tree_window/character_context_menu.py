"""Provide a context menu class for characters.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.tree_window.element_context_menu import ElementContextMenu
from nvlib.nv_locale import _


class CharacterContextMenu(ElementContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self.add_separator()
        self.add_cascade(
            label=_('Set Status'),
            menu=master.crStatusMenu,
        )
        self.add_separator()
        self.add_command(
            label=_('Export manuscript filtered by viewpoint'),
            command=master._export_manuscript,
        )
        self.add_command(
            label=_('Export synopsis filtered by viewpoint'),
            command=master._export_synopsis,
        )
        self._disableOnLock.extend([
            _('Set Status'),
            _('Export manuscript filtered by viewpoint'),
            _('Export synopsis filtered by viewpoint'),
        ])

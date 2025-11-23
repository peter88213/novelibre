"""Provide a context menu class for the "Book" branch.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.tree_window.world_root_context_menu import WorldRootContextMenu
from nvlib.nv_locale import _


class WorldContextMenu(WorldRootContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self.add_separator()
        self.add_command(
            label=_('Delete'), accelerator=KEYS.DELETE[1],
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
        self._disableOnLock.extend([
            _('Delete'),
            _('Cut'),
            _('Paste'),
        ])


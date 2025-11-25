"""Provide a context menu class for characters.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.context_menu_element import NvContextMenu
from nvlib.nv_locale import _


class ContextMenuCharacter(NvContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self._add_add_command()
        self._add_delete_command()
        self._add_clipboard_commands()
        self.add_separator()
        self._add_set_cr_status_cascade(master)
        self.add_separator()

        label = _('Export manuscript filtered by viewpoint')
        self.add_command(
            label=label,
            command=master._export_manuscript,
        )
        self._disableOnLock.append(label)

        label = _('Export synopsis filtered by viewpoint')
        self.add_command(
            label=label,
            command=master._export_synopsis,
        )
        self._disableOnLock.append(label)

        self._add_view_commands(master)

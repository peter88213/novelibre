"""Provide a class for the "Tools" menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.nv_locale import _
import tkinter as tk


class ToolsMenu(tk.Menu, NvMenu):

    def __init__(self, view, controller):
        tk.Menu.__init__(self, tearoff=0)
        NvMenu.__init__(self, view, controller)

        label = _('Backup options')
        self.add_command(
            label=label,
            command=self._ctrl.open_backup_options,
        )

        self.add_separator()

        label = _('Open installation folder')
        self.add_command(
            label=label,
            command=self._ctrl.open_installationFolder,
        )

        self.add_separator()

        label = _('Plugin Manager')
        self.add_command(
            label=label,
            command=self._ctrl.open_plugin_manager,
        )

        self.add_separator()

        label = _('Show notes')
        self.add_command(
            label=label,
            command=self._ctrl.show_notes_list,
        )

        self.add_separator()


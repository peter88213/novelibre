"""Provide a class for the "File" menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.platform.platform_settings import PLATFORM
from nvlib.nv_locale import _
import tkinter as tk


class FileMenu(tk.Menu, NvMenu):

    def __init__(self, master, model, view, controller):
        tk.Menu.__init__(self, master, tearoff=0)
        NvMenu.__init__(self, master, model, view, controller)

        label = _('New')
        self.add_cascade(
            label=label,
            menu=self._ui.newMenu
        )

        label = _('Open...')
        self.add_command(
            label=label,
            accelerator=KEYS.OPEN_PROJECT[1],
            command=self._ctrl.open_project,
        )

        label = _('Reload')
        self.add_command(
            label=label,
            accelerator=KEYS.RELOAD_PROJECT[1],
            command=self._ctrl.reload_project,
        )
        self._disableOnClose.append(label)
        self._disableOnLock.append(label)

        label = _('Restore backup')
        self.add_command(
            label=label,
            accelerator=KEYS.RESTORE_BACKUP[1],
            command=self._ctrl.restore_backup,
        )
        self._disableOnClose.append(label)
        self._disableOnLock.append(label)

        self.add_separator()

        label = _('Refresh Tree')
        self.add_command(
            label=label,
            accelerator=KEYS.REFRESH_TREE[1],
            command=self._ctrl.refresh_tree,
        )
        self._disableOnClose.append(label)
        self._disableOnLock.append(label)

        label = _('Lock')
        self.add_command(
            label=label,
            accelerator=KEYS.LOCK_PROJECT[1],
            command=self._ctrl.lock,
        )
        self._disableOnClose.append(label)

        label = _('Unlock')
        self.add_command(
            label=label,
            accelerator=KEYS.UNLOCK_PROJECT[1],
            command=self._ctrl.unlock,
        )
        self._disableOnClose.append(label)

        label = _('Open Project folder')
        self.add_separator()
        self.add_command(
            label=label,
            accelerator=KEYS.FOLDER[1],
            command=self._ctrl.open_project_folder,
        )
        self._disableOnClose.append(label)

        label = _('Copy style sheet')
        self.add_command(
            label=label,
            command=self._ctrl.copy_css,
        )
        self._disableOnClose.append(label)

        label = _('Discard manuscript')
        self.add_command(
            label=label,
            command=self._ctrl.discard_manuscript,
        )
        self._disableOnClose.append(label)
        self._disableOnLock.append(label)

        self.add_separator()

        label = _('Save')
        self.add_command(
            label=label,
            accelerator=KEYS.SAVE_PROJECT[1],
            command=self._ctrl.save_project,
        )
        self._disableOnClose.append(label)
        self._disableOnLock.append(label)

        label = _('Save as...')
        self.add_command(
            label=label,
            accelerator=KEYS.SAVE_AS[1],
            command=self._ctrl.save_as,
        )
        self._disableOnClose.append(label)

        label = _('Close')
        self.add_command(
            label=label,
            command=self._ctrl.close_project,
        )
        self._disableOnClose.append(label)

        if PLATFORM == 'win':
            label = _('Exit'),
        else:
                label = _('Quit'),
        self.add_command(
            label=label,
            accelerator=KEYS.QUIT_PROGRAM[1],
            command=self._ctrl.on_quit,
        )


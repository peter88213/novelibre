"""Provide a class for a backup options dialog.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.view.modal_dialog import ModalDialog
from nvlib.gui.platform.platform_settings import KEYS
from mvclib.widgets.label_disp import LabelDisp
from nvlib.gui.pop_up.backup_options_ctrl import BackupOptionsCtrl
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class BackupOptionsDialog(ModalDialog, BackupOptionsCtrl):
    """A pop-up window with export preference settings."""
    LABEL_WIDTH = 20

    def __init__(self, model, view, controller, **kw):
        super().__init__(view, **kw)
        self.initialize_controller(model, view, controller)
        self._ui.restore_status()

        self.title(_('Backup options'))
        window = ttk.Frame(self)
        window.pack(
            fill='both',
            padx=50,
            pady=5
            )
        frame1 = ttk.Frame(window)
        frame1.pack(fill='both', side='left')

        # Backup directory display.
        self.backupDirVar = tk.StringVar(frame1, value=prefs['backup_dir'])
        self.backupDirDisplay = LabelDisp(
            frame1,
            f"{_('Backup directory')}:",
            self.backupDirVar,
            lblWidth=self.LABEL_WIDTH,
            )

        # Button: Change backup directory.
        ttk.Button(
            frame1,
            text=_('Change backup directory'), command=self.set_backup_dir,
            ).pack(anchor='w', fill='x')

        # Button: Open backup directory.
        ttk.Button(
            frame1,
            text=_('Open backup directory'), command=self.open_backup_dir,
            ).pack(anchor='w', fill='x')

        # Checkbox: Ask whether backup copies shall be created.
        self.enableBackupVar = tk.BooleanVar(frame1, value=prefs['enable_backup'])
        ttk.Checkbutton(
            frame1,
            text=_('Create backup copies'),
            variable=self.enableBackupVar
            ).pack(padx=5, pady=5, anchor='w')
        self.enableBackupVar.trace('w', self.change_enable_backup)

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        # "Close" button.
        ttk.Button(
            self,
            text=_('Close'),
            command=self.destroy
            ).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            self,
            text=_('Online help'),
            command=self.open_help
            ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], self.open_help)


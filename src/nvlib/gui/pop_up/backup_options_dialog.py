"""Provide a class for a backup options dialog.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import filedialog
from tkinter import ttk

from nvlib.controller.services.nv_help import NvHelp
from nvlib.controller.sub_controller import SubController
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.widgets.label_disp import LabelDisp
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.model.file.doc_open import open_document
from nvlib.novx_globals import norm_path
from nvlib.nv_globals import HOME_DIR
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class BackupOptionsDialog(ModalDialog, SubController):
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
            text=_('Change backup directory'), command=self._set_backup_dir,
            ).pack(anchor='w', fill='x')

        # Button: Open backup directory.
        ttk.Button(
            frame1,
            text=_('Open backup directory'), command=self._open_backup_dir,
            ).pack(anchor='w', fill='x')

        # Checkbox: Ask whether backup copies shall be created.
        self.enableBackupVar = tk.BooleanVar(
            frame1,
            value=prefs['enable_backup']
        )
        ttk.Checkbutton(
            frame1,
            text=_('Create backup copies'),
            variable=self.enableBackupVar
            ).pack(padx=5, pady=5, anchor='w')
        self.enableBackupVar.trace('w', self._change_enable_backup)

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
            command=self._open_help
            ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], self.open_help)

    def _change_enable_backup(self, *args):
        prefs['enable_backup'] = self.enableBackupVar.get()
        if not prefs['enable_backup']:
            return

        if not os.path.isdir(prefs['backup_dir']):
            self._set_backup_dir()

    def _open_backup_dir(self):
        # Open the backup directory with the OS file manager.
        self._ui.restore_status()
        if not os.path.isdir(prefs['backup_dir']):
            self._ui.set_status(
                f'#{_("Backup directory not found")}. {_("Please check the setting")}.')
            return

        try:
            open_document(prefs['backup_dir'])
        except Exception as ex:
            self._ui.set_status(f'!{str(ex)}')

    def _open_help(self, event=None):
        NvHelp.open_help_page(
            f'tools_menu.html#{_("Backup options").lower()}')

    def _set_backup_dir(self):
        self._ui.restore_status()
        if os.path.isdir(prefs['backup_dir']):
            initDir = prefs['backup_dir']
        else:
            initDir = HOME_DIR
        backupDir = filedialog.askdirectory(initialdir=initDir)
        if not backupDir:
            self._ui.set_status(
                f'#{_("Action canceled by user")}.')
            return

        prefs['backup_dir'] = backupDir
        self.backupDirVar.set(norm_path(backupDir))

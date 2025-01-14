"""Provide a mixin class for a backup options controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import filedialog

from mvclib.controller.sub_controller import SubController
from nvlib.controller.services.nv_help import NvHelp
from nvlib.model.file.doc_open import open_document
from nvlib.novx_globals import norm_path
from nvlib.nv_globals import HOME_DIR
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class BackupOptionsCtrl(SubController):

    def change_enable_backup(self, *args):
        prefs['enable_backup'] = self.enableBackupVar.get()
        if not prefs['enable_backup']:
            return

        if not os.path.isdir(prefs['backup_dir']):
            self.set_backup_dir()

    def open_backup_dir(self):
        """Open the backup directory with the OS file manager."""
        self._ui.restore_status()
        if not os.path.isdir(prefs['backup_dir']):
            self._ui.set_status(f'#{_("Backup directory not found")}. {_("Please check the setting")}.')
            return

        open_document(prefs['backup_dir'])

    def open_help(self, event=None):
        NvHelp.open_help_page(f'tools_menu.html#{_("Backup options").lower()}')

    def set_backup_dir(self):
        self._ui.restore_status()
        if os.path.isdir(prefs['backup_dir']):
            initDir = prefs['backup_dir']
        else:
            initDir = HOME_DIR
        backupDir = filedialog.askdirectory(initialdir=initDir)
        if not backupDir:
            self._ui.set_status(f'#{_("Action canceled by user")}.')
            return

        prefs['backup_dir'] = backupDir
        self.backupDirVar.set(norm_path(backupDir))

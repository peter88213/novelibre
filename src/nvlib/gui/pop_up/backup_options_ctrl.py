"""Provide a mixin class for a backup options controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
from tkinter import filedialog

from mvclib.controller.sub_controller import SubController
from nvlib.novx_globals import norm_path
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

        try:
            os.startfile(norm_path(prefs['backup_dir']))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(prefs['backup_dir']))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(prefs['backup_dir']))
                    # Mac
                except:
                    pass
        return 'break'

    def set_backup_dir(self):
        self._ui.restore_status()
        if os.path.isdir(prefs['backup_dir']):
            startDir = prefs['backup_dir']
        else:
            startDir = str(Path.home()).replace('\\', '/')
        backupDir = filedialog.askdirectory(initialdir=startDir)
        if not backupDir:
            self._ui.set_status(f'#{_("Action canceled by user")}.')
            return

        prefs['backup_dir'] = backupDir
        self.backupDirVar.set(norm_path(backupDir))

"""Provide a mixin class for an export options controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import filedialog
import zipfile

from nvlib.controller.services.nv_help import NvHelp
from nvlib.controller.sub_controller import SubController
from nvlib.nv_globals import USER_STYLES_DIR
from nvlib.nv_globals import USER_STYLES_XML
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class ExportOptionsCtrl(SubController):

    def change_ask_doc_open(self, *args):
        prefs['ask_doc_open'] = self.askDocOpenVar.get()

    def change_lock_on_export(self, *args):
        prefs['lock_on_export'] = self.lockOnExportVar.get()

    def open_help(self, event=None):
        NvHelp.open_help_page(f'export_menu.html#{_("options").lower()}')

    def restore_default_styles(self, *args):
        try:
            os.remove(USER_STYLES_XML)
        except:
            pass

    def set_user_styles(self, *args):
        os.makedirs(USER_STYLES_DIR, exist_ok=True)
        fileTypes = [
            (f'{_("ODF Text Document Template")} (*.ott)', '.ott'),
            (f'{_("ODF Text Document")} (*.odt)', '.odt') ,
        ]
        docTemplate = filedialog.askopenfilename(
            filetypes=fileTypes,
            defaultextension=fileTypes[0][1],
            )
        if not docTemplate:
            return

        try:
            with zipfile.ZipFile(docTemplate) as myzip:
                myzip.extract('styles.xml', path=USER_STYLES_DIR)
        except:
            pass


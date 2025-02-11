"""Provide a mixin class for an export options controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import filedialog
from xml.etree import ElementTree as ET
import zipfile

from nvlib.controller.services.nv_help import NvHelp
from nvlib.controller.sub_controller import SubController
from nvlib.nv_globals import USER_STYLES_DIR
from nvlib.nv_globals import USER_STYLES_XML
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
from nvlib.model.odt.odt_writer import OdtWriter


class ExportOptionsCtrl(SubController):

    def change_ask_doc_open(self, *args):
        prefs['ask_doc_open'] = self.askDocOpenVar.get()

    def change_lock_on_export(self, *args):
        prefs['lock_on_export'] = self.lockOnExportVar.get()

    def open_help(self, event=None):
        NvHelp.open_help_page(f'export_menu.html#{_("options").lower()}')

    def restore_default_styles(self, *args):
        self._ui.restore_status()
        try:
            os.remove(USER_STYLES_XML)
        except:
            self._ui.set_status(f'#{_("Default styles are already set")}.')
        else:
            self._ui.set_status(f'{_("Default styles are restored")}.')

    def set_user_styles(self, *args):
        self._ui.restore_status()
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

        templateName = os.path.basename(docTemplate)
        try:
            with zipfile.ZipFile(docTemplate) as myzip:
                with myzip.open('styles.xml') as myfile:
                    stylesXmlStr = myfile.read().decode('utf-8')
            stylesXmlStr = OdtWriter.discard_novelibre_styles(stylesXmlStr)
            with open(USER_STYLES_XML, 'w', encoding='utf-8') as f:
                f.write(stylesXmlStr)
        except:
            self._ui.set_status(f'!{_("Invalid document template")}: "{templateName}".')
        else:
            self._ui.set_status(f'{_("Document template is set")}: "{templateName}".')


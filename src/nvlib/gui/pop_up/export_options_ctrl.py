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
            stylesXmlStr = self._discard_novelibre_styles(stylesXmlStr)
            with open(USER_STYLES_XML, 'w', encoding='utf-8') as f:
                f.write(stylesXmlStr)
        except:
            self._ui.set_status(f'!{_("Invalid document template")}: "{templateName}".')
        else:
            self._ui.set_status(f'{_("Document template is set")}: "{templateName}".')

    def _discard_novelibre_styles(self, stylesXmlStr):
        namespaces = dict(
            office='urn:oasis:names:tc:opendocument:xmlns:office:1.0',
            style='urn:oasis:names:tc:opendocument:xmlns:style:1.0',
            text='urn:oasis:names:tc:opendocument:xmlns:text:1.0',
            table='urn:oasis:names:tc:opendocument:xmlns:table:1.0',
            draw='urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
            fo='urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
            xlink='http://www.w3.org/1999/xlink',
            dc='http://purl.org/dc/elements/1.1/',
            meta='urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
            number='urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0',
            svg='urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0',
            chart='urn:oasis:names:tc:opendocument:xmlns:chart:1.0',
            dr3d='urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0',
            math='http://www.w3.org/1998/Math/MathML',
            form='urn:oasis:names:tc:opendocument:xmlns:form:1.0',
            script='urn:oasis:names:tc:opendocument:xmlns:script:1.0',
            ooo='http://openoffice.org/2004/office',
            ooow='http://openoffice.org/2004/writer',
            oooc='http://openoffice.org/2004/calc',
            dom='http://www.w3.org/2001/xml-events',
            rpt='http://openoffice.org/2005/report',
            of='urn:oasis:names:tc:opendocument:xmlns:of:1.2',
            xhtml='http://www.w3.org/1999/xhtml',
            grddl='http://www.w3.org/2003/g/data-view#',
            tableooo='http://openoffice.org/2009/table',
            loext='urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0'
        )
        for prefix in namespaces:
            ET.register_namespace(prefix, namespaces[prefix])
        root = ET.fromstring(stylesXmlStr)
        officeStyles = root.find('office:styles', namespaces)
        novelibreStyleNames = []
        novelibreStyles = ET.fromstring(OdtWriter._NOVELIBRE_STYLES)
        for novelibreStyle in novelibreStyles.iterfind('style:style', namespaces):
            novelibreStyleNames.append(novelibreStyle.attrib[f"{{{namespaces['style']}}}name"])
        stylesToDiscard = []
        for officeStyle in officeStyles.iterfind('style:style', namespaces):
            officeStyleName = officeStyle.attrib[f"{{{namespaces['style']}}}name"]
            if officeStyleName in novelibreStyleNames:
                stylesToDiscard.append(officeStyle)
        for officeStyle in stylesToDiscard:
            officeStyles.remove(officeStyle)
        stylesXmlStr = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
        return stylesXmlStr


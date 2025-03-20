"""Provide a mixin class for an reimport controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os

from nvlib.controller.services.nv_help import NvHelp
from nvlib.controller.sub_controller import SubController
from nvlib.model.odf.check_odf import odf_is_locked
from nvlib.novx_globals import norm_path
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class ReimportCtrl(SubController):

    def import_document(self, event=None):
        try:
            filePath = self.documentCollection.selection()[0]
        except IndexError:
            pass
        else:
            self._ctrl.import_odf(sourcePath=filePath, parent=self)
        importButtonState = 'disabled'
        self.importButton.configure(state=importButtonState)
        self.list_documents()

    def delete_document(self, event=None):
        filePath = self.documentCollection.selection()[0]
        if filePath and self._ui.ask_yes_no(
            message=f'{_("Delete file")}?',
            detail=norm_path(filePath),
            title=_('Discard'),
            parent=self
            ):
            try:
                os.remove(filePath)
                self.documentCollection.delete(filePath)
            except Exception as ex:
                self._ui.set_status(f'!{str(ex)}')

    def list_documents(self):
        prjDir, prjFile = os.path.split(self._mdl.prjFile.filePath)
        prjName, __ = os.path.splitext(prjFile)
        self._prjDocuments = {}
        for file in os.listdir(prjDir):
            for docType in self._docTypes:
                if file == f'{prjName}{docType}':
                    self._prjDocuments[f'{prjDir}/{file}'] = self._docTypes[docType]
        self._reset_tree()
        for filePath in self._prjDocuments:
            timestamp = os.path.getmtime(filePath)
            nodeTags = []
            try:
                documentType = self._prjDocuments[filePath]
            except:
                documentType = _('No document type')
            try:
                documentDate = datetime.fromtimestamp(timestamp).strftime('%c')
            except:
                documentDate = _('unknown')
            columns = [documentType, documentDate]
            if odf_is_locked(filePath):
                nodeTags.append('locked')
            elif timestamp > self._mdl.prjFile.timestamp:
                nodeTags.append('newer')
            self.documentCollection.insert('', 'end', filePath, values=columns, tags=tuple(nodeTags))

    def on_select_document(self, event=None):
        try:
            filePath = self.documentCollection.selection()[0]
        except IndexError:
            delButtonState = 'disabled'
            impButtonState = 'disabled'
        else:
            if odf_is_locked(filePath):
                delButtonState = 'disabled'
                if self.importModeVar.get() != 2:
                    impButtonState = 'disabled'
                else:
                    impButtonState = 'normal'
            else:
                delButtonState = 'normal'
                impButtonState = 'normal'
        self.deleteButton.configure(state=delButtonState)
        self.importButton.configure(state=impButtonState)

    def open_help(self, event=None):
        NvHelp.open_help_page(f'import_menu.html')

    def save_options(self, event=None, *args):
        """Save "discard temporary documents" state."""
        prefs['import_mode'] = str(self.importModeVar.get())

    def _reset_tree(self):
        """Clear the displayed tree."""
        for child in self.documentCollection.get_children(''):
            self.documentCollection.delete(child)


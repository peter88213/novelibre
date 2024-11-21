"""Provide a mixin class for controlling the project update manager.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from mvclib.controller.sub_controller import SubController
from nvlib.model.odf.check_odf import odf_is_locked
from nvlib.novx_globals import _
from nvlib.nv_globals import open_help


class PrjUpdaterCtrl(SubController):
    """Project update manager.
    
    A pop-up window displaying a picklist of previously exported documents
    for re-import.
    """

    def delete_document(self, event=None):
        filePath = self.documentCollection.selection()[0]
        if filePath and self._ui.ask_yes_no(f'{_("Delete file")} "{filePath}"?'):
            try:
                os.remove(filePath)
                self.documentCollection.delete(filePath)
            except Exception as ex:
                self._ui.set_status(f'!{str(ex)}')

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

    def import_document(self, event=None):
        try:
            filePath = self.documentCollection.selection()[0]
        except IndexError:
            pass
        else:
            self._ctrl.import_odf(sourcePath=filePath)
        importButtonState = 'disabled'
        self.importButton.configure(state=importButtonState)
        self.list_documents()

    def open_help(self, event=None):
        open_help(f'import_menu.html')


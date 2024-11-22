"""Provide a mixin class for an export options controller.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController
from nvlib.novx_globals import _
from nvlib.nv_globals import open_help
from nvlib.nv_globals import prefs


class ExportOptionsCtrl(SubController):

    def change_ask_doc_open(self, *args):
        prefs['ask_doc_open'] = self.askDocOpenVar.get()

    def change_lock_on_export(self, *args):
        prefs['lock_on_export'] = self.lockOnExportVar.get()

    def open_help(self, event=None):
        open_help(f'export_menu.html#{_("options").lower()}')

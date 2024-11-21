"""Provide a class for a project update manager.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os
from tkinter import ttk

from mvclib.view.modal_dialog import ModalDialog
from nvlib.controller.pop_up.prj_updater_ctrl import PrjUpdaterCtrl
from nvlib.model.converter.novx_converter import NovxConverter
from nvlib.model.odf.check_odf import odf_is_locked
from nvlib.novx_globals import _
from nvlib.nv_globals import prefs
from nvlib.view.platform.platform_settings import KEYS
import tkinter as tk


class PrjUpdater(ModalDialog, PrjUpdaterCtrl):
    """Project update manager.
    
    A pop-up window displaying a picklist of previously exported documents
    for re-import.
    """

    def __init__(self, model, view, controller, **kw):
        if model.prjFile.filePath is None:
            return

        super().__init__(view, **kw)
        self.initialize_controller(model, view, controller)

        self.title(_('Exported documents'))
        window = ttk.Frame(self)
        window.pack(fill='both', expand=True)

        columns = 'Document', 'Date'
        self.documentCollection = ttk.Treeview(window, columns=columns, show='headings', selectmode='browse')
        self.documentCollection.pack(fill='both', expand=True)
        self.documentCollection.bind('<<TreeviewSelect>>', self.on_select_document)
        self.documentCollection.tag_configure('newer', foreground='green')
        self.documentCollection.tag_configure('locked', foreground='red')

        self.documentCollection.column('Document', width=300, minwidth=250, stretch=True)
        self.documentCollection.heading('Document', text=_('Document'), anchor='w')
        self.documentCollection.column('Date', minwidth=120, stretch=False)
        self.documentCollection.heading('Date', text=_('Date'), anchor='w')

        # "Discard after import" checkbox.
        IMPORT_MODES = [
            _("Discard documents only when sections are split"),
            _("Always discard documents after import"),
            _("Import documents even if locked; do not discard")
            ]
        try:
            importMode = int(prefs['import_mode'])
        except:
            importMode = 0
        if importMode >= len(IMPORT_MODES):
            importMode = 0

        self.importModeVar = tk.IntVar(window, value=importMode)
        for i, buttonLabel in enumerate(IMPORT_MODES):
            ttk.Radiobutton(
                window,
                text=buttonLabel,
                variable=self.importModeVar,
                value=i,
                command=self.on_select_document
                ).pack(padx=5, pady=1, anchor='w')
        self.importModeVar.trace('w', self._save_options)

        # "Import" button.
        self.importButton = ttk.Button(window, text=_('Import'), command=self.import_document, state='disabled')
        self.importButton.pack(padx=5, pady=5, side='left')

        # "Discard" button.
        self.deleteButton = ttk.Button(window, text=_('Discard'), command=self.delete_document, state='disabled')
        self.deleteButton.pack(padx=5, pady=5, side='left')

        # "Refresh view" button.
        self._refreshButton = ttk.Button(window, text=_('Refresh view'), command=self.list_documents)
        self._refreshButton.pack(padx=5, pady=5, side='left')

        # "Close" button.
        ttk.Button(window, text=_('Close'), command=self.destroy).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            window,
            text=_('Online help'),
            command=self.open_help
            ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], self.open_help)
        self.documentCollection.bind('<Double-1>', self.import_document)
        self.documentCollection.bind('<Return>', self.import_document)

        self._docTypes = {}
        for docClass in NovxConverter.IMPORT_SOURCE_CLASSES:
            self._docTypes[f'{docClass.SUFFIX}{docClass.EXTENSION}'] = docClass.DESCRIPTION

        self.list_documents()

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

    def _reset_tree(self):
        """Clear the displayed tree."""
        for child in self.documentCollection.get_children(''):
            self.documentCollection.delete(child)

    def _save_options(self, event=None, *args):
        """Save "discard temporary documents" state."""
        prefs['import_mode'] = str(self.importModeVar.get())


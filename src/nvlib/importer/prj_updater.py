"""Provide a class for a project update manager.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os
from tkinter import ttk

from novxlib.converter.novx_converter import NovxConverter
from novxlib.novx_globals import _
from novxlib.odf.check_odf import odf_is_locked
from nvlib.nv_globals import open_help
from nvlib.nv_globals import prefs
from nvlib.view.key_definitions import KEYS
import tkinter as tk


class PrjUpdater(tk.Toplevel):
    """Project update manager.
    
    A pop-up window displaying a picklist of previously exported documents
    for re-import.
    """

    def __init__(self, model, view, controller, size, **kw):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        if self._mdl.prjFile.filePath is None:
            return

        super().__init__(**kw)
        self.title(f'{_("Exported documents")} - novelibre @release')
        self.geometry(size)
        self.grab_set()
        self.focus()
        window = ttk.Frame(self)
        window.pack(fill='both', expand=True)

        columns = 'Document', 'Date'
        self._documentCollection = ttk.Treeview(window, columns=columns, show='headings', selectmode='browse')
        self._documentCollection.pack(fill='both', expand=True)
        self._documentCollection.bind('<<TreeviewSelect>>', self._on_select_document)
        self._documentCollection.tag_configure('newer', foreground='green')
        self._documentCollection.tag_configure('locked', foreground='red')

        self._documentCollection.column('Document', width=300, minwidth=250, stretch=True)
        self._documentCollection.heading('Document', text=_('Document'), anchor='w')
        self._documentCollection.column('Date', minwidth=120, stretch=False)
        self._documentCollection.heading('Date', text=_('Date'), anchor='w')

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

        self._importMode = tk.IntVar(window, value=importMode)
        for i, buttonLabel in enumerate(IMPORT_MODES):
            ttk.Radiobutton(
                window,
                text=buttonLabel,
                variable=self._importMode,
                value=i,
                command=self._on_select_document
                ).pack(padx=5, pady=1, anchor='w')
        self._importMode.trace('w', self._save_options)

        # "Import" button.
        self._importButton = ttk.Button(window, text=_('Import'), command=self._import_document, state='disabled')
        self._importButton.pack(padx=5, pady=5, side='left')

        # "Discard" button.
        self._deleteButton = ttk.Button(window, text=_('Discard'), command=self._delete_document, state='disabled')
        self._deleteButton.pack(padx=5, pady=5, side='left')

        # "Refresh view" button.
        self._refreshButton = ttk.Button(window, text=_('Refresh view'), command=self.list_documents)
        self._refreshButton.pack(padx=5, pady=5, side='left')

        # "Close" button.
        ttk.Button(window, text=_('Close'), command=self.destroy).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            window,
            text=_('Online help'),
            command=self._open_help
            ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP, self._open_help)
        self._documentCollection.bind('<Double-1>', self._import_document)
        self._documentCollection.bind('<Return>', self._import_document)

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
            self._documentCollection.insert('', 'end', filePath, values=columns, tags=tuple(nodeTags))

    def _delete_document(self, event=None):
        filePath = self._documentCollection.selection()[0]
        if filePath and self._ui.ask_yes_no(f'{_("Delete file")} "{filePath}"?'):
            try:
                os.remove(filePath)
                self._documentCollection.delete(filePath)
            except Exception as ex:
                self._ui.set_status(f'!{str(ex)}')

    def _on_select_document(self, event=None):
        try:
            filePath = self._documentCollection.selection()[0]
        except IndexError:
            delButtonState = 'disabled'
            impButtonState = 'disabled'
        else:
            if odf_is_locked(filePath):
                delButtonState = 'disabled'
                if self._importMode.get() != 2:
                    impButtonState = 'disabled'
                else:
                    impButtonState = 'normal'
            else:
                delButtonState = 'normal'
                impButtonState = 'normal'
        self._deleteButton.configure(state=delButtonState)
        self._importButton.configure(state=impButtonState)

    def _import_document(self, event=None):
        try:
            filePath = self._documentCollection.selection()[0]
        except IndexError:
            pass
        else:
            self._ctrl.import_odf(sourcePath=filePath)
        importButtonState = 'disabled'
        self._importButton.configure(state=importButtonState)
        self.list_documents()

    def _open_help(self, event=None):
        open_help(f'import_menu.html')

    def _update_project(self, event=None):
        pass

    def _reset_tree(self):
        """Clear the displayed tree."""
        for child in self._documentCollection.get_children(''):
            self._documentCollection.delete(child)

    def _save_options(self, event=None, *args):
        """Save "discard temporary documents" state."""
        prefs['import_mode'] = str(self._importMode.get())


"""Provide a class for an re import dialog.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.view.modal_dialog import ModalDialog
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.pop_up.reimport_ctrl import ReimportCtrl
from nvlib.model.converter.novx_converter import NovxConverter
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class ReimportDialog(ModalDialog, ReimportCtrl):
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
        self.importModeVar.trace('w', self.save_options)

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


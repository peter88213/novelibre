"""Provide a class for an re import dialog.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os
from tkinter import ttk

from nvlib.controller.sub_controller import SubController
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.model.converter.novx_conversion import NovxConversion
from nvlib.model.odf.check_odf import odf_is_locked
from nvlib.novx_globals import norm_path
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class ReimportDialog(ModalDialog, SubController, NovxConversion):
    """Project update manager.
    
    A pop-up window displaying a picklist of previously 
    exported documents for re-import.
    """
    MIN_HEIGHT = 400
    MIN_WIDTH = 600
    RESIZABLE = True

    def __init__(self, model, view, controller, **kw):
        if model.prjFile.filePath is None:
            return

        super().__init__(view, **kw)
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._ui.restore_status()

        self.title(_('Exported documents'))
        self.iconphoto(False, view.icons.updateFromManuscriptIcon)
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

        mainWindow = ttk.Frame(self)
        mainWindow.pack(fill='both', expand=True)

        columns = 'Document', 'Date'
        self._documentCollection = ttk.Treeview(
            mainWindow,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        scrollY = ttk.Scrollbar(
            self._documentCollection,
            orient='vertical',
            command=self._documentCollection.yview,
        )
        self._documentCollection.configure(yscrollcommand=scrollY.set)
        scrollY.pack(side='right', fill='y')

        self._documentCollection.pack(fill='both', expand=True)
        self._documentCollection.bind(
            '<<TreeviewSelect>>', self._on_select_document)
        self._documentCollection.tag_configure(
            'newer', foreground='green')
        self._documentCollection.tag_configure(
            'locked', foreground='red')

        self._documentCollection.column(
            'Document', width=300, minwidth=250, stretch=True)
        self._documentCollection.heading(
            'Document', text=_('Document'), anchor='w')
        self._documentCollection.column(
            'Date', minwidth=120, stretch=False)
        self._documentCollection.heading(
            'Date', text=_('Date'), anchor='w')

        #--- Settings.

        # "Discard after import" checkbox.
        IMPORT_MODES = [
            _("Discard documents only if the project structure is modified"),
            _("Always discard documents after import"),
            _("Import documents even if locked; do not discard")
        ]
        try:
            importMode = int(prefs['import_mode'])
        except:
            importMode = 0
        if importMode >= len(IMPORT_MODES):
            importMode = 0

        self._importModeVar = tk.IntVar(mainWindow, value=importMode)
        for i, buttonLabel in enumerate(IMPORT_MODES):
            ttk.Radiobutton(
                mainWindow,
                text=buttonLabel,
                variable=self._importModeVar,
                value=i,
                command=self._save_options,
            ).pack(padx=5, pady=1, anchor='w')

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        #--- Footer bar.
        footer = tk.Frame(self)
        footer.pack(fill='both', expand=False)

        # "Import" button.
        self._importButton = ttk.Button(
            footer,
            text=_('Import'),
            command=self._import_document,
            state='disabled'
        )
        self._importButton.pack(padx=5, pady=5, side='left')

        # "Discard" button.
        self._deleteButton = ttk.Button(
            footer,
            text=_('Discard'),
            command=self._delete_document,
            state='disabled'
        )
        self._deleteButton.pack(padx=5, pady=5, side='left')

        # "Refresh view" button.
        self._refreshButton = ttk.Button(
            footer,
            text=_('Refresh view'),
            command=self._list_documents
        )
        self._refreshButton.pack(padx=5, pady=5, side='left')

        # "Close" button.
        ttk.Button(
            footer,
            text=_('Close'),
            command=self.destroy,
        ).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            footer,
            text=_('Help'),
            command=self._open_help,
        ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], self._open_help)
        self._documentCollection.bind(
            '<Double-1>', self._import_document)
        self._documentCollection.bind(
            '<Return>', self._import_document)

        self._docTypes = {}
        for docClass in self.IMPORT_SOURCE_CLASSES:
            self._docTypes[f'{docClass.SUFFIX}{docClass.EXTENSION}'
                           ] = docClass.DESCRIPTION

        self._list_documents()

    def _delete_document(self, event=None):
        filePath = self._documentCollection.selection()[0]
        if filePath and self._ui.ask_yes_no(
            message=_('Delete file?'),
            detail=norm_path(filePath),
            title=_('Discard'),
            parent=self
            ):
            try:
                os.remove(filePath)
                self._documentCollection.delete(filePath)
            except Exception as ex:
                self._ui.set_status(f'!{str(ex)}')

    def _import_document(self, event=None):
        self._ui.restore_status()
        try:
            filePath = self._documentCollection.selection()[0]
        except IndexError:
            pass
        else:
            self._ctrl.import_odf(sourcePath=filePath, parent=self)
        importButtonState = 'disabled'
        self._importButton.configure(state=importButtonState)
        self._list_documents()

    def _list_documents(self):
        if not self._mdl.prjFile:
            return

        prjDir, prjFile = os.path.split(self._mdl.prjFile.filePath)
        prjName, __ = os.path.splitext(prjFile)
        self._prjDocuments = {}
        for file in os.listdir(prjDir):
            for docType in self._docTypes:
                if file == f'{prjName}{docType}':
                    self._prjDocuments[f'{prjDir}/{file}'] = (
                        self._docTypes[docType]
                    )
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
            self._documentCollection.insert(
                '',
                'end',
                filePath,
                values=columns,
                tags=tuple(nodeTags)
            )

    def _on_select_document(self, event=None):
        try:
            filePath = self._documentCollection.selection()[0]
        except IndexError:
            delButtonState = 'disabled'
            impButtonState = 'disabled'
        else:
            if odf_is_locked(filePath):
                delButtonState = 'disabled'
                if self._importModeVar.get() != 2:
                    impButtonState = 'disabled'
                else:
                    impButtonState = 'normal'
            else:
                delButtonState = 'normal'
                impButtonState = 'normal'
        self._deleteButton.configure(state=delButtonState)
        self._importButton.configure(state=impButtonState)

    def _open_help(self, event=None):
        self._ctrl.open_help(page=f'import_menu.html')

    def _reset_tree(self):
        """Clear the displayed tree."""
        for child in self._documentCollection.get_children(''):
            self._documentCollection.delete(child)

    def _save_options(self, event=None, *args):
        """Save "discard temporary documents" state."""
        prefs['import_mode'] = str(self._importModeVar.get())


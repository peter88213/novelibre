"""Provide a class for export settings.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.view.modal_dialog import ModalDialog
from nvlib.novx_globals import _
from nvlib.nv_globals import open_help
from nvlib.nv_globals import prefs
from nvlib.view.platform.platform_settings import KEYS
import tkinter as tk


class ExportOptionsWindow(ModalDialog):
    """A pop-up window with export preference settings."""

    def __init__(self, model, view, controller, **kw):
        ModalDialog.__init__(self, model, view, controller, **kw)
        self.title(_('"Export" options'))
        window = ttk.Frame(self)
        window.pack(
            fill='both',
            padx=5,
            pady=5
            )
        frame1 = ttk.Frame(window)
        frame1.pack(fill='both', side='left')

        # Checkbox: Ask whether documents should be opened straight after export.
        self._askDocOpen = tk.BooleanVar(frame1, value=prefs['ask_doc_open'])
        ttk.Checkbutton(
            frame1,
            text=_('Ask before opening exported documents'),
            variable=self._askDocOpen
            ).pack(padx=5, pady=5, anchor='w')
        self._askDocOpen.trace('w', self._change_ask_doc_open)

        # Checkbox: Lock the project after document export.
        self._lockOnExport = tk.BooleanVar(frame1, value=prefs['lock_on_export'])
        ttk.Checkbutton(
            frame1,
            text=_('Lock the project after document export for editing'),
            variable=self._lockOnExport
            ).pack(padx=5, pady=5, anchor='w')
        self._lockOnExport.trace('w', self._change_lock_on_export)

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        # "Close" button.
        ttk.Button(
            self,
            text=_('Close'),
            command=self.destroy
            ).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            self,
            text=_('Online help'),
            command=self.open_help
            ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], self.open_help)

    def _change_ask_doc_open(self, *args):
        prefs['ask_doc_open'] = self._askDocOpen.get()

    def _change_lock_on_export(self, *args):
        prefs['lock_on_export'] = self._lockOnExport.get()

    def open_help(self, event=None):
        open_help(f'export_menu.html#{_("options").lower()}')

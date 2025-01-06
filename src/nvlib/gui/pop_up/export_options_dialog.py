"""Provide a class for an export options dialog.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.view.modal_dialog import ModalDialog
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.pop_up.export_options_ctrl import ExportOptionsCtrl
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class ExportOptionsDialog(ModalDialog, ExportOptionsCtrl):
    """A pop-up window with export preference settings."""

    def __init__(self, model, view, controller, **kw):
        super().__init__(view, **kw)
        self.initialize_controller(model, view, controller)

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
        self.askDocOpenVar = tk.BooleanVar(frame1, value=prefs['ask_doc_open'])
        ttk.Checkbutton(
            frame1,
            text=_('Ask before opening exported documents'),
            variable=self.askDocOpenVar
            ).pack(padx=5, pady=5, anchor='w')
        self.askDocOpenVar.trace('w', self.change_ask_doc_open)

        # Checkbox: Lock the project after document export.
        self.lockOnExportVar = tk.BooleanVar(frame1, value=prefs['lock_on_export'])
        ttk.Checkbutton(
            frame1,
            text=_('Lock the project after document export for editing'),
            variable=self.lockOnExportVar
            ).pack(padx=5, pady=5, anchor='w')
        self.lockOnExportVar.trace('w', self.change_lock_on_export)

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


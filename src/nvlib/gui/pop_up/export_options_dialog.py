"""Provide a class for an export options dialog.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.platform.platform_settings import KEYS
from nvlib.controller.sub_controller import SubController
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk
from nvlib.controller.services.nv_help import NvHelp


class ExportOptionsDialog(ModalDialog, SubController):
    """A pop-up window with export preference settings."""

    def __init__(self, model, view, controller, **kw):
        super().__init__(view, **kw)
        self.initialize_controller(model, view, controller)

        self.title(_('"Export" options'))
        window = ttk.Frame(self)
        window.pack(
            fill='both',
            pady=5
            )
        frame1 = ttk.Frame(window)
        frame1.pack(fill='both', padx=50)

        # Checkbox: Ask whether documents should be opened straight after export.
        self._askDocOpenVar = tk.BooleanVar(frame1, value=prefs['ask_doc_open'])
        ttk.Checkbutton(
            frame1,
            text=_('Ask before opening exported documents'),
            variable=self._askDocOpenVar
            ).pack(padx=5, pady=5, anchor='w')
        self._askDocOpenVar.trace('w', self._change_ask_doc_open)

        # Checkbox: Lock the project after document export.
        self._lockOnExportVar = tk.BooleanVar(frame1, value=prefs['lock_on_export'])
        ttk.Checkbutton(
            frame1,
            text=_('Lock the project after document export for editing'),
            variable=self._lockOnExportVar
            ).pack(padx=5, pady=5, anchor='w')
        self._lockOnExportVar.trace('w', self._change_lock_on_export)

        ttk.Separator(window, orient='horizontal').pack(fill='x')

        frame2 = ttk.Frame(window)
        frame2.pack(fill='both', padx=50)

        # "Select document template" button.
        ttk.Button(
            frame2,
            text=_('Select document template'),
            command=self._ctrl.fileManager.set_user_styles
            ).pack(padx=5, pady=5, anchor='w', fill='x')

        # "Restore default styles" button.
        ttk.Button(
            frame2,
            text=_('Restore default styles'),
            command=self._ctrl.fileManager.restore_default_styles
            ).pack(padx=5, pady=5, anchor='w', fill='x')

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
            command=self._open_help
            ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], self._open_help)

    def _change_ask_doc_open(self, *args):
        prefs['ask_doc_open'] = self._askDocOpenVar.get()

    def _change_lock_on_export(self, *args):
        prefs['lock_on_export'] = self._lockOnExportVar.get()

    def _open_help(self, event=None):
        NvHelp.open_help_page(f'export_menu.html#{_("options").lower()}')


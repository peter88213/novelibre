"""Provide a class for a view settings and options dialog.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.view.modal_dialog import ModalDialog
from mvclib.widgets.drag_drop_listbox import DragDropListbox
from nvlib.controller.pop_up.view_options_window_ctrl import ViewOptionsCtrl
from nvlib.novx_globals import _
from nvlib.nv_globals import prefs
from nvlib.view.platform.platform_settings import KEYS
import tkinter as tk


class ViewOptionsDialog(ModalDialog, ViewOptionsCtrl):
    """A pop-up window with view preference settings."""

    def __init__(self, model, view, controller, **kw):
        super().__init__(view, **kw)
        self.initialize_controller(model, view, controller)

        self.title(_('"View" options'))
        window = ttk.Frame(self)
        window.pack(
            fill='both',
            padx=5,
            pady=5
            )
        frame1 = ttk.Frame(window)
        frame1.pack(fill='both', side='left')

        ttk.Separator(window, orient='vertical').pack(fill='y', padx=10, side='left')
        frame2 = ttk.Frame(window)
        frame2.pack(fill='both', side='left')

        # Combobox for coloring mode setting.
        self.coloringModeStrVar = tk.StringVar(value=self._ui.tv.COLORING_MODES[self._ui.tv.coloringMode])
        self.coloringModeStrVar.trace('w', self.change_colors)
        ttk.Label(
            frame1,
            text=_('Coloring mode')
            ).pack(padx=5, pady=5, anchor='w')
        ttk.Combobox(
            frame1,
            textvariable=self.coloringModeStrVar,
            values=self._ui.tv.COLORING_MODES,
            width=20
            ).pack(padx=5, pady=5, anchor='w')

        ttk.Separator(frame1, orient='horizontal').pack(fill='x', pady=10)

        # Checkbox for large toolbar buttons.
        self._largeIconsVar = tk.BooleanVar(frame1, value=prefs['large_icons'])
        ttk.Checkbutton(
            frame1,
            text=_('Large toolbar icons'),
            variable=self._largeIconsVar,
            command=self.change_icon_size,
            ).pack(padx=5, pady=5, anchor='w')

        # Checkbox for ISO-formatted date display.
        self._localizeDate = tk.BooleanVar(frame1, value=prefs['localize_date'])
        ttk.Checkbutton(
            frame1,
            text=_('Display localized dates'),
            variable=self._localizeDate,
            command=self.change_localize_date,
            ).pack(padx=5, pady=5, anchor='w')

        # Listbox for column reordering.
        ttk.Label(
            frame2,
            text=_('Columns')
            ).pack(padx=5, pady=5, anchor='w')
        self._coIdsByTitle = {}
        for coId, title, __ in self._ui.tv.columns:
            self._coIdsByTitle[title] = coId
        self.colEntriesVar = tk.Variable(value=list(self._coIdsByTitle))
        DragDropListbox(
            frame2,
            listvariable=self.colEntriesVar,
            width=20
            ).pack(padx=5, pady=5, anchor='w')
        ttk.Button(
            frame2,
            text=_('Apply'),
            command=self.change_column_order
            ).pack(padx=5, pady=5, anchor='w')

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


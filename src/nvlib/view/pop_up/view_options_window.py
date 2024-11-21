"""Provide a class for view settings.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.view.modal_dialog import ModalDialog
from mvclib.widgets.drag_drop_listbox import DragDropListbox
from nvlib.controller.pop_up.view_options_window_ctrl import ViewOptionsWindowCtrl
from nvlib.novx_globals import _
from nvlib.novx_globals import list_to_string
from nvlib.nv_globals import open_help
from nvlib.nv_globals import prefs
from nvlib.view.platform.platform_settings import KEYS
import tkinter as tk


class ViewOptionsWindow(ModalDialog, ViewOptionsWindowCtrl):
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

    def change_colors(self, *args, **kwargs):
        cmStr = self.coloringModeStrVar.get()
        self._ui.tv.coloringMode = self._ui.tv.COLORING_MODES.index(cmStr)
        self._ui.tv.refresh()

    def change_column_order(self, *args, **kwargs):
        srtColumns = []
        titles = self.colEntriesVar.get()
        for title in titles:
            srtColumns.append(self._coIdsByTitle[title])
        prefs['column_order'] = list_to_string(srtColumns)
        self._ui.tv.configure_columns()
        self._ui.tv.refresh()

    def change_icon_size(self, *args):
        prefs['large_icons'] = self._largeIconsVar.get()
        self._ui.show_info(_('The change takes effect after next startup.'), title=f'{_("Change icon size")}')

    def change_localize_date(self, *args):
        prefs['localize_date'] = self._localizeDate.get()
        self._ui.tv.refresh()
        self._ui.propertiesView.refresh()

    def open_help(self, event=None):
        open_help(f'view_menu.html#{_("options").lower()}')

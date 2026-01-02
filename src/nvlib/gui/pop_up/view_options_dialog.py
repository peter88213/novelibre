"""Provide a class for a view settings and options dialog.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.widgets.drag_drop_listbox import DragDropListbox
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk
from nvlib.controller.services.nv_help import NvHelp
from nvlib.controller.sub_controller import SubController
from nvlib.novx_globals import list_to_string


class ViewOptionsDialog(ModalDialog, SubController):
    """A pop-up window with view preference settings."""

    def __init__(self, view, **kw):
        super().__init__(view, **kw)
        self._ui = view

        self.title(_('"View" options'))
        self.iconphoto(False, view.icons.settingsIcon)
        window = ttk.Frame(self)
        window.pack(
            fill='both',
            padx=5,
            pady=5
        )
        frame1 = ttk.Frame(window)
        frame1.pack(fill='both', side='left')

        ttk.Separator(
            window,
            orient='vertical',
        ).pack(fill='y', padx=10, side='left')
        frame2 = ttk.Frame(window)
        frame2.pack(fill='both', side='left')

        # Combobox for coloring mode setting.
        self._coloringModeStrVar = tk.StringVar(
            value=self._ui.tv.COLORING_MODES[self._ui.tv.coloringMode]
        )
        self._coloringModeStrVar.trace('w', self._change_colors)
        ttk.Label(
            frame1,
            text=_('Coloring mode'),
        ).pack(padx=5, pady=5, anchor='w')
        ttk.Combobox(
            frame1,
            textvariable=self._coloringModeStrVar,
            values=self._ui.tv.COLORING_MODES,
            width=20,
        ).pack(padx=5, pady=5, anchor='w')

        ttk.Separator(frame1, orient='horizontal').pack(fill='x', pady=10)

        # Checkbox for large toolbar buttons.
        self._largeIconsVar = tk.BooleanVar(
            frame1,
            value=prefs['large_icons'],
        )
        ttk.Checkbutton(
            frame1,
            text=_('Large icons'),
            variable=self._largeIconsVar,
            command=self._change_icon_size,
        ).pack(padx=5, pady=5, anchor='w')

        # Checkbox for ISO-formatted date display.
        self._localizeDate = tk.BooleanVar(
            frame1,
            value=prefs['localize_date'],
        )
        ttk.Checkbutton(
            frame1,
            text=_('Display localized dates'),
            variable=self._localizeDate,
            command=self._change_localize_date,
        ).pack(padx=5, pady=5, anchor='w')

        # Listbox for column reordering.
        ttk.Label(
            frame2,
            text=_('Columns'),
        ).pack(padx=5, pady=5, anchor='w')
        self._coIdsByTitle = {}
        for coId, title, __ in self._ui.tv.columns:
            self._coIdsByTitle[title] = coId
        self._colEntriesVar = tk.Variable(
            value=list(self._coIdsByTitle),
        )
        DragDropListbox(
            frame2,
            listvariable=self._colEntriesVar,
            width=20,
        ).pack(padx=5, pady=5, anchor='w')
        ttk.Button(
            frame2,
            text=_('Apply'),
            command=self._change_column_order,
        ).pack(padx=5, pady=5, anchor='w')

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        # "Close" button.
        ttk.Button(
            self,
            text=_('Close'),
            command=self.destroy,
        ).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            self,
            text=_('Online help'),
            command=self._open_help,
        ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], self._open_help)

    def _change_colors(self, *args, **kwargs):
        cmStr = self._coloringModeStrVar.get()
        self._ui.tv.coloringMode = self._ui.tv.COLORING_MODES.index(cmStr)
        self._ui.tv.refresh()

    def _change_column_order(self, *args, **kwargs):
        srtColumns = []
        titles = self._colEntriesVar.get()
        for title in titles:
            srtColumns.append(self._coIdsByTitle[title])
        prefs['column_order'] = list_to_string(srtColumns)
        self._ui.tv.configure_columns()
        self._ui.tv.refresh()

    def _change_icon_size(self, *args):
        prefs['large_icons'] = self._largeIconsVar.get()
        self._ui.show_info(
            message=_('Icon size changed'),
            detail=f"{_('The change takes effect after next startup')}.",
            title=_('"View" options'),
            parent=self
        )

    def _change_localize_date(self, *args):
        prefs['localize_date'] = self._localizeDate.get()
        self._ui.tv.refresh()
        self._ui.propertiesView.refresh()

    def _open_help(self, event=None):
        NvHelp.open_help_page(f'view_menu.html#{_("options").lower()}')

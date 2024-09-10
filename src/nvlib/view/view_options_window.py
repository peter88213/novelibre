"""Provide a class for view settings.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from novxlib.novx_globals import _
from novxlib.novx_globals import list_to_string
from nvlib.nv_globals import open_help
from nvlib.nv_globals import prefs
from nvlib.widgets.drag_drop_listbox import DragDropListbox
import tkinter as tk


class ViewOptionsWindow(tk.Toplevel):
    """A pop-up window with view preference settings."""

    def __init__(self, size, view, **kw):
        """Open a pop-up window to edit the view options.
        
        Positional arguments:
            size -- str: Window size and coordinates.
            view -- Reference to the application's main view.
        """
        self._ui = view
        super().__init__(**kw)
        self.title(_('"View" options'))
        self.geometry(size)
        self.grab_set()
        self.focus()
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
        self._coloringModeStr = tk.StringVar(value=self._ui.tv.COLORING_MODES[self._ui.tv.coloringMode])
        self._coloringModeStr.trace('w', self._change_colors)
        ttk.Label(
            frame1,
            text=_('Coloring mode')
            ).pack(padx=5, pady=5, anchor='w')
        ttk.Combobox(
            frame1,
            textvariable=self._coloringModeStr,
            values=self._ui.tv.COLORING_MODES,
            width=20
            ).pack(padx=5, pady=5, anchor='w')

        ttk.Separator(frame1, orient='horizontal').pack(fill='x', pady=10)

        # Checkbox for large toolbar buttons.
        self._largeIcons = tk.BooleanVar(frame1, value=prefs['large_icons'])
        ttk.Checkbutton(
            frame1,
            text=_('Large toolbar icons'),
            variable=self._largeIcons,
            command=self._change_icon_size,
            ).pack(padx=5, pady=5, anchor='w')

        # Checkbox for ISO-formatted date display.
        self._localizeDate = tk.BooleanVar(frame1, value=prefs['localize_date'])
        ttk.Checkbutton(
            frame1,
            text=_('Display localized dates'),
            variable=self._localizeDate,
            command=self._change_localize_date,
            ).pack(padx=5, pady=5, anchor='w')

        # Listbox for column reordering.
        ttk.Label(
            frame2,
            text=_('Columns')
            ).pack(padx=5, pady=5, anchor='w')
        self._coIdsByTitle = {}
        for coId, title, __ in self._ui.tv.columns:
            self._coIdsByTitle[title] = coId
        self._colEntries = tk.Variable(value=list(self._coIdsByTitle))
        DragDropListbox(
            frame2,
            listvariable=self._colEntries,
            width=20
            ).pack(padx=5, pady=5, anchor='w')
        ttk.Button(
            frame2,
            text=_('Apply'),
            command=self._change_column_order
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
            command=self._open_help
            ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(self._ui.keys.OPEN_HELP[0], self._open_help)

    def _change_colors(self, *args, **kwargs):
        cmStr = self._coloringModeStr.get()
        self._ui.tv.coloringMode = self._ui.tv.COLORING_MODES.index(cmStr)
        self._ui.tv.refresh()

    def _change_column_order(self, *args, **kwargs):
        srtColumns = []
        titles = self._colEntries.get()
        for title in titles:
            srtColumns.append(self._coIdsByTitle[title])
        prefs['column_order'] = list_to_string(srtColumns)
        self._ui.tv.configure_columns()
        self._ui.tv.refresh()

    def _change_icon_size(self, *args):
        prefs['large_icons'] = self._largeIcons.get()
        self._ui.show_info(_('The change takes effect after next startup.'), title=f'{_("Change icon size")}')

    def _change_localize_date(self, *args):
        prefs['localize_date'] = self._localizeDate.get()
        self._ui.tv.refresh()
        self._ui.propertiesView.refresh()

    def _open_help(self, event=None):
        open_help(f'view_menu.html#{_("options").lower()}')

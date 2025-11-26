"""Provide a class for the "File" menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.nv_locale import _
import tkinter as tk


class ViewMenu(tk.Menu, NvMenu):

    def __init__(self, master, model, view, controller):
        tk.Menu.__init__(self, master, tearoff=0)
        NvMenu.__init__(self, master, model, view, controller)

        label = _('Show Book')
        self.add_separator()
        self.add_command(
            label=label,
            command=self._ui.tv.show_book,
        )
        self._disableOnClose.append(label)

        label = _('Show Characters')
        self.add_command(
            label=label,
            command=self._ui.tv.show_characters,
        )
        self._disableOnClose.append(label)

        label = _('Show Locations')
        self.add_command(
            label=label,
            command=self._ui.tv.show_locations,
        )
        self._disableOnClose.append(label)

        label = _('Show Items')
        self.add_command(
            label=label,
            command=self._ui.tv.show_items,
        )
        self._disableOnClose.append(label)

        label = _('Show Plot lines')
        self.add_command(
            label=label,
            command=self._ui.tv.show_plot_lines,
        )
        self._disableOnClose.append(label)

        label = _('Show Project notes')
        self.add_command(
            label=label,
            command=self._ui.tv.show_project_notes,
        )
        self._disableOnClose.append(label)

        self._add_view_commands(master)

        label = _('Expand selected')
        self.add_command(
            label=label,
            command=self._ui.tv.expand_selected,
        )
        self._disableOnClose.append(label)

        label = _('Collapse selected')
        self.add_command(
            label=label,
            command=self._ui.tv.collapse_selected,
        )
        self._disableOnClose.append(label)

        self.add_separator()

        label = _('Toggle Text viewer')
        self.add_command(
            label=label,
            accelerator=KEYS.TOGGLE_VIEWER[1],
            command=self._ui.toggle_contents_view,
        )

        label = _('Toggle Properties')
        self.add_command(
            label=label,
            accelerator=KEYS.TOGGLE_PROPERTIES[1],
            command=self._ui.toggle_properties_view,
        )

        label = _('Detach/Dock Properties')
        self.add_command(
            label=label,
            accelerator=KEYS.DETACH_PROPERTIES[1],
            command=self._ui.toggle_properties_window,
        )

        label = _('Options')
        self.add_separator()
        self.add_command(
            label=label,
            command=self._ctrl.open_view_options,
        )


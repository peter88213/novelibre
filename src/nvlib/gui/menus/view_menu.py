"""Provide a class for the "View" menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.nv_locale import _


class ViewMenu(NvMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)

        label = _('Show Book')
        self.add_command(
            label=label,
            command=self._ui.tv.show_book,
        )
        self.disableOnClose.append(label)

        label = _('Show Characters')
        self.add_command(
            label=label,
            command=self._ui.tv.show_characters,
        )
        self.disableOnClose.append(label)

        label = _('Show Locations')
        self.add_command(
            label=label,
            command=self._ui.tv.show_locations,
        )
        self.disableOnClose.append(label)

        label = _('Show Items')
        self.add_command(
            label=label,
            command=self._ui.tv.show_items,
        )
        self.disableOnClose.append(label)

        label = _('Show Plot lines')
        self.add_command(
            label=label,
            command=self._ui.tv.show_plot_lines,
        )
        self.disableOnClose.append(label)

        label = _('Show Project notes')
        self.add_command(
            label=label,
            command=self._ui.tv.show_project_notes,
        )
        self.disableOnClose.append(label)

        self.add_separator()
        self._add_view_commands()

        label = _('Expand selected')
        self.add_command(
            label=label,
            command=self._ui.tv.expand_selected,
        )
        self.disableOnClose.append(label)

        label = _('Collapse selected')
        self.add_command(
            label=label,
            command=self._ui.tv.collapse_selected,
        )
        self.disableOnClose.append(label)

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

        self.add_separator()

        label = _('Options')
        self.add_command(
            label=label,
            command=self._ctrl.open_view_options,
        )


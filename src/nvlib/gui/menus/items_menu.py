"""Provide a class for the "Items" menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.nv_locale import _


class ItemsMenu(NvMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)

        label = _('Add')
        self.add_command(
            label=label,
            command=self._ctrl.add_new_item,
        )
        self._disableOnLock.append(label)

        self.add_separator()

        label = _('Import')
        self.add_command(
            label=label,
            command=self._ctrl.import_item_data,
        )
        self._disableOnLock.append(label)

        self.add_separator()

        label = _('Export item descriptions for editing')
        self.add_command(
            label=label,
            command=self._ctrl.export_item_desc,
        )
        self._disableOnLock.append(label)

        label = _('Export item table')
        self.add_command(
            label=label,
            command=self._ctrl.export_item_list,
        )
        self._disableOnLock.append(label)

        self.add_separator()

        label = _('Show table in Browser')
        self.add_command(
            label=label,
            command=self._ctrl.show_item_list,
        )

"""Provide a mixin class for a view settings and options controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from mvclib.controller.sub_controller import SubController
from nvlib.controller.services.nv_help import NvHelp
from nvlib.novx_globals import list_to_string
from nvlib.nv_locale import _


class ViewOptionsCtrl(SubController):

    def change_colors(self, *args, **kwargs):
        cmStr = self.coloringModeStrVar.get()
        self._ui.tv.coloringMode = self._ui.tv.COLORING_MODES.index(cmStr)
        self._ui.tv.refresh()

    def change_column_order(self, *args, **kwargs):
        srtColumns = []
        titles = self.colEntriesVar.get()
        for title in titles:
            srtColumns.append(self._coIdsByTitle[title])
        self._ctrl.prefs['column_order'] = list_to_string(srtColumns)
        self._ui.tv.configure_columns()
        self._ui.tv.refresh()

    def change_icon_size(self, *args):
        self._ctrl.prefs['large_icons'] = self._largeIconsVar.get()
        self._ui.show_info(_('The change takes effect after next startup.'), title=f'{_("Change icon size")}')

    def change_localize_date(self, *args):
        self._ctrl.prefs['localize_date'] = self._localizeDate.get()
        self._ui.tv.refresh()
        self._ui.propertiesView.refresh()

    def open_help(self, event=None):
        NvHelp.open_help_page(f'view_menu.html#{_("options").lower()}')

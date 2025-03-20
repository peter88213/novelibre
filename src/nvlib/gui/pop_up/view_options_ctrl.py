"""Provide a mixin class for a view settings and options controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from nvlib.controller.services.nv_help import NvHelp
from nvlib.controller.sub_controller import SubController
from nvlib.novx_globals import list_to_string
from nvlib.nv_globals import prefs
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
        prefs['column_order'] = list_to_string(srtColumns)
        self._ui.tv.configure_columns()
        self._ui.tv.refresh()

    def change_icon_size(self, *args):
        prefs['large_icons'] = self._largeIconsVar.get()
        self._ui.show_info(
            message=_('Icon size changed'),
            detail=f"{_('The change takes effect after next startup')}.",
            title=_('"View" options'),
            parent=self
            )

    def change_localize_date(self, *args):
        prefs['localize_date'] = self._localizeDate.get()
        self._ui.tv.refresh()
        self._ui.propertiesView.refresh()

    def open_help(self, event=None):
        NvHelp.open_help_page(f'view_menu.html#{_("options").lower()}')

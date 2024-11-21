"""Provide a mixin class for a plugin manager controller.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import webbrowser

from mvclib.controller.sub_controller import SubController
from nvlib.novx_globals import _
from nvlib.nv_globals import open_help


class PluginManagerCtrl(SubController):
    """A pop-up window displaying a list of all plugins found on application startup."""

    def delete_module(self, event=None):
        moduleName = self.moduleCollection.selection()[0]
        if moduleName:
            if self._ctrl.plugins.delete_file(moduleName):
                self.deleteButton.configure(state='disabled')
                if self._ctrl.plugins[moduleName].isActive:
                    self._ui.show_info(_('The plugin remains active until next start.'), title=f'{moduleName} {_("deleted")}')
                else:
                    self.moduleCollection.delete(moduleName)

    def on_select_module(self, event):
        moduleName = self.moduleCollection.selection()[0]
        homeButtonState = 'disabled'
        deleteButtonState = 'disabled'
        if moduleName:
            try:
                if self._ctrl.plugins[moduleName].URL:
                    homeButtonState = 'normal'
            except:
                pass
            try:
                if self._ctrl.plugins[moduleName].filePath:
                    deleteButtonState = 'normal'
            except:
                pass
        self.homeButton.configure(state=homeButtonState)
        self.deleteButton.configure(state=deleteButtonState)

    def open_help(self, event=None):
        open_help(f'tools_menu.html#{_("plugin-manager").lower()}')

    def open_home_page(self, event=None):
        moduleName = self.moduleCollection.selection()[0]
        if moduleName:
            try:
                url = self._ctrl.plugins[moduleName].URL
                if url:
                    webbrowser.open(url)
            except:
                pass


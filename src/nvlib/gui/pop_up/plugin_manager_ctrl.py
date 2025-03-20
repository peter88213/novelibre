"""Provide a mixin class for a plugin manager controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import webbrowser

from nvlib.controller.services.nv_help import NvHelp
from nvlib.controller.sub_controller import SubController
from nvlib.nv_locale import _
from pip._vendor.typing_extensions import Self


class PluginManagerCtrl(SubController):

    def delete_plugin(self, event=None):
        pluginName = self.pluginTree.selection()[0]
        if not pluginName:
            return

        if not pluginName in self._ctrl.plugins:
            return

        if not self._ctrl.plugins[pluginName].filePath:
            return

        if not self._ui.ask_yes_no(
            message=f'{_("Delete file")}?',
            detail=self._ctrl.plugins[pluginName].filePath,
            title=_('Plugin Manager'),
            parent=self
            ):
            return

        if self._ctrl.plugins.delete_file(pluginName):
            self.deleteButton.configure(state='disabled')
            if self._ctrl.plugins[pluginName].isActive:
                self._ui.show_info(
                    message=f'{pluginName} {_("deleted")}',
                    detail=f"{_('The plugin remains active until next start')}.",
                    title=_('Plugin Manager'),
                    parent=self
                    )
            else:
                self.pluginTree.delete(pluginName)

    def on_select_plugin(self, event):
        try:
            pluginName = self.pluginTree.selection()[0]
        except IndexError:
            # can happen after plugin deletion
            return

        homeButtonState = 'disabled'
        deleteButtonState = 'disabled'
        if pluginName:
            try:
                if self._ctrl.plugins[pluginName].URL:
                    homeButtonState = 'normal'
            except:
                pass
            try:
                if self._ctrl.plugins[pluginName].filePath:
                    deleteButtonState = 'normal'
            except:
                pass
        self.homeButton.configure(state=homeButtonState)
        self.deleteButton.configure(state=deleteButtonState)

    def open_help(self, event=None):
        NvHelp.open_help_page(f'tools_menu.html#{_("plugin-manager").lower()}')

    def open_homepage(self, event=None):
        pluginName = self.pluginTree.selection()[0]
        if pluginName:
            try:
                url = self._ctrl.plugins[pluginName].URL
                if url:
                    webbrowser.open(url)
            except:
                pass


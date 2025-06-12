"""Provide a class for a plugin manager dialog.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk
import webbrowser

from nvlib.controller.services.nv_help import NvHelp
from nvlib.controller.sub_controller import SubController
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.nv_locale import _


class PluginManagerDialog(ModalDialog, SubController):
    """A pop-up window displaying a list of all plugins found on application startup."""

    MIN_HEIGHT = 450

    def __init__(self, view, controller, **kw):
        super().__init__(view, **kw)
        self.minsize(1, self.MIN_HEIGHT)
        self._ui = view
        self._ctrl = controller

        self.title(f'{_("Installed plugins")} - novelibre @release')

        columns = 'Plugin', 'Version', 'novelibre API', 'Description'
        self._pluginTree = ttk.Treeview(
            self, columns=columns, show='headings', selectmode='browse')

        # scrollY = ttk.Scrollbar(
        #    self._pluginTree, orient='vertical', command=self._pluginTree.yview)
        # self._pluginTree.configure(yscrollcommand=scrollY.set)
        # scrollY.pack(side='right', fill='y')
        #--- unsolved problem: adding a scollbar makes the window shrink to minimum

        self._pluginTree.pack(fill='both', expand=True)
        self._pluginTree.bind('<<TreeviewSelect>>', self._on_select_plugin)
        self._pluginTree.tag_configure('rejected', foreground='red')
        self._pluginTree.tag_configure('inactive', foreground='gray')

        self._pluginTree.column('Plugin', width=150, minwidth=120, stretch=False)
        self._pluginTree.heading('Plugin', text=_('Plugin'), anchor='w')
        self._pluginTree.column('Version', width=100, minwidth=100, stretch=False)
        self._pluginTree.heading('Version', text=_('Version'), anchor='w')
        self._pluginTree.column('novelibre API', width=100, minwidth=100, stretch=False)
        self._pluginTree.heading('novelibre API', text=_('novelibre API'), anchor='w')
        self._pluginTree.column('Description', width=400, stretch=True)
        self._pluginTree.heading('Description', text=_('Description'), anchor='w')

        for pluginName in self._ctrl.plugins:
            nodeTags = []
            try:
                version = self._ctrl.plugins[pluginName].VERSION
            except AttributeError:
                version = _('unknown')
            try:
                description = self._ctrl.plugins[pluginName].DESCRIPTION
            except AttributeError:
                description = _('No description')
            try:
                apiRequired = self._ctrl.plugins[pluginName].API_VERSION
            except AttributeError:
                try:
                    apiRequired = self._ctrl.plugins[pluginName].NOVELTREE_API
                    # might be a 1.x API plugin
                except AttributeError:
                    apiRequired = _('unknown')
            columns = [pluginName, version, apiRequired, description]
            if self._ctrl.plugins[pluginName].isRejected:
                nodeTags.append('rejected')
                # Mark rejected modules, represented by a dummy.
            elif not self._ctrl.plugins[pluginName].isActive:
                nodeTags.append('inactive')
                # Mark loaded yet incompatible modules.
            self._pluginTree.insert(
                '', 'end', pluginName, values=columns, tags=tuple(nodeTags))

        self._footer = ttk.Frame(self)
        self._footer.pack(fill='both', expand=False)

        # "Home page" button.
        self._homeButton = ttk.Button(
            self._footer,
            text=_('Home page'),
            command=self._open_homepage,
            state='disabled'
        )
        self._homeButton.pack(padx=5, pady=5, side='left')

        # "Delete" button.
        self._deleteButton = ttk.Button(
            self._footer,
            text=_('Delete'),
            command=self._delete_plugin,
            state='disabled'
        )
        self._deleteButton.pack(padx=5, pady=5, side='left')

        # "Close" button.
        ttk.Button(
            self._footer,
            text=_('Close'),
            command=self.destroy,
        ).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            self._footer,
            text=_('Online help'),
            command=self._open_help,
        ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], self._open_help)

    def _delete_plugin(self, event=None):
        pluginName = self._pluginTree.selection()[0]
        if not pluginName:
            return

        if not pluginName in self._ctrl.plugins:
            return

        if not self._ctrl.plugins[pluginName].filePath:
            return

        if not self._ui.ask_yes_no(
            message=_('Delete file?'),
            detail=self._ctrl.plugins[pluginName].filePath,
            title=_('Plugin Manager'),
            parent=self
        ):
            return

        if self._ctrl.plugins.delete_file(pluginName):
            self._deleteButton.configure(state='disabled')
            if self._ctrl.plugins[pluginName].isActive:
                self._ui.show_info(
                    message=f'{pluginName} {_("deleted")}',
                    detail=f"{_('The plugin remains active until next start')}.",
                    title=_('Plugin Manager'),
                    parent=self
                )
            else:
                self._pluginTree.delete(pluginName)

    def _on_select_plugin(self, event):
        try:
            pluginName = self._pluginTree.selection()[0]
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
        self._homeButton.configure(state=homeButtonState)
        self._deleteButton.configure(state=deleteButtonState)

    def _open_help(self, event=None):
        NvHelp.open_help_page(f'tools_menu.html#{_("plugin-manager").lower()}')

    def _open_homepage(self, event=None):
        pluginName = self._pluginTree.selection()[0]
        if pluginName:
            try:
                url = self._ctrl.plugins[pluginName].URL
                if url:
                    webbrowser.open(url)
            except:
                pass


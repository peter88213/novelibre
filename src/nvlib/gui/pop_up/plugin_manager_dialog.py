"""Provide a class for a plugin manager dialog.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.pop_up.plugin_manager_ctrl import PluginManagerCtrl
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.nv_locale import _


class PluginManagerDialog(ModalDialog, PluginManagerCtrl):
    """A pop-up window displaying a list of all plugins found on application startup."""

    MIN_HEIGHT = 450

    def __init__(self, model, view, controller, **kw):
        super().__init__(view, **kw)
        self.minsize(1, self.MIN_HEIGHT)
        self.initialize_controller(model, view, controller)

        self.title(f'{_("Installed plugins")} - novelibre @release')

        columns = 'Plugin', 'Version', 'novelibre API', 'Description'
        self.pluginCollection = ttk.Treeview(self, columns=columns, show='headings', selectmode='browse')

        # scrollY = ttk.Scrollbar(self.pluginCollection, orient='vertical', command=self.pluginCollection.yview)
        # self.pluginCollection.configure(yscrollcommand=scrollY.set)
        # scrollY.pack(side='right', fill='y')
        #--- unsolved problem: adding a scollbar makes the window shrink to minimum

        self.pluginCollection.pack(fill='both', expand=True)
        self.pluginCollection.bind('<<TreeviewSelect>>', self.on_select_plugin)
        self.pluginCollection.tag_configure('rejected', foreground='red')
        self.pluginCollection.tag_configure('inactive', foreground='gray')

        self.pluginCollection.column('Plugin', width=150, minwidth=120, stretch=False)
        self.pluginCollection.heading('Plugin', text=_('Plugin'), anchor='w')
        self.pluginCollection.column('Version', width=100, minwidth=100, stretch=False)
        self.pluginCollection.heading('Version', text=_('Version'), anchor='w')
        self.pluginCollection.column('novelibre API', width=100, minwidth=100, stretch=False)
        self.pluginCollection.heading('novelibre API', text=_('novelibre API'), anchor='w')
        self.pluginCollection.column('Description', width=400, stretch=True)
        self.pluginCollection.heading('Description', text=_('Description'), anchor='w')

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
            self.pluginCollection.insert('', 'end', pluginName, values=columns, tags=tuple(nodeTags))

        self._footer = ttk.Frame(self)
        self._footer.pack(fill='both', expand=False)

        # "Home page" button.
        self.homeButton = ttk.Button(
            self._footer,
            text=_('Home page'),
            command=self.open_homepage,
            state='disabled'
            )
        self.homeButton.pack(padx=5, pady=5, side='left')

        # "Delete" button.
        self.deleteButton = ttk.Button(
            self._footer,
            text=_('Delete'),
            command=self.delete_plugin,
            state='disabled'
            )
        self.deleteButton.pack(padx=5, pady=5, side='left')

        # "Close" button.
        ttk.Button(
            self._footer,
            text=_('Close'),
            command=self.destroy
            ).pack(padx=5, pady=5, side='right')

        # "Help" button.
        ttk.Button(
            self._footer,
            text=_('Online help'),
            command=self.open_help
            ).pack(padx=5, pady=5, side='right')

        # Set Key bindings.
        self.bind(KEYS.OPEN_HELP[0], self.open_help)


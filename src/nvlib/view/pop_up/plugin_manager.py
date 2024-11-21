"""Provide a class for a plugin manager.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.view.modal_dialog import ModalDialog
from nvlib.controller.pop_up.plugin_manager_ctrl import PluginManagerCtrl
from nvlib.novx_globals import _
from nvlib.view.platform.platform_settings import KEYS


class PluginManager(ModalDialog, PluginManagerCtrl):
    """A pop-up window displaying a list of all plugins found on application startup."""

    def __init__(self, model, view, controller, **kw):
        super().__init__(view, **kw)
        self.initialize_controller(model, view, controller)

        self.title(f'{_("Installed plugins")} - novelibre @release')

        columns = 'Module', 'Version', 'novelibre API', 'Description'
        self.moduleCollection = ttk.Treeview(self, columns=columns, show='headings', selectmode='browse')

        # scrollY = ttk.Scrollbar(self.moduleCollection, orient='vertical', command=self.moduleCollection.yview)
        # self.moduleCollection.configure(yscrollcommand=scrollY.set)
        # scrollY.pack(side='right', fill='y')
        #--- unsolved problem: adding a scollbar makes the window shrink to minimum

        self.moduleCollection.pack(fill='both', expand=True)
        self.moduleCollection.bind('<<TreeviewSelect>>', self.on_select_module)
        self.moduleCollection.tag_configure('rejected', foreground='red')
        self.moduleCollection.tag_configure('inactive', foreground='gray')

        self.moduleCollection.column('Module', width=150, minwidth=120, stretch=False)
        self.moduleCollection.heading('Module', text=_('Module'), anchor='w')
        self.moduleCollection.column('Version', width=100, minwidth=100, stretch=False)
        self.moduleCollection.heading('Version', text=_('Version'), anchor='w')
        self.moduleCollection.column('novelibre API', width=100, minwidth=100, stretch=False)
        self.moduleCollection.heading('novelibre API', text=_('novelibre API'), anchor='w')
        self.moduleCollection.column('Description', width=400, stretch=True)
        self.moduleCollection.heading('Description', text=_('Description'), anchor='w')

        for moduleName in self._ctrl.plugins:
            nodeTags = []
            try:
                version = self._ctrl.plugins[moduleName].VERSION
            except AttributeError:
                version = _('unknown')
            try:
                description = self._ctrl.plugins[moduleName].DESCRIPTION
            except AttributeError:
                description = _('No description')
            try:
                apiRequired = self._ctrl.plugins[moduleName].API_VERSION
            except AttributeError:
                try:
                    apiRequired = self._ctrl.plugins[moduleName].NOVELTREE_API
                    # might be a 1.x API plugin
                except AttributeError:
                    apiRequired = _('unknown')
            columns = [moduleName, version, apiRequired, description]
            if self._ctrl.plugins[moduleName].isRejected:
                nodeTags.append('rejected')
                # Mark rejected modules, represented by a dummy.
            elif not self._ctrl.plugins[moduleName].isActive:
                nodeTags.append('inactive')
                # Mark loaded yet incompatible modules.
            self.moduleCollection.insert('', 'end', moduleName, values=columns, tags=tuple(nodeTags))

        self._footer = ttk.Frame(self)
        self._footer.pack(fill='both', expand=False)

        # "Home page" button.
        self.homeButton = ttk.Button(
            self._footer,
            text=_('Home page'),
            command=self.open_home_page,
            state='disabled'
            )
        self.homeButton.pack(padx=5, pady=5, side='left')

        # "Delete" button.
        self.deleteButton = ttk.Button(
            self._footer,
            text=_('Delete'),
            command=self.delete_module,
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


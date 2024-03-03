"""Provide a class for a plugin manager.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk
import webbrowser

from novxlib.novx_globals import _
import tkinter as tk


class PluginManager(tk.Toplevel):

    def __init__(self, size, view, controller, **kw):
        """Plugin manager. 

        A pop-up window displaying a list of all plugins found on application startup.
        """
        self._ui = view
        self._ctrl = controller
        super().__init__(**kw)
        self.title(f'{_("Installed plugins")} - novelibre @release')
        self.geometry(size)
        self.grab_set()
        self.focus()
        window = ttk.Frame(self)
        window.pack(fill='both', expand=True)

        columns = 'Module', 'Version', 'novelibre API', 'Description'
        self._moduleCollection = ttk.Treeview(window, columns=columns, show='headings', selectmode='browse')
        self._moduleCollection.pack(fill='both', expand=True)
        self._moduleCollection.bind('<<TreeviewSelect>>', self._on_select_module)
        self._moduleCollection.tag_configure('rejected', foreground='red')
        self._moduleCollection.tag_configure('inactive', foreground='gray')

        self._moduleCollection.column('Module', width=150, minwidth=120, stretch=False)
        self._moduleCollection.heading('Module', text=_('Module'), anchor='w')
        self._moduleCollection.column('Version', width=100, minwidth=100, stretch=False)
        self._moduleCollection.heading('Version', text=_('Version'), anchor='w')
        self._moduleCollection.column('novelibre API', width=100, minwidth=100, stretch=False)
        self._moduleCollection.heading('novelibre API', text=_('novelibre API'), anchor='w')
        self._moduleCollection.column('Description', width=400, stretch=True)
        self._moduleCollection.heading('Description', text=_('Description'), anchor='w')

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
            self._moduleCollection.insert('', 'end', moduleName, values=columns, tags=tuple(nodeTags))

        # "Home page" button.
        self._homeButton = ttk.Button(window, text=_('Home page'), command=self._open_home_page, state='disabled')
        self._homeButton.pack(padx=5, pady=5, side='left')

        # "Delete" button.
        self._deleteButton = ttk.Button(window, text=_('Delete'), command=self._delete_module, state='disabled')
        self._deleteButton.pack(padx=5, pady=5, side='left')

        # "Close" button.
        ttk.Button(window, text=_('Close'), command=self.destroy).pack(padx=5, pady=5, side='left')

    def _delete_module(self, event=None):
        moduleName = self._moduleCollection.selection()[0]
        if moduleName:
            if self._ctrl.plugins.delete_file(moduleName):
                self._deleteButton.configure(state='disabled')
                if self._ctrl.plugins[moduleName].isActive:
                    self._ui.show_info(_('The plugin remains active until next start.'), title=f'{moduleName} {_("deleted")}')
                else:
                    self._moduleCollection.delete(moduleName)

    def _on_select_module(self, event):
        moduleName = self._moduleCollection.selection()[0]
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
        self._homeButton.configure(state=homeButtonState)
        self._deleteButton.configure(state=deleteButtonState)

    def _open_home_page(self, event=None):
        moduleName = self._moduleCollection.selection()[0]
        if moduleName:
            try:
                url = self._ctrl.plugins[moduleName].URL
                if url:
                    webbrowser.open(url)
            except:
                pass


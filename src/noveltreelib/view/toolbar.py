"""Toolbar class for noveltree.


Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk
import sys
import os
from novxlib.novx_globals import AC_ROOT
from novxlib.novx_globals import CH_ROOT
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import IT_ROOT
from novxlib.novx_globals import LC_ROOT
from novxlib.novx_globals import MANUSCRIPT_SUFFIX
from novxlib.novx_globals import PN_ROOT
import tkinter as tk
from noveltreelib.noveltree_globals import prefs


class Toolbar:
    """Toolbar plugin class."""

    def __init__(self, view, controller):
        """Add a toolbar.
        
        Positional arguments:
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.
        """
        self._ctrl = controller
        self._ui = view
        iconPath = f'{os.path.dirname(sys.argv[0])}/icons/toolbar'
        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16

        # Add a toolbar to the editor window.
        self._buttonBar = tk.Frame(self._ui.mainWindow)
        self._buttonBar.pack(expand=False, before=self._ui.appWindow, fill='both')

        # "Go back" button.
        goBackIcon = tk.PhotoImage(file=f'{iconPath}/tb_goBack{size}.png')
        self._goBackButton = ttk.Button(
            self._buttonBar,
            image=goBackIcon,
            command=self._ui.tv.go_back
            )
        self._goBackButton.pack(side='left')
        self._goBackButton.image = goBackIcon

        # "Go forward" button.
        goForwardIcon = tk.PhotoImage(file=f'{iconPath}/tb_goForward{size}.png')
        self._goForwardButton = ttk.Button(
            self._buttonBar,
            image=goForwardIcon,
            command=self._ui.tv.go_forward
            )
        self._goForwardButton.pack(side='left')
        self._goForwardButton.image = goForwardIcon

        # Separator.
        tk.Frame(self._buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # "View Book" button.
        viewBookIcon = tk.PhotoImage(file=f'{iconPath}/tb_viewBook{size}.png')
        self._viewBookButton = ttk.Button(
            self._buttonBar,
            image=viewBookIcon,
            command=lambda: self._ui.tv.show_branch(CH_ROOT)
            )
        self._viewBookButton.pack(side='left')
        self._viewBookButton.image = viewBookIcon

        # "View Characters" button.
        viewCharactersIcon = tk.PhotoImage(file=f'{iconPath}/tb_viewCharacters{size}.png')
        self._viewCharactersButton = ttk.Button(
            self._buttonBar,
            image=viewCharactersIcon,
            command=lambda: self._ui.tv.show_branch(CR_ROOT)
            )
        self._viewCharactersButton.pack(side='left')
        self._viewCharactersButton.image = viewCharactersIcon

        # "View Locations" button.
        viewLocationsIcon = tk.PhotoImage(file=f'{iconPath}/tb_viewLocations{size}.png')
        self._viewLocationsButton = ttk.Button(
            self._buttonBar,
            image=viewLocationsIcon,
            command=lambda: self._ui.tv.show_branch(LC_ROOT)
            )
        self._viewLocationsButton.pack(side='left')
        self._viewLocationsButton.image = viewLocationsIcon

        # "View Items" button.
        viewItemsIcon = tk.PhotoImage(file=f'{iconPath}/tb_viewItems{size}.png')
        self._viewItemsButton = ttk.Button(
            self._buttonBar,
            image=viewItemsIcon,
            command=lambda: self._ui.tv.show_branch(IT_ROOT)
            )
        self._viewItemsButton.pack(side='left')
        self._viewItemsButton.image = viewItemsIcon

        # "View Arcs" button.
        viewArcsIcon = tk.PhotoImage(file=f'{iconPath}/tb_viewArcs{size}.png')
        self._viewArcsButton = ttk.Button(
            self._buttonBar,
            image=viewArcsIcon,
            command=lambda: self._ui.tv.show_branch(AC_ROOT)
            )
        self._viewArcsButton.pack(side='left')
        self._viewArcsButton.image = viewArcsIcon

        # "View Projectnotes" button.
        viewProjectnotesIcon = tk.PhotoImage(file=f'{iconPath}/tb_viewProjectnotes{size}.png')
        self._viewProjectnotesButton = ttk.Button(
            self._buttonBar,
            image=viewProjectnotesIcon,
            command=lambda: self._ui.tv.show_branch(PN_ROOT)
            )
        self._viewProjectnotesButton.pack(side='left')
        self._viewProjectnotesButton.image = viewProjectnotesIcon

        # Separator.
        tk.Frame(self._buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # "Save" button.
        saveIcon = tk.PhotoImage(file=f'{iconPath}/tb_save{size}.png')
        self._saveButton = ttk.Button(
            self._buttonBar,
            image=saveIcon,
            command=self._ctrl.save_project
            )
        self._saveButton.pack(side='left')
        self._saveButton.image = saveIcon

        # "Lock/Unlock" button.
        lockIcon = tk.PhotoImage(file=f'{iconPath}/tb_lock{size}.png')
        self._lockButton = ttk.Button(
            self._buttonBar,
            image=lockIcon,
            command=self._ctrl.toggle_lock
            )
        self._lockButton.pack(side='left')
        self._lockButton.image = lockIcon

        # "Manuscript" button.
        manuscriptIcon = tk.PhotoImage(file=f'{iconPath}/tb_manuscript{size}.png')
        self._manuscriptButton = ttk.Button(
            self._buttonBar,
            image=manuscriptIcon,
            command=lambda:self._ctrl.export_document(MANUSCRIPT_SUFFIX)
            )
        self._manuscriptButton.pack(side='left')
        self._manuscriptButton.image = manuscriptIcon

        # "Update from manuscript" button.
        updateFromManuscriptIcon = tk.PhotoImage(file=f'{iconPath}/tb_updateFromManuscript{size}.png')
        self._updateButton = ttk.Button(
            self._buttonBar,
            image=updateFromManuscriptIcon,
            command=lambda: self._ctrl.update_from_odt(suffix=MANUSCRIPT_SUFFIX)
            )
        self._updateButton.pack(side='left')
        self._updateButton.image = updateFromManuscriptIcon

        # Reverse order (side='right').

        # "Toggle properties" button.
        propertiesIcon = tk.PhotoImage(file=f'{iconPath}/tb_properties{size}.png')
        self._propertiesButton = ttk.Button(
            self._buttonBar,
            image=propertiesIcon,
            command=self._ui.toggle_properties_view
            )
        self._propertiesButton.pack(side='right')
        self._propertiesButton.image = propertiesIcon

        # "Toggle content viewer" button.
        viewerIcon = tk.PhotoImage(file=f'{iconPath}/tb_viewer{size}.png')
        self._viewerButton = ttk.Button(
            self._buttonBar,
            image=viewerIcon,
            command=self._ui.toggle_contents_view
            )
        self._viewerButton.pack(side='right')
        self._viewerButton.image = viewerIcon

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._saveButton.config(state='disabled')
        self._lockButton.config(state='disabled')
        self._updateButton.config(state='disabled')
        self._manuscriptButton.config(state='disabled')
        self._viewBookButton.config(state='disabled')
        self._viewCharactersButton.config(state='disabled')
        self._viewLocationsButton.config(state='disabled')
        self._viewItemsButton.config(state='disabled')
        self._viewArcsButton.config(state='disabled')
        self._viewProjectnotesButton.config(state='disabled')
        self._goBackButton.config(state='disabled')
        self._goForwardButton.config(state='disabled')
        self._propertiesButton.config(state='disabled')
        self._viewerButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._saveButton.config(state='normal')
        self._lockButton.config(state='normal')
        self._updateButton.config(state='normal')
        self._manuscriptButton.config(state='normal')
        self._viewBookButton.config(state='normal')
        self._viewCharactersButton.config(state='normal')
        self._viewLocationsButton.config(state='normal')
        self._viewItemsButton.config(state='normal')
        self._viewArcsButton.config(state='normal')
        self._viewProjectnotesButton.config(state='normal')
        self._goBackButton.config(state='normal')
        self._goForwardButton.config(state='normal')
        self._propertiesButton.config(state='normal')
        self._viewerButton.config(state='normal')


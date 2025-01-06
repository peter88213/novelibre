"""Toolbar class for novelibre.


Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.toolbar.toolbar_ctrl import ToolbarCtrl
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class Toolbar(ToolbarCtrl):
    """Toolbar class."""

    def __init__(self, parent, model, view, controller):
        """Add a toolbar.
        
        Positional arguments:
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.
        """
        self.initialize_controller(model, view, controller)

        # Add a toolbar to the editor window.
        self.buttonBar = ttk.Frame(self._ui.mainWindow)

        # "Go back" button.
        self.goBackButton = ttk.Button(
            self.buttonBar,
            text=_('Back'),
            image=self._ui.icons.goBackIcon,
            command=self._ui.tv.go_back
            )
        self.goBackButton.pack(side='left')
        self.goBackButton.image = self._ui.icons.goBackIcon

        # "Go forward" button.
        self.goForwardButton = ttk.Button(
            self.buttonBar,
            text=_('Forward'),
            image=self._ui.icons.goForwardIcon,
            command=self._ui.tv.go_forward
            )
        self.goForwardButton.pack(side='left')
        self.goForwardButton.image = self._ui.icons.goForwardIcon

        # Separator.
        tk.Frame(self.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # "View Book" button.
        self.viewBookButton = ttk.Button(
            self.buttonBar,
            text=_('Book'),
            image=self._ui.icons.viewBookIcon,
            command=self._ui.tv.show_book
            )
        self.viewBookButton.pack(side='left')
        self.viewBookButton.image = self._ui.icons.viewBookIcon

        # "View Characters" button.
        self.viewCharactersButton = ttk.Button(
            self.buttonBar,
            text=_('Characters'),
            image=self._ui.icons.viewCharactersIcon,
            command=self._ui.tv.show_characters
            )
        self.viewCharactersButton.pack(side='left')
        self.viewCharactersButton.image = self._ui.icons.viewCharactersIcon

        # "View Locations" button.
        self.viewLocationsButton = ttk.Button(
            self.buttonBar,
            text=_('Locations'),
            image=self._ui.icons.viewLocationsIcon,
            command=self._ui.tv.show_locations
            )
        self.viewLocationsButton.pack(side='left')
        self.viewLocationsButton.image = self._ui.icons.viewLocationsIcon

        # "View Items" button.
        self.viewItemsButton = ttk.Button(
            self.buttonBar,
            text=_('Items'),
            image=self._ui.icons.viewItemsIcon,
            command=self._ui.tv.show_items
            )
        self.viewItemsButton.pack(side='left')
        self.viewItemsButton.image = self._ui.icons.viewItemsIcon

        # "View Plot lines" button.
        self.viewPlotLinesButton = ttk.Button(
            self.buttonBar,
            text=_('Plot lines'),
            image=self._ui.icons.viewPlotLinesIcon,
            command=self._ui.tv.show_plot_lines
            )
        self.viewPlotLinesButton.pack(side='left')
        self.viewPlotLinesButton.image = self._ui.icons.viewPlotLinesIcon

        # "View Projectnotes" button.
        self.viewProjectnotesButton = ttk.Button(
            self.buttonBar,
            text=_('Project notes'),
            image=self._ui.icons.viewProjectnotesIcon,
            command=self._ui.tv.show_project_notes
            )
        self.viewProjectnotesButton.pack(side='left')
        self.viewProjectnotesButton.image = self._ui.icons.viewProjectnotesIcon

        # Separator.
        tk.Frame(self.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # "Save" button.
        self.saveButton = ttk.Button(
            self.buttonBar,
            text=_('Save'),
            image=self._ui.icons.saveIcon,
            command=self._ctrl.save_project
            )
        self.saveButton.pack(side='left')
        self.saveButton.image = self._ui.icons.saveIcon

        # "Lock/Unlock" button.
        self.lockButton = ttk.Button(
            self.buttonBar,
            text=_('Lock/unlock'),
            image=self._ui.icons.lockIcon,
            command=self._ctrl.toggle_lock
            )
        self.lockButton.pack(side='left')
        self.lockButton.image = self._ui.icons.lockIcon

        # "Update from manuscript" button.
        self.updateButton = ttk.Button(
            self.buttonBar,
            text=_('Update from manuscript'),
            image=self._ui.icons.updateFromManuscriptIcon,
            command=self._ctrl.update_from_manuscript
            )
        self.updateButton.pack(side='left')
        self.updateButton.image = self._ui.icons.updateFromManuscriptIcon

        # "Manuscript" button.
        self.manuscriptButton = ttk.Button(
            self.buttonBar,
            text=_('Export Manuscript'),
            image=self._ui.icons.manuscriptIcon,
            command=self._ctrl.open_manuscript
            )
        self.manuscriptButton.pack(side='left')
        self.manuscriptButton.image = self._ui.icons.manuscriptIcon

        # Separator.
        tk.Frame(self.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # "Add" button.
        self.addElementButton = ttk.Button(
            self.buttonBar,
            text=_('Add'),
            image=self._ui.icons.addIcon,
            command=self._ctrl.add_new_element
            )
        self.addElementButton.pack(side='left')
        self.addElementButton.image = self._ui.icons.addIcon

        # "Add Child" button.
        self.addChildButton = ttk.Button(
            self.buttonBar,
            text=_('Add child'),
            image=self._ui.icons.addChildIcon,
            command=self._ctrl.add_new_child
            )
        self.addChildButton.pack(side='left')
        self.addChildButton.image = self._ui.icons.addChildIcon

        # "Add Parent" button.
        self.addParentButton = ttk.Button(
            self.buttonBar,
            text=_('Add parent'),
            image=self._ui.icons.addParentIcon,
            command=self._ctrl.add_new_parent
            )
        self.addParentButton.pack(side='left')
        self.addParentButton.image = self._ui.icons.addParentIcon

        # "Delete" button.
        self.deleteElementButton = ttk.Button(
            self.buttonBar,
            text=_('Delete'),
            image=self._ui.icons.removeIcon,
            command=self._ctrl.delete_elements
            )
        self.deleteElementButton.pack(side='left')
        self.deleteElementButton.image = self._ui.icons.removeIcon

        # Reverse order (side='right').

        # "Toggle properties" button.
        self.propertiesButton = ttk.Button(
            self.buttonBar,
            text=_('Toggle Properties'),
            image=self._ui.icons.propertiesIcon,
            command=self._ui.toggle_properties_view
            )
        self.propertiesButton.pack(side='right')
        self.propertiesButton.image = self._ui.icons.propertiesIcon

        # "Toggle content viewer" button.
        self.viewerButton = ttk.Button(
            self.buttonBar,
            text=_('Toggle Text viewer'),
            image=self._ui.icons.viewerIcon,
            command=self._ui.toggle_contents_view
            )
        self.viewerButton.pack(side='right')
        self.viewerButton.image = self._ui.icons.viewerIcon

        self.buttonBar.pack(expand=False, before=self._ui.appWindow, fill='both')
        self._set_hovertips()

    def _set_hovertips(self):
        if not prefs['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(self.addChildButton, f"{self.addChildButton['text']} ({KEYS.ADD_CHILD[1]})")
        Hovertip(self.addElementButton, f"{self.addElementButton['text']} ({KEYS.ADD_ELEMENT[1]})")
        Hovertip(self.addParentButton, f"{self.addParentButton['text']} ({KEYS.ADD_PARENT[1]})")
        Hovertip(self.goBackButton, self.goBackButton['text'])
        Hovertip(self.goForwardButton, self.goForwardButton['text'])
        Hovertip(self.lockButton, self.lockButton['text'])
        Hovertip(self.manuscriptButton, self.manuscriptButton['text'])
        Hovertip(self.propertiesButton, f"{self.propertiesButton['text']} ({KEYS.TOGGLE_PROPERTIES[1]})")
        Hovertip(self.saveButton, f"{self.saveButton['text']} ({KEYS.SAVE_PROJECT[1]})")
        Hovertip(self.deleteElementButton, f"{self.deleteElementButton['text']} ({KEYS.DELETE[1]})")
        Hovertip(self.updateButton, self.updateButton['text'])
        Hovertip(self.viewBookButton, self.viewBookButton['text'])
        Hovertip(self.viewCharactersButton, self.viewCharactersButton['text'])
        Hovertip(self.viewItemsButton, self.viewItemsButton['text'])
        Hovertip(self.viewLocationsButton, self.viewLocationsButton['text'])
        Hovertip(self.viewPlotLinesButton, self.viewPlotLinesButton['text'])
        Hovertip(self.viewProjectnotesButton, self.viewProjectnotesButton['text'])
        Hovertip(self.viewerButton, f"{self.viewerButton['text']} ({KEYS.TOGGLE_VIEWER[1]})")


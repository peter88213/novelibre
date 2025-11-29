"""Toolbar class for novelibre.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.controller.sub_controller import SubController
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.tooltip import Hovertip
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class Toolbar(SubController):
    """A toolbar with buttons and hovertips."""

    def __init__(self, view, controller):
        """Add a toolbar.
        
        Positional arguments:
            parent: tk.Frame -- The parent window.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.
        """
        self._ui = view
        self._ctrl = controller
        self._disableOnLock = []
        self._disableOnClose = []

        # Add a toolbar to the editor window.
        self.buttonBar = ttk.Frame(self._ui.mainWindow)

        # "Go back" button.
        self.goBackButton = self.new_button(
            text=_('Back'),
            image=self._ui.icons.goBackIcon,
            command=self._ui.tv.go_back,
            disableOnLock=False,
            accelerator=KEYS.BACK[1],
        )
        self.goBackButton.pack(side='left')

        # "Go forward" button.
        self.goForwardButton = self.new_button(
            text=_('Forward'),
            image=self._ui.icons.goForwardIcon,
            command=self._ui.tv.go_forward,
            disableOnLock=False,
            accelerator=KEYS.FORWARD[1],
        )
        self.goForwardButton.pack(side='left')

        self.add_separator()

        # "View Book" button.
        self.viewBookButton = self.new_button(
            text=_('Book'),
            image=self._ui.icons.viewBookIcon,
            command=self._ui.tv.show_book,
            disableOnLock=False,
        )
        self.viewBookButton.pack(side='left')

        # "View Characters" button.
        self.viewCharactersButton = self.new_button(
            text=_('Characters'),
            image=self._ui.icons.viewCharactersIcon,
            command=self._ui.tv.show_characters,
            disableOnLock=False,
        )
        self.viewCharactersButton.pack(side='left')

        # "View Locations" button.
        self.viewLocationsButton = self.new_button(
            text=_('Locations'),
            image=self._ui.icons.viewLocationsIcon,
            command=self._ui.tv.show_locations,
            disableOnLock=False,
        )
        self.viewLocationsButton.pack(side='left')

        # "View Items" button.
        self.viewItemsButton = self.new_button(
            text=_('Items'),
            image=self._ui.icons.viewItemsIcon,
            command=self._ui.tv.show_items,
            disableOnLock=False,
        )
        self.viewItemsButton.pack(side='left')

        # "View Plot lines" button.
        self.viewPlotLinesButton = self.new_button(
            text=_('Plot lines'),
            image=self._ui.icons.viewPlotLinesIcon,
            command=self._ui.tv.show_plot_lines,
            disableOnLock=False,
        )
        self.viewPlotLinesButton.pack(side='left')

        # "View Projectnotes" button.
        self.viewProjectnotesButton = self.new_button(
            text=_('Project notes'),
            image=self._ui.icons.viewProjectnotesIcon,
            command=self._ui.tv.show_project_notes,
            disableOnLock=False,
        )
        self.viewProjectnotesButton.pack(side='left')

        self.add_separator()

        # "Save" button.
        self.saveButton = self.new_button(
            text=_('Save'),
            image=self._ui.icons.saveIcon,
            command=self._ctrl.save_project,
            accelerator=KEYS.SAVE_PROJECT[1],
        )
        self.saveButton.pack(side='left')

        # "Lock/Unlock" button.
        self.lockButton = self.new_button(
            text=_('Lock/unlock'),
            image=self._ui.icons.lockIcon,
            command=self._ctrl.toggle_lock,
            disableOnLock=False,
        )
        self.lockButton.pack(side='left')

        # "Update from manuscript" button.
        self.updateButton = self.new_button(
            text=_('Update from manuscript'),
            image=self._ui.icons.updateFromManuscriptIcon,
            command=self._ctrl.update_from_manuscript,
        )
        self.updateButton.pack(side='left')

        # "Manuscript" button.
        self.manuscriptButton = self.new_button(
            text=_('Export Manuscript'),
            image=self._ui.icons.manuscriptIcon,
            command=self._ctrl.open_manuscript,
        )
        self.manuscriptButton.pack(side='left')

        self.add_separator()

        # "Add" button.
        self.addElementButton = self.new_button(
            text=_('Add'),
            image=self._ui.icons.addIcon,
            command=self._ctrl.add_new_element,
            accelerator=KEYS.ADD_ELEMENT[1],
        )
        self.addElementButton.pack(side='left')

        # "Add Child" button.
        self.addChildButton = self.new_button(
            text=_('Add child'),
            image=self._ui.icons.addChildIcon,
            command=self._ctrl.add_new_child,
            accelerator=KEYS.ADD_CHILD[1],
        )
        self.addChildButton.pack(side='left')

        # "Add Parent" button.
        self.addParentButton = self.new_button(
            text=_('Add parent'),
            image=self._ui.icons.addParentIcon,
            command=self._ctrl.add_new_parent,
            accelerator=KEYS.ADD_PARENT[1],
        )
        self.addParentButton.pack(side='left')

        # "Delete" button.
        self.deleteElementButton = self.new_button(
            text=_('Delete'),
            image=self._ui.icons.removeIcon,
            command=self._ctrl.delete_elements,
            accelerator=KEYS.DELETE[1],
        )
        self.deleteElementButton.pack(side='left')

        self.add_separator()

        # "Cut" button.
        self.cutButton = self.new_button(
            text=f"{_('Cut')} ({KEYS.CUT[1]})",
            image=self._ui.icons.cutIcon,
            command=self._ctrl.cut_element,
        )
        self.cutButton.pack(side='left')

        # "Copy" button.
        self.copyButton = self.new_button(
            text=f"{_('Copy')} ({KEYS.COPY[1]})",
            image=self._ui.icons.copyIcon,
            command=self._ctrl.copy_element,
        )
        self.copyButton.pack(side='left')

        # "Paste" button.
        self.pasteButton = self.new_button(
            text=f"{_('Paste')} ({KEYS.PASTE[1]})",
            image=self._ui.icons.pasteIcon,
            command=self._ctrl.paste_element,
        )
        self.pasteButton.pack(side='left')

        # Reverse order (side='right').

        # "Toggle properties" button.
        self.propertiesButton = self.new_button(
            text=_('Toggle Properties'),
            image=self._ui.icons.propertiesIcon,
            command=self._ui.toggle_properties_view,
            disableOnClose=False,
            disableOnLock=False,
            accelerator=KEYS.TOGGLE_PROPERTIES[1],
        )
        self.propertiesButton.pack(side='right')

        # "Toggle content viewer" button.
        self.viewerButton = self.new_button(
            text=_('Toggle Text viewer'),
            image=self._ui.icons.viewerIcon,
            command=self._ui.toggle_contents_view,
            disableOnClose=False,
            disableOnLock=False,
            accelerator=KEYS.TOGGLE_VIEWER[1],

        )
        self.viewerButton.pack(side='right')

        self.buttonBar.pack(
            expand=False, before=self._ui.appWindow, fill='both')

    def add_separator(self):
        tk.Frame(
            self.buttonBar,
            bg=prefs['color_separator'],
            width=1,
        ).pack(side='left', fill='y', padx=4)

    def disable_menu(self):
        for button in self._disableOnClose:
            button.config(state='disabled')

    def enable_menu(self):
        for button in self._disableOnClose:
            button.config(state='normal')

    def lock(self):
        for button in self._disableOnLock:
            button.config(state='disabled')

    def new_button(
        self,
        text,
        image,
        command,
        disableOnClose=True,
        disableOnLock=True,
        accelerator=None,
    ):
        newButton = ttk.Button(
            self.buttonBar,
            text=text,
            image=image,
            command=command,
        )
        newButton.image = image
        if disableOnClose:
            self._disableOnClose.append(newButton)
        if disableOnLock:
            self._disableOnLock.append(newButton)

        if prefs['enable_hovertips']:
            if accelerator is None:
                hoverText = text
            else:
                hoverText = f'{text} ({accelerator})'
            Hovertip(newButton, hoverText)

        return newButton

    def unlock(self):
        for button in self._disableOnLock:
            button.config(state='normal')


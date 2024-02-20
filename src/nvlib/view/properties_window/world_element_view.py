"""Provide an abstract class for viewing world element properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod
import os
from pathlib import Path
import subprocess
from tkinter import filedialog
from tkinter import ttk

from nvlib.nv_globals import prefs
from nvlib.view.properties_window.basic_view import BasicView
from nvlib.widgets.collection_box import CollectionBox
from nvlib.widgets.folding_frame import FoldingFrame
from nvlib.widgets.label_entry import LabelEntry
from nvlib.widgets.my_string_var import MyStringVar
from novxlib.file.doc_open import open_document
from novxlib.novx_globals import _
from novxlib.novx_globals import list_to_string
from novxlib.novx_globals import norm_path
from novxlib.novx_globals import string_to_list


class WorldElementView(BasicView, ABC):
    """Class for viewing world element properties.
    
    Adds to the right pane:
    - An "Aka" entry.
    - A "Tags" entry.   
    """
    _HEIGHT_LIMIT = 10

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        self._fullNameFrame = ttk.Frame(self._elementInfoWindow)
        self._fullNameFrame.pack(anchor='w', fill='x')

        # 'AKA' entry.
        self._aka = MyStringVar()
        self._akaEntry = LabelEntry(self._elementInfoWindow, text=_('AKA'), textvariable=self._aka, lblWidth=self._LBL_X)
        self._akaEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._akaEntry)
        self._akaEntry.entry.bind('<Return>', self.apply_changes)

        # 'Tags' entry.
        self._tags = MyStringVar()
        self._tagsEntry = LabelEntry(self._elementInfoWindow, text=_('Tags'), textvariable=self._tags, lblWidth=self._LBL_X)
        self._tagsEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._tagsEntry)
        self._tagsEntry.entry.bind('<Return>', self.apply_changes)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self._inputWidgets.append(widget)

        self._prefsShowLinks = None

    def apply_changes(self, event=None):
        """Apply changes of element title, description and notes."""
        super().apply_changes()

        # 'AKA' entry.
        self._element.aka = self._aka.get()

        # 'Tags' entry.
        newTags = self._tags.get()
        self._element.tags = string_to_list(newTags)

    @abstractmethod
    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        super().set_data(elementId)

        # 'AKA' entry.
        self._aka.set(self._element.aka)

        # 'Tags' entry.
        if self._element.tags is not None:
            self._tagsStr = list_to_string(self._element.tags)
        else:
            self._tagsStr = ''
        self._tags.set(self._tagsStr)

        # Links window.
        if prefs[self._prefsShowLinks]:
            self._linksWindow.show()
        else:
            self._linksWindow.hide()
        linkList = list(self._element.links.values())
        self._linkCollection.cList.set(linkList)
        listboxSize = len(linkList)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._linkCollection.cListbox.config(height=listboxSize)
        if not self._linkCollection.cListbox.curselection() or not self._linkCollection.cListbox.focus_get():
            self._linkCollection.deactivate_buttons()

    def _activate_link_buttons(self, event=None):
        if self._element.links:
            self._linkCollection.activate_buttons()
        else:
            self._linkCollection.deactivate_buttons()

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_button_bar()

    def _create_links_window(self):
        """A folding frame with a "Links" listbox and control buttons."""
        ttk.Separator(self._propertiesFrame, orient='horizontal').pack(fill='x')
        self._linksWindow = FoldingFrame(self._propertiesFrame, _('Links'), self._toggle_links_window)
        self._linksWindow.pack(fill='x')
        self._linkCollection = CollectionBox(
            self._linksWindow,
            cmdAdd=self._add_link,
            cmdRemove=self._remove_link,
            cmdOpen=self._open_link,
            cmdActivate=self._activate_link_buttons,
            lblOpen=_('Open link'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self._inputWidgets.extend(self._linkCollection.inputWidgets)
        self._linkCollection.pack(fill='x')

    def _toggle_links_window(self, event=None):
        """Hide/show the "links" window.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs[self._prefsShowLinks]:
            self._linksWindow.hide()
            prefs[self._prefsShowLinks] = False
        else:
            self._linksWindow.show()
            prefs[self._prefsShowLinks] = True

    def _add_link(self):
        """Select a link and add it to the list."""
        fileTypes = [(_('Image file'), '.jpg'),
                     (_('Image file'), '.jpeg'),
                     (_('Image file'), '.png'),
                     (_('Image file'), '.gif'),
                     (_('Text file'), '.txt'),
                     (_('Text file'), '.md'),
                     (_('All files'), '.*'),
                     ]
        selectedPath = filedialog.askopenfilename(filetypes=fileTypes)
        if selectedPath:
            try:
                homeDir = str(Path.home()).replace('\\', '/')
                shortPath = selectedPath.replace(homeDir, '~')
            except:
                shortPath = selectedPath
            links = self._element.links
            if links is None:
                links = {}
            links[shortPath] = None
            self._element.links = links

    def _open_link(self, event=None):
        """Open the selected link."""
        try:
            selection = self._linkCollection.cListbox.curselection()[0]
        except:
            return

        linkPath = list(self._element.links)[selection]
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            linkPath = linkPath.replace('~', homeDir)
        except:
            pass
        try:
            extension = os.path.splitext(linkPath)[1]
        except IndexError:
            pass
        else:
            launcher = self._ctrl.launchers.get(extension, '')
            if os.path.isfile(launcher):
                subprocess.Popen([launcher, linkPath])
                return

        if os.path.isfile(linkPath):
            open_document(linkPath)
            return

        self._ui.show_error(
            f"{_('File not found')}: {norm_path(linkPath)}",
            title=_('Cannot open link')
            )
        return

    def _remove_link(self, event=None):
        """Remove a link from the list."""
        try:
            selection = self._linkCollection.cListbox.curselection()[0]
        except:
            return

        linkPath = list(self._element.links)[selection]
        if self._ui.ask_yes_no(f'{_("Remove link")}: "{self._element.links[linkPath]}"?'):
            links = self._element.links
            try:
                del links[linkPath]
            except:
                pass
            else:
                self._element.links = links


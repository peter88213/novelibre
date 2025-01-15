"""Provide a mixin class for controlling an element properties view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import abstractmethod
import os
from tkinter import filedialog

from mvclib.controller.sub_controller import SubController
from nvlib.novx_globals import CH_ROOT
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class BasicViewCtrl(SubController):
    _HEIGHT_LIMIT = 10

    def initialize_controller(self, model, view, controller):
        super().initialize_controller(model, view, controller)

        self.element = None
        self.elementId = None
        self._pickingMode = False
        self._pickCommand = None
        self._isLocked = False
        self._uiEscBinding = ''
        self._uiBtn1Binding = ''
        self._lastSelected = ''
        self.doNotUpdate = False

    def activate_link_buttons(self, event=None):
        if self.element.links:
            self.linkCollection.enable_buttons()
        else:
            self.linkCollection.disable_buttons()

    def add_link(self):
        """Select a link and add it to the list."""
        fileTypes = [
            (_('Image file'), '.jpg'),
            (_('Image file'), '.jpeg'),
            (_('Image file'), '.png'),
            (_('Image file'), '.gif'),
            (_('Text file'), '.txt'),
            (_('Text file'), '.md'),
            (_('ODF document'), '.odt'),
            (_('ODF document'), '.ods'),
            (_('All files'), '.*'),
            ]
        selectedPath = filedialog.askopenfilename(filetypes=fileTypes)
        if selectedPath:
            shortPath = self._ctrl.linkProcessor.shorten_path(selectedPath)
            links = self.element.links
            if links is None:
                links = {}
            links[shortPath] = selectedPath
            self.element.links = links

    def apply_changes(self, event=None):
        """Apply changes of element title, description, and notes."""
        if self.element is None:
            return

        # Title entry.
        titleStr = self.indexCard.title.get()
        if titleStr:
            titleStr = titleStr.strip()
        elif self.elementId != CH_ROOT:
            titleStr = self.elementId
        self.element.title = titleStr

        # Description entry.
        if self.indexCard.bodyBox.hasChanged:
            self.element.desc = self.indexCard.bodyBox.get_text()

        # Notes textbox (if any).
        if hasattr(self.element, 'notes') and self.notesWindow.hasChanged:
            self.element.notes = self.notesWindow.get_text()

    def lock(self):
        """Inhibit element change."""
        self.indexCard.lock()
        try:
            self.notesWindow.config(state='disabled')
        except:
            pass
        for widget in self.inputWidgets:
            widget.config(state='disabled')
        self._isLocked = True

    def open_link(self, event=None):
        """Open the selected link."""
        try:
            selection = self.linkCollection.cListbox.curselection()[0]
        except:
            return

        self._ctrl.open_link(self.element, selection)

    def remove_link(self, event=None):
        """Remove a link from the list."""
        try:
            selection = self.linkCollection.cListbox.curselection()[0]
        except:
            return

        linkPath = list(self.element.links)[selection]
        if self._ui.ask_yes_no(f'{_("Remove link")}: "{self.element.links[linkPath]}"?'):
            links = self.element.links
            try:
                del links[linkPath]
            except:
                pass
            else:
                self.element.links = links

    @abstractmethod
    def set_data(self, elementId):
        """Update the view with element's data.
        
        Note: subclasses must set self.element before calling this method.
        """
        self.elementId = elementId
        if self.element is None:
            return

        # Title entry.
        self.indexCard.title.set(self.element.title)

        # Description entry.
        self.indexCard.bodyBox.clear()
        self.indexCard.bodyBox.set_text(self.element.desc)

        # Links window.
        if hasattr(self.element, 'links'):
            if prefs[self.prefsShowLinks]:
                self.linksWindow.show()
            else:
                self.linksWindow.hide()
            linkList = []
            for path in self.element.links:
                linkList.append(os.path.basename(path))
            self.linkCollection.cList.set(linkList)
            listboxSize = len(linkList)
            if listboxSize > self._HEIGHT_LIMIT:
                listboxSize = self._HEIGHT_LIMIT
            self.linkCollection.cListbox.config(height=listboxSize)
            if not self.linkCollection.cListbox.curselection() or not self.linkCollection.cListbox.focus_get():
                self.linkCollection.disable_buttons()

        # Notes entry (if any).
        if hasattr(self.element, 'notes'):
            self.notesWindow.clear()
            self.notesWindow.set_text(self.element.notes)

    def unlock(self):
        """Enable element change."""
        self.indexCard.unlock()
        try:
            self.notesWindow.config(state='normal')
        except:
            pass
        for widget in self.inputWidgets:
            widget.config(state='normal')
        self._isLocked = False

    def _end_picking_mode(self, event=None):
        if self._pickingMode:
            if self._pickCommand is not None:
                self._pickCommand()
                self._pickCommand = None
            self._ui.root.bind('<Button-1>', self._uiBtn1Binding)
            self._ui.root.bind('<Escape>', self._uiEscBinding)
            self._ui.tv.config(cursor='arrow')
            self._ui.tv.see_node(self._lastSelected)
            self._ui.tv.tree.selection_set(self._lastSelected)
            self._pickingMode = False
        self._ui.restore_status()

    def _report_missing_reference_date(self):
        self._ui.show_error(
            _('Please enter a reference date.'),
            title=_('Cannot convert date/days'))

    def _start_picking_mode(self, event=None, command=None):
        """Start the picking mode for element selection.        
        
        Change the mouse cursor to "+" and expand the "Book" subtree.
        Now the tree selection does not trigger the viewer, 
        but tries to add the selected element to the collection.  
        
        To end the picking mode, press the Escape key.
        """
        self._pickCommand = command
        if not self._pickingMode:
            self._lastSelected = self._ui.selectedNode
            self._ui.tv.config(cursor='plus')
            self._ui.tv.open_children('')
            self._uiEscBinding = self._ui.root.bind('<Escape>')
            self._ui.root.bind('<Escape>', self._end_picking_mode)
            self._uiBtn1Binding = self._ui.root.bind('<Button-1>')
            self._ui.root.bind('<Button-1>', self._end_picking_mode)
            self._pickingMode = True
        self._ui.set_status(_('Pick Mode (click here or press Esc to exit)'), colors=('maroon', 'white'))


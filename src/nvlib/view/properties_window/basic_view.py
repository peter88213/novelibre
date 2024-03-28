"""Provide an abstract class for viewing novelibre project element properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod
from tkinter import ttk

from novxlib.novx_globals import _
from nvlib.nv_globals import prefs
from nvlib.widgets.index_card import IndexCard
from nvlib.widgets.text_box import TextBox
from tkinter import filedialog
from nvlib.widgets.collection_box import CollectionBox
from nvlib.widgets.folding_frame import FoldingFrame


class BasicView(ttk.Frame, ABC):
    """Abstract base class for viewing tree element properties.
    
    Adds to the right pane:
    - An "index card" with title and description of the element (optional).
    - A text box fpr element notes (optional).
    - Navigation buttons (go to next/previous element). 
    """
    _HEIGHT_LIMIT = 10

    _LBL_X = 10
    # Width of left-placed labels.

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            parent -- Parent widget to display this widget.
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        """
        super().__init__(parent)

        self._mdl = model
        self._ui = view
        self._ctrl = controller

        self._elementId = None
        self._element = None
        self._tagsStr = ''
        self._parent = parent
        self._inputWidgets = []

        self.doNotUpdate = False
        self._pickingMode = False
        self._isLocked = False

        # Frame for element specific informations.
        self._propertiesFrame = ttk.Frame(self)
        self._propertiesFrame.pack(expand=True, fill='both')

        self._prefsShowLinks = None
        self._create_frames()

    def _activate_link_buttons(self, event=None):
        if self._element.links:
            self._linkCollection.enable_buttons()
        else:
            self._linkCollection.disable_buttons()

    def apply_changes(self, event=None):
        """Apply changes of element title, description, and notes."""
        if self._element is None:
            return

        # Title entry.
        titleStr = self._indexCard.title.get()
        if titleStr:
            titleStr = titleStr.strip()
        self._element.title = titleStr

        # Description entry.
        if self._indexCard.bodyBox.hasChanged:
            self._element.desc = self._indexCard.bodyBox.get_text()

        # Notes textbox (if any).
        if hasattr(self._element, 'notes') and self._notesWindow.hasChanged:
            self._element.notes = self._notesWindow.get_text()

    def focus_title(self):
        """Prepare the title entry for manual input."""
        self._indexCard.titleEntry.focus()
        self._indexCard.titleEntry.icursor(0)
        self._indexCard.titleEntry.selection_range(0, 'end')

    def hide(self):
        """Hide the view."""
        self.pack_forget()

    def lock(self):
        """Inhibit element change."""
        self._indexCard.lock()
        try:
            self._notesWindow.config(state='disabled')
        except:
            pass
        for widget in self._inputWidgets:
            widget.config(state='disabled')
        self._isLocked = True

    @abstractmethod
    def set_data(self, elementId):
        """Update the view with element's data.
        
        Note: subclasses must set self._element before calling this method.
        """
        self._elementId = elementId
        self._tagsStr = ''
        if self._element is not None:

            # Title entry.
            self._indexCard.title.set(self._element.title)

            # Description entry.
            self._indexCard.bodyBox.clear()
            self._indexCard.bodyBox.set_text(self._element.desc)

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
                self._linkCollection.disable_buttons()

            # Notes entry (if any).
            if hasattr(self._element, 'notes'):
                self._notesWindow.clear()
                self._notesWindow.set_text(self._element.notes)

        if self._pickingMode:
            self._start_picking_mode()
            # refreshing the status bar

    def show(self):
        """Make the view visible."""
        self.pack(expand=True, fill='both')

    def unlock(self):
        """Enable element change."""
        self._indexCard.unlock()
        try:
            self._notesWindow.config(state='normal')
        except:
            pass
        for widget in self._inputWidgets:
            widget.config(state='normal')
        self._isLocked = False

    def _add_link(self):
        """Select a link and add it to the list."""
        fileTypes = [(_('Image file'), '.jpg'),
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
            links = self._element.links
            if links is None:
                links = {}
            links[shortPath] = None
            self._element.links = links

    def _add_separator(self):
        ttk.Separator(self._propertiesFrame, orient='horizontal').pack(fill='x')

    def _create_button_bar(self):
        """Create a button bar at the bottom."""
        self._buttonBar = ttk.Frame(self)
        self._buttonBar.pack(fill='x')

        # "Previous" button.
        ttk.Button(self._buttonBar, text=_('Previous'), command=self._load_prev).pack(side='left', fill='x', expand=True, padx=1, pady=2)

        # "Next" button.
        ttk.Button(self._buttonBar, text=_('Next'), command=self._load_next).pack(side='left', fill='x', expand=True, padx=1, pady=2)

    def _create_element_info_window(self):
        """Create a window for element specific information."""
        self._elementInfoWindow = ttk.Frame(self._propertiesFrame)
        self._elementInfoWindow.pack(fill='x')

    @abstractmethod
    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        pass

    def _create_index_card(self):
        """Create an "index card" for element title and description."""
        self._indexCard = IndexCard(
            self._propertiesFrame,
            bd=2,
            fg=prefs['color_text_fg'],
            bg=prefs['color_text_bg'],
            relief='ridge'
            )
        self._indexCard.bodyBox['height'] = prefs['index_card_height']
        self._indexCard.pack(expand=False, fill='both')
        self._indexCard.titleEntry.bind('<Return>', self.apply_changes)
        self._indexCard.titleEntry.bind('<FocusOut>', self.apply_changes)
        self._indexCard.bodyBox.bind('<FocusOut>', self.apply_changes)

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

    def _create_notes_window(self):
        """Create a text box for element notes."""
        self._notesWindow = TextBox(
            self._propertiesFrame,
            wrap='word',
            undo=True,
            autoseparators=True,
            maxundo=-1,
            height=0,
            width=10,
            padx=5,
            pady=5,
            bg=prefs['color_notes_bg'],
            fg=prefs['color_notes_fg'],
            insertbackground=prefs['color_notes_fg'],
            )
        self._notesWindow.pack(expand=True, fill='both')
        self._notesWindow.bind('<FocusOut>', self.apply_changes)

    def _end_picking_mode(self, event=None):
        if self._pickingMode:
            self._ui.tv.tree.bind('<<TreeviewSelect>>', self._treeSelectBinding)
            self._ui.root.bind('<Escape>', self._uiEscBinding)
            self._ui.tv.config(cursor='arrow')
            self._ui.tv.tree.see(self._lastSelected)
            self._ui.tv.tree.selection_set(self._lastSelected)
            self._pickingMode = False
        self._ui.restore_status()

    def _load_next(self):
        """Load the next tree element of the same type."""
        thisNode = self._ui.tv.tree.selection()[0]
        nextNode = self._ui.tv.next_node(thisNode)
        if nextNode:
            self._ui.tv.tree.see(nextNode)
            self._ui.tv.tree.selection_set(nextNode)

    def _load_prev(self):
        """Load the next tree element of the same type."""
        thisNode = self._ui.tv.tree.selection()[0]
        prevNode = self._ui.tv.prev_node(thisNode)
        if prevNode:
            self._ui.tv.tree.see(prevNode)
            self._ui.tv.tree.selection_set(prevNode)

    def _open_link(self, event=None):
        """Open the selected link."""
        try:
            selection = self._linkCollection.cListbox.curselection()[0]
        except:
            return

        linkPath = list(self._element.links)[selection]
        self._ctrl.open_link(linkPath)

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

    def _start_picking_mode(self, event=None):
        """Start the picking mode for element selection.        
        
        Change the mouse cursor to "+" and expand the "Book" subtree.
        Now the tree selection does not trigger the viewer, 
        but tries to add the selected element to the collection.  
        
        To end the picking mode, press the Escape key.
        """
        if not self._pickingMode:
            self._lastSelected = self._ui.tv.tree.selection()[0]
            self._ui.tv.config(cursor='plus')
            self._ui.tv.open_children('')
            self._treeSelectBinding = self._ui.tv.tree.bind('<<TreeviewSelect>>')
            self._uiEscBinding = self._ui.root.bind('<Esc>')
            self._ui.root.bind('<Escape>', self._end_picking_mode)
            self._ui.statusBar.bind('<Button-1>', self._end_picking_mode)
            self._pickingMode = True
        self._ui.set_status(_('Pick Mode (click here or press Esc to exit)'), colors=('maroon', 'white'))

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


"""Provide an abstract class for viewing noveltree project element properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod
from tkinter import ttk

from noveltreelib.noveltree_globals import prefs
from noveltreelib.widgets.index_card import IndexCard
from noveltreelib.widgets.text_box import TextBox
from novxlib.novx_globals import _


class BasicView(ttk.Frame, ABC):
    """Abstract base class for viewing tree element properties.
    
    Adds to the right pane:
    - An "index card" with title and description of the element (optional).
    - A text box fpr element notes (optional).
    - Navigation buttons (go to next/previous element). 
    """

    _LBL_X = 10
    # Width of left-placed labels.

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            view: NoveltreeUi -- Reference to the user interface.
            parent -- Parent widget to display this widget.

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

        # Frame for element specific informations.
        self._propertiesFrame = ttk.Frame(self)
        self._propertiesFrame.pack(expand=True, fill='both')

        self._create_frames()

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

            # Notes entry (if any).
            if hasattr(self._element, 'notes'):
                self._notesWindow.clear()
                self._notesWindow.set_text(self._element.notes)

    def show(self):
        """Make the view visible."""
        self.pack(expand=True, fill='both')

    def unlock(self):
        """enable element change."""
        self._indexCard.unlock()
        try:
            self._notesWindow.config(state='normal')
        except:
            pass
        for widget in self._inputWidgets:
            widget.config(state='normal')

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
            self._pickingMode = True


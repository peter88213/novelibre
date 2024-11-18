"""Provide an abstract class for viewing novelibre project element properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import abstractmethod
from tkinter import ttk

from mvclib.view.observer import Observer
from mvclib.widgets.folding_frame import FoldingFrame
from mvclib.widgets.index_card import IndexCard
from mvclib.widgets.text_box import TextBox
from nvlib.novx_globals import _
from nvlib.nv_globals import prefs
from nvlib.view.widgets.collection_box import CollectionBox


class BasicView(ttk.Frame, Observer):
    """Abstract base class for viewing tree element properties.
    
    Adds to the right pane:
    - An "index card" with title and description of the element (optional).
    - A text box fpr element notes (optional).
    - Navigation buttons (go to next/previous element). 
    """

    _LBL_X = 10
    # Width of left-placed labels.

    def __init__(self, parent, model, view, controller, **kw):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            parent -- Parent widget to display this widget.
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        """
        super().__init__(parent, **kw)

        self._mdl = model
        self._ui = view
        self._ctrl = controller

        self.elementId = None
        self.element = None
        self.tagsStr = ''
        self._parent = parent
        self.inputWidgets = []

        self._pickingMode = False
        self._pickCommand = None
        self._uiEscBinding = ''
        self._uiBtn1Binding = ''

        self.doNotUpdate = False
        self.isLocked = False

        # Frame for element specific informations.
        self._propertiesFrame = ttk.Frame(self)
        self._propertiesFrame.pack(expand=True, fill='both')

        self.prefsShowLinks = None
        self._create_frames()

    def focus_title(self):
        """Prepare the title entry for manual input."""
        self.indexCard.titleEntry.focus()
        self.indexCard.titleEntry.icursor(0)
        self.indexCard.titleEntry.selection_range(0, 'end')

    def hide(self):
        """Hide the view."""
        self.element = None
        self.pack_forget()

    def show(self):
        """Make the view visible."""
        self.pack(expand=True, fill='both')

    def _activate_link_buttons(self, event=None):
        if self.element.links:
            self.linkCollection.enable_buttons()
        else:
            self.linkCollection.disable_buttons()

    def _add_separator(self):
        ttk.Separator(self._propertiesFrame, orient='horizontal').pack(fill='x')

    def _create_button_bar(self):
        """Create a button bar at the bottom."""
        self._buttonBar = ttk.Frame(self)
        self._buttonBar.pack(fill='x')

        # "Previous" button.
        ttk.Button(self._buttonBar, text=_('Previous'), command=self.load_prev).pack(side='left', fill='x', expand=True, padx=1, pady=2)

        # "Next" button.
        ttk.Button(self._buttonBar, text=_('Next'), command=self.load_next).pack(side='left', fill='x', expand=True, padx=1, pady=2)

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
        self.indexCard = IndexCard(
            self._propertiesFrame,
            bd=2,
            fg=prefs['color_text_fg'],
            bg=prefs['color_text_bg'],
            relief='ridge'
            )
        self.indexCard.bodyBox['height'] = prefs['index_card_height']
        self.indexCard.pack(expand=False, fill='both')
        self.indexCard.titleEntry.bind('<Return>', self.get_data)
        self.indexCard.titleEntry.bind('<FocusOut>', self.get_data)
        self.indexCard.bodyBox.bind('<FocusOut>', self.get_data)

    def _create_links_window(self):
        """A folding frame with a "Links" listbox and control buttons."""
        ttk.Separator(self._propertiesFrame, orient='horizontal').pack(fill='x')
        self.linksWindow = FoldingFrame(self._propertiesFrame, _('Links'), self._toggle_links_window)
        self.linksWindow.pack(fill='x')
        self.linkCollection = CollectionBox(
            self.linksWindow,
            cmdAdd=self._add_link,
            cmdRemove=self.remove_link,
            cmdOpen=self.open_link,
            cmdActivate=self._activate_link_buttons,
            lblOpen=_('Open link'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self.inputWidgets.extend(self.linkCollection.inputWidgets)
        self.linkCollection.pack(fill='x')

    def _create_notes_window(self):
        """Create a text box for element notes."""
        self.notesWindow = TextBox(
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
        self.notesWindow.pack(expand=True, fill='both')
        self.notesWindow.bind('<FocusOut>', self.get_data)

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

    def start_picking_mode(self, event=None, command=None):
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

    def _toggle_links_window(self, event=None):
        """Hide/show the "links" window.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs[self.prefsShowLinks]:
            self.linksWindow.hide()
            prefs[self.prefsShowLinks] = False
        else:
            self.linksWindow.show()
            prefs[self.prefsShowLinks] = True


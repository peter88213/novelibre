"""Provide an abstract class for viewing novelibre project element properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import abstractmethod
from tkinter import ttk

from nvlib.gui.observer import Observer
from nvlib.gui.widgets.collection_box import CollectionBox
from nvlib.gui.widgets.folding_frame import FoldingFrame
from nvlib.gui.widgets.index_card import IndexCard
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.gui.widgets.text_box import TextBox
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class BasicView(ttk.Frame, Observer):
    """Abstract base class for viewing tree element properties.
    
    Adds to the right pane:
    - An "index card" with title and description of the element (optional).
    - A text box fpr element notes (optional).
    - Navigation buttons (go to next/previous element). 
    """

    _LBL_X = 15
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
        self.initialize_controller(model, view, controller)

        self._parent = parent
        self.inputWidgets = []

        # Frame for element specific informations.
        self.propertiesFrame = ttk.Frame(self)
        self.propertiesFrame.pack(expand=True, fill='both')

        self._prefsShowLinks = None
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

    def refresh(self):
        """ Overrides the abstract superclass method."""
        pass

    def show(self):
        """Make the view visible."""
        self.pack(expand=True, fill='both')

    def _add_separator(self):
        ttk.Separator(self.propertiesFrame, orient='horizontal').pack(fill='x')

    def _create_button_bar(self):
        """Create a button bar at the bottom."""
        self._buttonBar = ttk.Frame(self)
        self._buttonBar.pack(fill='x')

        # "Previous" button.
        ttk.Button(
            self._buttonBar,
            text=_('Previous'),
            command=self._ui.tv.load_prev
            ).pack(side='left', fill='x', expand=True, padx=1, pady=2)

        # "Next" button.
        ttk.Button(
            self._buttonBar,
            text=_('Next'),
            command=self._ui.tv.load_next
            ).pack(side='left', fill='x', expand=True, padx=1, pady=2)

    def _create_element_info_window(self):
        """Create a window for element specific information."""
        self.elementInfoWindow = ttk.Frame(self.propertiesFrame)
        self.elementInfoWindow.pack(fill='x')

    @abstractmethod
    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        pass

    def _create_index_card(self):
        """Create an "index card" for element title and description."""
        self.indexCard = IndexCard(
            self.propertiesFrame,
            bd=2,
            fg=prefs['color_text_fg'],
            bg=prefs['color_text_bg'],
            relief='ridge'
            )
        self.indexCard.bodyBox['height'] = prefs['index_card_height']
        self.indexCard.pack(expand=False, fill='both')
        self.indexCard.titleEntry.bind('<Return>', self.apply_changes)
        self.indexCard.titleEntry.bind('<FocusOut>', self.apply_changes)
        self.indexCard.bodyBox.bind('<FocusOut>', self.apply_changes)

    def _create_links_window(self):
        """A folding frame with a "Links" listbox and control buttons."""
        ttk.Separator(self.propertiesFrame, orient='horizontal').pack(fill='x')
        self.linksWindow = FoldingFrame(
            self.propertiesFrame,
            _('Links'),
            self._toggle_links_window
            )
        self.linksWindow.pack(fill='x')

        # Link count preview.
        self.linksPreviewVar = MyStringVar()
        linksPreview = ttk.Label(
            self.linksWindow.titleBar,
            textvariable=self.linksPreviewVar,
            )
        linksPreview.pack(side='left', padx=2)
        linksPreview.bind(
            '<Button-1>',
            self._toggle_links_window
            )

        # Link list.
        self.linkCollection = CollectionBox(
            self.linksWindow,
            cmdAdd=self.add_link,
            cmdRemove=self.remove_link,
            cmdOpen=self.open_link,
            cmdActivate=self.activate_link_buttons,
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
            self.propertiesFrame,
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
        self.notesWindow.bind('<FocusOut>', self.apply_changes)

    def _toggle_links_window(self, event=None):
        """Hide/show the "links" window.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs[self._prefsShowLinks]:
            self.linksWindow.hide()
            prefs[self._prefsShowLinks] = False
        else:
            self.linksWindow.show()
            prefs[self._prefsShowLinks] = True


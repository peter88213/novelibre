"""Provide a class for viewing novelibre project element properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import filedialog
from tkinter import ttk

from nvlib.controller.services.nv_help import NvHelp
from nvlib.gui.properties_window.blank_view import BlankView
from nvlib.gui.widgets.collection_box import CollectionBox
from nvlib.gui.widgets.index_card import IndexCard
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.gui.widgets.text_box import TextBox
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import norm_path
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class ElementView(BlankView):
    """Base class for viewing tree element properties.
    
    Adds to the right pane:
    - An "index card" with title and description of the element (optional).
    - A text box fpr element notes (optional).
    - Navigation buttons (go to next/previous element). 
    """
    _HELP_PAGE = 'properties.html'
    _LABEL_WIDTH = 15
    # Width of left-placed labels.

    _HEIGHT_LIMIT = 10
    _CHECK = '☑'

    def __init__(self, parent, model, view, controller, **kw):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            parent -- Parent widget to display this widget.
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        - Initialize element-specific tk entry data.
        - Place element-specific widgets in the element's info window.
        """
        super().__init__(parent, model, view, controller, **kw)
        self._pickingMode = False
        self._pickCommand = None
        self._isLocked = False
        self._uiEscBinding = ''
        self._uiBtn1Binding = ''
        self._lastSelected = ''
        self._doNotUpdate = False

        self.elementId = None
        self.inputWidgets = []

        # Frame for element specific informations.
        self._propertiesFrame = ttk.Frame(self)
        self._propertiesFrame.pack(expand=True, fill='both')

        self._prefsShowLinks = None
        self._create_frames()

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
        titleStr = self._indexCard.title.get()
        if titleStr:
            titleStr = titleStr.strip()
        elif self.elementId != CH_ROOT:
            titleStr = self.elementId
        self.element.title = titleStr

        # Description entry.
        if self._indexCard.bodyBox.hasChanged:
            self.element.desc = self._indexCard.bodyBox.get_text()

        # Notes textbox (if any).
        if hasattr(self.element, 'notes') and self.notesWindow.hasChanged:
            self.element.notes = self.notesWindow.get_text()

    def configure_display(self):
        """Expand or collapse the property frames."""

        #--- Links window.
        if hasattr(self.element, 'links'):
            if prefs[self._prefsShowLinks]:
                self.linksWindow.show()
                self.linksPreviewVar.set('')
            else:
                self.linksWindow.hide()
                linksCount = len(self.element.links)
                if linksCount:
                    self.linksPreviewVar.set(str(linksCount))
                else:
                    self.linksPreviewVar.set('')

    def focus_title(self):
        """Prepare the title entry for manual input."""
        self._indexCard.titleEntry.focus()
        self._indexCard.titleEntry.icursor(0)
        self._indexCard.titleEntry.selection_range(0, 'end')

    def lock(self):
        """Inhibit element change."""
        self._indexCard.lock()
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

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Note: subclasses must set self.element before calling this method.
        """
        self.elementId = elementId
        if self.element is None:
            return

        self.configure_display()

        # Title entry.
        self._indexCard.title.set(self.element.title)

        # Description entry.
        self._indexCard.bodyBox.clear()
        self._indexCard.bodyBox.set_text(self.element.desc)

        # Links window.
        if hasattr(self.element, 'links'):
            linkList = []
            for path in self.element.links:
                linkList.append(os.path.basename(path))
            self.linkCollection.cList.set(linkList)
            listboxSize = len(linkList)
            if listboxSize > self._HEIGHT_LIMIT:
                listboxSize = self._HEIGHT_LIMIT
            self.linkCollection.cListbox.config(height=listboxSize)
            if (
                not self.linkCollection.cListbox.curselection()
                or not self.linkCollection.cListbox.focus_get()
            ):
                self.linkCollection.disable_buttons()

        # Notes entry (if any).
        if hasattr(self.element, 'notes'):
            self.notesWindow.clear()
            self.notesWindow.set_text(self.element.notes)

    def unlock(self):
        """Enable element change."""
        self._indexCard.unlock()
        try:
            self.notesWindow.config(state='normal')
        except:
            pass
        for widget in self.inputWidgets:
            widget.config(state='normal')
        self._isLocked = False

    def _activate_link_buttons(self, event=None):
        if self.element.links:
            self.linkCollection.enable_buttons()
        else:
            self.linkCollection.disable_buttons()

    def _add_separator(self):
        ttk.Separator(
            self._propertiesFrame,
            orient='horizontal'
        ).pack(fill='x')

    def _create_button_bar(self):
        # Create a button bar at the bottom.
        self._buttonBar = ttk.Frame(self)
        self._buttonBar.pack(fill='x')

        # "Previous" button.
        ttk.Button(
            self._buttonBar,
            text=_('Previous'),
            command=self._ui.tv.load_prev,
        ).pack(side='left', fill='x', expand=True, padx=1, pady=2)

        # "Help" button.
        ttk.Button(
            self._buttonBar,
            text=_('Online help'),
            command=self._open_help,
        ).pack(side='left', fill='x', expand=True, padx=1, pady=2)

        # "Next" button.
        ttk.Button(
            self._buttonBar,
            text=_('Next'),
            command=self._ui.tv.load_next,
        ).pack(side='left', fill='x', expand=True, padx=1, pady=2)

    def _create_element_info_window(self):
        # Create a window for element specific information.
        self._elementInfoWindow = ttk.Frame(self._propertiesFrame)
        self._elementInfoWindow.pack(fill='x')

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        pass

    def _create_index_card(self):
        # Create an "index card" for element title and description.
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
        # "A folding frame with a "Links" listbox and control buttons.
        ttk.Separator(
            self._propertiesFrame,
            orient='horizontal'
        ).pack(fill='x')
        self.linksWindow = self.SubFrame(
            self._propertiesFrame,
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
        linksPreview.bind('<Button-1>', self._toggle_links_window)

        # Link list.
        self.linkCollection = CollectionBox(
            self.linksWindow,
            cmdAdd=self.add_link,
            cmdRemove=self._remove_link,
            cmdOpen=self.open_link,
            cmdActivate=self._activate_link_buttons,
            lblOpen=_('Open link'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
        )
        self.inputWidgets.extend(self.linkCollection.inputWidgets)
        self.linkCollection.pack(fill='x')

    def _create_notes_window(self):
        # Create a text box for element notes.
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
        self.notesWindow.bind('<FocusOut>', self.apply_changes)

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

    def _open_help(self, event=None):
        NvHelp.open_help_page(self._HELP_PAGE)

    def _remove_link(self, event=None):
        # Remove a link from the list.
        try:
            selection = self.linkCollection.cListbox.curselection()[0]
        except:
            return

        linkPath = list(self.element.links)[selection]
        if self._ui.ask_yes_no(
            message=_('Remove link?'),
            detail=norm_path(self.element.links[linkPath]),
            ):
            links = self.element.links
            try:
                del links[linkPath]
            except:
                pass
            else:
                self.element.links = links

    def _report_missing_reference_date(self):
        self._ui.show_error(
            message=_('Cannot convert date/days'),
            detail=f"{_('Please enter a reference date')}."
            )

    def _start_picking_mode(self, event=None, command=None):
        # Start the picking mode for element selection.
        # Change the mouse cursor to "+" and expand the "Book" subtree.
        # Now the tree selection does not trigger the viewer,
        # but tries to add the selected element to the collection.
        # To end the picking mode, press the Escape key.
        self._pickCommand = command
        if not self._pickingMode:
            self._lastSelected = self._ui.selectedNode
            self._ui.tv.config(cursor='plus')
            self._uiEscBinding = self._ui.root.bind('<Escape>')
            self._ui.root.bind('<Escape>', self._end_picking_mode)
            self._uiBtn1Binding = self._ui.root.bind('<Button-1>')
            self._ui.root.bind('<Button-1>', self._end_picking_mode)
            self._pickingMode = True
        self._ui.set_status(
            _('Pick Mode (click here or press Esc to exit)'),
            colors=('maroon', 'white')
        )

    def _toggle_folding_frame(self):
        if not self._ctrl.isLocked:
            self.apply_changes()
        self.configure_display()

    def _toggle_links_window(self, event=None):
        # Hide/show the "links" window
        # Callback procedure for the FoldingFrame's button.
        if prefs[self._prefsShowLinks]:
            self.linksWindow.hide()
            prefs[self._prefsShowLinks] = False
        else:
            self.linksWindow.show()
            prefs[self._prefsShowLinks] = True
        self._toggle_folding_frame()


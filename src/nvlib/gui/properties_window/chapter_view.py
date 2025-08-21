"""Provide a class for viewing and editing chapter properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.element_view import ElementView
from nvlib.gui.widgets.folding_frame import FoldingFrame
from nvlib.gui.widgets.label_entry import LabelEntry
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.gui.widgets.text_box import TextBox
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class ChapterView(ElementView):
    """Class for viewing and editing chapter properties.
      
    Adds to the right pane:
    - A "Do not auto-number" checkbox.
    """
    _HELP_PAGE = 'chapter_view.html'

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- 'Unused' checkbox.
        self._isUnusedVar = tk.BooleanVar()
        self._isUnusedCheckbox = ttk.Checkbutton(
            self._elementInfoWindow,
            text=_('Unused'),
            variable=self._isUnusedVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._isUnusedCheckbox.pack(anchor='w')
        inputWidgets.append(self._isUnusedCheckbox)

        #--- 'Do not auto-number...' checkbox.
        self._noNumberVar = tk.BooleanVar()
        self._noNumberCheckbox = ttk.Checkbutton(
            self._elementInfoWindow,
            variable=self._noNumberVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._noNumberCheckbox.pack(anchor='w')
        inputWidgets.append(self._noNumberCheckbox)

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal'
        ).pack(fill='x')

        #--- 'Epigraph' entry.
        self._epigraphFrame = FoldingFrame(
            self._elementInfoWindow,
            _('Epigraph'),
            self._toggle_epigraph_window,
        )

        # Epigraph preview.
        self._epigraphPreviewVar = MyStringVar()
        epigraphPreview = ttk.Label(
            self._epigraphFrame.titleBar,
            textvariable=self._epigraphPreviewVar,
        )
        epigraphPreview.pack(side='left', padx=2)
        epigraphPreview.bind('<Button-1>', self._toggle_epigraph_window)

        self._epigraphBox = TextBox(self._epigraphFrame,
            wrap='word',
            undo=True,
            autoseparators=True,
            maxundo=-1,
            height=10,
            width=10,
            padx=5,
            pady=5,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
            insertbackground=prefs['color_text_fg'],
        )
        self._epigraphBox.pack(fill='x')
        inputWidgets.append(self._epigraphBox)

        #--- 'Epigraph source' entry.
        self._epigraphSrcVar = MyStringVar()
        self._epigraphSrcEntry = LabelEntry(
            self._epigraphFrame,
            text=_('Source'),
            textvariable=self._epigraphSrcVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._epigraphSrcEntry.pack(anchor='w')
        inputWidgets.append(self._epigraphSrcEntry)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

        self._prefsShowLinks = 'show_ch_links'

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        if self.element.isTrash:
            return

        super().apply_changes()

        #--- "Unused" checkbox.
        if self._isUnusedVar.get():
            self._ctrl.set_type_unused()
        else:
            self._ctrl.set_type_normal()

        #--- "Do not auto-number..." checkbox.
        self.element.noNumber = self._noNumberVar.get()

        #--- "Epigraph' entry.
        if self._epigraphBox.hasChanged:
            self.element.epigraph = self._epigraphBox.get_text()

        #--- "Epigraph source' entry.
        self.element.epigraphSrc = self._epigraphSrcVar.get()

    def configure_display(self):
        """Expand or collapse the property frames."""
        super().configure_display()

        #--- Epigraph frame.
        if prefs['show_ch_epigraph']:
            self._epigraphFrame.show()
            self._epigraphPreviewVar.set('')
        else:
            self._epigraphFrame.hide()
            if self.element.epigraph or self.element.epigraphSrc:
                self._epigraphPreviewVar.set(self._CHECK)
            else:
                self._epigraphPreviewVar.set('')

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Configure the "Do not auto-number" button, depending 
        on the chapter level.    
        Extends the superclass constructor.
        """
        self.element = self._mdl.novel.chapters[elementId]
        super().set_data(elementId)

        #--- "Unused" checkbox.
        if self.element.chType > 0:
            self._isUnusedVar.set(True)
        else:
            self._isUnusedVar.set(False)

        #--- "Do not auto-number..." checkbox.
        if self.element.chLevel == 1:
            labelText = _('Do not auto-number this part')
        else:
            labelText = _('Do not auto-number this chapter')
        self._noNumberCheckbox.configure(text=labelText)
        self._noNumberVar.set(self.element.noNumber)

        #--- Epigraph frame.
        self._epigraphBox.set_text(self.element.epigraph)
        self._epigraphSrcVar.set(self.element.epigraphSrc)

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _toggle_epigraph_window(self, event=None):
        # Hide/show the 'Epigraph' window.
        if prefs['show_ch_epigraph']:
            self._epigraphFrame.hide()
            prefs['show_ch_epigraph'] = False
        else:
            self._epigraphFrame.show()
            prefs['show_ch_epigraph'] = True
        self._toggle_folding_frame()

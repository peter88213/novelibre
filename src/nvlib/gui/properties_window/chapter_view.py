"""Provide a class for viewing and editing chapter properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.basic_view import BasicView
from nvlib.gui.properties_window.chapter_view_ctrl import ChapterViewCtrl
from nvlib.gui.widgets.folding_frame import FoldingFrame
from nvlib.gui.widgets.label_entry import LabelEntry
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.gui.widgets.text_box import TextBox
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class ChapterView(BasicView, ChapterViewCtrl):
    """Class for viewing and editing chapter properties.
      
    Adds to the right pane:
    - A "Do not auto-number" checkbox.
    """

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- 'Unused' checkbox.
        self.isUnusedVar = tk.BooleanVar()
        self.isUnusedCheckbox = ttk.Checkbutton(
            self.elementInfoWindow,
            text=_('Unused'),
            variable=self.isUnusedVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self.isUnusedCheckbox.pack(anchor='w')
        inputWidgets.append(self.isUnusedCheckbox)

        #--- 'Do not auto-number...' checkbox.
        self.noNumberVar = tk.BooleanVar()
        self.noNumberCheckbox = ttk.Checkbutton(
            self.elementInfoWindow,
            variable=self.noNumberVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self.noNumberCheckbox.pack(anchor='w')
        inputWidgets.append(self.noNumberCheckbox)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- 'Epigraph' entry.
        self.epigraphFrame = FoldingFrame(
            self.elementInfoWindow,
            _('Epigraph'),
            self._toggle_epigraph_window,
            )

        # Epigraph preview.
        self.epigraphPreviewVar = MyStringVar()
        epigraphPreview = ttk.Label(
            self.epigraphFrame.titleBar,
            textvariable=self.epigraphPreviewVar,
            )
        epigraphPreview.pack(side='left', padx=2)
        epigraphPreview.bind(
            '<Button-1>',
            self._toggle_epigraph_window
            )

        self.epigraphEntry = TextBox(self.epigraphFrame,
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
        self.epigraphEntry.pack(fill='x')
        inputWidgets.append(self.epigraphEntry)

        #--- 'Epigraph source' entry.
        self.epigraphSrcVar = MyStringVar()
        self._epigraphSrcEntry = LabelEntry(
            self.epigraphFrame,
            text=_('Source'),
            textvariable=self.epigraphSrcVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._epigraphSrcEntry.pack(anchor='w')
        inputWidgets.append(self._epigraphSrcEntry)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

        self._prefsShowLinks = 'show_ch_links'

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _toggle_epigraph_window(self, event=None):
        """Hide/show the 'Epigraph' textbox."""
        if prefs['show_ch_epigraph']:
            self.epigraphFrame.hide()
            prefs['show_ch_epigraph'] = False
        else:
            self.epigraphFrame.show()
            prefs['show_ch_epigraph'] = True
        self.toggle_folding_frame()
        self.set_data(self.elementId)

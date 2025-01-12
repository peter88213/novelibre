"""Provide a class for viewing and editing character properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.widgets.folding_frame import FoldingFrame
from mvclib.widgets.label_entry import LabelEntry
from mvclib.widgets.my_string_var import MyStringVar
from mvclib.widgets.text_box import TextBox
from nvlib.gui.properties_window.character_view_ctrl import CharacterViewCtrl
from nvlib.gui.properties_window.world_element_view import WorldElementView
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class CharacterView(WorldElementView, CharacterViewCtrl):
    """Class for viewing and editing character properties.

    Adds to the right pane:
    - A "Full name" entry.
    - A "Bio" folding frame.
    - A "Goals" folding frame.
    """
    _LBL_X = 15
    # Width of left-placed labels.

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- 'Full name' entry.
        self.fullNameVar = MyStringVar()
        self._fullNameEntry = LabelEntry(
            self._fullNameFrame,
            text=_('Full name'),
            textvariable=self.fullNameVar,
            command=self.apply_changes,
            lblWidth=self._LBL_X
            )
        self._fullNameEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._fullNameEntry)

        #--- Character status checkbox.
        self.isMajorVar = tk.BooleanVar()
        self._isMajorCheckbox = ttk.Checkbutton(
            self.elementInfoWindow,
            text=_('Major Character'),
            variable=self.isMajorVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._isMajorCheckbox.pack(anchor='w')
        inputWidgets.append(self._isMajorCheckbox)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- 'Bio' frame
        self.bioFrame = FoldingFrame(self.elementInfoWindow, '', self._toggle_bio_window)

        self.birthDateVar = MyStringVar()
        self._birthDateEntry = LabelEntry(
            self.bioFrame,
            text=_('Birth date'),
            textvariable=self.birthDateVar,
            command=self.apply_changes,
            lblWidth=self._LBL_X
            )
        self._birthDateEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._birthDateEntry)

        self.deathDateVar = MyStringVar()
        self._deathDateEntry = LabelEntry(
            self.bioFrame,
            text=_('Death date'),
            textvariable=self.deathDateVar,
            command=self.apply_changes,
            lblWidth=self._LBL_X
            )
        self._deathDateEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._deathDateEntry)

        self.bioEntry = TextBox(self.bioFrame,
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
        self.bioEntry.pack(fill='x')
        inputWidgets.append(self.bioEntry)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- 'Goals' entry.
        self.goalsFrame = FoldingFrame(self.elementInfoWindow, '', self._toggle_goals_window)
        self.goalsEntry = TextBox(self.goalsFrame,
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
        self.goalsEntry.pack(fill='x')
        inputWidgets.append(self.goalsEntry)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

        self.prefsShowLinks = 'show_cr_links'

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _toggle_bio_window(self, event=None):
        """Hide/show the 'Bio' textbox."""
        if prefs['show_cr_bio']:
            self.bioFrame.hide()
            prefs['show_cr_bio'] = False
        else:
            self.bioFrame.show()
            prefs['show_cr_bio'] = True
        self.scrollWindow.adjust_scrollbar()

    def _toggle_goals_window(self, event=None):
        """Hide/show the 'Goals' textbox."""
        if prefs['show_cr_goals']:
            self.goalsFrame.hide()
            prefs['show_cr_goals'] = False
        else:
            self.goalsFrame.show()
            prefs['show_cr_goals'] = True
        self.scrollWindow.adjust_scrollbar()


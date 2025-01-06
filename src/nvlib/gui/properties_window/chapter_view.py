"""Provide a class for viewing and editing chapter properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.basic_view import BasicView
from nvlib.gui.properties_window.chapter_view_ctrl import ChapterViewCtrl
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

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

        self.prefsShowLinks = 'show_ch_links'

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()


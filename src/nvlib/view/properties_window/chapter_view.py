"""Provide a class for viewing and editing chapter properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.controller.properties_window.chapter_view_ctrl import ChapterViewCtrl
from nvlib.novx_globals import _
from nvlib.view.properties_window.basic_view import BasicView
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
        self._isUnused = tk.BooleanVar()
        self._isUnusedCheckbox = ttk.Checkbutton(
            self.elementInfoWindow,
            text=_('Unused'),
            variable=self._isUnused,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._isUnusedCheckbox.pack(anchor='w')
        inputWidgets.append(self._isUnusedCheckbox)

        #--- 'Do not auto-number...' checkbox.
        self._noNumber = tk.BooleanVar()
        self._noNumberCheckbox = ttk.Checkbutton(
            self.elementInfoWindow,
            variable=self._noNumber,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._noNumberCheckbox.pack(anchor='w')
        inputWidgets.append(self._noNumberCheckbox)

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


"""Provide a class for viewing and editing plot points.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.controller.properties_window.plot_point_view_ctrl import PlotPointViewCtrl
from nvlib.novx_globals import _
from nvlib.view.properties_window.basic_view import BasicView
import tkinter as tk


class PlotPointView(BasicView, PlotPointViewCtrl):
    """Class for viewing and editing plot points.

    Adds to the right pane:
    - A label showing section associated with the turnong point. 
    - A button bar for managing the section assignments.
    """

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        self._lastSelected = ''
        self._treeSelectBinding = None
        self._uiEscBinding = None

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        # Associated section display.
        self._sectionFrame = ttk.Frame(self.elementInfoWindow)
        self._sectionFrame.pack(anchor='w', fill='x')
        ttk.Label(self._sectionFrame, text=f"{_('Section')}:").pack(anchor='w')
        self.sectionAssocTitle = tk.Label(self._sectionFrame, anchor='w', bg='white')
        self.sectionAssocTitle.pack(anchor='w', pady=2, fill='x')

        self._assignSectionButton = ttk.Button(self._sectionFrame, text=_('Assign section'), command=self._pick_section)
        self._assignSectionButton.pack(side='left', fill='x', expand=True)
        inputWidgets.append(self._assignSectionButton)

        self._clearAssignmentButton = ttk.Button(self._sectionFrame, text=_('Clear assignment'), command=self._clear_assignment)
        self._clearAssignmentButton.pack(side='left', fill='x', expand=True)
        inputWidgets.append(self._clearAssignmentButton)

        ttk.Button(self._sectionFrame, text=_('Go to section'), command=self._select_assigned_section).pack(side='left', fill='x', expand=True)

        for widget in inputWidgets:
            self.inputWidgets.append(widget)

        self._prefsShowLinks = 'show_pp_links'

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()


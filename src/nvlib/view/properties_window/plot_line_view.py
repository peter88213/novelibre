"""Provide a class for viewing and editing plot line properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.widgets.label_entry import LabelEntry
from mvclib.widgets.my_string_var import MyStringVar
from nvlib.controller.properties_window.plot_line_view_ctrl import PlotLineViewCtrl
from nvlib.novx_globals import _
from nvlib.view.properties_window.basic_view import BasicView


class PlotLineView(BasicView, PlotLineViewCtrl):
    """Class for viewing and editing plot line properties.
    
    Adds to the right pane:
    - A "Short name" entry.
    - The number of normal sections assigned to this arc.
    - A button to remove all section assigments to this arc.
    """

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        self._lastSelected = ''

        # 'Short name' entry.
        self.shortNameVar = MyStringVar()
        self._shortNameEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('Short name'),
            textvariable=self.shortNameVar,
            command=self.get_data,
            lblWidth=22
            )
        self._shortNameEntry.pack(anchor='w')
        inputWidgets.append(self._shortNameEntry)

        # Frame for plot line specific widgets.
        self.plotFrame = ttk.Frame(self._elementInfoWindow)
        self.plotFrame.pack(fill='x')
        self._nrSections = ttk.Label(self.plotFrame)
        self._nrSections.pack(side='left')
        self._clearButton = ttk.Button(self.plotFrame, text=_('Clear section assignments'), command=self._remove_sections)
        self._clearButton.pack(padx=1, pady=2)
        inputWidgets.append(self._clearButton)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.get_data)
            self.inputWidgets.append(widget)

        self.prefsShowLinks = 'show_pl_links'

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()


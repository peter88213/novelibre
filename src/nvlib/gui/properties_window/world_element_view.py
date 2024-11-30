"""Provide an abstract class for viewing world element properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.widgets.label_entry import LabelEntry
from mvclib.widgets.my_string_var import MyStringVar
from nvlib.novx_globals import _
from nvlib.gui.properties_window.basic_view import BasicView


class WorldElementView(BasicView):
    """Class for viewing world element properties.
    
    Adds to the right pane:
    - An "Aka" entry.
    - A "Tags" entry.   
    """

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        self._fullNameFrame = ttk.Frame(self.elementInfoWindow)
        self._fullNameFrame.pack(anchor='w', fill='x')

        # 'AKA' entry.
        self.akaVar = MyStringVar()
        self._akaEntry = LabelEntry(
            self.elementInfoWindow,
            text=_('AKA'),
            textvariable=self.akaVar,
            command=self.apply_changes,
            lblWidth=self._LBL_X
            )
        self._akaEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._akaEntry)

        # 'Tags' entry.
        self.tagsVar = MyStringVar()
        self._tagsEntry = LabelEntry(
            self.elementInfoWindow,
            text=_('Tags'),
            textvariable=self.tagsVar,
            command=self.apply_changes,
            lblWidth=self._LBL_X
            )
        self._tagsEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._tagsEntry)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()


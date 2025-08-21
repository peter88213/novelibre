"""Provide an abstract class for viewing world element properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.element_view import ElementView
from nvlib.gui.widgets.label_entry import LabelEntry
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.novx_globals import list_to_string
from nvlib.novx_globals import string_to_list
from nvlib.nv_locale import _


class WorldElementView(ElementView):
    """Class for viewing world element properties.
    
    Adds to the right pane:
    - An "Aka" entry.
    - A "Tags" entry.   
    """
    _HELP_PAGE = 'world_view.html'

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        self._fullNameFrame = ttk.Frame(self._elementInfoWindow)
        self._fullNameFrame.pack(anchor='w', fill='x')

        # 'AKA' entry.
        self._akaVar = MyStringVar()
        self._akaEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('AKA'),
            textvariable=self._akaVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._akaEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._akaEntry)

        # 'Tags' entry.
        self._tagsVar = MyStringVar()
        self._tagsEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('Tags'),
            textvariable=self._tagsVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._tagsEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._tagsEntry)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

    def apply_changes(self, event=None):
        """Apply changes of element title, description and notes."""
        if self.element is None:
            return

        super().apply_changes()

        # 'AKA' entry.
        self.element.aka = self._akaVar.get()

        # 'Tags' entry.
        self.element.tags = string_to_list(self._tagsVar.get())

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass method.
        """
        super().set_data(elementId)

        # 'AKA' entry.
        self._akaVar.set(self.element.aka)

        # 'Tags' entry.
        self._tagsVar.set(list_to_string(self.element.tags))

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()


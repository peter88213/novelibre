"""Provide a class for viewing and editing chapter properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.view.properties_window.basic_view import BasicView
from novxlib.novx_globals import _
import tkinter as tk


class ChapterView(BasicView):
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

        # 'Do not auto-number...' checkbutton.
        self._noNumber = tk.BooleanVar()
        self._noNumberCheckbox = ttk.Checkbutton(
            self._elementInfoWindow,
            variable=self._noNumber,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        inputWidgets.append(self._noNumberCheckbox)

        #--- 'Unused' checkbox.
        self._isUnused = tk.BooleanVar()
        self._isUnusedCheckbox = ttk.Checkbutton(
            self._elementInfoWindow,
            text=_('Unused'),
            variable=self._isUnused,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        inputWidgets.append(self._isUnusedCheckbox)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self._inputWidgets.append(widget)

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self._element.isTrash:
            return

        super().apply_changes()

        #--- 'Unused section' checkbox.
        if self._isUnused.get():
            self._ctrl.set_type(1)
        else:
            self._ctrl.set_type(0)

        # 'Do not auto-number...' checkbutton.
        self._element.noNumber = self._noNumber.get()

    def set_data(self, elementId):
        """Update the view with element's data.
        
        - Hide the info window, if the chapter ist the "trash bin". 
        - Show/hide the "Do not auto-number" button, depending on the chapter type.       
        - Configure the "Do not auto-number" button, depending on the chapter level.       
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.chapters[elementId]
        super().set_data(elementId)

        # 'Unused' checkbox.
        if self._element.chType > 0:
            self._isUnused.set(True)
        else:
            self._isUnused.set(False)

        # 'Do not auto-number...' checkbutton.
        if self._element.noNumber:
            self._noNumber.set(True)
        else:
            self._noNumber.set(False)

        # Hide properties, if the Chapter is the "trasch bin".
        if self._element.isTrash:
            self._elementInfoWindow.pack_forget()
            return

        if not self._elementInfoWindow.winfo_manager():
            self._elementInfoWindow.pack(fill='x')

        if not self._isUnusedCheckbox.winfo_manager():
            self._isUnusedCheckbox.pack(anchor='w')

        if self._element.chType == 0:
            if self._element.chLevel == 1:
                labelText = _('Do not auto-number this part')
            else:
                labelText = _('Do not auto-number this chapter')
            self._noNumberCheckbox.configure(text=labelText)
            if not self._noNumberCheckbox.winfo_manager():
                self._noNumberCheckbox.pack(anchor='w')
        else:
            if self._noNumberCheckbox.winfo_manager():
                self._noNumberCheckbox.pack_forget()

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_button_bar()


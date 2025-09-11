"""Provide a class for viewing and editing chapter properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.element_view import ElementView
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

        #--- 'Has epigraph' checkbox.
        self._hasEpigraphVar = tk.BooleanVar()
        self._hasEpigraphCheckbox = ttk.Checkbutton(
            self._elementInfoWindow,
            text=_('The first section is an epigraph'),
            variable=self._hasEpigraphVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._hasEpigraphCheckbox.pack(anchor='w')
        inputWidgets.append(self._hasEpigraphCheckbox)

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

        #--- "Has epigraph" checkbox.
        self.element.hasEpigraph = self._hasEpigraphVar.get()

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

        #--- "Has epigraph" checkbox.
        self._hasEpigraphVar.set(self.element.hasEpigraph)

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()


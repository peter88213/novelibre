"""Provide a class for viewing and editing plot line properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.view.properties_window.basic_view import BasicView
from nvlib.widgets.label_entry import LabelEntry
from nvlib.widgets.my_string_var import MyStringVar
from novxlib.novx_globals import _


class PlotLineView(BasicView):
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
        self._shortName = MyStringVar()
        self._shortNameEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('Short name'),
            textvariable=self._shortName,
            command=self.apply_changes,
            lblWidth=22
            )
        self._shortNameEntry.pack(anchor='w')
        inputWidgets.append(self._shortNameEntry)

        # Frame for plot line specific widgets.
        self._arcFrame = ttk.Frame(self._elementInfoWindow)
        self._arcFrame.pack(fill='x')
        self._nrSections = ttk.Label(self._arcFrame)
        self._nrSections.pack(side='left')
        self._clearButton = ttk.Button(self._arcFrame, text=_('Clear section assignments'), command=self._remove_sections)
        self._clearButton.pack(padx=1, pady=2)
        inputWidgets.append(self._clearButton)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self._inputWidgets.append(widget)

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        super().apply_changes()

        # 'Short name' entry.
        self._element.shortName = self._shortName.get()

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.plotLines[elementId]
        super().set_data(elementId)

        # 'Plot line name' entry.
        self._shortName.set(self._element.shortName)

        # Frame for plot line specific widgets.
        if self._element.sections is not None:
            self._nrSections['text'] = f'{_("Number of sections")}: {len(self._element.sections)}'

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_button_bar()

    def _remove_sections(self):
        """Remove all section references.
        
        Remove also all section associations from the children points.
        """
        if self._ui.ask_yes_no(f'{_("Remove all sections from the plot line")} "{self._element.shortName}"?'):
            # Remove section back references.
            if self._element.sections:
                self.doNotUpdate = True
                for scId in self._element.sections:
                    self._mdl.novel.sections[scId].scPlotLines.remove(self._elementId)
                for ppId in self._mdl.novel.tree.get_children(self._elementId):
                    scId = self._mdl.novel.plotPoints[ppId].sectionAssoc
                    if scId is not None:
                        del(self._mdl.novel.sections[scId].scPlotPoints[ppId])
                        self._mdl.novel.plotPoints[ppId].sectionAssoc = None
                self._element.sections = []
                self.set_data(self._elementId)
                self.doNotUpdate = False


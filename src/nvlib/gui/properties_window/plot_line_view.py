"""Provide a class for viewing and editing plot line properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.basic_view import BasicView
from nvlib.gui.widgets.label_entry import LabelEntry
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.nv_locale import _


class PlotLineView(BasicView):
    """Class for viewing and editing plot line properties.
    
    Adds to the right pane:
    - A "Short name" entry.
    - The number of normal sections assigned to this arc.
    - A button to remove all section assigments to this arc.
    """
    _LABEL_WIDTH = 22
    # Width of left-placed labels.

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        # 'Short name' entry.
        self._shortNameVar = MyStringVar()
        self._shortNameEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('Short name'),
            textvariable=self._shortNameVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._shortNameEntry.pack(anchor='w')
        inputWidgets.append(self._shortNameEntry)

        # Frame for plot line specific widgets.
        self._plotFrame = ttk.Frame(self._elementInfoWindow)
        self._plotFrame.pack(fill='x')
        self._nrSectionsView = ttk.Label(
            self._plotFrame,
        )
        self._nrSectionsView.pack(side='left')
        self._clearButton = ttk.Button(
            self._plotFrame,
            text=_('Clear section assignments'),
            command=self._remove_sections,
        )
        self._clearButton.pack(padx=1, pady=2)
        inputWidgets.append(self._clearButton)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

        self._prefsShowLinks = 'show_pl_links'

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        super().apply_changes()

        # 'Short name' entry.
        self.element.shortName = self._shortNameVar.get()

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.plotLines[elementId]
        super().set_data(elementId)

        # 'Plot line name' entry.
        self._shortNameVar.set(self.element.shortName)

        # Frame for plot line specific widgets.
        if self.element.sections is not None:
            i = 0
            for scId in self.element.sections:
                if self._mdl.novel.sections[scId].scType == 0:
                    i += 1
            self._nrSectionsView['text'] = f'{_("Number of sections")}: {i}'

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _remove_sections(self):
        # Remove all section references.
        # Remove also all section associations from the children points.
        if self._ui.ask_yes_no(
            message=_('Remove all sections from the plot line?'),
            detail=f'({self.element.shortName}) {self.element.title}'
        ):
            # Remove section back references.
            if self.element.sections:
                self._doNotUpdate = True
                for scId in self.element.sections:
                    self._mdl.novel.sections[scId].scPlotLines.remove(self.elementId)
                for ppId in self._mdl.novel.tree.get_children(self.elementId):
                    scId = self._mdl.novel.plotPoints[ppId].sectionAssoc
                    if scId is not None:
                        del(self._mdl.novel.sections[scId].scPlotPoints[ppId])
                        self._mdl.novel.plotPoints[ppId].sectionAssoc = None
                self.element.sections = []
                self.set_data(self.elementId)
                self._doNotUpdate = False


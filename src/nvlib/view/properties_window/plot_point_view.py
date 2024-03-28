"""Provide a class for viewing and editing plot points.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.view.properties_window.basic_view import BasicView
from novxlib.novx_globals import CH_ROOT
from novxlib.novx_globals import SECTION_PREFIX
from novxlib.novx_globals import _
import tkinter as tk


class TurningPointView(BasicView):
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

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

        # Associated section display.
        self._sectionFrame = ttk.Frame(self._elementInfoWindow)
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
            self._inputWidgets.append(widget)

        self._prefsShowLinks = 'show_pp_links'

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.plotPoints[elementId]
        super().set_data(elementId)

        # Associated section display.
        try:
            sectionTitle = self._mdl.novel.sections[self._element.sectionAssoc].title
        except:
            sectionTitle = ''
        self.sectionAssocTitle['text'] = sectionTitle

    def _assign_section(self, event=None):
        """Associate the selected section with the Plot point.
        
        End the picking mode after the section is assigned.
        """
        nodeId = self._ui.tv.tree.selection()[0]
        if nodeId.startswith(SECTION_PREFIX):
            if self._mdl.novel.sections[nodeId].scType == 0:
                self._clear_assignment()
                # Associate the point with the section.
                plId = self._ui.tv.tree.parent(self._elementId)
                arcSections = self._mdl.novel.plotLines[plId].sections
                if arcSections is None:
                    arcSections = [nodeId]
                elif not nodeId in arcSections:
                    arcSections.append(nodeId)
                self._mdl.novel.plotLines[plId].sections = arcSections
                self._mdl.novel.sections[nodeId].scPlotPoints[self._elementId] = plId
                if not plId in self._mdl.novel.sections[nodeId].scPlotLines:
                    self._mdl.novel.sections[nodeId].scPlotLines.append(plId)
                self._element.sectionAssoc = nodeId
        self._end_picking_mode()

    def _clear_assignment(self):
        """Unassign a section from the Plot point."""
        scId = self._element.sectionAssoc
        if scId is not None:
            del(self._mdl.novel.sections[scId].scPlotPoints[self._elementId])
            self._element.sectionAssoc = None

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _select_assigned_section(self):
        """Select the section assigned to the plot point."""
        if self._element.sectionAssoc is not None:
            targetNode = self._element.sectionAssoc
            self._ui.tv.tree.see(targetNode)
            self._ui.tv.tree.selection_set(targetNode)

    def _pick_section(self):
        """Enter the "associate section" selection mode."""
        self._start_picking_mode()
        self._ui.tv.tree.bind('<<TreeviewSelect>>', self._assign_section)
        self._ui.tv.tree.see(CH_ROOT)


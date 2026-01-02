"""Provide a class for viewing and editing plot points.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.element_view import ElementView
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class PlotPointView(ElementView):
    """Class for viewing and editing plot points.

    Adds to the right pane:
    - A label showing section associated with the turnong point. 
    - A button bar for managing the section assignments.
    """
    _HELP_PAGE = 'point_view.html'

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal'
        ).pack(fill='x')

        # Associated section display.
        self._sectionFrame = ttk.Frame(self._elementInfoWindow)
        self._sectionFrame.pack(anchor='w', fill='x')
        ttk.Label(
            self._sectionFrame,
            text=f"{_('Section')}:"
        ).pack(anchor='w')
        self._sectionAssocTitle = tk.Label(
            self._sectionFrame,
            anchor='w',
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
        )
        self._sectionAssocTitle.pack(anchor='w', pady=2, fill='x')

        self._assignSectionButton = ttk.Button(
            self._sectionFrame,
            text=_('Assign section'),
            command=self.pick_section,
        )
        self._assignSectionButton.pack(side='left', fill='x', expand=True)
        inputWidgets.append(self._assignSectionButton)

        self._clearAssignmentButton = ttk.Button(
            self._sectionFrame,
            text=_('Clear assignment'),
            command=self.clear_assignment,
        )
        self._clearAssignmentButton.pack(side='left', fill='x', expand=True)
        inputWidgets.append(self._clearAssignmentButton)

        ttk.Button(
            self._sectionFrame,
            text=_('Go to section'),
            command=self.go_to_assigned_section).pack(
                side='left',
                fill='x',
                expand=True)

        for widget in inputWidgets:
            self.inputWidgets.append(widget)

        self._prefsShowLinks = 'show_pp_links'

    def clear_assignment(self):
        """Unassign a section from the Plot point."""
        scId = self.element.sectionAssoc
        if scId is not None:
            del(self._mdl.novel.sections[scId].scPlotPoints[self.elementId])
            self.element.sectionAssoc = None

    def go_to_assigned_section(self):
        """Select the section assigned to the plot point."""
        if self.element.sectionAssoc is not None:
            targetNode = self.element.sectionAssoc
            self._ui.tv.see_node(targetNode)
            self._ui.tv.tree.selection_set(targetNode)

    def pick_section(self):
        """Enter the "associate section" selection mode."""
        self._ui.tv.save_branch_status()
        self._ui.tv.close_children('')
        self._ui.tv.open_children(CH_ROOT)
        self._start_picking_mode(command=self._assign_section)
        self._ui.tv.see_node(CH_ROOT)

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.plotPoints[elementId]
        super().set_data(elementId)

        # Associated section display.
        try:
            sectionTitle = (
                self._mdl.novel.sections[self.element.sectionAssoc].title
            )
        except:
            sectionTitle = ''
        self._sectionAssocTitle['text'] = sectionTitle

    def _assign_section(self, event=None):
        # Associate the selected section with the Plot point.
        # End the picking mode after the section is assigned.
        nodeId = self._ui.tv.tree.selection()[0]
        if nodeId.startswith(SECTION_PREFIX):
            if self._mdl.novel.sections[nodeId].scType == 0:
                self.clear_assignment()
                # Associate the point with the section.
                plId = self._ui.tv.tree.parent(self.elementId)
                arcSections = self._mdl.novel.plotLines[plId].sections
                if arcSections is None:
                    arcSections = [nodeId]
                elif not nodeId in arcSections:
                    arcSections.append(nodeId)
                self._mdl.novel.plotLines[plId].sections = arcSections
                self._mdl.novel.sections[
                    nodeId].scPlotPoints[self.elementId] = plId
                if not plId in self._mdl.novel.sections[nodeId].scPlotLines:
                    self._mdl.novel.sections[nodeId].scPlotLines.append(plId)
                self.element.sectionAssoc = nodeId
        self._ui.tv.restore_branch_status()

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()


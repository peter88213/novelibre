"""Provide a class for viewing and editing plot points.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.element_view import ElementView
from nvlib.gui.widgets.folding_frame import FoldingFrame
from nvlib.gui.widgets.text_box import TextBox
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

        # Assigned section display.
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

        buttonBar1 = ttk.Frame(self._sectionFrame)
        buttonBar1.pack(pady=2, fill='x', expand=True)

        self._assignSectionButton = ttk.Button(
            buttonBar1,
            text=_('Assign section'),
            command=self.pick_section,
        )
        self._assignSectionButton.pack(side='left', fill='x', expand=True)
        inputWidgets.append(self._assignSectionButton)

        self._clearAssignmentButton = ttk.Button(
            buttonBar1,
            text=_('Clear assignment'),
            command=self.clear_assignment,
        )
        self._clearAssignmentButton.pack(side='left', fill='x', expand=True)
        inputWidgets.append(self._clearAssignmentButton)

        ttk.Button(
            buttonBar1,
            text=_('Go to section'),
            command=self.go_to_assigned_section).pack(
                side='left',
                fill='x',
                expand=True,
            )

        # Frame for the plot line notes of the assigned section.
        self._notesFrame = FoldingFrame(
            self._sectionFrame,
            _("The assigned section's plot line notes"),
            self._toggle_notes_frame,
        )

        self._plotNotesWindow = TextBox(
            self._notesFrame,
            wrap='word',
            height=self._indexCard.bodyBox['height'],
            padx=5,
            pady=5,
            bg=prefs['color_inactive_bg'],
            fg=prefs['color_text_fg'],
        )
        self._plotNotesWindow.pack(fill='x')

        buttonBar2 = ttk.Frame(self._notesFrame)
        buttonBar2.pack(pady=2, fill='x', expand=True)

        self._submitNotesButton = ttk.Button(
            buttonBar2,
            text=_('Replace this with the plot point description'),
            command=self._submit_plotline_notes,
        )
        self._submitNotesButton.pack(fill='x', expand=True)
        inputWidgets.append(self._submitNotesButton)

        self._adoptNotesButton = ttk.Button(
            buttonBar2,
            text=_('Replace the plot point description with this'),
            command=self._adopt_plotline_notes,
        )
        self._adoptNotesButton.pack(fill='x', expand=True)
        inputWidgets.append(self._adoptNotesButton)

        for widget in inputWidgets:
            self.inputWidgets.append(widget)

        self._prefsShowLinks = 'show_pp_links'

    def clear_assignment(self):
        """Unassign a section from the Plot point."""
        scId = self.element.sectionAssoc
        if scId is not None:
            del(self._mdl.novel.sections[scId].scPlotPoints[self.elementId])
            self.element.sectionAssoc = None

    def configure_display(self):
        """Expand or collapse the property frames."""
        super().configure_display()
        if prefs['show_plotline_notes']:
            self._notesFrame.show()
        else:
            self._notesFrame.hide()

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

        # Assigned section display.
        scId = self.element.sectionAssoc
        self._plotNotesWindow.config(state='normal')
        try:
            associatedSection = self._mdl.novel.sections[scId]
        except:
            sectionTitle = ''
            self._plotNotesWindow.clear()
        else:
            sectionTitle = associatedSection.title or ''
            plId = self._ui.tv.tree.parent(self.elementId)
            plotlineNotes = self._mdl.novel.sections[scId].plotlineNotes.get(plId, None)
            if plotlineNotes is None:
                self._plotNotesWindow.clear()
            else:
                self._plotNotesWindow.set_text(plotlineNotes)
        self._plotNotesWindow.config(state='disabled')
        self._sectionAssocTitle['text'] = sectionTitle

    def _adopt_plotline_notes(self):
        scId = self.element.sectionAssoc
        if scId is None:
            return

        plId = self._ui.tv.tree.parent(self.elementId)
        plotlineNotes = self._mdl.novel.sections[scId].plotlineNotes.get(plId, None)
        if plotlineNotes is not None:
            self.element.desc = plotlineNotes

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

                # Reuse existing plot line notes or plot point description.
                if not self._mdl.novel.sections[nodeId].plotlineNotes.get(plId, None):
                    self._submit_plotline_notes(plId)
                elif not self.element.desc:
                    self._adopt_plotline_notes(plId)

        self._ui.tv.restore_branch_status()

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._activate_color_field()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _submit_plotline_notes(self):
        if not self.element.desc:
            return

        scId = self.element.sectionAssoc
        if scId is None:
            return

        plotlineNotes = self._mdl.novel.sections[scId].plotlineNotes
        plId = self._ui.tv.tree.parent(self.elementId)
        plotlineNotes[plId] = self.element.desc
        self._mdl.novel.sections[scId].plotlineNotes = plotlineNotes

    def _toggle_notes_frame(self, event=None):
        # Hide/show the 'Plot line notes' frame.
        if prefs['show_plotline_notes']:
            self._notesFrame.hide()
            prefs['show_plotline_notes'] = False
        else:
            self._notesFrame.show()
            prefs['show_plotline_notes'] = True
        self._toggle_folding_frame()


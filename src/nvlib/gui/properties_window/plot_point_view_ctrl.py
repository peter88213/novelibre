"""Provide a mixin class for controlling the plot point properties view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.properties_window.basic_view_ctrl import BasicViewCtrl
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import SECTION_PREFIX


class PlotPointViewCtrl(BasicViewCtrl):

    def clear_assignment(self):
        """Unassign a section from the Plot point."""
        scId = self.element.sectionAssoc
        if scId is not None:
            del(self._mdl.novel.sections[scId].scPlotPoints[self._elementId])
            self.element.sectionAssoc = None

    def go_to_assigned_section(self):
        """Select the section assigned to the plot point."""
        if self.element.sectionAssoc is not None:
            targetNode = self.element.sectionAssoc
            self._ui.tv.see_node(targetNode)
            self._ui.tv.tree.selection_set(targetNode)

    def pick_section(self):
        """Enter the "associate section" selection mode."""
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
            sectionTitle = self._mdl.novel.sections[self.element.sectionAssoc].title
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
                self.clear_assignment()
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
                self.element.sectionAssoc = nodeId


"""Provide a mixin class for controlling the plot line properties view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.properties_window.basic_view_ctrl import BasicViewCtrl
from nvlib.novx_globals import _


class PlotLineViewCtrl(BasicViewCtrl):
    """Class for viewing and editing plot line properties.
    
    Adds to the right pane:
    - A "Short name" entry.
    - The number of normal sections assigned to this arc.
    - A button to remove all section assigments to this arc.
    """

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        super().apply_changes()

        # 'Short name' entry.
        self.element.shortName = self.shortNameVar.get()

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.plotLines[elementId]
        super().set_data(elementId)

        # 'Plot line name' entry.
        self.shortNameVar.set(self.element.shortName)

        # Frame for plot line specific widgets.
        if self.element.sections is not None:
            self.nrSectionsView['text'] = f'{_("Number of sections")}: {len(self.element.sections)}'

    def _remove_sections(self):
        """Remove all section references.
        
        Remove also all section associations from the children points.
        """
        if self._ui.ask_yes_no(f'{_("Remove all sections from the plot line")} "{self.element.shortName}"?'):
            # Remove section back references.
            if self.element.sections:
                self.doNotUpdate = True
                for scId in self.element.sections:
                    self._mdl.novel.sections[scId].scPlotLines.remove(self._elementId)
                for ppId in self._mdl.novel.tree.get_children(self._elementId):
                    scId = self._mdl.novel.plotPoints[ppId].sectionAssoc
                    if scId is not None:
                        del(self._mdl.novel.sections[scId].scPlotPoints[ppId])
                        self._mdl.novel.plotPoints[ppId].sectionAssoc = None
                self.element.sections = []
                self.set_data(self._elementId)
                self.doNotUpdate = False


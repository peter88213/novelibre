"""Provide a mixin class for controlling the chapter properties view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.properties_window.basic_view_ctrl import BasicViewCtrl
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class ChapterViewCtrl(BasicViewCtrl):
    """Class for viewing and editing chapter properties.
      
    Adds to the right pane:
    - A "Do not auto-number" checkbox.
    """

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        if self.element.isTrash:
            return

        super().apply_changes()

        #--- 'Unused' checkbox.
        if self.isUnusedVar.get():
            self._ctrl.set_type_unused()
        else:
            self._ctrl.set_type_normal()

        #--- 'Do not auto-number...' checkbox.
        self.element.noNumber = self.noNumberVar.get()

        #--- 'Epigraph' entry.
        if self.epigraphEntry.hasChanged:
            self.element.epigraph = self.epigraphEntry.get_text()

    def set_data(self, elementId):
        """Update the view with element's data.
        
        - Configure the "Do not auto-number" button, depending on the chapter level.       
        Extends the superclass constructor.
        """
        self.element = self._mdl.novel.chapters[elementId]
        super().set_data(elementId)

        #--- 'Unused' checkbox.
        if self.element.chType > 0:
            self.isUnusedVar.set(True)
        else:
            self.isUnusedVar.set(False)

        #--- 'Do not auto-number...' checkbox.
        if self.element.chLevel == 1:
            labelText = _('Do not auto-number this part')
        else:
            labelText = _('Do not auto-number this chapter')
        self.noNumberCheckbox.configure(text=labelText)
        self.noNumberVar.set(self.element.noNumber)

        #--- 'Epigraph' entry.
        if prefs['show_ch_epigraph']:
            self.epigraphFrame.show()
        else:
            self.epigraphFrame.hide()
        self.epigraphEntry.set_text(self.element.epigraph)


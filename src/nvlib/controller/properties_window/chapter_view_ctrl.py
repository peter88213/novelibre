"""Provide a mixin class for controlling the chapter properties view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.properties_window.basic_view_ctrl import BasicViewCtrl
from nvlib.novx_globals import _


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
        if self._isUnused.get():
            self._ctrl.set_type(1, [self.elementId])
        else:
            self._ctrl.set_type(0, [self.elementId])

        #--- 'Do not auto-number...' checkbox.
        self.element.noNumber = self._noNumber.get()

    def set_data(self, elementId):
        """Update the view with element's data.
        
        - Configure the "Do not auto-number" button, depending on the chapter level.       
        Extends the superclass constructor.
        """
        self.element = self._mdl.novel.chapters[elementId]
        super().set_data(elementId)

        #--- 'Unused' checkbox.
        if self.element.chType > 0:
            self._isUnused.set(True)
        else:
            self._isUnused.set(False)

        #--- 'Do not auto-number...' checkbox.
        if self.element.chLevel == 1:
            labelText = _('Do not auto-number this part')
        else:
            labelText = _('Do not auto-number this chapter')
        self._noNumberCheckbox.configure(text=labelText)
        if self.element.noNumber:
            self._noNumber.set(True)
        else:
            self._noNumber.set(False)


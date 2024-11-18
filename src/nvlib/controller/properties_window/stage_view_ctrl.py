"""Provide a mixin class for controlling the stage properties view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.properties_window.basic_view_ctrl import BasicViewCtrl


class StageViewCtrl(BasicViewCtrl):

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.sections[elementId]
        super().set_data(elementId)


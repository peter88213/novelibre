"""Provide a mixin class for controlling the world element properties view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod

from nvlib.controller.properties_window.basic_view_ctrl import BasicViewCtrl
from nvlib.novx_globals import list_to_string
from nvlib.novx_globals import string_to_list


class WorldElementViewCtrl(BasicViewCtrl, ABC):

    def apply_changes(self, event=None):
        """Apply changes of element title, description and notes."""
        if self.element is None:
            return

        super().apply_changes()

        # 'AKA' entry.
        self.element.aka = self.akaVar.get()

        # 'Tags' entry.
        newTags = self.tagsVar.get()
        self.element.tags = string_to_list(newTags)

    @abstractmethod
    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass method.
        """
        super().set_data(elementId)

        # 'AKA' entry.
        self.akaVar.set(self.element.aka)

        # 'Tags' entry.
        if self.element.tags is not None:
            self._tagsStr = list_to_string(self.element.tags)
        else:
            self._tagsStr = ''
        self.tagsVar.set(self._tagsStr)


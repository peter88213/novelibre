"""Provide a generic class for novelibre story world element representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.basic_element_tags import BasicElementTags


class WorldElement(BasicElementTags):
    """Story world element representation (may be location or item)."""

    def __init__(
        self,
        aka=None,
        **kwargs
    ):
        """Extends the superclass constructor"""
        super().__init__(**kwargs)
        self._aka = aka

    @property
    def aka(self):
        return self._aka

    @aka.setter
    def aka(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._aka != newVal:
            self._aka = newVal
            self.on_element_change()


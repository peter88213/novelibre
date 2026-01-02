"""Provide a class for a novelibre element with notes and tags.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.basic_element_notes import BasicElementNotes


class BasicElementTags(BasicElementNotes):
    """Basic element with notes and tags."""

    def __init__(
        self,
        tags=None,
        **kwargs
    ):
        """Extends the superclass constructor"""
        super().__init__(**kwargs)
        self._tags = tags

    @property
    def tags(self):
        # list of str
        return self._tags

    @tags.setter
    def tags(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) is str
        if self._tags != newVal:
            self._tags = newVal
            self.on_element_change()


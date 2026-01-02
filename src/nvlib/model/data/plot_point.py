"""Provide a class for novelibre plot point representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.basic_element_notes import BasicElementNotes


class PlotPoint(BasicElementNotes):
    """Plot point representation."""

    def __init__(
        self,
        sectionAssoc=None,
        **kwargs
    ):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)

        self._sectionAssoc = sectionAssoc

    @property
    def sectionAssoc(self):
        # str: ID of the associated section
        return self._sectionAssoc

    @sectionAssoc.setter
    def sectionAssoc(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._sectionAssoc != newVal:
            self._sectionAssoc = newVal
            self.on_element_change()


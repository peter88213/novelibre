"""Provide a class for novelibre chapter representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from nvlib.model.data.basic_element_notes import BasicElementNotes


class Chapter(BasicElementNotes):
    """novelibre chapter representation."""

    def __init__(
        self,
        chLevel=None,
        chType=None,
        noNumber=None,
        isTrash=None,
        hasEpigraph=None,
        **kwargs
    ):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)
        self._chLevel = chLevel
        self._chType = chType
        self._noNumber = noNumber
        self._isTrash = isTrash
        self._hasEpigraph = hasEpigraph

    @property
    def chLevel(self):
        # 1 = Part level.
        # 2 = Regular chapter level.
        return self._chLevel

    @chLevel.setter
    def chLevel(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._chLevel != newVal:
            self._chLevel = newVal
            self.on_element_change()

    @property
    def chType(self):
        # 0 = Normal.
        # 1 = Unused.
        return self._chType

    @chType.setter
    def chType(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._chType != newVal:
            self._chType = newVal
            self.on_element_change()

    @property
    def noNumber(self):
        # True: Exclude this chapter from auto-numbering.
        # False: Auto-number this chapter, if applicable.
        return self._noNumber

    @noNumber.setter
    def noNumber(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._noNumber != newVal:
            self._noNumber = newVal
            self.on_element_change()

    @property
    def isTrash(self):
        # True: This chapter is the novelibre project's "trash bin".
        # False: This is a chapter or part.
        return self._isTrash

    @isTrash.setter
    def isTrash(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._isTrash != newVal:
            self._isTrash = newVal
            self.on_element_change()

    @property
    def hasEpigraph(self):
        # True: The first section is an epigraph; its title is the source.
        # False: The first section is a regular one.
        return self._hasEpigraph

    @hasEpigraph.setter
    def hasEpigraph(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._hasEpigraph != newVal:
            self._hasEpigraph = newVal
            self.on_element_change()


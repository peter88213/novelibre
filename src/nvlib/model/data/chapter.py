"""Provide a class for novelibre chapter representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.basic_element_notes import BasicElementNotes


class Chapter(BasicElementNotes):
    """novelibre chapter representation."""

    def __init__(self,
            chLevel=None,
            chType=None,
            noNumber=None,
            isTrash=None,
            **kwargs):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)
        self._chLevel = chLevel
        self._chType = chType
        self._noNumber = noNumber
        self._isTrash = isTrash

    @property
    def chLevel(self):
        # 1 = Part level.
        # 2 = Regular chapter level.
        return self._chLevel

    @chLevel.setter
    def chLevel(self, newVal):
        if newVal is not None:
            assert type(newVal) == int
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
            assert type(newVal) == int
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
            assert type(newVal) == bool
        if self._noNumber != newVal:
            self._noNumber = newVal
            self.on_element_change()

    @property
    def isTrash(self):
        # True: This chapter is the novelibre project's "trash bin"
        # False: This is a chapter or part.
        return self._isTrash

    @isTrash.setter
    def isTrash(self, newVal):
        if newVal is not None:
            assert type(newVal) == bool
        if self._isTrash != newVal:
            self._isTrash = newVal
            self.on_element_change()

    def from_xml(self, xmlElement):
        super().from_xml(xmlElement)
        typeStr = xmlElement.get('type', '0')
        if typeStr in ('0', '1'):
            self.chType = int(typeStr)
        else:
            self.chType = 1
        chLevel = xmlElement.get('level', None)
        if chLevel == '1':
            self.chLevel = 1
        else:
            self.chLevel = 2
        self.isTrash = xmlElement.get('isTrash', None) == '1'
        self.noNumber = xmlElement.get('noNumber', None) == '1'

    def to_xml(self, xmlElement):
        super().to_xml(xmlElement)
        if self.chType:
            xmlElement.set('type', str(self.chType))
        if self.chLevel == 1:
            xmlElement.set('level', '1')
        if self.isTrash:
            xmlElement.set('isTrash', '1')
        if self.noNumber:
            xmlElement.set('noNumber', '1')

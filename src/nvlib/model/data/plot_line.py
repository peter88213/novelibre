"""Provide a class for novelibre plot line representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.basic_element_notes import BasicElementNotes
from nvlib.novx_globals import string_to_list
import xml.etree.ElementTree as ET


class PlotLine(BasicElementNotes):
    """Plot line representation."""

    def __init__(self,
            shortName=None,
            sections=None,
            **kwargs):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)

        self._shortName = shortName
        self._sections = sections

    @property
    def shortName(self):
        # str: name of the plot line
        return self._shortName

    @shortName.setter
    def shortName(self, newVal):
        if newVal is not None:
            assert type(newVal) == str
        if self._shortName != newVal:
            self._shortName = newVal
            self.on_element_change()

    @property
    def sections(self):
        # List of str: IDs of the sections associated with the plot line.
        try:
            return self._sections[:]
        except TypeError:
            return None

    @sections.setter
    def sections(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) == str
        if self._sections != newVal:
            self._sections = newVal
            self.on_element_change()

    def from_xml(self, xmlElement):
        super().from_xml(xmlElement)
        self.shortName = self._get_element_text(xmlElement, 'ShortName')
        plSections = []
        xmlSections = xmlElement.find('Sections')
        if xmlSections is not None:
            scIds = xmlSections.get('ids', None)
            if scIds is not None:
                for scId in string_to_list(scIds, divider=' '):
                    plSections.append(scId)
        self.sections = plSections

    def to_xml(self, xmlElement):
        super().to_xml(xmlElement)
        if self.shortName:
            ET.SubElement(xmlElement, 'ShortName').text = self.shortName
        if self.sections:
            attrib = {'ids':' '.join(self.sections)}
            ET.SubElement(xmlElement, 'Sections', attrib=attrib)

"""Provide a class for novelibre plot line XML import and export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.novx.basic_element_notes_novx import BasicElementNotesNovx
from nvlib.novx_globals import string_to_list
import xml.etree.ElementTree as ET


class PlotLineNovx(BasicElementNotesNovx):
    """Plot line representation."""

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        element.shortName = self._get_element_text(xmlElement, 'ShortName')
        plSections = []
        xmlSections = xmlElement.find('Sections')
        if xmlSections is not None:
            scIds = xmlSections.get('ids', None)
            if scIds is not None:
                for scId in string_to_list(scIds, divider=' '):
                    plSections.append(scId)
        element.sections = plSections

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.shortName:
            ET.SubElement(xmlElement, 'ShortName').text = element.shortName
        if element.sections:
            attrib = {'ids':' '.join(element.sections)}
            ET.SubElement(xmlElement, 'Sections', attrib=attrib)

"""Provide a class for novelibre plot point XML import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.novx.basic_element_notes_novx import BasicElementNotesNovx
import xml.etree.ElementTree as ET


class PlotPointNovx(BasicElementNotesNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        xmlSectionAssoc = xmlElement.find('Section')
        if xmlSectionAssoc is not None:
            element.sectionAssoc = xmlSectionAssoc.get('id', None)

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.sectionAssoc:
            ET.SubElement(
                xmlElement,
                'Section',
                attrib={'id': element.sectionAssoc},
            )

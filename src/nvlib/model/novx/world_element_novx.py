"""Provide a class for novelibre story world element  XML import and export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.novx.basic_element_tags_novx import BasicElementTagsNovx
import xml.etree.ElementTree as ET


class WorldElementNovx(BasicElementTagsNovx):
    """Story world element representation (may be location or item)."""

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        element.aka = self._get_element_text(xmlElement, 'Aka')

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.aka:
            ET.SubElement(xmlElement, 'Aka').text = element.aka


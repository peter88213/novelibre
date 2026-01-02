"""Provide a class for a novelibre element XML import and export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.novx.basic_element_novx import BasicElementNovx


class BasicElementNotesNovx(BasicElementNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        element.notes = self._xml_element_to_text(xmlElement.find('Notes'))

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.notes:
            xmlElement.append(self._text_to_xml_element('Notes', element.notes))


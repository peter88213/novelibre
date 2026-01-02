"""Provide a class for novelibre element XML import and export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.novx.basic_element_notes_novx import BasicElementNotesNovx
from nvlib.novx_globals import list_to_string
from nvlib.novx_globals import string_to_list
import xml.etree.ElementTree as ET


class BasicElementTagsNovx(BasicElementNotesNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        tags = string_to_list(self._get_element_text(xmlElement, 'Tags'))
        strippedTags = []
        for tag in tags:
            strippedTags.append(tag.strip())
        element.tags = strippedTags

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        tagStr = list_to_string(element.tags)
        if tagStr:
            ET.SubElement(xmlElement, 'Tags').text = tagStr


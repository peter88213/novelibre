"""Provide a class for novelibre character XML import and export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.model.novx.world_element_novx import WorldElementNovx
import xml.etree.ElementTree as ET


class CharacterNovx(WorldElementNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        element.isMajor = xmlElement.get('major', None) == '1'
        element.fullName = self._get_element_text(xmlElement, 'FullName')
        element.bio = self._xml_element_to_text(xmlElement.find('Bio'))
        element.goals = self._xml_element_to_text(xmlElement.find('Goals'))
        element.birthDate = PyCalendar.verified_date(
            self._get_element_text(xmlElement, 'BirthDate')
        )
        element.deathDate = PyCalendar.verified_date(
            self._get_element_text(xmlElement, 'DeathDate')
        )

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.isMajor:
            xmlElement.set('major', '1')
        if element.fullName:
            ET.SubElement(xmlElement, 'FullName').text = element.fullName
        if element.bio:
            xmlElement.append(self._text_to_xml_element('Bio', element.bio))
        if element.goals:
            xmlElement.append(self._text_to_xml_element('Goals', element.goals))
        if element.birthDate:
            ET.SubElement(xmlElement, 'BirthDate').text = element.birthDate
        if element.deathDate:
            ET.SubElement(xmlElement, 'DeathDate').text = element.deathDate


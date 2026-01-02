"""Provide a class for novelibre section XML import and export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from nvlib.model.data.py_calendar import PyCalendar
from nvlib.model.novx.basic_element_tags_novx import BasicElementTagsNovx
from nvlib.novx_globals import string_to_list
from nvlib.novx_globals import verified_int_string
import xml.etree.ElementTree as ET


class SectionNovx(BasicElementTagsNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)

        # Attributes.
        typeStr = xmlElement.get('type', '0')
        if typeStr in ('0', '1', '2', '3'):
            element.scType = int(typeStr)
        else:
            element.scType = 1
        status = xmlElement.get('status', '1')
        if status in ('1', '2', '3', '4', '5'):
            element.status = int(status)
        else:
            element.status = 1
        scene = xmlElement.get('scene', '0')
        if scene in ('0', '1', '2', '3'):
            element.scene = int(scene)
        else:
            element.scene = 0

        if not element.scene:
            # looking for deprecated attribute from DTD 1.3
            sceneKind = xmlElement.get('pacing', None)
            if sceneKind in ('1', '2'):
                element.scene = int(sceneKind) + 1

        element.appendToPrev = xmlElement.get('append', None) == '1'

        # Viewpoint.
        xmlViewpoint = xmlElement.find('Viewpoint')
        if xmlViewpoint is not None:
            element.viewpoint = xmlViewpoint.get('id', None)

        # Goal/Conflict/outcome.
        element.goal = self._xml_element_to_text(xmlElement.find('Goal'))
        element.conflict = self._xml_element_to_text(xmlElement.find('Conflict'))
        element.outcome = self._xml_element_to_text(xmlElement.find('Outcome'))

        # Plot line notes.
        xmlPlotlineNotes = xmlElement.find('PlotNotes')
        # looking for deprecated element from DTD 1.3
        if xmlPlotlineNotes is None:
            xmlPlotlineNotes = xmlElement
        plotlineNotes = {}
        for xmlPlotlineNote in xmlPlotlineNotes.iterfind('PlotlineNotes'):
            plId = xmlPlotlineNote.get('id', None)
            plotlineNotes[plId] = self._xml_element_to_text(xmlPlotlineNote)
        element.plotlineNotes = plotlineNotes

        # Date/Day and Time.
        if xmlElement.find('Date') is not None:
            element.date = PyCalendar.verified_date(xmlElement.find('Date').text)
        elif xmlElement.find('Day') is not None:
            element.day = verified_int_string(xmlElement.find('Day').text)

        if xmlElement.find('Time') is not None:
            element.time = PyCalendar.verified_time(xmlElement.find('Time').text)

        # Duration.
        element.lastsDays = verified_int_string(
            self._get_element_text(xmlElement, 'LastsDays')
        )
        element.lastsHours = verified_int_string(
            self._get_element_text(xmlElement, 'LastsHours')
        )
        element.lastsMinutes = verified_int_string(
            self._get_element_text(xmlElement, 'LastsMinutes')
        )

        # Characters references.
        scCharacters = []
        xmlCharacters = xmlElement.find('Characters')
        if xmlCharacters is not None:
            crIds = xmlCharacters.get('ids', None)
            if crIds is not None:
                for crId in string_to_list(crIds, divider=' '):
                    scCharacters.append(crId)
        element.characters = scCharacters

        # Locations references.
        scLocations = []
        xmlLocations = xmlElement.find('Locations')
        if xmlLocations is not None:
            lcIds = xmlLocations.get('ids', None)
            if lcIds is not None:
                for lcId in string_to_list(lcIds, divider=' '):
                    scLocations.append(lcId)
        element.locations = scLocations

        # Items references.
        scItems = []
        xmlItems = xmlElement.find('Items')
        if xmlItems is not None:
            itIds = xmlItems.get('ids', None)
            if itIds is not None:
                for itId in string_to_list(itIds, divider=' '):
                    scItems.append(itId)
        element.items = scItems

        # Content.
        xmlContent = xmlElement.find('Content')
        if xmlContent is not None:
            xmlStr = ET.tostring(
                xmlContent,
                encoding='utf-8',
                short_empty_elements=False
                ).decode('utf-8')
            xmlStr = xmlStr.replace('<Content>', '').replace('</Content>', '')

            # Remove indentiation, if any.
            lines = xmlStr.split('\n')
            newlines = []
            for line in lines:
                newlines.append(line.strip())
            xmlStr = ''.join(newlines)
            if xmlStr:
                element.sectionContent = xmlStr
            else:
                element.sectionContent = '<p></p>'
        elif element.scType < 2:
            # normal or unused section; not a stage
            element.sectionContent = '<p></p>'

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.scType:
            xmlElement.set('type', str(element.scType))
        if element.status > 1:
            xmlElement.set('status', str(element.status))
        if element.scene > 0:
            xmlElement.set('scene', str(element.scene))
        if element.appendToPrev:
            xmlElement.set('append', '1')

        # Viewpoint.
        if element.viewpoint:
            ET.SubElement(
                xmlElement,
                'Viewpoint',
                attrib={'id':element.viewpoint},
            )

        # Goal/Conflict/Outcome.
        if element.goal:
            xmlElement.append(
                self._text_to_xml_element('Goal', element.goal)
            )
        if element.conflict:
            xmlElement.append(
                self._text_to_xml_element('Conflict', element.conflict)
            )
        if element.outcome:
            xmlElement.append(
                self._text_to_xml_element('Outcome', element.outcome)
            )

        # Plot line notes.
        if element.plotlineNotes:
            for plId in element.plotlineNotes:
                if not plId in element.scPlotLines:
                    continue

                if not element.plotlineNotes[plId]:
                    continue

                xmlPlotlineNotes = self._text_to_xml_element(
                    'PlotlineNotes', element.plotlineNotes[plId]
                )
                xmlPlotlineNotes.set('id', plId)
                xmlElement.append(xmlPlotlineNotes)

        # Date/Day and Time.
        if element.date:
            ET.SubElement(xmlElement, 'Date').text = element.date
        elif element.day:
            ET.SubElement(xmlElement, 'Day').text = element.day
        if element.time:
            ET.SubElement(xmlElement, 'Time').text = element.time

        # Duration.
        if element.lastsDays and element.lastsDays != '0':
            ET.SubElement(xmlElement, 'LastsDays').text = element.lastsDays
        if element.lastsHours and element.lastsHours != '0':
            ET.SubElement(xmlElement, 'LastsHours').text = element.lastsHours
        if element.lastsMinutes and element.lastsMinutes != '0':
            ET.SubElement(xmlElement, 'LastsMinutes').text = element.lastsMinutes

        # Characters references.
        if element.characters:
            ET.SubElement(
                xmlElement,
                'Characters',
                attrib={'ids':' '.join(element.characters)},
            )

        # Locations references.
        if element.locations:
            ET.SubElement(
                xmlElement,
                'Locations',
                attrib={'ids':' '.join(element.locations)},
            )

        # Items references.
        if element.items:
            ET.SubElement(
                xmlElement,
                'Items',
                attrib={'ids':' '.join(element.items)},
            )

        # Content.
        sectionContent = element.sectionContent
        if sectionContent:
            if not sectionContent in ('<p></p>', '<p />'):
                xmlElement.append(
                    ET.fromstring(f'<Content>{sectionContent}</Content>')
                )

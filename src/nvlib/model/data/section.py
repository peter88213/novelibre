"""Provide a class for novelibre section representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from nvlib.model.data.basic_element_tags import BasicElementTags
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.model.data.word_counter import WordCounter
from nvlib.novx_globals import string_to_list
from nvlib.novx_globals import verified_int_string
import xml.etree.ElementTree as ET


class Section(BasicElementTags):
    """novelibre section representation."""

    NULL_DATE = '0001-01-01'
    NULL_TIME = '00:00:00'
    wordCounter = WordCounter()

    def __init__(
        self,
        scType=None,
        scene=None,
        status=None,
        appendToPrev=None,
        viewpoint=None,
        goal=None,
        conflict=None,
        outcome=None,
        plotNotes=None,
        scDate=None,
        scTime=None,
        day=None,
        lastsMinutes=None,
        lastsHours=None,
        lastsDays=None,
        characters=None,
        locations=None,
        items=None,
        **kwargs
    ):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)
        self._sectionContent = None
        self.wordCount = 0
        # To be updated by the sectionContent setter

        # Initialize properties.
        self._scType = scType
        self._scene = scene
        self._status = status
        self._appendToPrev = appendToPrev
        self._goal = goal
        self._conflict = conflict
        self._outcome = outcome
        self._plotlineNotes = plotNotes
        try:
            self._weekDay = PyCalendar.weekday(scDate)
            self._localeDate = PyCalendar.locale_date(scDate)
            self._date = scDate
        except:
            self._weekDay = None
            self._localeDate = None
            self._date = None
        self._time = scTime
        self._day = day
        self._lastsMinutes = lastsMinutes
        self._lastsHours = lastsHours
        self._lastsDays = lastsDays
        self._viewpoint = viewpoint
        self._characters = characters
        self._locations = locations
        self._items = items

        self.scPlotLines = []
        # Back references to PlotLine.sections
        self.scPlotPoints = {}
        # Back references to PlotPoint.sectionAssoc
        # key: plot point ID, value: plot line ID

    @property
    def sectionContent(self):
        return self._sectionContent

    @sectionContent.setter
    def sectionContent(self, text):
        """Set sectionContent updating the word count."""
        if text is not None:
            assert type(text) is str
        if self._sectionContent != text:
            self._sectionContent = text
            if text is not None:
                self.wordCount = self.wordCounter.get_word_count(text)
            else:
                self.wordCount = 0
            self.on_element_change()

    @property
    def scType(self):
        # 0 = Normal
        # 1 = Unused
        # 2 = Level 1 stage
        # 3 = Level 2 stage
        return self._scType

    @scType.setter
    def scType(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._scType != newVal:
            self._scType = newVal
            self.on_element_change()

    @property
    def scene(self):
        # 0 = not a scene
        # 1 = action scene
        # 2 = reaction scene
        # 3 = other scene
        return self._scene

    @scene.setter
    def scene(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._scene != newVal:
            self._scene = newVal
            self.on_element_change()

    @property
    def status(self):
        # 1 - Outline
        # 2 - Draft
        # 3 - 1st Edit
        # 4 - 2nd Edit
        # 5 - Done
        return self._status

    @status.setter
    def status(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._status != newVal:
            self._status = newVal
            self.on_element_change()

    @property
    def appendToPrev(self):
        # True - append this section to the previous one
        #        without a section separator
        # False - put a section separator between this section
        #         and the previous one
        return self._appendToPrev

    @appendToPrev.setter
    def appendToPrev(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._appendToPrev != newVal:
            self._appendToPrev = newVal
            self.on_element_change()

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._goal != newVal:
            self._goal = newVal
            self.on_element_change()

    @property
    def conflict(self):
        return self._conflict

    @conflict.setter
    def conflict(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._conflict != newVal:
            self._conflict = newVal
            self.on_element_change()

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._outcome != newVal:
            self._outcome = newVal
            self.on_element_change()

    @property
    def plotlineNotes(self):
        # Dict of {plot line ID: text}
        try:
            return dict(self._plotlineNotes)
        except TypeError:
            return None

    @plotlineNotes.setter
    def plotlineNotes(self, newVal):
        if newVal is not None:
            for elem in newVal:
                val = newVal[elem]
                if val is not None:
                    assert type(val) is str
        if self._plotlineNotes != newVal:
            self._plotlineNotes = newVal
            self.on_element_change()

    @property
    def date(self):
        # YYYY-MM-DD
        return self._date

    @date.setter
    def date(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._date != newVal:
            if not newVal:
                self._date = None
                self._weekDay = None
                self._localeDate = None
                self.on_element_change()
                return

            try:
                self._weekDay = PyCalendar.weekday(newVal)
            except:
                return
                # date and week day remain unchanged

            try:
                self._localeDate = PyCalendar.locale_date(newVal)
            except:
                self._localeDate = newVal
            self._date = newVal
            self.on_element_change()

    @property
    def weekDay(self):
        # the number of the day ot the week
        return self._weekDay

    @property
    def localeDate(self):
        # the preferred date representation for the current locale
        return self._localeDate

    @property
    def time(self):
        # hh:mm:ss
        return self._time

    @time.setter
    def time(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._time != newVal:
            self._time = newVal
            self.on_element_change()

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._day != newVal:
            self._day = newVal
            self.on_element_change()

    @property
    def lastsMinutes(self):
        return self._lastsMinutes

    @lastsMinutes.setter
    def lastsMinutes(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._lastsMinutes != newVal:
            self._lastsMinutes = newVal
            self.on_element_change()

    @property
    def lastsHours(self):
        return self._lastsHours

    @lastsHours.setter
    def lastsHours(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._lastsHours != newVal:
            self._lastsHours = newVal
            self.on_element_change()

    @property
    def lastsDays(self):
        return self._lastsDays

    @lastsDays.setter
    def lastsDays(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._lastsDays != newVal:
            self._lastsDays = newVal
            self.on_element_change()

    @property
    def viewpoint(self):
        return self._viewpoint

    @viewpoint.setter
    def viewpoint(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._viewpoint != newVal:
            self._viewpoint = newVal
            self.on_element_change()

    @property
    def characters(self):
        # list of character IDs
        try:
            return self._characters[:]
        except TypeError:
            return None

    @characters.setter
    def characters(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) is str
        if self._characters != newVal:
            self._characters = newVal
            self.on_element_change()

    @property
    def locations(self):
        # List of location IDs
        try:
            return self._locations[:]
        except TypeError:
            return None

    @locations.setter
    def locations(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) is str
        if self._locations != newVal:
            self._locations = newVal
            self.on_element_change()

    @property
    def items(self):
        # List of Item IDs
        try:
            return self._items[:]
        except TypeError:
            return None

    @items.setter
    def items(self, newVal):
        if newVal is not None:
            for elem in newVal:
                if elem is not None:
                    assert type(elem) is str
        if self._items != newVal:
            self._items = newVal
            self.on_element_change()

    def day_to_date(self, referenceDate):
        """Convert day to specific date.
        
        Positional argument:
        referenceDate: str -- reference date in isoformat.

        On success, return True. Otherwise return False. 
        """
        if self._date:
            return True

        try:
            self.date = PyCalendar.specific_date(self._day, referenceDate)
            self._day = None
            return True

        except:
            self.date = None
            return False

    def date_to_day(self, referenceDate):
        """Convert specific date to day.
        
        Positional argument:
        referenceDate: str -- reference date in isoformat.
        
        On success, return True. Otherwise return False. 
        """
        if self._day:
            return True

        try:
            self._day = PyCalendar.unspecific_date(self._date, referenceDate)
            self.date = None
            return True

        except:
            self._day = None
            return False

    def from_xml(self, xmlElement):
        super().from_xml(xmlElement)

        # Attributes.
        typeStr = xmlElement.get('type', '0')
        if typeStr in ('0', '1', '2', '3'):
            self.scType = int(typeStr)
        else:
            self.scType = 1
        status = xmlElement.get('status', None)
        if status in ('2', '3', '4', '5'):
            self.status = int(status)
        else:
            self.status = 1
        scene = xmlElement.get('scene', 0)
        if scene in ('1', '2', '3'):
            self.scene = int(scene)
        else:
            self.scene = 0

        if not self.scene:
            # looking for deprecated attribute from DTD 1.3
            sceneKind = xmlElement.get('pacing', None)
            if sceneKind in ('1', '2'):
                self.scene = int(sceneKind) + 1

        self.appendToPrev = xmlElement.get('append', None) == '1'

        # Viewpoint.
        xmlViewpoint = xmlElement.find('Viewpoint')
        if xmlViewpoint is not None:
            self.viewpoint = xmlViewpoint.get('id', None)

        # Goal/Conflict/outcome.
        self.goal = self._xml_element_to_text(xmlElement.find('Goal'))
        self.conflict = self._xml_element_to_text(xmlElement.find('Conflict'))
        self.outcome = self._xml_element_to_text(xmlElement.find('Outcome'))

        # Plot notes.
        xmlPlotNotes = xmlElement.find('PlotNotes')
        # looking for deprecated element from DTD 1.3
        if xmlPlotNotes is None:
            xmlPlotNotes = xmlElement
        plotNotes = {}
        for xmlPlotLineNote in xmlPlotNotes.iterfind('PlotlineNotes'):
            plId = xmlPlotLineNote.get('id', None)
            plotNotes[plId] = self._xml_element_to_text(xmlPlotLineNote)
        self.plotlineNotes = plotNotes

        # Date/Day and Time.
        if xmlElement.find('Date') is not None:
            self.date = PyCalendar.verified_date(xmlElement.find('Date').text)
        elif xmlElement.find('Day') is not None:
            self.day = verified_int_string(xmlElement.find('Day').text)

        if xmlElement.find('Time') is not None:
            self.time = PyCalendar.verified_time(xmlElement.find('Time').text)

        # Duration.
        self.lastsDays = verified_int_string(
            self._get_element_text(xmlElement, 'LastsDays')
        )
        self.lastsHours = verified_int_string(
            self._get_element_text(xmlElement, 'LastsHours')
        )
        self.lastsMinutes = verified_int_string(
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
        self.characters = scCharacters

        # Locations references.
        scLocations = []
        xmlLocations = xmlElement.find('Locations')
        if xmlLocations is not None:
            lcIds = xmlLocations.get('ids', None)
            if lcIds is not None:
                for lcId in string_to_list(lcIds, divider=' '):
                    scLocations.append(lcId)
        self.locations = scLocations

        # Items references.
        scItems = []
        xmlItems = xmlElement.find('Items')
        if xmlItems is not None:
            itIds = xmlItems.get('ids', None)
            if itIds is not None:
                for itId in string_to_list(itIds, divider=' '):
                    scItems.append(itId)
        self.items = scItems

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
                self.sectionContent = xmlStr
            else:
                self.sectionContent = '<p></p>'
        elif self.scType < 2:
            # normal or unused section; not a stage
            self.sectionContent = '<p></p>'

    def get_end_date_time(self):
        """Return the end (date, time, day) tuple 
        
        calculated from start and duration.
        """
        endDate = None
        endTime = None
        endDay = None
        if self.time:
            if self.date:
                try:
                    endDate, endTime = PyCalendar.get_end_date_time(self)
                except:
                    pass
            elif self.day:
                try:
                    endDay, endTime = PyCalendar.get_end_day_time(self)
                except:
                    pass
            else:
                endTime = PyCalendar.get_end_time(self)
        return endDate, endTime, endDay

    def to_xml(self, xmlElement):
        super().to_xml(xmlElement)
        if self.scType:
            xmlElement.set('type', str(self.scType))
        if self.status > 1:
            xmlElement.set('status', str(self.status))
        if self.scene > 0:
            xmlElement.set('scene', str(self.scene))
        if self.appendToPrev:
            xmlElement.set('append', '1')

        # Viewpoint.
        if self.viewpoint:
            ET.SubElement(
                xmlElement,
                'Viewpoint',
                attrib={'id':self.viewpoint},
            )

        # Goal/Conflict/Outcome.
        if self.goal:
            xmlElement.append(
                self._text_to_xml_element('Goal', self.goal)
            )
        if self.conflict:
            xmlElement.append(
                self._text_to_xml_element('Conflict', self.conflict)
            )
        if self.outcome:
            xmlElement.append(
                self._text_to_xml_element('Outcome', self.outcome)
            )

        # Plot notes.
        if self.plotlineNotes:
            for plId in self.plotlineNotes:
                if not plId in self.scPlotLines:
                    continue

                if not self.plotlineNotes[plId]:
                    continue

                xmlPlotlineNotes = self._text_to_xml_element(
                    'PlotlineNotes', self.plotlineNotes[plId]
                )
                xmlPlotlineNotes.set('id', plId)
                xmlElement.append(xmlPlotlineNotes)

        # Date/Day and Time.
        if self.date:
            ET.SubElement(xmlElement, 'Date').text = self.date
        elif self.day:
            ET.SubElement(xmlElement, 'Day').text = self.day
        if self.time:
            ET.SubElement(xmlElement, 'Time').text = self.time

        # Duration.
        if self.lastsDays and self.lastsDays != '0':
            ET.SubElement(xmlElement, 'LastsDays').text = self.lastsDays
        if self.lastsHours and self.lastsHours != '0':
            ET.SubElement(xmlElement, 'LastsHours').text = self.lastsHours
        if self.lastsMinutes and self.lastsMinutes != '0':
            ET.SubElement(xmlElement, 'LastsMinutes').text = self.lastsMinutes

        # Characters references.
        if self.characters:
            ET.SubElement(
                xmlElement,
                'Characters',
                attrib={'ids':' '.join(self.characters)},
            )

        # Locations references.
        if self.locations:
            ET.SubElement(
                xmlElement,
                'Locations',
                attrib={'ids':' '.join(self.locations)},
            )

        # Items references.
        if self.items:
            ET.SubElement(
                xmlElement,
                'Items',
                attrib={'ids':' '.join(self.items)},
            )

        # Content.
        sectionContent = self.sectionContent
        if sectionContent:
            if not sectionContent in ('<p></p>', '<p />'):
                xmlElement.append(
                    ET.fromstring(f'<Content>{sectionContent}</Content>')
                )

"""Provide a class for novelibre section representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from nvlib.model.data.basic_element_tags import BasicElementTags
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.model.data.word_counter import WordCounter


class Section(BasicElementTags):
    """novelibre section representation."""

    NULL_DATE = '0001-01-01'
    NULL_TIME = '00:00:00'

    wordCounter = WordCounter()
    # a strategy class that can be replaced at runtime

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
        plotlineNotes=None,
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
        self._hasComment = False
        # To be updated by the sectionContent setter

        # Initialize properties.
        self._scType = scType
        self._scene = scene
        self._status = status
        self._appendToPrev = appendToPrev
        self._goal = goal
        self._conflict = conflict
        self._outcome = outcome
        self._plotlineNotes = plotlineNotes
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
                self._hasComment = '<comment>' in self._sectionContent
            else:
                self.wordCount = 0
                self._hasComment = False
            self.on_element_change()

    @property
    def hasComment(self):
        # True if the contents include at least one comment
        return self._hasComment

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


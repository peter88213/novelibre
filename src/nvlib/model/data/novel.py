"""Provide a class for a novel representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import locale
import re

from nvlib.model.data.basic_element import BasicElement
from nvlib.model.data.py_calendar import PyCalendar

LANGUAGE_TAG = re.compile(r'\<(p|span) xml\:lang=\"(.*?)\".*?\>')


class Novel(BasicElement):
    """Novel representation."""

    def __init__(
        self,
        authorName=None,
        wordTarget=None,
        wordCountStart=None,
        languageCode=None,
        countryCode=None,
        renumberChapters=None,
        renumberParts=None,
        renumberWithinParts=None,
        romanChapterNumbers=None,
        romanPartNumbers=None,
        saveWordCount=None,
        workPhase=None,
        chapterHeadingPrefix=None,
        chapterHeadingSuffix=None,
        partHeadingPrefix=None,
        partHeadingSuffix=None,
        noSceneField1=None,
        noSceneField2=None,
        noSceneField3=None,
        otherSceneField1=None,
        otherSceneField2=None,
        otherSceneField3=None,
        crField1=None,
        crField2=None,
        referenceDate=None,
        tree=None,
        **kwargs
    ):
        """Extends the superclass constructor."""
        super().__init__(**kwargs)
        self._authorName = authorName
        self._wordTarget = wordTarget
        self._wordCountStart = wordCountStart
        self._languageCode = languageCode
        self._countryCode = countryCode
        self._renumberChapters = renumberChapters
        self._renumberParts = renumberParts
        self._renumberWithinParts = renumberWithinParts
        self._romanChapterNumbers = romanChapterNumbers
        self._romanPartNumbers = romanPartNumbers
        self._saveWordCount = saveWordCount
        self._workPhase = workPhase
        self._chapterHeadingPrefix = chapterHeadingPrefix
        self._chapterHeadingSuffix = chapterHeadingSuffix
        self._partHeadingPrefix = partHeadingPrefix
        self._partHeadingSuffix = partHeadingSuffix
        self._noSceneField1 = noSceneField1
        self._noSceneField2 = noSceneField2
        self._noSceneField3 = noSceneField3
        self._otherSceneField1 = otherSceneField1
        self._otherSceneField2 = otherSceneField2
        self._otherSceneField3 = otherSceneField3
        self._crField1 = crField1
        self._crField2 = crField2

        self.chapters = {}
        # key = chapter ID, value = Chapter instance.
        self.sections = {}
        # key = section ID, value = Section instance.
        self.plotPoints = {}
        # key = section ID, value = PlotPoint instance.
        self.languages = None
        # List of non-document languages occurring as section markup.
        # Format: ll-CC,
        # where ll is the language code, and CC is the country code.
        self.plotLines = {}
        # key = plot line ID, value = PlotLine instance.
        self.locations = {}
        # key = location ID, value = WorldElement instance.
        self.items = {}
        # key = item ID, value = WorldElement instance.
        self.characters = {}
        # key = character ID, value = Character instance.
        self.projectNotes = {}
        # key = note ID, value = note instance.
        try:
            self.referenceWeekDay = PyCalendar.weekday(referenceDate)
            self._referenceDate = referenceDate
            # YYYY-MM-DD
        except:
            self.referenceWeekDay = None
            self._referenceDate = None
        self.tree = tree

    @property
    def authorName(self):
        return self._authorName

    @authorName.setter
    def authorName(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._authorName != newVal:
            self._authorName = newVal
            self.on_element_change()

    @property
    def wordTarget(self):
        return self._wordTarget

    @wordTarget.setter
    def wordTarget(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._wordTarget != newVal:
            self._wordTarget = newVal
            self.on_element_change()

    @property
    def wordCountStart(self):
        return self._wordCountStart

    @wordCountStart.setter
    def wordCountStart(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._wordCountStart != newVal:
            self._wordCountStart = newVal
            self.on_element_change()

    @property
    def languageCode(self):
        # Language code acc. to ISO 639-1.
        return self._languageCode

    @languageCode.setter
    def languageCode(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._languageCode != newVal:
            self._languageCode = newVal
            self.on_element_change()

    @property
    def countryCode(self):
        # Country code acc. to ISO 3166-2.
        return self._countryCode

    @countryCode.setter
    def countryCode(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._countryCode != newVal:
            self._countryCode = newVal
            self.on_element_change()

    @property
    def renumberChapters(self):
        # True: Auto-number chapters
        # False: Do not auto-number chapters
        return self._renumberChapters

    @renumberChapters.setter
    def renumberChapters(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._renumberChapters != newVal:
            self._renumberChapters = newVal
            self.on_element_change()

    @property
    def renumberParts(self):
        # True: Auto-number parts
        # False: Do not auto-number parts
        return self._renumberParts

    @renumberParts.setter
    def renumberParts(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._renumberParts != newVal:
            self._renumberParts = newVal
            self.on_element_change()

    @property
    def renumberWithinParts(self):
        # True: When auto-numbering chapters,
        # start with 1 at each part beginning
        # False: When auto-numbering chapters, ignore parts
        return self._renumberWithinParts

    @renumberWithinParts.setter
    def renumberWithinParts(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._renumberWithinParts != newVal:
            self._renumberWithinParts = newVal
            self.on_element_change()

    @property
    def romanChapterNumbers(self):
        # True: Use Roman chapter numbers when auto-numbering
        # False: Use Arabic chapter numbers when auto-numbering
        return self._romanChapterNumbers

    @romanChapterNumbers.setter
    def romanChapterNumbers(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._romanChapterNumbers != newVal:
            self._romanChapterNumbers = newVal
            self.on_element_change()

    @property
    def romanPartNumbers(self):
        # True: Use Roman part numbers when auto-numbering
        # False: Use Arabic part numbers when auto-numbering
        return self._romanPartNumbers

    @romanPartNumbers.setter
    def romanPartNumbers(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._romanPartNumbers != newVal:
            self._romanPartNumbers = newVal
            self.on_element_change()

    @property
    def saveWordCount(self):
        # True: Save daily word count log
        # False: Do not save daily word count log
        return self._saveWordCount

    @saveWordCount.setter
    def saveWordCount(self, newVal):
        if newVal is not None:
            assert type(newVal) is bool
        if self._saveWordCount != newVal:
            self._saveWordCount = newVal
            self.on_element_change()

    @property
    def workPhase(self):
        # None - Undefined
        # 1 - Outline
        # 2 - Draft
        # 3 - 1st Edit
        # 4 - 2nd Edit
        # 5 - Done
        return self._workPhase

    @workPhase.setter
    def workPhase(self, newVal):
        if newVal is not None:
            assert type(newVal) is int
        if self._workPhase != newVal:
            self._workPhase = newVal
            self.on_element_change()

    @property
    def chapterHeadingPrefix(self):
        return self._chapterHeadingPrefix

    @chapterHeadingPrefix.setter
    def chapterHeadingPrefix(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._chapterHeadingPrefix != newVal:
            self._chapterHeadingPrefix = newVal
            self.on_element_change()

    @property
    def chapterHeadingSuffix(self):
        return self._chapterHeadingSuffix

    @chapterHeadingSuffix.setter
    def chapterHeadingSuffix(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._chapterHeadingSuffix != newVal:
            self._chapterHeadingSuffix = newVal
            self.on_element_change()

    @property
    def partHeadingPrefix(self):
        return self._partHeadingPrefix

    @partHeadingPrefix.setter
    def partHeadingPrefix(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._partHeadingPrefix != newVal:
            self._partHeadingPrefix = newVal
            self.on_element_change()

    @property
    def partHeadingSuffix(self):
        return self._partHeadingSuffix

    @partHeadingSuffix.setter
    def partHeadingSuffix(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._partHeadingSuffix != newVal:
            self._partHeadingSuffix = newVal
            self.on_element_change()

    @property
    def noSceneField1(self):
        return self._noSceneField1

    @noSceneField1.setter
    def noSceneField1(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._noSceneField1 != newVal:
            self._noSceneField1 = newVal
            self.on_element_change()

    @property
    def noSceneField2(self):
        return self._noSceneField2

    @noSceneField2.setter
    def noSceneField2(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._noSceneField2 != newVal:
            self._noSceneField2 = newVal
            self.on_element_change()

    @property
    def noSceneField3(self):
        return self._noSceneField3

    @noSceneField3.setter
    def noSceneField3(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._noSceneField3 != newVal:
            self._noSceneField3 = newVal
            self.on_element_change()

    @property
    def otherSceneField1(self):
        return self._otherSceneField1

    @otherSceneField1.setter
    def otherSceneField1(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._otherSceneField1 != newVal:
            self._otherSceneField1 = newVal
            self.on_element_change()

    @property
    def otherSceneField2(self):
        return self._otherSceneField2

    @otherSceneField2.setter
    def otherSceneField2(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._otherSceneField2 != newVal:
            self._otherSceneField2 = newVal
            self.on_element_change()

    @property
    def otherSceneField3(self):
        return self._otherSceneField3

    @otherSceneField3.setter
    def otherSceneField3(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._otherSceneField3 != newVal:
            self._otherSceneField3 = newVal
            self.on_element_change()

    @property
    def crField1(self):
        return self._crField1

    @crField1.setter
    def crField1(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._crField1 != newVal:
            self._crField1 = newVal
            self.on_element_change()

    @property
    def crField2(self):
        return self._crField2

    @crField2.setter
    def crField2(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._crField2 != newVal:
            self._crField2 = newVal
            self.on_element_change()

    @property
    def referenceDate(self):
        return self._referenceDate

    @referenceDate.setter
    def referenceDate(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._referenceDate != newVal:
            if not newVal:
                self._referenceDate = None
                self.referenceWeekDay = None
                self.on_element_change()
            else:
                try:
                    self.referenceWeekDay = PyCalendar.weekday(newVal)
                except:
                    pass
                    # date and week day remain unchanged
                else:
                    self._referenceDate = newVal
                    self.on_element_change()

    def check_locale(self):
        """Check the document's locale (language code and country code).
        
        If the locale is missing, set the system locale.  
        If the locale doesn't look plausible, set "no language".      
        """
        if not self._languageCode:
            # Use the system locale.
            try:
                sysLng, sysCtr = locale.getlocale()[0].split('_')
            except:
                # Fallback for old Windows versions.
                sysLng, sysCtr = locale.getdefaultlocale()[0].split('_')
            self.languageCode = sysLng
            self.countryCode = sysCtr
            return

        if len(self._languageCode) != 2:
            # Set "No language information".
            self.languageCode = 'zxx'
            self.countryCode = None
            return

        if self._countryCode and len(self._countryCode) != 2:
            # Set "No country information".
            self.countryCode = None

    def get_languages(self):
        """Determine the languages used in the document.
        
        Populate the self.languages list with all language codes 
        found in the section contents.        
        Example:
        - language markup: 
          'Standard text <span xml:lang="en-AU"]Australian text</span>.'
        - language code: 'en-AU'
        """

        def languages(text):
            # Yield the language codes appearing in text.
            m = LANGUAGE_TAG.search(text)
            while m:
                text = text[m.span()[1]:]
                yield m.group(2)
                m = LANGUAGE_TAG.search(text)

        self.languages = []
        for scId in self.sections:
            text = self.sections[scId].sectionContent
            if text:
                for language in languages(text):
                    if not language in self.languages:
                        self.languages.append(language)

    def update_plot_lines(self):
        """Update redundant model data.
        
        Set section back references to PlotLine.sections 
        and PlotPoint.sectionAssoc. 
        """
        for scId in self.sections:
            self.sections[scId].scPlotPoints = {}
            self.sections[scId].scPlotLines = []
            for plId in self.plotLines:
                if scId in self.plotLines[plId].sections:
                    self.sections[scId].scPlotLines.append(plId)
                    for ppId in self.tree.get_children(plId):
                        if self.plotPoints[ppId].sectionAssoc == scId:
                            self.sections[scId].scPlotPoints[ppId] = plId
                            break


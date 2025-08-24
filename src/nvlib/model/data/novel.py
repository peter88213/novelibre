"""Provide a class for a novel representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import locale
import re

from nvlib.model.data.basic_element import BasicElement
from nvlib.model.data.py_calendar import PyCalendar
import xml.etree.ElementTree as ET

LANGUAGE_TAG = re.compile(r'\<span xml\:lang=\"(.*?)\"\>')


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
        noScnField1=None,
        noScnField2=None,
        noScnField3=None,
        otherScnField1=None,
        otherScnField2=None,
        otherScnField3=None,
        chrExtraField1=None,
        chrExtraField2=None,
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
        self._noScnField1 = noScnField1
        self._noScnField2 = noScnField2
        self._noScnField3 = noScnField3
        self._otherScnField1 = otherScnField1
        self._otherScnField2 = otherScnField2
        self._otherScnField3 = otherScnField3
        self._chrExtraField1 = chrExtraField1
        self._chrExtraField2 = chrExtraField2

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
    def noScnField1(self):
        return self._noScnField1

    @noScnField1.setter
    def noScnField1(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._noScnField1 != newVal:
            self._noScnField1 = newVal
            self.on_element_change()

    @property
    def noScnField2(self):
        return self._noScnField2

    @noScnField2.setter
    def noScnField2(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._noScnField2 != newVal:
            self._noScnField2 = newVal
            self.on_element_change()

    @property
    def noScnField3(self):
        return self._noScnField3

    @noScnField3.setter
    def noScnField3(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._noScnField3 != newVal:
            self._noScnField3 = newVal
            self.on_element_change()

    @property
    def otherScnField1(self):
        return self._otherScnField1

    @otherScnField1.setter
    def otherScnField1(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._otherScnField1 != newVal:
            self._otherScnField1 = newVal
            self.on_element_change()

    @property
    def otherScnField2(self):
        return self._otherScnField2

    @otherScnField2.setter
    def otherScnField2(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._otherScnField2 != newVal:
            self._otherScnField2 = newVal
            self.on_element_change()

    @property
    def otherScnField3(self):
        return self._otherScnField3

    @otherScnField3.setter
    def otherScnField3(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._otherScnField3 != newVal:
            self._otherScnField3 = newVal
            self.on_element_change()

    @property
    def chrExtraField1(self):
        return self._chrExtraField1

    @chrExtraField1.setter
    def chrExtraField1(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._chrExtraField1 != newVal:
            self._chrExtraField1 = newVal
            self.on_element_change()

    @property
    def chrExtraField2(self):
        return self._chrExtraField2

    @chrExtraField2.setter
    def chrExtraField2(self, newVal):
        if newVal is not None:
            assert type(newVal) is str
        if self._chrExtraField2 != newVal:
            self._chrExtraField2 = newVal
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
        if not self._languageCode or self._languageCode == 'None':
            # Language isn't set.
            try:
                sysLng, sysCtr = locale.getlocale()[0].split('_')
            except:
                # Fallback for old Windows versions.
                sysLng, sysCtr = locale.getdefaultlocale()[0].split('_')
            self._languageCode = sysLng
            self._countryCode = sysCtr
            self.on_element_change()
            return

        try:
            # Plausibility check: code must have two characters.
            if len(self._languageCode) == 2:
                if len(self._countryCode) == 2:
                    return
                    # keep the setting
        except:
            # code isn't a string
            pass
        # Existing language or country field looks not plausible
        self._languageCode = 'zxx'
        self._countryCode = 'none'
        self.on_element_change()

    def from_xml(self, xmlElement):
        super().from_xml(xmlElement)
        self.renumberChapters = xmlElement.get(
            'renumberChapters', None) == '1'
        self.renumberParts = xmlElement.get(
            'renumberParts', None) == '1'
        self.renumberWithinParts = xmlElement.get(
            'renumberWithinParts', None) == '1'
        self.romanChapterNumbers = xmlElement.get(
            'romanChapterNumbers', None) == '1'
        self.romanPartNumbers = xmlElement.get(
            'romanPartNumbers', None) == '1'
        self.saveWordCount = xmlElement.get(
            'saveWordCount', None) == '1'
        workPhase = xmlElement.get('workPhase', None)
        if workPhase in ('1', '2', '3', '4', '5'):
            self.workPhase = int(workPhase)
        else:
            self.workPhase = None

        # Author.
        self.authorName = self._get_element_text(xmlElement, 'Author')

        # Chapter heading prefix/suffix.
        self.chapterHeadingPrefix = self._get_element_text(
            xmlElement,
            'ChapterHeadingPrefix'
        )
        self.chapterHeadingSuffix = self._get_element_text(
            xmlElement,
            'ChapterHeadingSuffix'
        )

        # Part heading prefix/suffix.
        self.partHeadingPrefix = self._get_element_text(
            xmlElement,
            'PartHeadingPrefix'
        )
        self.partHeadingSuffix = self._get_element_text(
            xmlElement,
            'PartHeadingSuffix'
        )

        # No scene's fields.
        self.noScnField1 = self._get_element_text(
            xmlElement,
            'CustomPlotProgress',
            default=self.noScnField1,
        )
        self.noScnField2 = self._get_element_text(
            xmlElement,
            'CustomCharacterization',
            default=self.noScnField2,
        )
        self.noScnField3 = self._get_element_text(
            xmlElement,
            'CustomWorldBuilding',
            default=self.noScnField3,
        )

        # Other scene's fields.
        self.otherScnField1 = self._get_element_text(
            xmlElement,
            'CustomGoal',
            default=self.otherScnField1,
        )
        self.otherScnField2 = self._get_element_text(
            xmlElement,
            'CustomConflict',
            default=self.otherScnField2,
        )
        self.otherScnField3 = self._get_element_text(
            xmlElement,
            'CustomOutcome',
            default=self.otherScnField3,
        )

        # Character extra field 1.
        self.chrExtraField1 = self._get_element_text(
            xmlElement,
            'CustomChrGoals',
            default=self.chrExtraField1,
        )

        # Word count start/Word target.
        if xmlElement.find('WordCountStart') is not None:
            self.wordCountStart = int(
                xmlElement.find('WordCountStart').text
            )
        else:
            self.wordCountStart = 0
        if xmlElement.find('WordTarget') is not None:
            self.wordTarget = int(
                xmlElement.find('WordTarget').text
            )

        # Reference date.
        self.referenceDate = PyCalendar.verified_date(
            self._get_element_text(xmlElement, 'ReferenceDate')
        )

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
                yield m.group(1)
                m = LANGUAGE_TAG.search(text)

        self.languages = []
        for scId in self.sections:
            text = self.sections[scId].sectionContent
            if text:
                for language in languages(text):
                    if not language in self.languages:
                        self.languages.append(language)

    def to_xml(self, xmlElement):
        super().to_xml(xmlElement)
        if self.renumberChapters:
            xmlElement.set('renumberChapters', '1')
        if self.renumberParts:
            xmlElement.set('renumberParts', '1')
        if self.renumberWithinParts:
            xmlElement.set('renumberWithinParts', '1')
        if self.romanChapterNumbers:
            xmlElement.set('romanChapterNumbers', '1')
        if self.romanPartNumbers:
            xmlElement.set('romanPartNumbers', '1')
        if self.saveWordCount:
            xmlElement.set('saveWordCount', '1')
        if self.workPhase is not None:
            xmlElement.set('workPhase', str(self.workPhase))

        # Author.
        if self.authorName:
            ET.SubElement(
                xmlElement,
                'Author',
            ).text = self.authorName

        # Chapter heading prefix/suffix.
        if self.chapterHeadingPrefix:
            ET.SubElement(
                xmlElement,
                'ChapterHeadingPrefix',
            ).text = self.chapterHeadingPrefix
        if self.chapterHeadingSuffix:
            ET.SubElement(
                xmlElement,
                'ChapterHeadingSuffix',
            ).text = self.chapterHeadingSuffix

        # Part heading prefix/suffix.
        if self.partHeadingPrefix:
            ET.SubElement(
                xmlElement,
                'PartHeadingPrefix',
            ).text = self.partHeadingPrefix
        if self.partHeadingSuffix:
            ET.SubElement(
                xmlElement,
                'PartHeadingSuffix',
            ).text = self.partHeadingSuffix

        # No scene's fields.
        if self.noScnField1:
            ET.SubElement(
                xmlElement,
                'CustomPlotProgress',
            ).text = self.noScnField1
        if self.noScnField2:
            ET.SubElement(
                xmlElement,
                'CustomCharacterization',
            ).text = self.noScnField2
        if self.noScnField3:
            ET.SubElement(
                xmlElement,
                'CustomWorldBuilding',
            ).text = self.noScnField3

        # Other scene's fields.
        if self.otherScnField1:
            ET.SubElement(
                xmlElement,
                'CustomGoal',
            ).text = self.otherScnField1
        if self.otherScnField2:
            ET.SubElement(
                xmlElement,
                'CustomConflict',
            ).text = self.otherScnField2
        if self.otherScnField3:
            ET.SubElement(
                xmlElement,
                'CustomOutcome',
            ).text = self.otherScnField3

        # Character Extra field name.
        if self.chrExtraField1:
            ET.SubElement(
                xmlElement,
                'CustomChrGoals',
            ).text = self.chrExtraField1

        # Word count start/Word target.
        if self.wordCountStart:
            ET.SubElement(
                xmlElement,
                'WordCountStart',
            ).text = str(self.wordCountStart)
        if self.wordTarget:
            ET.SubElement(
                xmlElement,
                'WordTarget',
            ).text = str(self.wordTarget)

        # Reference date.
        if self.referenceDate:
            ET.SubElement(
                xmlElement,
                'ReferenceDate',
            ).text = self.referenceDate

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


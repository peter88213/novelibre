"""Provide a class for novel XML import and export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.model.novx.basic_element_novx import BasicElementNovx
import xml.etree.ElementTree as ET


class NovelNovx(BasicElementNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        element.renumberChapters = xmlElement.get(
            'renumberChapters', None) == '1'
        element.renumberParts = xmlElement.get(
            'renumberParts', None) == '1'
        element.renumberWithinParts = xmlElement.get(
            'renumberWithinParts', None) == '1'
        element.romanChapterNumbers = xmlElement.get(
            'romanChapterNumbers', None) == '1'
        element.romanPartNumbers = xmlElement.get(
            'romanPartNumbers', None) == '1'
        element.saveWordCount = xmlElement.get(
            'saveWordCount', None) == '1'
        workPhase = xmlElement.get('workPhase', None)
        if workPhase in ('1', '2', '3', '4', '5'):
            element.workPhase = int(workPhase)
        else:
            element.workPhase = None

        # Author.
        element.authorName = self._get_element_text(xmlElement, 'Author')

        # Chapter heading prefix/suffix.
        element.chapterHeadingPrefix = self._get_element_text(
            xmlElement,
            'ChapterHeadingPrefix'
        )
        element.chapterHeadingSuffix = self._get_element_text(
            xmlElement,
            'ChapterHeadingSuffix'
        )

        # Part heading prefix/suffix.
        element.partHeadingPrefix = self._get_element_text(
            xmlElement,
            'PartHeadingPrefix'
        )
        element.partHeadingSuffix = self._get_element_text(
            xmlElement,
            'PartHeadingSuffix'
        )

        # No scene's fields.
        element.noSceneField1 = self._get_element_text(
            xmlElement,
            'CustomPlotProgress',
            default=element.noSceneField1,
        )
        element.noSceneField2 = self._get_element_text(
            xmlElement,
            'CustomCharacterization',
            default=element.noSceneField2,
        )
        element.noSceneField3 = self._get_element_text(
            xmlElement,
            'CustomWorldBuilding',
            default=element.noSceneField3,
        )

        # Other scene's fields.
        element.otherSceneField1 = self._get_element_text(
            xmlElement,
            'CustomGoal',
            default=element.otherSceneField1,
        )
        element.otherSceneField2 = self._get_element_text(
            xmlElement,
            'CustomConflict',
            default=element.otherSceneField2,
        )
        element.otherSceneField3 = self._get_element_text(
            xmlElement,
            'CustomOutcome',
            default=element.otherSceneField3,
        )

        # Character fields.
        element.crField1 = self._get_element_text(
            xmlElement,
            'CustomChrBio',
            default=element.crField1,
        )
        element.crField2 = self._get_element_text(
            xmlElement,
            'CustomChrGoals',
            default=element.crField2,
        )

        # Word count start/Word target.
        if xmlElement.find('WordCountStart') is not None:
            element.wordCountStart = int(
                xmlElement.find('WordCountStart').text
            )
        else:
            element.wordCountStart = 0
        if xmlElement.find('WordTarget') is not None:
            element.wordTarget = int(
                xmlElement.find('WordTarget').text
            )

        # Reference date.
        element.referenceDate = PyCalendar.verified_date(
            self._get_element_text(xmlElement, 'ReferenceDate')
        )

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.renumberChapters:
            xmlElement.set('renumberChapters', '1')
        if element.renumberParts:
            xmlElement.set('renumberParts', '1')
        if element.renumberWithinParts:
            xmlElement.set('renumberWithinParts', '1')
        if element.romanChapterNumbers:
            xmlElement.set('romanChapterNumbers', '1')
        if element.romanPartNumbers:
            xmlElement.set('romanPartNumbers', '1')
        if element.saveWordCount:
            xmlElement.set('saveWordCount', '1')
        if element.workPhase is not None:
            xmlElement.set('workPhase', str(element.workPhase))

        # Author.
        if element.authorName:
            ET.SubElement(
                xmlElement,
                'Author',
            ).text = element.authorName

        # Chapter heading prefix/suffix.
        if element.chapterHeadingPrefix:
            ET.SubElement(
                xmlElement,
                'ChapterHeadingPrefix',
            ).text = element.chapterHeadingPrefix
        if element.chapterHeadingSuffix:
            ET.SubElement(
                xmlElement,
                'ChapterHeadingSuffix',
            ).text = element.chapterHeadingSuffix

        # Part heading prefix/suffix.
        if element.partHeadingPrefix:
            ET.SubElement(
                xmlElement,
                'PartHeadingPrefix',
            ).text = element.partHeadingPrefix
        if element.partHeadingSuffix:
            ET.SubElement(
                xmlElement,
                'PartHeadingSuffix',
            ).text = element.partHeadingSuffix

        # No scene fields names.
        if element.noSceneField1:
            ET.SubElement(
                xmlElement,
                'CustomPlotProgress',
            ).text = element.noSceneField1
        if element.noSceneField2:
            ET.SubElement(
                xmlElement,
                'CustomCharacterization',
            ).text = element.noSceneField2
        if element.noSceneField3:
            ET.SubElement(
                xmlElement,
                'CustomWorldBuilding',
            ).text = element.noSceneField3

        # Other scene fields names.
        if element.otherSceneField1:
            ET.SubElement(
                xmlElement,
                'CustomGoal',
            ).text = element.otherSceneField1
        if element.otherSceneField2:
            ET.SubElement(
                xmlElement,
                'CustomConflict',
            ).text = element.otherSceneField2
        if element.otherSceneField3:
            ET.SubElement(
                xmlElement,
                'CustomOutcome',
            ).text = element.otherSceneField3

        # Character fields names.
        if element.crField1:
            ET.SubElement(
                xmlElement,
                'CustomChrBio',
            ).text = element.crField1
        if element.crField2:
            ET.SubElement(
                xmlElement,
                'CustomChrGoals',
            ).text = element.crField2

        # Word count start/Word target.
        if element.wordCountStart:
            ET.SubElement(
                xmlElement,
                'WordCountStart',
            ).text = str(element.wordCountStart)
        if element.wordTarget:
            ET.SubElement(
                xmlElement,
                'WordTarget',
            ).text = str(element.wordTarget)

        # Reference date.
        if element.referenceDate:
            ET.SubElement(
                xmlElement,
                'ReferenceDate',
            ).text = element.referenceDate


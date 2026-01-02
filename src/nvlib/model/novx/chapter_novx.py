"""Provide a class for novelibre chapter XML import and export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from nvlib.model.novx.basic_element_notes_novx import BasicElementNotesNovx


class ChapterNovx(BasicElementNotesNovx):

    def import_data(self, element, xmlElement):
        super().import_data(element, xmlElement)
        typeStr = xmlElement.get('type', '0')
        if typeStr in ('0', '1'):
            element.chType = int(typeStr)
        else:
            element.chType = 1
        chLevel = xmlElement.get('level', '2')
        if chLevel in ('1', '2'):
            element.chLevel = int(chLevel)
        else:
            element.chLevel = 2
        element.isTrash = xmlElement.get('isTrash', None) == '1'
        element.noNumber = xmlElement.get('noNumber', None) == '1'
        element.hasEpigraph = xmlElement.get('hasEpigraph', None) == '1'

    def export_data(self, element, xmlElement):
        super().export_data(element, xmlElement)
        if element.chType:
            xmlElement.set('type', str(element.chType))
        if element.chLevel == 1:
            xmlElement.set('level', '1')
        if element.isTrash:
            xmlElement.set('isTrash', '1')
        if element.noNumber:
            xmlElement.set('noNumber', '1')
        if element.hasEpigraph:
            xmlElement.set('hasEpigraph', '1')

"""Provide classes for upgrading novx XML files.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re
from xml import sax

from nvlib.model.data.id_generator import new_id
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


class NovxUpgrader:
    """Upgrades outdated novx files to DTD version 1.11."""

    @classmethod
    def upgrade_file_version(
        cls,
        xmlRoot,
        fileMajorVersion,
        fileMinorVersion,
    ):
        # Convert the data from legacy files
        # Return the version number adjusted, if applicable.
        if fileMajorVersion == 1:
            if fileMinorVersion < 7:
                cls._upgrade_to_1_7(xmlRoot)
                fileMinorVersion = 7
            if fileMinorVersion < 8:
                cls._upgrade_to_1_8(xmlRoot)
                fileMinorVersion = 8
            if fileMinorVersion < 11:
                cls._upgrade_to_1_11(xmlRoot)
                fileMinorVersion = 11
        return fileMajorVersion, fileMinorVersion

    @classmethod
    def _upgrade_to_1_7(cls, xmlRoot):
        # Determine the viewpoints from the section character lists.
        # Update xmlRoot.
        for xmlSection in xmlRoot.iter('SECTION'):
            xmlCharacters = xmlSection.find('Characters')
            if xmlCharacters is not None:
                crIds = xmlCharacters.get('ids', None)
                if crIds is not None:
                    crId = crIds.split(' ')[0]
                    ET.SubElement(
                        xmlSection,
                        'Viewpoint',
                        attrib={'id':crId},
                    )

    @classmethod
    def _upgrade_to_1_8(cls, xmlRoot):
        # Convert epigraphs into sections and set the chapter's flag.
        allSections = []

        for xmlSection in xmlRoot.iter(tag='SECTION'):
            allSections.append(xmlSection.attrib['id'])

        xmlChapters = xmlRoot.find('CHAPTERS')
        if xmlChapters is None:
            return

        for xmlChapter in xmlChapters.iterfind('CHAPTER'):
            xmlEpigraph = xmlChapter.find('Epigraph')
            xmlEpigraphSrc = xmlChapter.find('EpigraphSrc')
            if xmlEpigraph is not None:
                xmlChapter.remove(xmlEpigraph)

                # Set the chapter attribute.
                xmlChapter.set('hasEpigraph', '1')

                # Create a new section for the epigraph.
                xmlNewSection = ET.Element('SECTION')

                # Generate section ID.
                newId = new_id(allSections, SECTION_PREFIX)
                allSections.append(newId)
                xmlNewSection.set('id', newId)

                # Auto-generate a generic title.
                ET.SubElement(xmlNewSection, 'Title').text = _('Epigraph')

                # Use the Epigraph element as content.
                xmlNewSection.append(xmlEpigraph)
                xmlEpigraph.tag = 'Content'

                # Generate the Desc element from the EpigraphSrc text.
                if xmlEpigraphSrc is not None:
                    xmlChapter.remove(xmlEpigraphSrc)
                    xmlNewSection.append(
                        ET.fromstring(
                           f'<Desc><p>{xmlEpigraphSrc.text}</p></Desc>'
                        )
                    )

                # Tntegrate the new section.
                xmlChapter.insert(0, xmlNewSection)

    @classmethod
    def _upgrade_to_1_11(cls, xmlRoot):
        # Remove attributes from the paragraphs.
        for xmlSection in xmlRoot.iter(tag='SECTION'):
            xmlContent = xmlSection.find('Content')
            if xmlContent is None:
                continue

            xmlStr = ET.tostring(
                xmlContent,
                encoding='utf-8',
            ).decode('utf-8')
            if not re.search(r'<[ph]\d* [sx]', xmlStr):
                # the section doesn't contain any paragraphs with attributes
                continue

            # Process deprecated attributes
            converter = Converter1_11()
            converter.feed(xmlStr)
            xmlStr = converter.get_result()
            xmlSection.remove(xmlContent)
            xmlSection.append(ET.fromstring(xmlStr))


class Converter1_11(sax.ContentHandler):
    # Replaces "quotations" style paragraphs with h4.
    # Adds a span for the paragraph's language, if needed.

    def feed(self, xmlString):
        self._tags = []
        self._xmlLines = []
        sax.parseString(xmlString, self)

    def get_result(self):
        while self._tags:
            self._xmlLines.append(f'</{self._tags.pop()}>')
        return ''.join(self._xmlLines)

    def characters(self, content):
        self._xmlLines.append(content)

    def endElement(self, name):
        tags = self._tags.pop()
        for name in tags:
            self._xmlLines.append(f'</{name}>')

    def startElement(self, name, attrs):
        if not attrs.items():
            # No attributes -> preserve original tag.
            self._xmlLines.append(f'<{name}>')
            self._tags.append([name])
            return

        if name == 'span':
            # Preserve span with original attribute.
            attrKey, attrValue = attrs.items()[0]
            self._xmlLines.append(f'<{name} {attrKey}="{attrValue}">')
            self._tags.append([name])
            return

        # Remove attributes and change tag.
        language = None
        for attribute in attrs.items():
            attrKey, attrValue = attribute
            if attrKey == 'style' and attrValue == 'quotations':
                name = 'h4'
            elif attrKey == 'xml:lang':
                language = attrValue
        tags = []
        self._xmlLines.append(f'<{name}>')
        if language is not None:
            self._xmlLines.append(f'<span xml:lang="{language}">')
            tags.append('span')
        tags.append(name)
        self._tags.append(tags)


"""Provide classes for upgrading novx XML files.

Copyright (c) 2026 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.id_generator import new_id
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


class NovxUpgrader:
    """Upgrades outdated novx files to DTD version 1.8."""

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


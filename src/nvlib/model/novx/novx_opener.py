"""Provide a class for opening and preprocessing novx XML files.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.id_generator import new_id
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


class NovxOpener:
    """novx XML data reader, verifier, and preprocessor."""

    @classmethod
    def get_xml_root(cls, filePath, majorVersion, minorVersion):
        """Return a reference to the XML root of the novx file at filePath.
        
        majorVersion and minorVersion are integers.
        Check the file version and preprocess the data, if applicable.
        """
        try:
            xmlTree = ET.parse(filePath)
        except Exception as ex:
            normPath = norm_path(filePath)
            raise RuntimeError(
                f'{_("Cannot process file")}: "{normPath}" - {str(ex)}'
            )

        xmlRoot = xmlTree.getroot()
        if xmlRoot.tag != 'novx':
            msg = _("No valid xml root element found in file")
            raise RuntimeError(f'{msg}: "{norm_path(filePath)}".')

        fileMajorVersion, fileMinorVersion = cls._get_file_version(
            xmlRoot,
            filePath,
        )
        fileMajorVersion, fileMinorVersion = cls._upgrade_file_version(
            xmlRoot,
            fileMajorVersion,
            fileMinorVersion,
        )
        cls._check_version(
            fileMajorVersion,
            fileMinorVersion,
            filePath,
            majorVersion,
            minorVersion,
        )
        return xmlRoot

    @classmethod
    def _check_version(
            cls,
            fileMajorVersion,
            fileMinorVersion,
            filePath,
            majorVersion,
            minorVersion,
    ):
        # Raise an exception if the file
        # is not compatible with the supported DTD.
        if fileMajorVersion > majorVersion:
            msg = _('The project "{}" was created with a newer novelibre version.')
            raise RuntimeError(msg.format(norm_path(filePath)))

        if fileMajorVersion < majorVersion:
            msg = _('The project "{}" was created with an outdated novelibre version.')
            raise RuntimeError(msg.format(norm_path(filePath)))

        if fileMinorVersion > minorVersion:
            msg = _('The project "{}" was created with a newer novelibre version.')
            raise RuntimeError(msg.format(norm_path(filePath)))

    @classmethod
    def _upgrade_file_version(
            cls,
            xmlRoot,
            fileMajorVersion,
            fileMinorVersion,
    ):
        # Convert the data from legacy files
        # Return the version number adjusted, if applicable.
        if fileMajorVersion == 1 and fileMinorVersion < 7:
            cls._upgrade_to_1_7(xmlRoot)
            fileMinorVersion = 7
        if fileMajorVersion == 1 and fileMinorVersion < 8:
            cls._upgrade_to_1_8(xmlRoot)
            fileMinorVersion = 8
        return fileMajorVersion, fileMinorVersion

    @classmethod
    def _get_file_version(cls, xmlRoot, filePath):
        # Return the major and minor file version as integers.
        # Raise an exception if there is none.
        # Update xmlRoot.
        try:
            (
                fileMajorVersionStr,
                fileMinorVersionStr
            ) = xmlRoot.attrib['version'].split('.')
            fileMajorVersion = int(fileMajorVersionStr)
            fileMinorVersion = int(fileMinorVersionStr)
        except (KeyError, ValueError):
            msg = _("No valid version found in file")
            raise RuntimeError(msg.format(norm_path(filePath)))

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


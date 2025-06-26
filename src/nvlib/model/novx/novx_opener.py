"""Provide a class for opening and preprocessing novx XML files.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import Error
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
            raise Error(
                f'{_("Cannot process file")}: "{normPath}" - {str(ex)}'
            )

        xmlRoot = xmlTree.getroot()
        if xmlRoot.tag != 'novx':
            msg = _("No valid xml root element found in file")
            raise Error(f'{msg}: "{norm_path(filePath)}".')

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
            raise Error(msg.format(norm_path(filePath)))

        if fileMajorVersion < majorVersion:
            msg = _('The project "{}" was created with an outdated novelibre version.')
            raise Error(msg.format(norm_path(filePath)))

        if fileMinorVersion > minorVersion:
            msg = _('The project "{}" was created with a newer novelibre version.')
            raise Error(msg.format(norm_path(filePath)))

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
            raise Error(msg.format(norm_path(filePath)))

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


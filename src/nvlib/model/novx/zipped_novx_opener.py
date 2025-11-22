"""Provide a class for opening and preprocessing zipped novx XML files.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import zipfile

from nvlib.model.novx.novx_opener import NovxOpener
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


class ZippedNovxOpener(NovxOpener):
    """novx XML data reader, verifier, and preprocessor."""

    NOVX_EXTENSIONS = [
        '.novx',
    ]
    ZIP_EXTENSIONS = [
        '.zip',
    ]

    @classmethod
    def get_xml_root(cls, filePath, majorVersion, minorVersion):
        """Return a reference to the XML root of the novx file at filePath.
        
        majorVersion and minorVersion are integers.
        Check the file version and preprocess the data, if applicable.
        """
        __, extension = os.path.splitext(filePath)
        try:
            if not extension in cls.ZIP_EXTENSIONS:
                raise RuntimeError('File type is not supported')

            with zipfile.ZipFile(filePath, 'r') as z:
                fileNames = z.namelist()
                xmlRoot = None
                for fileName in fileNames:
                    __, extension = os.path.splitext(fileName)
                    if extension in cls.NOVX_EXTENSIONS:
                        with z.open(fileName, 'r') as f:
                            xmlStr = f.read()
                        xmlRoot = ET.fromstring(xmlStr)
                        break

                if xmlRoot is None:
                    raise RuntimeError('File type is not supported')

        except Exception as ex:
            normPath = norm_path(filePath)
            raise RuntimeError(
                f'{_("Cannot process file")}: "{normPath}" - {str(ex)}'
            )

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


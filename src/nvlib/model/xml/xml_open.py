"""Provide a helper module for xml file operation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import Error
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


def get_xml_root(filePath):
    try:
        xmlTree = ET.parse(filePath)
    except Exception as ex:
        raise Error(f'{_("Cannot process file")}: "{norm_path(filePath)}" - {str(ex)}')

    return xmlTree.getroot()

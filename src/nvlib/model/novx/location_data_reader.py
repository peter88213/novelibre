"""Provide an XML location data file reader class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.novx.novx_file import NovxFile
from nvlib.novx_globals import _
import xml.etree.ElementTree as ET


class LocationDataReader(NovxFile):
    """XML location data file reader."""
    DESCRIPTION = _('XML location data file')
    EXTENSION = '.xml'

    def read(self):
        """Parse the xml files and get the instance variables.
        
        Overrides the superclass method.
        """
        tree = ET.parse(self.filePath)
        root = ET.Element('ROOT')
        root.append(tree.getroot())
        self._read_locations(root)


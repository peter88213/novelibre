"""Provide a class for novelibre XML data files.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.model.novx.novx_file import NovxFile
from nvlib.novx_globals import DATA_SUFFIX
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


class DataWriter(NovxFile):
    """novelibre XML data files representation.
       
    novelibre can import or export characters, locations and items as separate
    xml files. This class represents a set of three xml files generated from
    a novelibre project.
    """
    DESCRIPTION = _('novelibre XML data files')
    EXTENSION = '.xml'
    SUFFIX = DATA_SUFFIX

    XML_HEADER = '<?xml version="1.0" encoding="utf-8"?>\n'

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath, **kwargs)
        path, __ = os.path.splitext(filePath)
        self._dataFiles = dict(
            CHARACTERS=f'{path}_Characters.xml',
            LOCATIONS=f'{path}_Locations.xml',
            ITEMS=f'{path}_Items.xml',
            ARCS=f'{path}_Plotlines.xml',
        )

    def _postprocess_xml_file(self, filePath):
        """Postprocess three xml files created by ElementTree.
        
        Positional argument:
            filePath: str -- not used by this method.
            
        Postprocess and write the xml data files.        
        Extends the superclass method.
        """
        for xmlBranch in self._dataFiles:
            super()._postprocess_xml_file(self._dataFiles[xmlBranch])

    def _write_element_tree(self, xmlProject):
        """Save the characters/locations/items subtrees as separate xml files.
        
        Positional argument:
            xmlProject -- NovxFile instance.
            
        Extract the characters/locations/items xml subtrees 
        from a novelibre project.
        Generate the xml file paths from the .novx path and 
        write each xmlBranch to an xml file.
        Raise the "RuntimeError" exception in case of error. 
        """
        for xmlBranch in self._dataFiles:
            elementSubtree = xmlProject.xmlTree.find(xmlBranch)
            elementTree = ET.ElementTree(elementSubtree)
            try:
                elementTree.write(
                    self._dataFiles[xmlBranch],
                    xml_declaration=False,
                    encoding='utf-8',
                )
            except(PermissionError):
                raise RuntimeError(
                    f'{_("File is write protected")}: '
                    f'"{norm_path(self._dataFiles[xmlBranch])}".'
                )


"""Provide a base class for ODT documents that contain formatted text.

Copyright (c) 2024-2026 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.content_splitter import ContentSplitter
from nvlib.model.odt.odt_reader import OdtReader
from nvlib.model.xml.xml_element_joiner import XmlElementJoiner


class OdtRFormatted(OdtReader):
    """ODT file reader.
    
    Provide methods and data for processing chapters with formatted text.
    """
    SPLITTER = ContentSplitter

    def __init__(self, filePath, **kwargs):
        super().__init__(filePath)
        self.splitter = self.SPLITTER()
        self.xmlElementJoiner = XmlElementJoiner()

    def read(self):
        """Parse the file and get the instance variables.
        
        Extends the superclass method.
        """
        self.novel.languages = []
        super().read()

        # Split sections, if necessary.
        self.projectStructureModified = self.splitter.split_sections(
            self.novel
        )

    def join_consecutive_xml_elements(self, xmlText):
        xmlText = self.xmlElementJoiner.join_consecutive_formatting(xmlText)
        xmlText = self.xmlElementJoiner.join_consecutive_spans(xmlText)
        return xmlText

"""Provide a base class for ODT documents containing text that is formatted in novelibre.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.splitter import Splitter
from nvlib.model.odt.odt_reader import OdtReader


class OdtRFormatted(OdtReader):
    """ODT file reader.
    
    Provide methods and data for processing chapters with formatted text.
    """

    def read(self):
        """Parse the file and get the instance variables.
        
        Extends the superclass method.
        """
        self.novel.languages = []
        super().read()

        # Split sections, if necessary.
        sectionSplitter = Splitter()
        self.sectionsSplit = sectionSplitter.split_sections(self.novel)


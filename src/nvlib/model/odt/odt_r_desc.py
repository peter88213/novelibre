"""Provide a base class for ODT documents that contain descriptive text.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.desc_splitter import DescSplitter
from nvlib.model.odt.odt_reader import OdtReader


class OdtRDesc(OdtReader):
    """ODT file reader.
    
    Provide methods and data for processing chapters with formatted text.
    """

    _SEPARATORS = {
        'h1': f'{DescSplitter.PART_SEPARATOR} ',
        'h2': f'{DescSplitter.CHAPTER_SEPARATOR} ',
        'h3': f'{DescSplitter.SECTION_SEPARATOR} ',
        'h4': f'{DescSplitter.APPENDED_SECTION_SEPARATOR} ',
    }

    def read(self):
        """Parse the file and get the instance variables.
        
        Extends the superclass method.
        """
        self.novel.languages = []
        super().read()

        # Split sections, if necessary.
        sectionSplitter = DescSplitter()
        self.sectionsSplit = sectionSplitter.split_sections(self.novel)


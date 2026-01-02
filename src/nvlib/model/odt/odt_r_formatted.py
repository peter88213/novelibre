"""Provide a base class for ODT documents that contain formatted text.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.splitter import Splitter
from nvlib.model.odt.odt_reader import OdtReader


class OdtRFormatted(OdtReader):
    """ODT file reader.
    
    Provide methods and data for processing chapters with formatted text.
    """

    _SEPARATORS = {
        'h1': f'{Splitter.PART_SEPARATOR} ',
        'h2': f'{Splitter.CHAPTER_SEPARATOR} ',
        'h3': f'{Splitter.SECTION_SEPARATOR} ',
        'h4': f'{Splitter.APPENDED_SECTION_SEPARATOR} ',
    }

    def read(self):
        """Parse the file and get the instance variables.
        
        Extends the superclass method.
        """
        self.novel.languages = []
        super().read()

        # Split sections, if necessary.
        sectionSplitter = Splitter()
        self.sectionsSplit = sectionSplitter.split_sections(self.novel)

    def _remove_redundant_tags(self, text):
        for tag in(
            'em',
            'strong',
        ):
            text = text.replace(f'</{tag}><{tag}>', '')
        return text

"""Provide a class for ODT item invisibly tagged descriptions import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_reader import OdtReader
from nvlib.novx_globals import ITEMS_SUFFIX
from nvlib.nv_locale import _


class OdtRItems(OdtReader):
    """ODT item descriptions file reader.

    Import a item sheet with invisibly tagged descriptions.
    """
    DESCRIPTION = _('Item descriptions')
    SUFFIX = ITEMS_SUFFIX

    def __init__(self, filePath, **kwargs):
        """Initialize local instance variables for parsing.

        Positional arguments:
            filePath: str -- path to the file 
            represented by the Novel instance.
            
        The ODT parser works like a state machine. 
        The item ID must be saved between the transitions.         
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._itId = None

    def handle_data(self, data):
        """collect data within item sections.

        Positional arguments:
            data: str -- text to be stored. 
        
        Overrides the superclass method.
        """
        if self._itId is None:
            return

        self._lines.append(data)

    def handle_endtag(self, tag):
        """Recognize the end of the item section and save data.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.

        Overrides the superclass method.
        """
        if self._itId is None:
            return

        if tag == 'div':
            self.novel.items[self._itId].desc = ''.join(self._lines).rstrip()
            self._lines.clear()
            self._itId = None
            return

        if tag == 'p':
            self._lines.append('\n')


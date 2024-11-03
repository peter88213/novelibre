"""Provide a class for ODT item invisibly tagged descriptions import.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re

from nvlib.model.data.world_element import WorldElement
from nvlib.novx_globals import ITEMS_SUFFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import _
from nvlib.model.odt.odt_reader import OdtReader


class OdtRItems(OdtReader):
    """ODT item descriptions file reader.

    Import a item sheet with invisibly tagged descriptions.
    """
    DESCRIPTION = _('Item descriptions')
    SUFFIX = ITEMS_SUFFIX

    def __init__(self, filePath, **kwargs):
        """Initialize local instance variables for parsing.

        Positional arguments:
            filePath: str -- path to the file represented by the Novel instance.
            
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
            self._lines = []
            self._itId = None
            return

        if tag == 'p':
            self._lines.append('\n')

    def handle_starttag(self, tag, attrs):
        """Identify items.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes found inside the tag’s <> brackets.
        
        Overrides the superclass method.
        """
        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].startswith('ItID'):
                    self._itId = f"{ITEM_PREFIX}{re.search('[0-9]+', attrs[0][1]).group()}"
                    if not self._itId in self.novel.items:
                        self.novel.tree.append(IT_ROOT, self._itId)
                        self.novel.items[self._itId] = WorldElement()
            return

        if tag == 's':
            self._lines.append(' ')

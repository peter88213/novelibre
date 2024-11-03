"""Provide a class for ODT invisibly tagged location descriptions import.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re

from nvlib.model.data.world_element import WorldElement
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATIONS_SUFFIX
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import _
from nvlib.model.odt.odt_reader import OdtReader


class OdtRLocations(OdtReader):
    """ODT location descriptions file reader.

    Import a location sheet with invisibly tagged descriptions.
    """
    DESCRIPTION = _('Location descriptions')
    SUFFIX = LOCATIONS_SUFFIX

    def __init__(self, filePath, **kwargs):
        """Initialize local instance variables for parsing.

        Positional arguments:
            filePath: str -- path to the file represented by the Novel instance.
            
        The ODT parser works like a state machine. 
        The location ID must be saved between the transitions.         
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._lcId = None

    def handle_data(self, data):
        """collect data within location sections.
        
        Positional arguments:
            data: str -- text to be stored. 
        
        Overrides the superclass method.
        """
        if self._lcId is None:
            return

        self._lines.append(data)

    def handle_endtag(self, tag):
        """Recognize the end of the location section and save data.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.

        Overrides the superclass method.
        """
        if self._lcId is None:
            return

        if tag == 'div':
            self.novel.locations[self._lcId].desc = ''.join(self._lines).rstrip()
            self._lines = []
            self._lcId = None
            return

        if tag == 'p':
            self._lines.append('\n')

    def handle_starttag(self, tag, attrs):
        """Identify locations.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes found inside the tag’s <> brackets.
        
        Overrides the superclass method.
        """
        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].startswith('LcID'):
                    self._lcId = f"{LOCATION_PREFIX}{re.search('[0-9]+', attrs[0][1]).group()}"
                    if not self._lcId in self.novel.locations:
                        self.novel.tree.append(LC_ROOT, self._lcId)
                        self.novel.locations[self._lcId] = WorldElement()
            return

        if tag == 's':
            self._lines.append(' ')

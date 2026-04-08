"""Provide a class for ODT invisibly tagged project notes import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_reader import OdtReader
from nvlib.novx_globals import PROJECTNOTES_SUFFIX
from nvlib.nv_locale import _


class OdtRProjectNotes(OdtReader):
    """ODT project notes file reader.

    Import project notest with invisible tags.
    """
    DESCRIPTION = _('Project notes')
    SUFFIX = PROJECTNOTES_SUFFIX

    def __init__(self, filePath, **kwargs):
        """Initialize local instance variables for parsing.

        Positional arguments:
            filePath: str -- path to the file 
            represented by the Novel instance.
            
        The ODT parser works like a state machine. 
        The project note ID must be saved between the transitions.         
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._pnId = None

    def handle_data(self, data):
        """collect data within project notes sections.

        Positional arguments:
            data: str -- text to be stored. 
        
        Overrides the superclass method.
        """
        if self._pnId is None:
            return

        self._lines.append(data)

    def handle_endtag(self, tag):
        """Recognize the end of the project notes section and save data.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.

        Overrides the superclass method.
        """
        if self._pnId is None:
            return

        if tag == 'div':
            self.novel.projectNotes[self._pnId].desc = ''.join(self._lines).rstrip()
            self._lines.clear()
            self._pnId = None
            return

        if tag == 'p':
            self._lines.append('\n')


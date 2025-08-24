"""Provide a class for ODT invisibly tagged character descriptions import.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re

from nvlib.model.data.character import Character
from nvlib.model.odt.odt_reader import OdtReader
from nvlib.novx_globals import CHARACTERS_SUFFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CR_ROOT
from nvlib.nv_locale import _


class OdtRCharacters(OdtReader):
    """ODT character descriptions file reader.

    Import a character sheet with invisibly tagged descriptions.
    """
    DESCRIPTION = _('Character descriptions')
    SUFFIX = CHARACTERS_SUFFIX

    def __init__(self, filePath, **kwargs):
        """Initialize local instance variables for parsing.

        Positional arguments:
            filePath: str -- path to the file 
            represented by the Novel instance.
            
        The ODT parser works like a state machine. 
        Character ID and section title must be saved 
        between the transitions.         
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._crId = None
        self._section = None

    def handle_data(self, data):
        """collect data within character sections.

        Positional arguments:
            data: str -- text to be stored. 
        
        Overrides the superclass method.
        """
        if self._section is None:
            return

        self._lines.append(data)

    def handle_endtag(self, tag):
        """Recognize the end of the character section and save data.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.

        Overrides the superclass method.
        """
        if self._crId is None:
            return

        if tag == 'div':

            if self._section == 'desc':
                self.novel.characters[self._crId].desc = ''.join(
                    self._lines).rstrip()
                self._lines.clear()
                self._section = None
                return

            if self._section == 'bio':
                self.novel.characters[self._crId].bio = ''.join(
                    self._lines).rstrip()
                self._lines.clear()
                self._section = None
                return

            if self._section == 'goals':
                self.novel.characters[self._crId].goals = ''.join(
                    self._lines).rstrip()
                self._lines.clear()
                self._section = None
                return

            if self._section == 'field2':
                self.novel.characters[self._crId].field2 = ''.join(
                    self._lines).rstrip()
                self._lines.clear()
                self._section = None
                return

            if self._section == 'notes':
                self.novel.characters[self._crId].notes = ''.join(
                    self._lines).rstrip()
                self._lines.clear()
                self._section = None
            return

        if tag == 'p':
            self._lines.append('\n')

    def handle_starttag(self, tag, attrs):
        """Identify characters with subsections.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes 
                     found inside the tag’s <> brackets.
        
        Overrides the superclass method.
        """
        if tag == 'div':
            if attrs[0][0] == 'id':

                if attrs[0][1].startswith('desc'):
                    self._crId = (
                        f"{CHARACTER_PREFIX}"
                        f"{re.search('[0-9]+', attrs[0][1]).group()}"
                    )
                    if not self._crId in self.novel.characters:
                        self.novel.tree.append(CR_ROOT, self._crId)
                        self.novel.characters[self._crId] = Character()
                    self._section = 'desc'
                    return

                if attrs[0][1].startswith('bio'):
                    self._section = 'bio'
                    return

                if attrs[0][1].startswith('goals'):
                    self._section = 'goals'
                    return

                if attrs[0][1].startswith('notes'):
                    self._section = 'notes'
            return

        if tag == 's':
            self._lines.append(' ')

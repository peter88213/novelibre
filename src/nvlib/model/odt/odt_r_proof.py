"""Provide a class for ODT visibly tagged chapters and sections import.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re

from nvlib.model.data.splitter import Splitter
from nvlib.model.odt.odt_r_formatted import OdtRFormatted
from nvlib.novx_globals import Error
from nvlib.novx_globals import PROOF_SUFFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


class OdtRProof(OdtRFormatted):
    """ODT proof reading file reader.

    Import a manuscript with visibly tagged chapters and sections.
    """
    DESCRIPTION = _('Tagged manuscript for proofing')
    SUFFIX = PROOF_SUFFIX

    def __init__(self, filePath, **kwargs):
        """Initialize the ODT parser and local instance variables for parsing.
        
        Positional arguments:
            filePath: str -- path to the file represented by the File instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            

        The ODT parser works like a state machine. 
        Section ID, chapter ID and processed lines must be saved between the transitions.         
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._content = False

    def handle_data(self, data):
        """Parse the paragraphs and build the document structure.      

        Positional arguments:
            data: str -- text to be parsed. 
        
        Overrides the superclass method.
        """
        try:
            if f'[{SECTION_PREFIX}' in data:
                self._scId = f"{SECTION_PREFIX}{re.search('[0-9]+', data).group()}"
                self._lines.clear()
                return

            if f'[/{SECTION_PREFIX}]' in data:
                if self._scId in self.novel.sections:
                    self._lines.pop()
                    # remove the paragraph tag
                    text = ''.join(self._lines)
                    self.novel.sections[self._scId].sectionContent = text.strip()
                    self._lines.clear()
                self._scId = None
                self._content = False
                return

            if self._scId is not None:
                self._lines.append(data)
        except:
            raise Error(f'{_("Corrupt marker")}: "{data}"')

    def handle_endtag(self, tag):
        """Recognize the paragraph's end.      
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.

        Overrides the superclass method.
        """
        if tag == 'p':
            if self._content:
                self._lines.append('</p>')
                return

            if self._scId:
                self._content = True
            return

        if tag in ('em', 'strong', 'comment', 'creator', 'date', 'note', 'note-citation', 'ul', 'li'):
            self._lines.append(f'</{tag}>')
            return

        if tag == 'lang':
            self._lines.append('</span>')
            return

        if tag == 'div':
            text = ''.join(self._lines)
            self.novel.sections[self._scId].sectionContent = text
            self._lines.clear()
            self._scId = None
            return

        if tag == 'h1':
            self._lines.append('\n')
            return

        if tag == 'h2':
            self._lines.append('\n')

    def handle_starttag(self, tag, attrs):
        """Recognize the paragraph's beginning.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes found inside the tag’s <> brackets.
        
        Overrides the superclass method.
        """
        if self._content:

            if tag == 'p':
                attributes = ''
                try:
                    for att in attrs:
                        attributes = f'{attributes} {att[0]}="{att[1]}"'
                        if att[0] == 'lang':
                            if not att[1] in self.novel.languages:
                                self.novel.languages.append(att[1])
                except:
                    pass
                self._lines.append(f'<p{attributes}>')
                return

            if tag in('em', 'strong', 'comment', 'creator', 'date', 'note-citation', 'ul', 'li'):
                self._lines.append(f'<{tag}>')
                return

            if tag == 'lang':
                if attrs[0][0] == 'lang':
                    if not attrs[0][1] in self.novel.languages:
                        self.novel.languages.append(attrs[0][1])
                    self._lines.append(f'<span xml:lang="{attrs[0][1]}">')
                return

            if tag == 'h2':
                self._lines.append(f'{Splitter.CHAPTER_SEPARATOR} ')
                return

            if tag == 'h1':
                self._lines.append(f'{Splitter.PART_SEPARATOR} ')
                return

            if tag == 's':
                self._lines.append(' ')
                return

            if tag == 'note':
                attributes = ''
                for att in attrs:
                    attributes = f'{attributes} {att[0]}="{att[1]}"'
                self._lines.append(f'<note {attributes}>')
                return

            if tag == 'body':
                for attr in attrs:
                    if attr[0] == 'language':
                        if attr[1]:
                            self.novel.languageCode = attr[1]
                    elif attr[0] == 'country':
                        if attr[1]:
                            self.novel.countryCode = attr[1]


"""Provide a class for ODT 'work in progress' import.

Conventions:
A work in progress has no third level heading.

-   Heading 1 -- New chapter title (beginning a new section).
-   Heading 2 -- New chapter title.
-   * * * -- Section divider (not needed for the first section in a chapter).
-   Comments right at the section beginning are considered section titles.
-   All other text is considered section content.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re
from xml.sax.saxutils import unescape

from nvlib.model.data.chapter import Chapter
from nvlib.model.data.section import Section
from nvlib.model.odt.odt_r_formatted import OdtRFormatted
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


class OdtRImport(OdtRFormatted):
    """ODT 'work in progress' file reader.

    Import untagged chapters and sections.
    """
    DESCRIPTION = _('Work in progress')
    SUFFIX = ''
    _SCENE_DIVIDER = '* * *'
    _LOW_WORDCOUNT = 10

    def __init__(self, filePath, **kwargs):
        """Initialize local instance variables for parsing.

        Positional arguments:
            filePath: str -- path to the file represented by the Novel instance.
            
        The ODT parser works like a state machine. 
        Chapter and section count must be saved between the transitions.         
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._chCount = 0
        self._scCount = 0

    def handle_data(self, data):
        """Collect data within section sections.

        Positional arguments:
            data: str -- text to be stored. 
        
        Overrides the superclass method.
        """
        if self._scId is not None and self._SCENE_DIVIDER in data:
            self._scId = None
            return

        self._lines.append(data)

    def handle_endtag(self, tag):
        """Recognize the paragraph's end.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.

        Overrides the superclass method.
        """
        if tag == 'p':
            self._lines.append('</p>')
            if self._scId is None:
                return

            sectionText = ''.join(self._lines).rstrip()
            self.novel.sections[self._scId].sectionContent = sectionText
            if self.novel.sections[self._scId].wordCount < self._LOW_WORDCOUNT:
                self.novel.sections[self._scId].status = 1
                # Outline
            else:
                self.novel.sections[self._scId].status = 2
                # Draft
            return

        if tag in ('em', 'strong', 'comment', 'creator', 'date', 'note', 'note-citation', 'ul', 'li'):
            self._lines.append(f'</{tag}>')
            return

        if tag == 'lang':
            self._lines.append('</span>')
            return

        if tag in ('h1', 'h2'):
            self.novel.chapters[self._chId].title = unescape(re.sub('<.*?>', '', ''.join(self._lines)))
            self._lines = []
            return

        if tag == 'title':
            self.novel.title = ''.join(self._lines)

    def handle_starttag(self, tag, attrs):
        """Recognize the paragraph's beginning.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes found inside the tag’s <> brackets.
        
        Overrides the superclass method.
        """
        if tag == 'p':
            if self._scId is None and self._chId is not None:
                self._lines = []
                self._scCount += 1
                self._scId = f'{SECTION_PREFIX}{self._scCount}'
                self.novel.sections[self._scId] = Section(title=f'{_("Section")} {self._scCount}',
                                                      scType=0,
                                                      scene=0,
                                                      status=1,
                                                      )
                self.novel.tree.append(self._chId, self._scId)
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

        if tag == 'note':
            attributes = ''
            for att in attrs:
                attributes = f'{attributes} {att[0]}="{att[1]}"'
            self._lines.append(f'<note {attributes}>')
            return

        if tag in ('h1', 'h2'):
            self._scId = None
            self._lines = []
            self._chCount += 1
            self._chId = f'{CHAPTER_PREFIX}{self._chCount}'
            self.novel.chapters[self._chId] = Chapter(chType=0)
            self.novel.tree.append(CH_ROOT, self._chId)
            if tag == 'h1':
                self.novel.chapters[self._chId].chLevel = 1
            else:
                self.novel.chapters[self._chId].chLevel = 2
            return

        if tag == 'div':
            self._scId = None
            self._chId = None
            return

        if tag == 'meta':
            if attrs[0][1] == 'author':
                self.novel.authorName = attrs[1][1]
            if attrs[0][1] == 'description':
                self.novel.desc = attrs[1][1]
            return

        if tag == 'title':
            self._lines = []
            return

        if tag == 'body':
            for attr in attrs:
                if attr[0] == 'language':
                    if attr[1]:
                        self.novel.languageCode = attr[1]
                elif attr[0] == 'country':
                    if attr[1]:
                        self.novel.countryCode = attr[1]
            return

        if tag == 's':
            self._lines.append(' ')

    def read(self):
        """Parse the file and get the instance variables.
        
        Initialize the languages list.
        Extends the superclass method.
        """
        self.novel.languages = []
        super().read()


"""Provide a class for ODT invisibly tagged chapters and sections import.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.splitter import Splitter
from nvlib.model.odt.odt_r_formatted import OdtRFormatted
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.nv_locale import _


class OdtRManuscript(OdtRFormatted):
    """ODT manuscript file reader.

    Import a manuscript with invisibly tagged chapters and sections.
    """
    DESCRIPTION = _('Editable manuscript')
    SUFFIX = MANUSCRIPT_SUFFIX

    def handle_data(self, data):
        """Collect data within section sections.

        Positional arguments:
            data: str -- text to be stored. 
        
        Overrides the superclass method.
        """
        if self._scId is None:
            return

        self._lines.append(data)

    def handle_endtag(self, tag):
        """Recognize the end of the section section and save data.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.

        Overrides the superclass method.
        """
        if self._scId is None:
            return

        if tag == 'p':
            self._lines.append('</p>')
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
            self._lines = []
            self._scId = None
            return

        if tag == 'h1':
            self._lines.append('\n')
            return

        if tag == 'h2':
            self._lines.append('\n')

    def handle_starttag(self, tag, attrs):
        """Identify sections and chapters.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the attributes found inside the tag’s <> brackets.
        
        Extends the superclass method by processing inline chapter and section dividers.
        """
        super().handle_starttag(tag, attrs)

        if self._scId is None:
            if tag == 'body':
                for attr in attrs:
                    if attr[0] == 'language':
                        if attr[1]:
                            self.novel.languageCode = attr[1]
                    elif attr[0] == 'country':
                        if attr[1]:
                            self.novel.countryCode = attr[1]
            return

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

        if tag == 'note':
            attributes = ''
            for att in attrs:
                attributes = f'{attributes} {att[0]}="{att[1]}"'
            self._lines.append(f'<note {attributes}>')


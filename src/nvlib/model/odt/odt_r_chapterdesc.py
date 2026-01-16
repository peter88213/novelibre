"""Provide a class for html invisibly tagged chapter descriptions import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.chapter_splitter import ChapterSplitter
from nvlib.model.odt.odt_r_desc import OdtRDesc
from nvlib.novx_globals import CHAPTERS_SUFFIX
from nvlib.nv_locale import _


class OdtRChapterDesc(OdtRDesc):
    """ODT chapter summaries file reader.

    Import a brief synopsis with invisibly tagged chapter descriptions.
    """
    DESCRIPTION = _('Chapter descriptions')
    SUFFIX = CHAPTERS_SUFFIX

    SPLITTER = ChapterSplitter

    def handle_data(self, data):
        """Collect data within chapter sections.

        Positional arguments:
            data: str -- text to be stored. 
        
        Overrides the superclass method.
        """
        if self._chId is None:
            return

        self._lines.append(data)

    def handle_endtag(self, tag):
        """Recognize the end of the chapter section and save data.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.

        Overrides the superclass method.
        """
        if self._chId is None:
            return

        if tag == 'div':
            self.novel.chapters[self._chId].desc = ''.join(
                self._lines).rstrip()
            self._lines.clear()
            self._chId = None
            return

        if tag == 'p':
            self._lines.append('\n')
            return

        if tag in self._SEPARATORS:
            self._lines.append('\n')
            return

    def handle_starttag(self, tag, attrs):
        """Identify sections and chapters.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.
            attrs -- list of (name, value) pairs containing the 
                     attributes found inside the tag’s <> brackets.
        
        Extends the superclass method by processing inline chapter 
        and section dividers.
        """
        super().handle_starttag(tag, attrs)

        if self._chId is None:
            if tag == 'body':
                self._set_novel_language(attrs)
        else:
            if tag in self._SEPARATORS:
                self._lines.append(self._SEPARATORS[tag])
                return


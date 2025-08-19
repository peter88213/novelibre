"""Provide a class for html invisibly tagged chapter descriptions import.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_reader import OdtReader
from nvlib.novx_globals import CHAPTERS_SUFFIX
from nvlib.nv_locale import _


class OdtRChapterDesc(OdtReader):
    """ODT chapter summaries file reader.

    Import a brief synopsis with invisibly tagged chapter descriptions.
    """
    DESCRIPTION = _('Chapter descriptions')
    SUFFIX = CHAPTERS_SUFFIX

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

        if tag == 'h1' or tag == 'h2':
            # the document might be created with novelibre
            # version 5.31.0 or earlier, where the heading
            # was not yet separated from the description
            self._lines.clear()


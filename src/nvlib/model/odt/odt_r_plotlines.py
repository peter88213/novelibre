"""Provide a class for ODT plot line/plot point descriptions import.

The plot lines/ plot points are invisibly tagged .

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_reader import OdtReader
from nvlib.novx_globals import PLOTLINES_SUFFIX
from nvlib.nv_locale import _


class OdtRPlotlines(OdtReader):
    """ODT plot line descriptions file reader.

    Import a document with invisibly tagged plot line/plot point descriptions.
    """
    DESCRIPTION = _('Plot lines')
    SUFFIX = PLOTLINES_SUFFIX

    def handle_data(self, data):
        """Collect data within section sections.

        Positional arguments:
            data: str -- text to be stored. 
        
        Overrides the superclass method.
        """
        if self._plId is not None or self._ppId is not None:
            self._lines.append(data)

    def handle_endtag(self, tag):
        """Recognize the end of the section section and save data.
        
        Positional arguments:
            tag: str -- name of the tag converted to lower case.

        Overrides the superclass method.
        """
        if self._plId is not None:
            if tag == 'div':
                text = ''.join(self._lines)
                self.novel.plotLines[self._plId].desc = text.rstrip()
                self._lines.clear()
                self._plId = None
                return

            if tag == 'p':
                self._lines.append('\n')
            return

        if self._ppId is not None:
            if tag == 'div':
                text = ''.join(self._lines)
                self.novel.plotPoints[self._ppId].desc = text.rstrip()
                self._lines.clear()
                self._ppId = None
                return

            if tag == 'p':
                self._lines.append('\n')


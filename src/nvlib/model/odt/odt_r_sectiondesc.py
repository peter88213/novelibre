"""Provide a class for ODT invisibly tagged section descriptions import.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_r_desc import OdtRDesc
from nvlib.novx_globals import SECTIONS_SUFFIX
from nvlib.nv_locale import _


class OdtRSectionDesc(OdtRDesc):
    """ODT section summaries file reader.

    Import a full synopsis with invisibly tagged section descriptions.
    """
    DESCRIPTION = _('Section descriptions')
    SUFFIX = SECTIONS_SUFFIX

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
        if self._scId is not None:
            if tag == 'div':
                text = ''.join(self._lines)
                self.novel.sections[self._scId].desc = text.rstrip()
                self._lines.clear()
                self._scId = None
                return

            if tag in self._SEPARATORS:
                self._lines.append('\n')
                return

            if tag == 'p':
                self._lines.append('\n')
            return

        if self._chId is not None:
            if tag == 'div':
                self._chId = None

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

        if self._scId is not None:
            if tag in self._SEPARATORS:
                self._lines.append(self._SEPARATORS[tag])
                return


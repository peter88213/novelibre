"""Provide a class for ODT brief synopsis export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_writer import OdtWriter
from nvlib.novx_globals import BRF_SYNOPSIS_SUFFIX
from nvlib.nv_locale import _


class OdtWBriefSynopsis(OdtWriter):
    """ODT brief synopsis templates.

    Export a brief synopsis with chapter titles and section titles.
    """
    DESCRIPTION = _('Brief synopsis')
    SUFFIX = BRF_SYNOPSIS_SUFFIX

    _fileHeader = (
        f'{OdtWriter._CONTENT_XML_HEADER}'
        '<text:p text:style-name="Title">$Title</text:p>\n'
        '<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters\n'
    )
    _partTemplate = (
        '<text:h text:style-name="Heading_20_1" text:outline-level="1">'
        '$Title</text:h>\n'
    )
    _chapterTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        '$Title</text:h>\n'
    )
    _sectionTemplate = (
        '<text:p text:style-name="Text_20_body">$Title</text:p>\n'
    )
    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

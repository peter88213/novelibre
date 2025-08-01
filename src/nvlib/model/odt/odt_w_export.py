"""Provide a class for ODT chapters and sections export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_w_formatted import OdtWFormatted
from nvlib.nv_locale import _


class OdtWExport(OdtWFormatted):
    """ODT novel templates.

    Export a non-reimportable manuscript with chapters and sections.
    """
    DESCRIPTION = _('manuscript')

    _fileHeader = (
        '$ContentHeader'
        '<text:p text:style-name="Title">$Title</text:p>\n'
        '<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters\n'
    )
    _partTemplate = (
        '<text:h text:style-name="Heading_20_1" text:outline-level="1">'
        '$Title</text:h>$Epigraph$EpigraphSrc\n'
    )
    _chapterTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        '$Title</text:h>$Epigraph$EpigraphSrc\n'
    )
    _sectionTemplate = '$SectionContent\n'

    _sectionDivider = '<text:p text:style-name="Heading_20_4">* * *</text:p>\n'
    _fileFooter = OdtWFormatted._CONTENT_XML_FOOTER


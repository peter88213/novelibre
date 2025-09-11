"""Provide a class for ODT invisibly tagged chapters and sections export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_w_formatted import OdtWFormatted
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.nv_locale import _


class OdtWManuscript(OdtWFormatted):
    """ODT manuscript templates.

    Export a manuscript with invisibly tagged chapters and sections.
    """
    DESCRIPTION = _('Editable manuscript')
    SUFFIX = MANUSCRIPT_SUFFIX

    _fileHeader = (
        '$ContentHeader'
        '<text:p text:style-name="Title">$Title</text:p>'
        '\n<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters\n'
    )
    _partTemplate = (
        '<text:h text:style-name="Heading_20_1" text:outline-level="1">'
        '$Title</text:h>\n'
    )
    _chapterTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        '$Title</text:h>\n'
    )
    _epigraphTemplate = (
        '<text:section text:style-name="Sect1" text:name="$ID">\n'
        '$SectionContent\n'
        '</text:section>\n'
        '$Desc\n'
    )
    _sectionTemplate = (
        f'<text:h text:style-name="{_("Heading_20_3_20_invisible")}" '
        'text:outline-level="3">$Title</text:h>\n'
        '<text:section text:style-name="Sect1" text:name="$ID">\n'
        '$SectionContent\n'
        '</text:section>\n'
    )
    _sectionDivider = (
        '<text:p text:style-name="Heading_20_4">* * *</text:p>\n'
    )
    _fileFooter = OdtWFormatted._CONTENT_XML_FOOTER


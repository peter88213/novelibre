"""Provide a class for ODT invisibly tagged chapter descriptions export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_writer import OdtWriter
from nvlib.novx_globals import CHAPTERS_SUFFIX
from nvlib.nv_locale import _


class OdtWChapterDesc(OdtWriter):
    """ODT chapter summaries templates.

    Export a synopsis with invisibly tagged chapter descriptions.
    """
    DESCRIPTION = _('Chapter descriptions')
    SUFFIX = CHAPTERS_SUFFIX

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
        '<text:section text:style-name="Sect1" text:name="$ID">\n'
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        '<text:a xlink:href="../$ProjectName$ManuscriptSuffix.odt#'
        '$Title|outline">$Title</text:a></text:h>\n'
        '$Desc\n'
        '</text:section>\n'
    )
    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

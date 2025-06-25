"""Provide a class for ODT story structure export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import STAGES_SUFFIX
from nvlib.nv_locale import _
from nvlib.model.odt.odt_writer import OdtWriter


class OdtWStages(OdtWriter):
    """ODT story structure file representation.

    Export a story structure description with the stages.
    """
    DESCRIPTION = _('Story structure')
    SUFFIX = STAGES_SUFFIX

    _fileHeader = (
        f'{OdtWriter._CONTENT_XML_HEADER}'
        '<text:p text:style-name="Title">$Title</text:p>\n'
        '<text:p text:style-name="Subtitle">$AuthorName</text:p>\n\n'
        '<text:h text:style-name="Heading_20_1" text:outline-level="1">'
        f'{_("Story structure")}</text:h>\n'
    )
    _stage1Template = (
        '<text:h text:style-name="Heading_20_1" text:outline-level="1">'
        '<text:bookmark text:name="$ID"/>$Title</text:h>\n'
        '<text:section text:style-name="Sect1" text:name="$ID">\n'
        '$Desc\n'
        '</text:section>\n'
    )
    _stage2Template = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        '<text:bookmark text:name="$ID"/>$Title</text:h>\n'
        '<text:section text:style-name="Sect1" text:name="$ID">\n'
        '$Desc\n'
        '</text:section>\n'
    )
    _fileFooter = OdtWriter._CONTENT_XML_FOOTER


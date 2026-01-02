"""Provide a class for ODT invisibly tagged section descriptions export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_writer import OdtWriter
from nvlib.novx_globals import SECTIONS_SUFFIX
from nvlib.nv_locale import _


class OdtWSectionDesc(OdtWriter):
    """ODT section summaries templates.

    Export a full synopsis with invisibly tagged section descriptions.
    """
    DESCRIPTION = _('Section descriptions')
    SUFFIX = SECTIONS_SUFFIX

    _fileHeader = (
        f'{OdtWriter._CONTENT_XML_HEADER}<text:p text:style-name="Title">'
        '$Title</text:p>\n'
        '<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters\n'
    )
    _partTemplate = (
        '<text:h text:style-name="Heading_20_1" text:outline-level="1">'
        '$Title</text:h>\n'
    )
    _chapterTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        '<text:a xlink:href="../$ProjectName$ManuscriptSuffix.odt#'
        '$Title|outline">$Title</text:a></text:h>\n'
    )
    _sectionTemplate = (
        f'<text:h text:style-name="{_("Heading_20_3_20_invisible")}" '
        'text:outline-level="3">$Title</text:h>\n'
        '<text:section text:style-name="Sect1" text:name="$ID">\n'
        '$Desc\n'
        '</text:section>\n'
    )
    _sectionDivider = '<text:p text:style-name="Heading_20_4">* * *</text:p>\n'
    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

    def _get_sectionMapping(
            self,
            scId,
            sectionNumber,
            wordsTotal,
            **kwargs
    ):
        """Return a mapping dictionary for a section section.
        
        Positional arguments:
            scId: str -- section ID.
            sectionNumber: int -- section number to be displayed.
            wordsTotal: int -- accumulated wordcount.
        
        Extends the superclass method.
        """
        sectionMapping = super()._get_sectionMapping(
            scId,
            sectionNumber,
            wordsTotal,
            **kwargs
        )
        sectionMapping['Manuscript'] = _('Manuscript')
        return sectionMapping

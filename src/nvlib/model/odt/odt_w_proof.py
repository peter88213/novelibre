"""Provide a class for ODT visibly tagged chapters and sections export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_w_formatted import OdtWFormatted
from nvlib.novx_globals import PROOF_SUFFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


class OdtWProof(OdtWFormatted):
    """ODT proof reading templates.

    Export a manuscript with visibly tagged chapters and sections.
    """
    DESCRIPTION = _('Tagged manuscript for proofing')
    SUFFIX = PROOF_SUFFIX

    _fileHeader = (
        '$ContentHeader<text:p text:style-name="Title">$Title</text:p>\n'
        '<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters\n'
    )
    _partTemplate = (
        '<text:h text:style-name="Heading_20_1" text:outline-level="1">'
        '$Title</text:h>'
    )
    _chapterTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        '$Title</text:h>'
    )
    _epigraphTemplate = (
        f'<text:p text:style-name="{_("Section_20_mark")}">[$ID]</text:p>\n'
        '$SectionContent\n'
        f'<text:p text:style-name="{_("Section_20_mark")}">'
        f'[/{SECTION_PREFIX}]</text:p>\n'
        '$Desc\n'
    )
    _sectionTemplate = (
        '<text:h text:style-name="Heading_20_3" text:outline-level="3">'
        '$Title</text:h>\n'
        f'<text:p text:style-name="{_("Section_20_mark")}">[$ID]</text:p>\n'
        '$SectionContent\n'
        f'<text:p text:style-name="{_("Section_20_mark")}">'
        f'[/{SECTION_PREFIX}]</text:p>\n'
    )
    _fileFooter = OdtWFormatted._CONTENT_XML_FOOTER

    def _convert_from_novx(
        self,
        text,
        quick=False,
        append=False,
        firstInChapter=False,
        xml=False,
        linebreaks=False,
        firstParagraphStyle='Text_20_body',
        epigraph=False,
    ):
        """Return text without markup, converted to target format.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick: bool -- if True, apply a conversion mode for one-liners 
                           without formatting.
            append: bool -- if True, indent the first paragraph.
            firstInChapter: bool: -- if True, the section begins a chapter.
            xml: bool -- if True, parse XML content. 
            linebreaks: bool -- if True and not xml, break the lines 
                                instead of creating paragraphs. 
            firstParagraphStyle: str -- The first paragraph's style, 
                                        if not xml and not append.
        
        Overrides the superclass method.
        """
        return super()._convert_from_novx(
            text,
            quick=quick,
            append=append,
            firstInChapter=False,
            xml=xml,
            linebreaks=linebreaks,
            firstParagraphStyle=firstParagraphStyle,
            epigraph=epigraph,
        )

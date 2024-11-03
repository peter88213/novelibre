"""Provide a class for ODT visibly tagged chapters and sections export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import PROOF_SUFFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.novx_globals import _
from nvlib.model.odt.odt_w_formatted import OdtWFormatted


class OdtWProof(OdtWFormatted):
    """ODT proof reading file writer.

    Export a manuscript with visibly tagged chapters and sections.
    """
    DESCRIPTION = _('Tagged manuscript for proofing')
    SUFFIX = PROOF_SUFFIX

    _fileHeader = f'''$ContentHeader<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters
'''

    _partTemplate = '''<text:h text:style-name="Heading_20_1" text:outline-level="1">$Title</text:h>
'''

    _chapterTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title</text:h>
'''

    _sectionTemplate = f'''<text:h text:style-name="Heading_20_3" text:outline-level="3">$Title</text:h>
<text:p text:style-name="{_('Section_20_mark')}">[$ID]</text:p>
$SectionContent
<text:p text:style-name="{_('Section_20_mark')}">[/{SECTION_PREFIX}]</text:p>
'''

    _fileFooter = OdtWFormatted._CONTENT_XML_FOOTER

    def _convert_from_novx(self, text, quick=False, append=False, firstInChapter=False, xml=False):
        """Return text without markup, converted to target format.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick: bool -- if True, apply a conversion mode for one-liners without formatting.
            append: bool -- if True, indent the first paragraph.
            firstInChapter: bool: -- if True, the section begins a chapter.
            xml: bool -- if True, parse XML content. 
        
        Overrides the superclass method.
        """
        return super()._convert_from_novx(text, quick=quick, append=append, firstInChapter=False, xml=xml)

"""Provide a class for ODT invisibly tagged part descriptions export.

Parts are chapters marked `This chapter  begins a new section` in novelibre.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_writer import OdtWriter
from nvlib.novx_globals import PARTS_SUFFIX
from nvlib.nv_locale import _


class OdtWPartDesc(OdtWriter):
    """ODT part summaries file writer.

    Export a synopsis with invisibly tagged part descriptions.
    """
    DESCRIPTION = _('Part descriptions')
    SUFFIX = PARTS_SUFFIX

    _fileHeader = f'''{OdtWriter._CONTENT_XML_HEADER}<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters
'''

    _partTemplate = '''<text:section text:style-name="Sect1" text:name="$ID">
<text:h text:style-name="Heading_20_1" text:outline-level="1"><text:a xlink:href="../$ProjectName$ManuscriptSuffix.odt#$Title|outline">$Title</text:a></text:h>
$Desc
</text:section>
'''

    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

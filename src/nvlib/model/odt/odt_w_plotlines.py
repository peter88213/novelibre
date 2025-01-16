"""Provide a class for ODT plot line descriptions export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_writer import OdtWriter
from nvlib.novx_globals import PLOTLINES_SUFFIX
from nvlib.nv_locale import _


class OdtWPlotlines(OdtWriter):
    """ODT plot lines description file representation.

    Export descriptions of plot lines and plot points.
    """
    DESCRIPTION = _('Plot lines')
    SUFFIX = PLOTLINES_SUFFIX

    _fileHeader = f'''{OdtWriter._CONTENT_XML_HEADER}<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>
'''

    _plotLineHeadingTemplate = f'''<text:h text:style-name="Heading_20_1" text:outline-level="1">{_('Plot lines')}</text:h>
'''

    _plotLineTemplate = '''<text:h text:style-name="Heading_20_2" text:outline-level="2"><text:bookmark text:name="$ID"/>$Title</text:h>
<text:section text:style-name="Sect1" text:name="$ID">
$Desc
</text:section>
'''

    _plotPointTemplate = '''<text:h text:style-name="Heading_20_3" text:outline-level="3"><text:bookmark text:name="$ID"/>$Title</text:h>
<text:section text:style-name="Sect1" text:name="$ID">
$Desc
</text:section>
$Section
'''

    _assocSectionTemplate = f'''
<text:p text:style-name="Text_20_body" />
<text:p text:style-name="Text_20_body">{_('Section')}: <text:span text:style-name="Emphasis">$SectionTitle</text:span></text:p>    
<text:p text:style-name="Text_20_body">→ <text:a xlink:href="../$ProjectName$SectionsSuffix.odt#$scID%7Cregion">{_('Description')}</text:a></text:p>
<text:p text:style-name="Text_20_body">→ <text:a xlink:href="../$ProjectName$ManuscriptSuffix.odt#$scID%7Cregion">{_('Manuscript')}</text:a></text:p>
'''

    _fileFooter = OdtWriter._CONTENT_XML_FOOTER


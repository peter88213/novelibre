"""Provide a class for ODS chapter list export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_w_chapterlist import OdsWChapterList
from nvlib.novx_globals import PARTLIST_SUFFIX
from nvlib.nv_locale import _


class OdsWPartList(OdsWChapterList):
    """ODS part list templates."""

    DESCRIPTION = _('Part table')
    SUFFIX = PARTLIST_SUFFIX

    _chapterTemplate = ''
    _partTemplate = (
        '   <table:table-row table:style-name="ro2">\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$ID</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Title</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Desc</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Epigraph</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$EpigraphSrc</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Notes</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:number-columns-repeated="1020"/>\n'
        '    </table:table-row>\n'
    )

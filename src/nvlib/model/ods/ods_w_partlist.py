"""Provide a class for ODS chapter list export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_w_chapterlist import OdsWChapterList
from nvlib.novx_globals import PARTLIST_SUFFIX
from nvlib.nv_locale import _


class OdsWPartList(OdsWChapterList):
    """ODS part list writer."""

    DESCRIPTION = _('Part list')
    SUFFIX = PARTLIST_SUFFIX

    _chapterTemplate = ''
    _partTemplate = '''   <table:table-row table:style-name="ro2">
     <table:table-cell office:value-type="string">
      <text:p>$ID</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Title</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Desc</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Epigraph</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$EpigraphSrc</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Notes</text:p>
     </table:table-cell>
     <table:table-cell table:number-columns-repeated="1020"/>
    </table:table-row>

'''

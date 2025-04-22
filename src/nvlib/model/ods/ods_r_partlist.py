"""Provide a class for ODS chapter list import.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_r_chapterlist import OdsRChapterList
from nvlib.novx_globals import PARTLIST_SUFFIX
from nvlib.nv_locale import _


class OdsRPartList(OdsRChapterList):
    """ODS part list reader."""

    DESCRIPTION = _('Part list')
    SUFFIX = PARTLIST_SUFFIX


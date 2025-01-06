"""Provide a class for ODT invisibly tagged part descriptions import.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import PARTS_SUFFIX
from nvlib.nv_locale import _
from nvlib.model.odt.odt_r_chapterdesc import OdtRChapterDesc


class OdtRPartDesc(OdtRChapterDesc):
    """ODT part summaries file reader.

    Parts are chapters marked in novelibre as beginning of a new section.
    Import a synopsis with invisibly tagged part descriptions.
    """
    DESCRIPTION = _('Part descriptions')
    SUFFIX = PARTS_SUFFIX

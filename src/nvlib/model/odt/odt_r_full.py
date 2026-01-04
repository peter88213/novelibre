"""Provide a class for ODT manuscript import including unused text.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_r_manuscript import OdtRManuscript
from nvlib.novx_globals import FULL_MANUSCRIPT_SUFFIX
from nvlib.nv_locale import _


class OdtRFull(OdtRManuscript):
    """ODT manuscript file reader.

    Import a manuscript with invisibly tagged chapters and sections.
    """
    DESCRIPTION = _('Manuscript including unused text')
    SUFFIX = FULL_MANUSCRIPT_SUFFIX


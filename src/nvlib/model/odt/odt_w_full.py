"""Provide a class for ODT manuscript export including unused text.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_w_manuscript import OdtWManuscript
from nvlib.novx_globals import FULL_MANUSCRIPT_SUFFIX
from nvlib.nv_locale import _


class OdtWFull(OdtWManuscript):
    """ODT manuscript templates including unused text.

    Export a manuscript with invisibly tagged chapters and sections.
    """
    DESCRIPTION = _('Manuscript including unused text')
    SUFFIX = FULL_MANUSCRIPT_SUFFIX

    _unusedChapterTemplate = OdtWManuscript._chapterTemplate
    _unusedSectionTemplate = OdtWManuscript._sectionTemplate

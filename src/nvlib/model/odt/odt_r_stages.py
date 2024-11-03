"""Provide a class for ODT invisibly tagged stage descriptions import.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import STAGES_SUFFIX
from nvlib.novx_globals import _
from nvlib.model.odt.odt_r_sectiondesc import OdtRSectionDesc


class OdtRStages(OdtRSectionDesc):
    """ODT stage summaries file reader.

    Import a story structure with invisibly tagged section descriptions.
    """
    DESCRIPTION = _('Story structure')
    SUFFIX = STAGES_SUFFIX


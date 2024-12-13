"""Provide a "sections by plot line" filter class for template-based file export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.nv_locale import _


class ScPlFilter:
    """Filter a section by filter criteria "belongs to plot line".
    
    Strategy class, implementing filtering criteria for template-based export.
    This is a stub with no filter criteria specified.
    """

    def __init__(self, plId):
        self._plId = plId

    def accept(self, source, scId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the section to check.
            scId -- ID of the section to check.       
        
        Return True if the plId matches an arc the section is assigned to.
        """
        try:
            if self._plId in source.novel.sections[scId].scPlotLines:
                return True

        except:
            pass
        return False

    def get_message(self, source):
        """Return a message about how the document exported from source is filtered."""
        return f'{_("Sections belonging to plot line")}: "{source.novel.plotLines[self._plId].title}"'

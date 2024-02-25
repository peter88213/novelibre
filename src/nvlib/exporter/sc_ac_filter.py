"""Provide a "sections by arc" filter class for template-based file export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from novxlib.novx_globals import _


class ScAcFilter:
    """Filter a section by filter criteria "belongs to arc".
    
    Strategy class, implementing filtering criteria for template-based export.
    This is a stub with no filter criteria specified.
    """

    def __init__(self, acId):
        self._acId = acId

    def accept(self, source, scId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the section to check.
            scId -- ID of the section to check.       
        
        Return True if the acId matches an arc the section is assigned to.
        """
        try:
            if self._acId in source.novel.sections[scId].scArcs:
                return True

        except:
            pass
        return False

    def get_message(self, source):
        """Return a message about how the document exported from source is filtered."""
        return f'{_("Sections belonging to arc")}: "{source.novel.arcs[self._acId].title}"'

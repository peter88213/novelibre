"""Provide a "chapters by plot line" filter class for template-based file export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from novxlib.novx_globals import _


class ChAcFilter:
    """Filter a chapter by filter criteria "belongs to plot line".
    
    Strategy class, implementing filtering criteria for template-based export.
    This is a stub with no filter criteria specified.
    """

    def __init__(self, acId):
        self._acId = acId

    def accept(self, source, chId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the chapter to check.
            chId -- ID of the chapter to check.       
        
        Return True if the acId matches an arc that at least
        one section in the chapter is assigned to.
        """
        for scId in source.novel.tree.get_children(chId):
            try:
                if self._acId in source.novel.sections[scId].scArcs:
                    return True

            except:
                pass
        return False

    def get_message(self, source):
        """Return a message about how the document exported from source is filtered."""
        return f'{_("Chapters belonging to plot line")}: "{source.novel.arcs[self._acId].title}"'

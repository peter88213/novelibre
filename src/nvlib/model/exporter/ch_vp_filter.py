"""Provide a "chapters by viewpoint" filter class for template-based file export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import _


class ChVpFilter:
    """Filter a chapter by filter criteria "has viewpoint".
    
    Strategy class, implementing filtering criteria for template-based export.
    This is a stub with no filter criteria specified.
    """

    def __init__(self, crId):
        self._crId = crId

    def accept(self, source, chId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the chapter to check.
            chId -- ID of the chapter to check.       
        
        Return True if the crId matches a viewpoint character of 
        at least one section of the chapter.
        """
        for scId in source.novel.tree.get_children(chId):
            try:
                if self._crId == source.novel.sections[scId].characters[0]:
                    return True

            except:
                pass
        return False

    def get_message(self, source):
        """Return a message about how the document exported from source is filtered."""
        return f'{_("Chapters from viewpoint")}: {source.novel.characters[self._crId].title}'

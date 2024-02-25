"""Provide a "sections by viewpoint" filter class for template-based file export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from novxlib.novx_globals import _


class ScVpFilter:
    """Filter a section by filter criteria "has viewpoint".
    
    Strategy class, implementing filtering criteria for template-based export.
    This is a stub with no filter criteria specified.
    """

    def __init__(self, filterElementId):
        self._filterElementId = filterElementId

    def accept(self, source, scId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the section to check.
            scId -- ID of the section to check.       
        
        Return True if the filterElementId matches the section's viewpoint character.
        """
        try:
            if self._filterElementId == source.novel.sections[scId].characters[0]:
                return True

        except:
            pass
        return False

    def get_message(self, source):
        """Return a message about how the document exported from source is filtered."""
        return f'{_("Sections from viewpoint")}: {source.novel.characters[self._filterElementId].title}'

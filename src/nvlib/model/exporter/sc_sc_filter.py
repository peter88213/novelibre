"""Provide a "section by ID" filter class for template-based file export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.file.filter import Filter


class ScScFilter(Filter):
    """Filter a section by filter criteria "has ID".
    
    Strategy class, implementing filtering criteria for template-based export.
    """

    def __init__(self, scId):
        self._scId = scId

    def accept(self, source, scId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the section to check.
            scId -- ID of the section to check.       
        
        Return True if the section ID matches the filter section ID.
        """
        if scId == self._scId:
            return True

        return False


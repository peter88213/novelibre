"""Provide a "chapter by ID" filter class for template-based file export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.exporter.filter import Filter
from nvlib.nv_locale import _


class ChChFilter(Filter):
    """Filter a chapter by filter criteria "has ID".
    
    Strategy class, implementing filtering criteria for 
    template-based export.
    """

    def __init__(self, chId):
        self._chId = chId

    def accept(self, source, chId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the chapter to check.
            chId -- ID of the chapter to check.       
        
        Return True if the chapter ID matches the filter chapter ID.
        """
        if chId == self._chId:
            return True

        return False


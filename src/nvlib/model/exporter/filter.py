"""Provide a generic filter class for template-based file export.

All specific filters inherit from this class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Filter:
    """Filter an element by filter criteria.
    
    Strategy class, implementing filtering criteria 
    for template-based export.
    This is a stub with no filter criteria specified.
    """

    def accept(self, source, eId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the entity to check.
            eId -- ID of the entity to check.       
        
        Return True if the entity is not to be filtered out.
        This is a stub to be overridden by subclass methods 
        implementing filters.
        """
        return True

    def get_message(self, source):
        """Return a message 
        
        The message is about how the document exported from source 
        is filtered.
        """
        return ''

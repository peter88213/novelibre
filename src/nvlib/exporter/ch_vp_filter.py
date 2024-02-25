"""Provide a "chapters by viewpoint" filter class for template-based file export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""


class ChVpFilter:
    """Filter a chapter by filter criteria "has viewpoint".
    
    Strategy class, implementing filtering criteria for template-based export.
    This is a stub with no filter criteria specified.
    """

    def __init__(self, filterElementId):
        self._filterElementId = filterElementId

    def accept(self, source, chId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- Novel instance holding the chapter to check.
            chId -- ID of the chapter to check.       
        
        Return True if the filterElementId matches a viewpoint character of 
        at least one section of the chapter.
        """
        try:
            for scId in source.novel.tree.get_children(chId):
                if self._filterElementId == source.novel.sections[scId].characters[0]:
                    return True

        except:
            pass
        return False

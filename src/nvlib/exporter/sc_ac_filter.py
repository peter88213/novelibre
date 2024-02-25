"""Provide a "sections by arc" filter class for template-based file export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""


class ScAcFilter:
    """Filter a section by filter criteria "belongs to arc".
    
    Strategy class, implementing filtering criteria for template-based export.
    This is a stub with no filter criteria specified.
    """

    def __init__(self, filterElementId):
        self._filterElementId = filterElementId

    def accept(self, source, scId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- Novel instance holding the section to check.
            scId -- ID of the section to check.       
        
        Return True if the filterElementId matches an arc the section is assigned to.
        """
        try:
            if self._filterElementId in source.novel.sections[scId].scArcs:
                return True

        except:
            pass
        return False

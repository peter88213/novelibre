"""Provide a "chapters by plot line" filter class for template-based file export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.file.filter import Filter
from nvlib.nv_locale import _


class ChPlFilter(Filter):
    """Filter a chapter by filter criteria "belongs to plot line".
    
    Strategy class, implementing filtering criteria for template-based export.
    """

    def __init__(self, plId):
        self._plId = plId

    def accept(self, source, chId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the chapter to check.
            chId -- ID of the chapter to check.       
        
        Return True if the plId matches a plot line that at least
        one section in the chapter is assigned to.
        """
        for scId in source.novel.tree.get_children(chId):
            try:
                if self._plId in source.novel.sections[scId].scPlotLines:
                    return True

            except:
                pass
        return False

    def get_message(self, source):
        """Return a message about how the document exported from source is filtered."""
        return f'{_("Chapters belonging to plot line")}: "{source.novel.plotLines[self._plId].title}"'

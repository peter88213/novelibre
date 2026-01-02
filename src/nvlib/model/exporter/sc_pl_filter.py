"""Provide a "sections by plot line" filter class.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.exporter.filter import Filter
from nvlib.nv_locale import _


class ScPlFilter(Filter):
    """Filter a section by filter criteria "belongs to plot line".
    
    Strategy class, implementing filtering criteria for 
    template-based export.
    """

    def __init__(self, plId):
        self._plId = plId

    def accept(self, source, scId):
        """Check whether an entity matches the filter criteria.
        
        Positional arguments:
            source -- File instance holding the section to check.
            scId -- ID of the section to check.       
        
        Return True if the plId matches a plot line 
        the section is assigned to.
        """
        try:
            if self._plId in source.novel.sections[scId].scPlotLines:
                return True

        except:
            pass
        return False

    def get_message(self, source):
        """Return a message 
        
        The message is about how the document exported from source 
        is filtered.
        """
        return (
            f'{_("Sections belonging to plot line")}: '
            f'"{source.novel.plotLines[self._plId].title}"'
        )

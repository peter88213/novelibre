"""Provide a class with a factory method for export filters.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.exporter.ch_ch_filter import ChChFilter
from nvlib.model.exporter.ch_pl_filter import ChPlFilter
from nvlib.model.exporter.ch_vp_filter import ChVpFilter
from nvlib.model.exporter.sc_pl_filter import ScPlFilter
from nvlib.model.exporter.sc_vp_filter import ScVpFilter
from nvlib.model.file.filter import Filter
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX


class FilterFactory:

    @staticmethod
    def get_section_filter(filterElementId):
        """Return a Filter (or subclass) instance.
        
        Positional arguments: 
            filterElementId: str -- ID of the element that serves as filter criteria. 
        
        """
        if filterElementId.startswith(CHARACTER_PREFIX):
            return ScVpFilter(filterElementId)

        if filterElementId.startswith(PLOT_LINE_PREFIX):
            return ScPlFilter(filterElementId)

        return Filter()

    @staticmethod
    def get_chapter_filter(filterElementId):
        """Return a Filter (or subclass) instance.
        
        Positional arguments: 
            filterElementId: str -- ID of the element that serves as filter criteria. 
        
        """
        if filterElementId.startswith(CHARACTER_PREFIX):
            return ChVpFilter(filterElementId)

        if filterElementId.startswith(CHAPTER_PREFIX):
            return ChChFilter(filterElementId)

        if filterElementId.startswith(PLOT_LINE_PREFIX):
            return ChPlFilter(filterElementId)

        return Filter()

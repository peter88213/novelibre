"""Provide a class with a factory method for export filters.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from novxlib.file.filter import Filter
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import ARC_PREFIX
from nvlib.exporter.sc_vp_filter import ScVpFilter
from nvlib.exporter.sc_ac_filter import ScAcFilter
from nvlib.exporter.ch_vp_filter import ChVpFilter
from nvlib.exporter.ch_ac_filter import ChAcFilter


class FilterFactory:

    @staticmethod
    def get_section_filter(filterElementId):
        """Return a Filter (or subclass) instance.
        
        Positional arguments: 
            filterElementId: str -- ID of the element that serves as filter criteria. 
        
        """
        if filterElementId.startswith(CHARACTER_PREFIX):
            return ScVpFilter(filterElementId)

        elif filterElementId.startswith(ARC_PREFIX):
            return ScAcFilter(filterElementId)

        else:
            return Filter()

    @staticmethod
    def get_chapter_filter(filterElementId):
        """Return a Filter (or subclass) instance.
        
        Positional arguments: 
            filterElementId: str -- ID of the element that serves as filter criteria. 
        
        """
        if filterElementId.startswith(CHARACTER_PREFIX):
            return ChVpFilter(filterElementId)

        elif filterElementId.startswith(ARC_PREFIX):
            return ChAcFilter(filterElementId)

        else:
            return Filter()

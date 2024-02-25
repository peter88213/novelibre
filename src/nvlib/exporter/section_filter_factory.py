"""Provide a class with a factory method for export filters.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from novxlib.file.filter import Filter
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import ARC_PREFIX
from nvlib.exporter.viewpoint_filter import ViewpointFilter
from nvlib.exporter.section_arc_filter import SectionArcFilter


class SectionFilterFactory:

    @staticmethod
    def get_filter(filterElementId):
        """Return a Filter (or subclass) instance.
        
        Positional arguments: 
            filterElementId: str -- ID of the element that serves as filter criteria. 
        
        """
        if filterElementId.startswith(CHARACTER_PREFIX):
            return ViewpointFilter(filterElementId)

        elif filterElementId.startswith(ARC_PREFIX):
            return SectionArcFilter(filterElementId)

        else:
            return Filter()

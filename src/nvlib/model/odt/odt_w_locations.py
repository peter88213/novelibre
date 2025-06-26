"""Provide a class for ODT invisibly tagged location descriptions export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_writer import OdtWriter
from nvlib.novx_globals import LOCATIONS_SUFFIX
from nvlib.nv_locale import _


class OdtWLocations(OdtWriter):
    """ODT location descriptions templates.

    Export a location sheet with invisibly tagged descriptions.
    """
    DESCRIPTION = _('Location descriptions')
    SUFFIX = LOCATIONS_SUFFIX

    _fileHeader = (
        f'{OdtWriter._CONTENT_XML_HEADER}'
        '<text:p text:style-name="Title">$Title</text:p>\n'
        '<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters\n'
    )
    _locationTemplate = (
        '<text:h text:style-name="Heading_20_2" '
        'text:outline-level="2">$Title$AKA</text:h>\n'
        '<text:section text:style-name="Sect1" text:name="$ID">\n'
        '$Desc\n'
        '</text:section>\n'
    )
    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

    def _get_locationMapping(self, lcId):
        """Return a mapping dictionary for a location section.
        
        Positional arguments:
            lcId: str -- location ID.
        
        Special formatting of alternate name. 
        Extends the superclass method.
        """
        locationMapping = super()._get_locationMapping(lcId)
        if self.novel.locations[lcId].aka:
            locationMapping['AKA'] = f' ("{self.novel.locations[lcId].aka}")'
        return locationMapping

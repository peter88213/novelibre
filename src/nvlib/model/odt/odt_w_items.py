"""Provide a class for ODT item invisibly tagged descriptions export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import ITEMS_SUFFIX
from nvlib.nv_locale import _
from nvlib.model.odt.odt_writer import OdtWriter


class OdtWItems(OdtWriter):
    """ODT item descriptions file writer.

    Export a item sheet with invisibly tagged descriptions.
    """
    DESCRIPTION = _('Item descriptions')
    SUFFIX = ITEMS_SUFFIX

    _fileHeader = (
        f'{OdtWriter._CONTENT_XML_HEADER}'
        '<text:p text:style-name="Title">$Title</text:p>\n'
        '<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters\n'
    )
    _itemTemplate = (
        '<text:h text:style-name="Heading_20_2" '
        'text:outline-level="2">$Title$AKA</text:h>\n'
        '<text:section text:style-name="Sect1" text:name="$ID">\n'
        '$Desc\n'
        '</text:section>\n'
    )
    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

    def _get_itemMapping(self, itId):
        """Return a mapping dictionary for an item section.
        
        Positional arguments:
            itId: str -- item ID.
        
        Special formatting of alternate name. 
        Extends the superclass method.
        """
        itemMapping = super()._get_itemMapping(itId)
        if self.novel.items[itId].aka:
            itemMapping['AKA'] = f' ("{self.novel.items[itId].aka}")'
        return itemMapping

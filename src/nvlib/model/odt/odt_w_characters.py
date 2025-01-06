"""Provide a class for ODT invisibly tagged character descriptions export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.novx_globals import CHARACTERS_SUFFIX
from nvlib.nv_locale import _
from nvlib.model.odt.odt_writer import OdtWriter


class OdtWCharacters(OdtWriter):
    """ODT character descriptions file writer.

    Export a character sheet with invisibly tagged descriptions.
    """
    DESCRIPTION = _('Character descriptions')
    SUFFIX = CHARACTERS_SUFFIX

    _fileHeader = f'''{OdtWriter._CONTENT_XML_HEADER}<text:p text:style-name="Title">$Title</text:p>
<text:p text:style-name="Subtitle">$AuthorName</text:p>$Filters
'''

    _characterTemplate = f'''<text:h text:style-name="Heading_20_2" text:outline-level="2">$Title$FullName$AKA</text:h>
<text:section text:style-name="Sect1" text:name="$ID">
<text:h text:style-name="Heading_20_3" text:outline-level="3">{_("Description")}</text:h>
<text:section text:style-name="Sect1" text:name="desc:$ID">
$Desc
</text:section>
<text:h text:style-name="Heading_20_3" text:outline-level="3">$CustomChrBio</text:h>
<text:section text:style-name="Sect1" text:name="bio:$ID">
$Bio
</text:section>
<text:h text:style-name="Heading_20_3" text:outline-level="3">$CustomChrGoals</text:h>
<text:section text:style-name="Sect1" text:name="goals:$ID">
$Goals
</text:section>
<text:h text:style-name="Heading_20_3" text:outline-level="3">{_("Notes")}</text:h>
<text:section text:style-name="Sect1" text:name="notes:$ID">
$Notes
</text:section>
</text:section>
'''

    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

    def _get_characterMapping(self, crId):
        """Return a mapping dictionary for a character section.
        
        Positional arguments:
            crId: str -- character ID.
        
        Special formatting of alternate and full name. 
        Extends the superclass method.
        """
        characterMapping = OdtWriter._get_characterMapping(self, crId)
        if self.novel.characters[crId].aka:
            characterMapping['AKA'] = f' ("{self.novel.characters[crId].aka}")'
        if self.novel.characters[crId].fullName:
            characterMapping['FullName'] = f'/{self.novel.characters[crId].fullName}'

        return characterMapping

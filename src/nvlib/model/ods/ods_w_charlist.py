"""Provide a class for ODS character list export.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from string import Template

from nvlib.model.ods.ods_writer import OdsWriter
from nvlib.novx_globals import CHARLIST_SUFFIX
from nvlib.nv_locale import _


class OdsWCharList(OdsWriter):
    """ODS character list writer."""

    DESCRIPTION = _('Character list')
    SUFFIX = CHARLIST_SUFFIX

    _fileHeader = f'''{OdsWriter._CONTENT_XML_HEADER}{DESCRIPTION}" table:style-name="ta1" table:print="false">
    <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:number-columns-repeated="3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="ce2"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="ce2"/>
    <table:table-column table:style-name="co2" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>
    <table:table-column table:style-name="co1" table:number-columns-repeated="1014" table:default-cell-style-name="Default"/>
     <table:table-row table:style-name="ro1" table:visibility="collapse">
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>ID</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Name</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Full name</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Aka</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Description</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Bio</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Goals</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="ce1" office:value-type="string">
      <text:p>Birth date</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="ce1" office:value-type="string">
      <text:p>Death date</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Importance</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Tags</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>Notes</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" table:number-columns-repeated="1014"/>
    </table:table-row>
     <table:table-row table:style-name="ro1">
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>ID</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Name")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Full name")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Aka")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Description")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>$CustomChrBio</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>$CustomChrGoals</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Birth date")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Death date")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Importance")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Tags")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" office:value-type="string">
      <text:p>{_("Notes")}</text:p>
     </table:table-cell>
     <table:table-cell table:style-name="Heading" table:number-columns-repeated="1014"/>
    </table:table-row>

'''
    _characterTemplate = '''   <table:table-row table:style-name="ro2">
     <table:table-cell office:value-type="string">
      <text:p>$ID</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Title</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$FullName</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$AKA</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Desc</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Bio</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Goals</text:p>
     </table:table-cell>
$BirthDateCell     
$DeathDateCell     
     <table:table-cell office:value-type="string">
      <text:p>$Status</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Tags</text:p>
     </table:table-cell>
     <table:table-cell office:value-type="string">
      <text:p>$Notes</text:p>
     </table:table-cell>
     <table:table-cell table:number-columns-repeated="1014"/>
    </table:table-row>

'''

    _fileFooter = OdsWriter._CONTENT_XML_FOOTER

    _emptyDateCell = '     <table:table-cell table:style-name="ce2"/>'
    _validBirthDateCell = '''     <table:table-cell office:value-type="date" office:date-value="$BirthDate">
      <text:p>$BirthDate</text:p>
     </table:table-cell>'''
    _validDeathDateCell = '''     <table:table-cell office:value-type="date" office:date-value="$DeathDate">
      <text:p>$DeathDate</text:p>
     </table:table-cell>'''

    def _get_characterMapping(self, crId):
        characterMapping = super()._get_characterMapping(crId)

        #--- $BirthDateCell: if no section date is given, the whole cell must be empty.
        if characterMapping['BirthDate']:
            characterMapping['BirthDateCell'] = Template(self._validBirthDateCell).safe_substitute(characterMapping)
        else:
            characterMapping['BirthDateCell'] = self._emptyDateCell

        #--- $DeathDateCell: if no section date is given, the whole cell must be empty.
        if characterMapping['DeathDate']:
            characterMapping['DeathDateCell'] = Template(self._validDeathDateCell).safe_substitute(characterMapping)
        else:
            characterMapping['DeathDateCell'] = self._emptyDateCell

        return characterMapping


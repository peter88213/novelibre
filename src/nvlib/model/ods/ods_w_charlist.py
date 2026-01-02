"""Provide a class for ODS character list export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from string import Template

from nvlib.model.ods.ods_writer import OdsWriter
from nvlib.novx_globals import CHARLIST_SUFFIX
from nvlib.nv_locale import _


class OdsWCharList(OdsWriter):
    """ODS character list templates."""

    DESCRIPTION = _('Character table')
    SUFFIX = CHARLIST_SUFFIX

    _fileHeader = (
        f'{OdsWriter._CONTENT_XML_HEADER}{DESCRIPTION}" '
        'table:style-name="ta1" table:print="false">\n'
        '    <table:table-column table:style-name="co1" '
        'table:visibility="collapse" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co2" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co2" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" '
        'table:number-columns-repeated="3" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co2" '
        'table:default-cell-style-name="ce2"/>\n'
        '    <table:table-column table:style-name="co2" '
        'table:default-cell-style-name="ce2"/>\n'
        '    <table:table-column table:style-name="co2" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co3" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co4" '
        'table:default-cell-style-name="Default"/>\n'
        '    <table:table-column table:style-name="co1" '
        'table:number-columns-repeated="1014" '
        'table:default-cell-style-name="Default"/>\n'
        '     <table:table-row table:style-name="ro1" '
        'table:visibility="collapse">\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>ID</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>Name</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>Full name</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>Aka</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>Description</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>Bio</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>Goals</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="ce1" '
        'office:value-type="string">\n'
        '      <text:p>Birth date</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="ce1" '
        'office:value-type="string">\n'
        '      <text:p>Death date</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>Importance</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>Tags</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>Notes</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'table:number-columns-repeated="1014"/>\n'
        '    </table:table-row>\n'
        '     <table:table-row table:style-name="ro1">\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>ID</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        f'      <text:p>{_("Name")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        f'      <text:p>{_("Full name")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        f'      <text:p>{_("Aka")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        f'      <text:p>{_("Description")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>$CharacterField1</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        '      <text:p>$CharacterField2</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        f'      <text:p>{_("Birth date")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        f'      <text:p>{_("Death date")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        f'      <text:p>{_("Importance")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        f'      <text:p>{_("Tags")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'office:value-type="string">\n'
        f'      <text:p>{_("Notes")}</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:style-name="Heading" '
        'table:number-columns-repeated="1014"/>\n'
        '    </table:table-row>\n'
    )
    _characterTemplate = (
        '   <table:table-row table:style-name="ro2">\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$ID</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Title</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$FullName</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$AKA</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Desc</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Bio</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Goals</text:p>\n'
        '     </table:table-cell>\n'
        '$BirthDateCell\n'
        '$DeathDateCell\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Status</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Tags</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell office:value-type="string">\n'
        '      <text:p>$Notes</text:p>\n'
        '     </table:table-cell>\n'
        '     <table:table-cell table:number-columns-repeated="1014"/>\n'
        '    </table:table-row>\n'
    )
    _fileFooter = OdsWriter._CONTENT_XML_FOOTER
    _emptyDateCell = '     <table:table-cell table:style-name="ce2"/>'
    _validBirthDateCell = (
        '     <table:table-cell office:value-type="date" '
        'office:date-value="$BirthDate">\n'
        '      <text:p>$BirthDate</text:p>\n'
        '     </table:table-cell>\n'
     )
    _validDeathDateCell = (
        '     <table:table-cell office:value-type="date" '
        'office:date-value="$DeathDate">\n'
        '      <text:p>$DeathDate</text:p>\n'
        '     </table:table-cell>\n'
    )

    def _get_characterMapping(self, crId):
        characterMapping = super()._get_characterMapping(crId)

        #--- $BirthDateCell:
        #    if no section date is given, the whole cell must be empty.
        if characterMapping['BirthDate']:
            characterMapping['BirthDateCell'] = Template(
                self._validBirthDateCell
            ).safe_substitute(characterMapping)
        else:
            characterMapping['BirthDateCell'] = self._emptyDateCell

        #--- $DeathDateCell:
        #    if no section date is given, the whole cell must be empty.
        if characterMapping['DeathDate']:
            characterMapping['DeathDateCell'] = Template(
                self._validDeathDateCell
            ).safe_substitute(characterMapping)
        else:
            characterMapping['DeathDateCell'] = self._emptyDateCell

        return characterMapping


"""Provide a class for ODT cross reference export.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from string import Template

from nvlib.model.data.cross_references import CrossReferences
from nvlib.model.odt.odt_writer import OdtWriter
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import XREF_SUFFIX
from nvlib.nv_locale import _


class OdtWXref(OdtWriter):
    """OpenDocument xml cross reference templates and writer."""
    DESCRIPTION = _('Cross reference')
    SUFFIX = XREF_SUFFIX

    _fileHeader = (
        f'{OdtWriter._CONTENT_XML_HEADER}'
        '<text:p text:style-name="Title">$Title</text:p>\n'
        '<text:p text:style-name="Subtitle">$AuthorName</text:p>\n'
    )
    _sectionTemplate = (
        '<text:p text:style-name="Text_20_body">\n'
        '<text:a xlink:href="../$ProjectName$ManuscriptSuffix.odt'
        '#$ID%7Cregion">$SectionNumber </text:a>'
        f'({_("Chp.")}$Chapter) $Title\n'
        '</text:p>\n'
    )
    _unusedSectionTemplate = (
        '<text:p text:style-name="Text_20_body">\n'
        f'$SectionNumber ({_("Chp.")}$Chapter) $Title ({_("Unused")})\n'
        '</text:p>\n'
    )
    _characterTemplate = (
        '<text:p text:style-name="Text_20_body">\n'
        '<text:a xlink:href='
        '"../$ProjectName$CharactersSuffix.odt#$ID%7Cregion">'
        '$Title</text:a> $FullName\n'
        '</text:p>\n'
    )
    _locationTemplate = (
        '<text:p text:style-name="Text_20_body">\n'
        '<text:a xlink:href='
        '"../$ProjectName$LocationsSuffix.odt#$ID%7Cregion">'
        '$Title</text:a>\n'
        '</text:p>\n'
    )
    _itemTemplate = (
        '<text:p text:style-name="Text_20_body">\n'
        '<text:a xlink:href="../$ProjectName$ItemsSuffix.odt#$ID%7Cregion">'
        '$Title</text:a>\n'
        '</text:p>\n'
    )
    _scnPerChrTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        f'{_("Sections")} {_("with")} {_("Character")} $Title:</text:h>\n'
    )
    _scnPerLocTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        f'{_("Sections")} {_("with")} {_("Location")} $Title:</text:h>\n'
    )
    _scnPerItmTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        f'{_("Sections")} {_("with")} {_("Item")} $Title:</text:h>\n'
    )
    _chrPerTagTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        f'{_("Characters")} {_("with")} {_("tag")} $Tag:</text:h>\n'
    )
    _locPerTagTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        f'{_("Locations")} {_("with")} {_("tag")} $Tag:</text:h>\n'
    )
    _itmPerTagTemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        f'{_("Items")} {_("with")} {_("tag")} $Tag:</text:h>\n'
    )
    _scnPerTagtemplate = (
        '<text:h text:style-name="Heading_20_2" text:outline-level="2">'
        f'{_("Sections")} {_("with")} {_("tag")} $Tag:</text:h>\n'
    )
    _fileFooter = OdtWriter._CONTENT_XML_FOOTER

    def __init__(self, filePath, **kwargs):
        """Delegate the cross reference to an external object.
        
        Applying the Strategy pattern.
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._xr = CrossReferences()

    def _get_characters(self):
        """Process the sections per character.
        
        Return a list of strings.
        Overrides the superclass method.
        """
        lines = []
        headerTemplate = Template(self._scnPerChrTemplate)
        for crId in self._xr.scnPerChr:
            if self._xr.scnPerChr[crId]:
                lines.append(
                    headerTemplate.safe_substitute(
                        self._get_characterMapping(crId)
                    )
                )
                lines.extend(
                    self._get_sections(
                        self._xr.scnPerChr[crId],
                    )
                )
        return lines

    def _get_characterTags(self):
        """Process the character related tags.
        
        Return a list of strings.
        """
        lines = []
        headerTemplate = Template(self._chrPerTagTemplate)
        template = Template(self._characterTemplate)
        for tag in self._xr.chrPerTag:
            if self._xr.chrPerTag[tag]:
                lines.append(
                    headerTemplate.safe_substitute(
                        self._get_tagMapping(tag)
                    )
                )
                for crId in self._xr.chrPerTag[tag]:
                    lines.append(
                        template.safe_substitute(
                            self._get_characterMapping(crId)
                        )
                    )
        return lines

    def _get_items(self):
        """Process the items.
        
        Return a list of strings.
        Overrides the superclass method.
        """
        lines = []
        headerTemplate = Template(self._scnPerItmTemplate)
        for itId in self._xr.scnPerItm:
            if self._xr.scnPerItm[itId]:
                lines.append(
                    headerTemplate.safe_substitute(
                        self._get_itemMapping(itId)
                    )
                )
                lines.extend(self._get_sections(self._xr.scnPerItm[itId]))
        return lines

    def _get_itemTags(self):
        """Process the item related tags.
        
        Return a list of strings.
        """
        lines = []
        headerTemplate = Template(self._itmPerTagTemplate)
        template = Template(self._itemTemplate)
        for tag in self._xr.itmPerTag:
            if self._xr.itmPerTag[tag]:
                lines.append(
                    headerTemplate.safe_substitute(
                        self._get_tagMapping(tag)
                    )
                )
                for itId in self._xr.itmPerTag[tag]:
                    lines.append(
                        template.safe_substitute(
                            self._get_itemMapping(itId)
                        )
                    )
        return lines

    def _get_locations(self):
        """Process the locations.
        
        Return a list of strings.
        Overrides the superclass method.
        """
        lines = []
        headerTemplate = Template(self._scnPerLocTemplate)
        for lcId in self._xr.scnPerLoc:
            if self._xr.scnPerLoc[lcId]:
                lines.append(
                    headerTemplate.safe_substitute(
                        self._get_locationMapping(lcId)
                    )
                )
                lines.extend(self._get_sections(self._xr.scnPerLoc[lcId]))
        return lines

    def _get_locationTags(self):
        """Process the location related tags.
        
        Return a list of strings.
        """
        lines = []
        headerTemplate = Template(self._locPerTagTemplate)
        template = Template(self._locationTemplate)
        for tag in self._xr.locPerTag:
            if self._xr.locPerTag[tag]:
                lines.append(
                    headerTemplate.safe_substitute(
                        self._get_tagMapping(tag)
                    )
                )
                for lcId in self._xr.locPerTag[tag]:
                    lines.append(
                        template.safe_substitute(
                            self._get_locationMapping(lcId)
                        )
                    )
        return lines

    def _get_sectionMapping(self, scId, **kwargs):
        """Return a mapping dictionary for a section section.

        Positional arguments:
            scId: str -- section ID.
        
        Extends the superclass template method.
        """
        sectionNumber = self._xr.srtSections.index(scId) + 1
        sectionMapping = super()._get_sectionMapping(
            scId,
            sectionNumber,
            0,
            **kwargs
        )
        chapterNumber = self.novel.tree.get_children(
            CH_ROOT).index(self._xr.chpPerScn[scId]) + 1
        sectionMapping['Chapter'] = str(chapterNumber)
        return sectionMapping

    def _get_sections(self, sections):
        """Process the sections.
        
        Positional arguments:
            sections -- iterable of section IDs.
        
        Return a list of strings.
        Overrides the superclass method.
        """
        lines = []
        for scId in sections:
            if self.novel.sections[scId].scType == 0:
                template = Template(self._sectionTemplate)
            elif self.novel.sections[scId].scType == 1:
                template = Template(self._unusedSectionTemplate)
            else:
                continue

            lines.append(template.safe_substitute(
                self._get_sectionMapping(scId))
            )
        return lines

    def _get_sectionTags(self):
        """Process the section related tags.
        
        Return a list of strings.
        """
        lines = []
        headerTemplate = Template(self._scnPerTagtemplate)
        for tag in self._xr.scnPerTag:
            if self._xr.scnPerTag[tag]:
                lines.append(
                    headerTemplate.safe_substitute(
                        self._get_tagMapping(tag)
                    )
                )
                lines.extend(self._get_sections(self._xr.scnPerTag[tag]))
        return lines

    def _get_tagMapping(self, tag):
        """Return a mapping dictionary for a tags section. 

        Positional arguments:
            tag: str -- a single section tag.
        """
        tagMapping = dict(
            Tag=tag,
        )
        return tagMapping

    def _get_text(self):
        """Call all processing methods.
        
        Return a string to be written to the output file.
        Overrides the superclass method.
        """
        self._xr.generate_xref(self.novel)
        lines = self._get_fileHeader()
        lines.extend(self._get_characters())
        lines.extend(self._get_locations())
        lines.extend(self._get_items())
        lines.extend(self._get_sectionTags())
        lines.extend(self._get_characterTags())
        lines.extend(self._get_locationTags())
        lines.extend(self._get_itemTags())
        lines.append(self._fileFooter)
        return ''.join(lines)

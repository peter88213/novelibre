"""Provide a class for ods plot list representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/yw-table
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from string import Template

from nvlib.model.hex_color import HexColor
from nvlib.model.ods.ods_writer import OdsWriter
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.novx_globals import PLOTLINES_SUFFIX
from nvlib.novx_globals import PLOTLIST_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import list_to_string
from nvlib.nv_locale import _


class OdsWPlotList(OdsWriter):
    """ODS plot list representation."""

    DESCRIPTION = _('ODS Plot table')
    SUFFIX = PLOTLIST_SUFFIX

    def write_content_xml(self):
        """Create the ODS table.
        
        Raise the "Error" exception in case of error. 
        Extends the superclass method.
        """
        fileHeader = Template(self._CONTENT_XML_HEADER).substitute(
            self._get_fileHeaderMapping()
        )
        odsText = [
            f'{fileHeader}{self.DESCRIPTION}" table:style-name="ta1" '
            'table:print="false">\n'
            '   <table:table-column table:style-name="co4" '
            'table:default-cell-style-name="Default"/>'
        ]

        # Get plot lines.
        if self.novel.tree.get_children(PL_ROOT) is not None:
            srtPlotLines = self.novel.tree.get_children(PL_ROOT)
        else:
            srtPlotLines = []

        # Plot line columns.
        for plId in srtPlotLines:
            odsText.append(
                '   <table:table-column table:style-name="co3" '
                'table:default-cell-style-name="Default"/>'
            )

        # Title row.
        odsText.append('   <table:table-row table:style-name="ro2">')
        odsText.append(self._new_cell(''))
        for plId in srtPlotLines:
            odsText.append(
                self._new_cell(
                    self.novel.plotLines[plId].title,
                    attr=f'table:style-name="h{plId}"',
                    link=f'{PLOTLINES_SUFFIX}.odt#{plId}'
                )
            )
        odsText.append('    </table:table-row>')

        # Section rows.
        for chId in self.novel.tree.get_children(CH_ROOT):
            for scId in self.novel.tree.get_children(chId):
                # Section row
                if self.novel.sections[scId].scType == 0:
                    odsText.append(
                        '   <table:table-row table:style-name="ro2">'
                    )
                    odsText.append(
                        self._new_cell(
                            self.novel.sections[scId].title,
                            link=f'{MANUSCRIPT_SUFFIX}.odt#{scId}%7Cregion'
                        )
                    )
                    for plId in srtPlotLines:
                        if scId in self.novel.plotLines[plId].sections:
                            plotPoints = []
                            for ppId in self.novel.tree.get_children(plId):
                                if (
                                    scId ==
                                    self.novel.plotPoints[ppId].sectionAssoc
                                ):
                                    plotPoints.append(
                                        self.novel.plotPoints[ppId].title
                                    )
                            odsText.append(
                                self._new_cell(
                                    list_to_string(plotPoints),
                                    attr=f'table:style-name="{plId}" '
                                )
                            )
                        else:
                            odsText.append(self._new_cell(''))
                    odsText.append(f'    </table:table-row>')

        odsText.append(self._CONTENT_XML_FOOTER)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(odsText))

    def _get_extra_styles(self, elements):

        DEFAULT_BG_COLOR = '#dfdfdf'
        DEFAULT_FG_COLOR = BLACK = '#000000'
        WHITE = '#ffffff'

        # Element column heading cell style.
        styleTemplateHeading = (
            '  <style:style style:name="h$Name" style:family="table-cell" '
            'style:parent-style-name="Default">\n'
            '   <style:table-cell-properties '
            'fo:background-color="$BgColor"/>\n'
            '   <style:text-properties fo:color="$FgColor" '
            'fo:font-weight="bold" '
            'style:font-weight-asian="bold" '
            'style:font-weight-complex="bold"/>\n'
            '  </style:style>'
        )

        # Element node cell style.
        styleTemplate = (
            '  <style:style style:name="$Name" style:family="table-cell" '
            'style:parent-style-name="Default">\n'
            '   <style:table-cell-properties '
            'fo:background-color="$DefaultBgColor" '
            'fo:border-bottom="none" '
            'fo:border-left="0.176cm solid $BgColor" '
            'fo:border-right="none" '
            'fo:border-top="none"/>\n'
            '   <style:text-properties fo:color="$DefaultFgColor"/>\n'
            '  </style:style>'
        )

        mappings = {
            'DefaultBgColor': DEFAULT_BG_COLOR,
            'DefaultFgColor': DEFAULT_FG_COLOR,
        }
        xmlText = []
        for elemId in elements:
            elemColor = elements[elemId].color
            if elemColor is not None:
                if HexColor.is_dark(elemColor):
                    fgColor = WHITE
                else:
                    fgColor = BLACK
                bgColor = elemColor
            else:
                fgColor = DEFAULT_FG_COLOR
                bgColor = DEFAULT_BG_COLOR

            mappings['Name'] = elemId
            mappings['BgColor'] = bgColor
            mappings['FgColor'] = fgColor
            styleXml = Template(styleTemplateHeading)
            xmlText.append(styleXml.substitute(mappings))
            styleXml = Template(styleTemplate)
            xmlText.append(styleXml.substitute(mappings))

        return '\n'.join(xmlText)

    def _get_fileHeaderMapping(self):
        fileHeaderMapping = {
            'Styles': self._get_extra_styles(self.novel.plotLines)
        }
        return fileHeaderMapping

    def _new_cell(self, text, attr='', link=''):
        """Return the markup for a table cell with text and attributes."""
        if link:
            attr = (
                f'{attr} table:formula="of:=HYPERLINK(&quot;file:///'
                f'{self.projectPath}/'
                f'{self._convert_from_novx(self.projectName)}{link}&quot;'
                f';&quot;{self._convert_from_novx(text, isLink=True)}&quot;)"'
            )
            text = ''
        else:
            text = f'\n      <text:p>{self._convert_from_novx(text)}</text:p>'
        return (
            f'     <table:table-cell {attr} '
            f'office:value-type="string">{text}\n'
            '     </table:table-cell>'
        )


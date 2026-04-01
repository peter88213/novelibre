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
        odsText = [
            self._get_content_xml_header(),
            (
                '   <table:table-column table:style-name="co4" '
                'table:default-cell-style-name="Default"/>'
            ),
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
                    attr=f'table:style-name="{plId}"',
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

    def _get_content_xml_header(self):

        DEFAULT_PLOTLINE_COLOR = '#dfdfdf'
        DEFAULT_TEXT_COLOR = BLACK = '#000000'
        WHITE = '#ffffff'

        styleTemplate = (
            '  <style:style style:name="$Name" style:family="table-cell" '
            'style:parent-style-name="Default">\n'
            '   <style:table-cell-properties fo:background-color="$BgColor"/>\n'
            '   <style:text-properties fo:color="$FgColor"/>\n'
            '  </style:style>'
        )
        additionalStyles = []
        for plId in self.novel.plotLines:
            plColor = self.novel.plotLines[plId].color
            if plColor is not None:
                if HexColor.is_dark(plColor):
                    fgColor = WHITE
                else:
                    fgColor = BLACK
                bgColor = plColor.lower()
            else:
                fgColor = DEFAULT_TEXT_COLOR
                bgColor = DEFAULT_PLOTLINE_COLOR
            styleXml = Template(styleTemplate)
            additionalStyles.append(
                styleXml.substitute(
                    {
                        'Name': plId,
                        'BgColor': bgColor,
                        'FgColor': fgColor,
                    }
                )
            )
        additionalStyles.append(' </office:automatic-styles>')
        fileHeader = super()._CONTENT_XML_HEADER.replace(
            ' </office:automatic-styles>',
            '\n'.join(additionalStyles)
        )
        return (
            f'{fileHeader}{self.DESCRIPTION}" table:style-name="ta1" '
            'table:print="false">'
        )

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


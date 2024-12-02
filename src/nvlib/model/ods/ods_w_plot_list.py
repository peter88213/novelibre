"""Provide a class for ods plot list representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/yw-table
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.ods.ods_writer import OdsWriter
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.novx_globals import PLOTLINES_SUFFIX
from nvlib.novx_globals import PLOTLIST_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import list_to_string
from nvlib.nv_locale import _


class OdsWPlotList(OdsWriter):
    """html plot list representation."""
    DESCRIPTION = _('ODS Plot list')
    SUFFIX = PLOTLIST_SUFFIX

    _CE_OFFSET = 6
    _ADDITIONAL_STYLES = '''
  <style:style style:name="ce5" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties style:text-align-source="value-type" style:repeat-content="false"/>
   <style:paragraph-properties fo:margin-left="0cm"/>
   <style:text-properties fo:color="#ff0000" fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold"/>
  </style:style>
  <style:style style:name="ce6" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#b0c4de"/>
  </style:style>
  <style:style style:name="ce7" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#ffd700"/>
  </style:style>
  <style:style style:name="ce8" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#ff7f50"/>
  </style:style>
  <style:style style:name="ce9" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#9acd32"/>
  </style:style>
  <style:style style:name="ce10" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#48d1cc"/>
  </style:style>
  <style:style style:name="ce11" style:family="table-cell" style:parent-style-name="Default">
   <style:table-cell-properties fo:background-color="#dda0dd"/>
  </style:style>
 </office:automatic-styles>'''

    _fileHeader = OdsWriter._CONTENT_XML_HEADER.replace(' </office:automatic-styles>', _ADDITIONAL_STYLES)
    _fileHeader = f'{_fileHeader}{DESCRIPTION}" table:style-name="ta1" table:print="false">'

    def write_content_xml(self):
        """Create the ODS table.
        
        Raise the "Error" exception in case of error. 
        Extends the superclass method.
        """

        odsText = [
            self._fileHeader,
            '<table:table-column table:style-name="co4" table:default-cell-style-name="Default"/>',
        ]

        plotLineColorsTotal = 6
        # total number of the background colors used in the "ce" table cell styles

        # Get plot lines.
        if self.novel.tree.get_children(PL_ROOT) is not None:
            plotLines = self.novel.tree.get_children(PL_ROOT)
        else:
            plotLines = []

        # Plot line columns.
        for plId in plotLines:
            odsText.append('<table:table-column table:style-name="co3" table:default-cell-style-name="Default"/>')

        # Title row.
        odsText.append('   <table:table-row table:style-name="ro2">')
        odsText.append(self._new_cell(''))
        for i, plId in enumerate(plotLines):
            colorIndex = (i % plotLineColorsTotal) + self._CE_OFFSET
            odsText.append(
                self._new_cell(
                    self.novel.plotLines[plId].title,
                    attr=f'table:style-name="ce{colorIndex}"',
                    link=f'{PLOTLINES_SUFFIX}.odt#{plId}'
                )
            )
        odsText.append('    </table:table-row>')

        # Section rows.
        for chId in self.novel.tree.get_children(CH_ROOT):
            for scId in self.novel.tree.get_children(chId):
                # Section row
                if self.novel.sections[scId].scType == 0:
                    odsText.append('   <table:table-row table:style-name="ro2">')
                    odsText.append(
                        self._new_cell(
                            self.novel.sections[scId].title,
                            link=f'{MANUSCRIPT_SUFFIX}.odt#{scId}%7Cregion'
                        )
                    )
                    for i, plId in enumerate(plotLines):
                        colorIndex = (i % plotLineColorsTotal) + self._CE_OFFSET
                        if scId in self.novel.plotLines[plId].sections:
                            plotPoints = []
                            for ppId in self.novel.tree.get_children(plId):
                                if scId == self.novel.plotPoints[ppId].sectionAssoc:
                                    plotPoints.append(self.novel.plotPoints[ppId].title)
                            odsText.append(
                                self._new_cell(
                                    list_to_string(plotPoints),
                                    attr=f'table:style-name="ce{colorIndex}" '
                                )
                            )
                        else:
                            odsText.append(self._new_cell(''))
                    odsText.append(f'    </table:table-row>')

        odsText.append(self._CONTENT_XML_FOOTER)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(odsText))

    def _new_cell(self, text, attr='', link=''):
        """Return the markup for a table cell with text and attributes."""
        if link:
            attr = f'{attr} table:formula="of:=HYPERLINK(&quot;file:///{self.projectPath}/{self._convert_from_novx(self.projectName)}{link}&quot;;&quot;{self._convert_from_novx(text, isLink=True)}&quot;)"'
            text = ''
        else:
            text = f'\n      <text:p>{self._convert_from_novx(text)}</text:p>'
        return f'     <table:table-cell {attr} office:value-type="string">{text}\n     </table:table-cell>'


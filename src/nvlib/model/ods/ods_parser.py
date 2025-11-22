"""Provide a class for parsing ODS documents.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re
import zipfile

from nvlib.model.odf.odf_file import OdfFile
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


class OdsParser:
    """An ODS document parser.
    
    Return a list of rows, containing lists of column cells.
    The novxlib csv import classes thus can be reused.
    """

    def get_rows(self, filePath, cellsPerRow):
        """Return a nested list with rows and cells from an ODS document.
        
        Positional arguments:
            filePath: str -- ODS document path.
            cellsPerRow: int -- Number of cells per row.
        
        First unzip the ODS file located at self.filePath, 
        then parse content.xml.
        """
        root = ET.fromstring(self._unzip_ods_file(filePath))

        #--- Parse 'content.xml'.
        body = root.find('office:body', OdfFile.NAMESPACES)
        spreadsheet = body.find('office:spreadsheet', OdfFile.NAMESPACES)
        table = spreadsheet.find('table:table', OdfFile.NAMESPACES)
        rows = []
        for row in table.iterfind('table:table-row', OdfFile.NAMESPACES):
            cells = []
            i = 0
            for cell in row.iterfind('table:table-cell', OdfFile.NAMESPACES):
                content = ''
                odfDate = cell.get(
                    f'{{{OdfFile.NAMESPACES["office"]}}}date-value'
                )
                odfTime = cell.get(
                    f'{{{OdfFile.NAMESPACES["office"]}}}time-value'
                )
                if odfDate:
                    cells.append(odfDate)
                elif odfTime:
                    t = re.search(r'PT(..)H(..)M(..)S', odfTime)
                    cells.append(f'{t.group(1)}:{t.group(2)}:{t.group(3)}')
                elif cell.find('text:p', OdfFile.NAMESPACES) is not None:
                    lines = []
                    for paragraph in cell.iterfind(
                        'text:p',
                        OdfFile.NAMESPACES
                    ):
                        lines.append(''.join(t for t in paragraph.itertext()))
                    content = '\n'.join(lines)
                    cells.append(content)
                elif i > 0:
                    cells.append(content)
                else:
                    # The ID cell is empty.
                    break

                i += 1
                if i >= cellsPerRow:
                    # The cell is excess, created by Calc.
                    break

                # Add repeated cells.
                attribute = cell.get(
                    (
                        f'{{{OdfFile.NAMESPACES["table"]}}}'
                        'number-columns-repeated'
                    )
                )
                if attribute:
                    repeat = int(attribute) - 1
                    for __ in range(repeat):
                        if i >= cellsPerRow:
                            # The cell is excess, created by Calc.
                            break

                        cells.append(content)
                        i += 1
            if cells:
                rows.append(cells)
                # print(cells)
        return rows

    def _unzip_ods_file(self, filePath):
        """Return an xml string from an ODS file specified by filePath."""
        try:
            with zipfile.ZipFile(filePath, 'r') as odfFile:
                content = odfFile.read('content.xml')
            return content

        except:
            raise RuntimeError(
                f'{_("Cannot read file")}: "{norm_path(filePath)}".'
            )


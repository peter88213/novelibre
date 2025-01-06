"""Provide a class for parsing ODS documents.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re
import zipfile

from nvlib.novx_globals import Error
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _
import xml.etree.ElementTree as ET


class OdsParser:
    """An ODS document parser.
    
    Return a list of rows, containing lists of column cells.
    The novxlib csv import classes thus can be reused.
    """

    def __init__(self):
        super().__init__()
        self._rows = []
        self._cells = []
        self._inCell = None
        self.__cellsPerRow = 0

    def get_rows(self, filePath, cellsPerRow):
        """Return a nested list with rows and cells from an ODS document.
        
        Positional arguments:
            filePath: str -- ODS document path.
            cellsPerRow: int -- Number of cells per row.
        
        First unzip the ODS file located at self.filePath, then parse content.xml.
        """
        namespaces = dict(
            office='urn:oasis:names:tc:opendocument:xmlns:office:1.0',
            text='urn:oasis:names:tc:opendocument:xmlns:text:1.0',
            table='urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        )
        content = self._unzip_ods_file(filePath)
        root = ET.fromstring(content)

        #--- Parse 'content.xml'.
        body = root.find('office:body', namespaces)
        spreadsheet = body.find('office:spreadsheet', namespaces)
        table = spreadsheet.find('table:table', namespaces)
        rows = []
        for row in table.iterfind('table:table-row', namespaces):
            cells = []
            i = 0
            for cell in row.iterfind('table:table-cell', namespaces):
                content = ''
                odfDate = cell.get(f'{{{namespaces["office"]}}}date-value')
                odfTime = cell.get(f'{{{namespaces["office"]}}}time-value')
                if odfDate:
                    cells.append(odfDate)
                elif odfTime:
                    t = re.search(r'PT(..)H(..)M(..)S', odfTime)
                    cells.append(f'{t.group(1)}:{t.group(2)}:{t.group(3)}')
                elif cell.find('text:p', namespaces) is not None:
                    lines = []
                    for paragraph in cell.iterfind('text:p', namespaces):
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
                attribute = cell.get(f'{{{namespaces["table"]}}}number-columns-repeated')
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
        """Return an xml string from the zipped ODS file."""
        try:
            with zipfile.ZipFile(filePath, 'r') as odfFile:
                content = odfFile.read('content.xml')
            return content

        except:
            raise Error(f'{_("Cannot read file")}: "{norm_path(filePath)}".')


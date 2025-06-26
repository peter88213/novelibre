"""Provide an abstract ODS file reader class.

Other ODS file readers inherit from this class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod

from nvlib.model.file.file_export import FileExport
from nvlib.model.odf.odf_reader import OdfReader
from nvlib.model.ods.ods_parser import OdsParser


class OdsReader(OdfReader, ABC):
    """Abstract OpenDocument spreadsheet document reader."""
    EXTENSION = '.ods'
    # overwrites File.EXTENSION
    _SEPARATOR = ','
    # delimits data fields within a record.
    _columnTitles = []
    _idPrefix = '??'

    _DIVIDER = FileExport._DIVIDER

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.

        Positional arguments:
            filePath: str -- path to the file 
            represented by the File instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._columns = {}
        # dict: {column title, {element ID, cell content}}
        self._rows = []

    @abstractmethod
    def read(self):
        """Parse the file and get the instance variables.
        
        Parse the ODS file located at filePath, fetching the rows.

        Overrides the superclass method.
        """
        self._rows.clear()
        cellsPerRow = len(self._columnTitles)
        parser = OdsParser()
        rows = parser.get_rows(self.filePath, cellsPerRow)
        for title in rows[0]:
            self._columns[title] = {}
        for row in rows:
            if row[0].startswith(self._idPrefix):
                for i, col in enumerate(self._columns):
                    self._columns[col][row[0]] = row[i]


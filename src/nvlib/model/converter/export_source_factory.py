"""Provide a factory class for one instance.

- A novx file object to read.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.model.converter.file_factory import FileFactory
from nvlib.novx_globals import Error
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _


class ExportSourceFactory(FileFactory):
    """Factory for a novx file object to read."""

    def new_file_objects(self, sourcePath, **kwargs):
        """Factory method.
        
        Instantiate a source object for conversion from a novelibre project.

        Positional arguments:
            sourcePath: str -- path to the source file to convert.

        Return a tuple with two elements:
        - sourceFile: a NovxFile subclass instance
        - targetFile: None

        Raise the "Error" exception in case of error. 
        """
        __, fileExtension = os.path.splitext(sourcePath)
        for fileClass in self._fileClasses:
            if fileClass.EXTENSION == fileExtension:
                sourceFile = fileClass(sourcePath, **kwargs)
                return sourceFile, None

        raise Error(
            (
                f'{_("File type is not supported")}: '
                f'"{norm_path(sourcePath)}".'
            )
        )

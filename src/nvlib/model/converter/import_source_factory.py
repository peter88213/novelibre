"""Provide a factory class for a document object to read.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.converter.file_factory import FileFactory
from nvlib.novx_globals import Error
from nvlib.nv_locale import _


class ImportSourceFactory(FileFactory):
    """A factory class that instantiates a documente object to read."""

    def new_file_objects(self, sourcePath, **kwargs):
        """Instantiate a source object for conversion to a novelibre project.       

        Positional arguments:
            sourcePath: str -- path to the source file to convert.

        Return a tuple with two elements:
        - sourceFile: a Novel subclass instance, or None in case of error
        - targetFile: None

        Raise the "Error" exception in case of error. 
        """
        for fileClass in self._fileClasses:
            if fileClass.SUFFIX is not None:
                if sourcePath.endswith(f'{fileClass.SUFFIX }{fileClass.EXTENSION}'):
                    sourceFile = fileClass(sourcePath, **kwargs)
                    return sourceFile, None

        raise Error(f'{_("This document is not meant to be written back")}.')

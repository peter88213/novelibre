"""Provide a factory class for a document object to write.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.model.converter.file_factory import FileFactory
from nvlib.novx_globals import Error
from nvlib.novx_globals import _


class ExportTargetFactory(FileFactory):
    """A factory class that instantiates a document object to write."""

    def new_file_objects(self, sourcePath, **kwargs):
        """Instantiate a target object for conversion from a novelibre project.

        Positional arguments:
            sourcePath: str -- path to the source file to convert.

        Required keyword arguments: 
            suffix: str -- target file name suffix.

        Return a tuple with two elements:
        - sourceFile: None
        - targetFile: a FileExport subclass instance
        
        Raise the "Error" exception in case of error.          
        """
        fileName, __ = os.path.splitext(sourcePath)
        suffix = kwargs['suffix']
        for fileClass in self._fileClasses:
            if fileClass.SUFFIX == suffix:
                if suffix is None:
                    suffix = ''
                targetFile = fileClass(f'{fileName}{suffix}{fileClass.EXTENSION}', **kwargs)
                return None, targetFile

        raise Error(f'{_("Export type is not supported")}: "{suffix}".')

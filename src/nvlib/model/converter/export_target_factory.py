"""Provide a factory class for one instance.

- A document object to write.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.model.converter.file_factory import FileFactory
from nvlib.nv_locale import _


class ExportTargetFactory(FileFactory):
    """Factory for a document object to write."""

    def new_file_objects(self, sourcePath, **kwargs):
        """Factory method.
        
        Instantiate a target object for conversion from a novelibre project.

        Positional arguments:
            sourcePath: str -- path to the source file to convert.

        Required keyword arguments: 
            suffix: str -- target file name suffix.

        Return a tuple with two elements:
        - sourceFile: None
        - targetFile: a FileExport subclass instance
        
        Raise the "RuntimeError" exception in case of error.          
        """
        fileName, __ = os.path.splitext(sourcePath)
        suffix = kwargs['suffix']
        for fileClass in self._fileClasses:
            if fileClass.SUFFIX == suffix:
                if suffix is None:
                    suffix = ''
                targetFile = fileClass(
                    f'{fileName}{suffix}{fileClass.EXTENSION}',
                    **kwargs
                )
                return None, targetFile

        raise RuntimeError(
            f'{_("Export type is not supported")}: "{suffix}".'
        )

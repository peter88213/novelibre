"""Provide a factory class for a document object to read and a new novelibre project.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import zipfile

from nvlib.model.converter.file_factory import FileFactory
from nvlib.model.novx.novx_file import NovxFile
from nvlib.novx_globals import BRF_SYNOPSIS_SUFFIX
from nvlib.novx_globals import Error
from nvlib.novx_globals import XREF_SUFFIX
from nvlib.nv_locale import _
from nvlib.novx_globals import norm_path
from nvlib.model.odt.odt_r_import import OdtRImport
from nvlib.model.odt.odt_r_outline import OdtROutline


class NewProjectFactory(FileFactory):
    """A factory class that instantiates a document object to read, 
    and a new novelibre project.

    Class constant:
        DO_NOT_IMPORT -- list of suffixes from file classes not meant to be imported.    
    """
    DO_NOT_IMPORT = [XREF_SUFFIX, BRF_SYNOPSIS_SUFFIX]

    def new_file_objects(self, sourcePath, **kwargs):
        """Instantiate a source and a target object for creation of a new novelibre project.

        Positional arguments:
            sourcePath: str -- path to the source file to convert.

        Return a tuple with two elements:
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance
        
        Raise the "Error" exception in case of error. 
        """
        if not self._canImport(sourcePath):
            raise Error(f'{_("This document is not meant to be written back")}.')

        fileName, __ = os.path.splitext(sourcePath)
        targetFile = NovxFile(f'{fileName}{NovxFile.EXTENSION}', **kwargs)
        if sourcePath.endswith('.odt'):
            # The source file might be an outline or a "work in progress".
            try:
                with zipfile.ZipFile(sourcePath, 'r') as odfFile:
                    content = odfFile.read('content.xml')
            except:
                raise Error(f'{_("Cannot read file")}: "{norm_path(sourcePath)}".')

            if bytes('Heading_20_3', encoding='utf-8') in content:
                sourceFile = OdtROutline(sourcePath, **kwargs)
            else:
                sourceFile = OdtRImport(sourcePath, **kwargs)
            return sourceFile, targetFile

        else:
            for fileClass in self._fileClasses:
                if fileClass.SUFFIX is not None:
                    if sourcePath.endswith(f'{fileClass.SUFFIX}{fileClass.EXTENSION}'):
                        sourceFile = fileClass(sourcePath, **kwargs)
                        return sourceFile, targetFile

            raise Error(f'{_("File type is not supported")}: "{norm_path(sourcePath)}".')

    def _canImport(self, sourcePath):
        """Check whether the source file can be imported to novelibre.
        
        Positional arguments: 
            sourcePath: str -- path of the file to be ckecked.
        
        Return True, if the file located at sourcepath is of an importable type.
        Otherwise, return False.
        """
        fileName, __ = os.path.splitext(sourcePath)
        for suffix in self.DO_NOT_IMPORT:
            if fileName.endswith(suffix):
                return False

        return True

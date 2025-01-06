"""Provide an abstract class for file representation.

All classes representing specific file formats inherit from this class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC
import os
from urllib.parse import quote

from nvlib.nv_locale import _


class File(ABC):
    """Abstract novel file representation.

    This class represents a file containing a novel with additional 
    attributes and structural information (a full set or a subset
    of the information included in a novelibre project file).
    """
    DESCRIPTION = _('File')
    EXTENSION = None
    SUFFIX = None
    # To be extended by subclass methods.

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.

        Positional arguments:
            filePath: str -- path to the file represented by the File instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.  
        """
        self.novel = None
        self._filePath = None
        # Path to the file. The setter only accepts files of a supported type as specified by EXTENSION.
        self.projectName = None
        # URL-coded file name without suffix and extension.
        self.projectPath = None
        # URL-coded path to the project directory.
        self.sectionsSplit = False
        self.filePath = filePath

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, filePath: str):
        """Setter for the filePath instance variable.
                
        - Format the path string according to Python's requirements. 
        - Accept only filenames with the right suffix and extension.
        """
        filePath = filePath.replace('\\', '/')
        if self.SUFFIX is not None:
            suffix = self.SUFFIX
        else:
            suffix = ''
        if filePath.lower().endswith(f'{suffix}{self.EXTENSION}'.lower()):
            self._filePath = filePath
            try:
                head, tail = os.path.split(os.path.realpath(filePath))
                # realpath() completes relative paths, but may not work on virtual file systems.
            except:
                head, tail = os.path.split(filePath)
            self.projectPath = quote(head.replace('\\', '/'), '/:')
            self.projectName = quote(tail.replace(f'{suffix}{self.EXTENSION}', ''))

    def is_locked(self):
        """Return True if the file is locked by its application."""
        return False

    def read(self):
        """Parse the file and get the instance variables.
        
        Raise the "Error" exception in case of error. 
        This is a stub to be overridden by subclass methods.
        """
        raise NotImplementedError

    def write(self):
        """Write instance variables to the file.
        
        Raise the "Error" exception in case of error. 
        This is a stub to be overridden by subclass methods.
        """
        raise NotImplementedError


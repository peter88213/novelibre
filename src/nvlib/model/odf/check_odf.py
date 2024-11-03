"""Helper module for ODF file operation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os


def odf_is_locked(filePath):
    """Check whether an ODF file specified by filePath is locked by OpenOffice/LibreOffice.
    
    Return True if a .lock file placed by OpenOffice/LibreOffice exists.
    Otherwise, return False. 
    """
    prjPath, fileName = os.path.split(filePath)
    return os.path.isfile(f'{prjPath}/.~lock.{fileName}#')


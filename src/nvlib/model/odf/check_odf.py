"""Helper module for ODF file operation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os


def odf_is_locked(filePath):
    """Check whether an ODF file is locked by OpenOffice/LibreOffice.
    
    Positional arguments:
    - filePath: str -- The ODF file to check.
    
    Return True if a .lock file placed by OpenOffice/LibreOffice exists.
    Otherwise, return False. 
    """
    prjPath, fileName = os.path.split(filePath)
    return os.path.isfile(f'{prjPath}/.~lock.{fileName}#')


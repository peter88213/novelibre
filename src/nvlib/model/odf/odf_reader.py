"""Provide an abstract ODF file reader class.

Other ODF file readers inherit from this class.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC

from nvlib.model.file.file import File
from nvlib.model.odf.check_odf import odf_is_locked


class OdfReader(File, ABC):
    """Abstract OpenDocument file reader."""

    def is_locked(self):
        """Return True if the file is locked by its application."""
        return odf_is_locked(self.filePath)

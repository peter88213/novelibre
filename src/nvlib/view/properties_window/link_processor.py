"""Provide a class for processing links.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
import subprocess

from novxlib.file.doc_open import open_document
from nvlib.nv_globals import launchers


class LinkProcessor:
    """Converter between file system paths and paths as stored with novx."""

    def to_novx(self, linkPath):
        """Return a path string where the home path is substituted with ~.
        
        Positional arguments:
            linkPath: str -- Full link path.
        """
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            linkPath = linkPath.replace(homeDir, '~')
        except:
            pass
        return linkPath

    def open_link(self, linkPath):
        """Open a link specified by linkPath.
        
        Positional arguments:
            linkPath: str -- Link path as stored in novx.
        """
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            linkPath = linkPath.replace('~', homeDir)
        except:
            pass
        try:
            extension = os.path.splitext(linkPath)[1]
        except IndexError:
            pass
        else:
            launcher = launchers.get(extension, '')
            if os.path.isfile(launcher):
                subprocess.Popen([launcher, linkPath])
                return True

        if os.path.isfile(linkPath):
            open_document(linkPath)
            return True

        return False


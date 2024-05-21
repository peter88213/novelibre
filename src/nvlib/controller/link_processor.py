"""Provide a class for processing links.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import glob
import os
from pathlib import Path
import subprocess

from novxlib.novx_globals import _
from novxlib.novx_globals import norm_path
from novxlib.novx_globals import open_document


class LinkProcessor:
    """Strategy class for link processing."""
    ZIM_NOTE_EXTENSION = '.txt'

    def __init__(self, model):
        self._mdl = model
        # holding the project path

    def shorten_path(self, linkPath):
        """Return a shortened path string. 
        
        Positional arguments:
            linkPath: str -- Full link path.
            
        If linkPath is on the same drive as the project path,
        the shortened path is relative to the project path.            
        """
        projectDir = os.path.split(self._mdl.prjFile.filePath)[0]
        try:
            linkPath = os.path.relpath(linkPath, projectDir)
        except ValueError:
            pass
        return linkPath.replace('\\', '/')

    def expand_path(self, linkPath):
        """Return an expanded path string.
        
        Positional arguments:
            linkPath: str -- Link path as stored in novx.

        A leading "~" is substituted with the full home path.            
        A path relative to the project path is expanded to a full path.
        """
        if linkPath.startswith('~'):
            homeDir = str(Path.home())
            linkPath = linkPath.replace('~', homeDir, 1)
        else:
            projectDir = os.path.split(self._mdl.prjFile.filePath)[0]
            linkPath = os.path.join(projectDir, linkPath)
        return os.path.realpath(linkPath).replace('\\', '/')

    def open_link(self, linkPath, launchers):
        """Open a link specified by linkPath. Return True on success.
        
        If linkPath is in a Zim wiki subdirectory, 
        start Zim with the specified page.   
        
        Positional arguments:
            linkPath: str -- Link path as stored in novx.
            launchers: dict -- key: extension, value: path to application.
        """
        linkPath = self.expand_path(linkPath)
        extension = None
        try:
            filePath, extension = os.path.splitext(linkPath)
            if extension == self.ZIM_NOTE_EXTENSION:
                launcher = launchers['.zim']
                if os.path.isfile(launcher):
                    pagePath = filePath.split('/')
                    zimPages = []
                    # this is for the page path in Zim notation

                    # Search backwards through the file branch.
                    while pagePath:
                        zimPages.insert(0, pagePath.pop())
                        zimPath = '/'.join(pagePath)
                        zimNotebook = glob.glob(norm_path(f'{zimPath}/*.zim'))
                        if zimNotebook:
                            # the link path belongs to a Zim wiki
                            subprocess.Popen([launcher, zimNotebook[0], ":".join(zimPages)])
                            return

        except:
            pass
        launcher = launchers.get(extension, '')
        if os.path.isfile(launcher):
            subprocess.Popen([launcher, linkPath])
            return

        if os.path.isfile(linkPath):
            open_document(linkPath)
            return

        raise FileNotFoundError(f"{_('File not found')}: {norm_path(linkPath)}")


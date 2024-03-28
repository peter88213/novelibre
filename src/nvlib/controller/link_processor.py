"""Provide a class for processing links.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import glob
import os
from pathlib import Path
import subprocess

from novxlib.file.doc_open import open_document
from novxlib.novx_globals import _
from novxlib.novx_globals import norm_path


class LinkProcessor:
    """Strategy class for link processing."""
    ZIM_NOTE_EXTENSION = '.txt'

    def __init__(self, model):
        self._mdl = model
        # this is needed for d

    def shorten_path(self, linkPath):
        """Return a shortened path string. 
        
        Positional arguments:
            linkPath: str -- Full link path.
            
        The project path is substituted with ".", if leading.
        Otherwise, the home path is substituted with "~", if leading.            
        """
        projectDir = os.path.split(self._mdl.prjFile.filePath)[0].replace('\\', '/')
        if linkPath.startswith(projectDir):
            linkPath = linkPath.replace(projectDir, '.')
        else:
            homeDir = str(Path.home()).replace('\\', '/')
            linkPath = linkPath.replace(homeDir, '~')
        return linkPath

    def expand_path(self, linkPath):
        """Return an expanded path string.
        
        Positional arguments:
            linkPath: str -- Link path as stored in novx.

        A leading "." is substituted with the project path.
        A leading "~" is substituted with the home path.            
        """
        if linkPath.startswith('.'):
            projectDir = os.path.split(self._mdl.prjFile.filePath)[0].replace('\\', '/')
            linkPath = linkPath.replace('.', projectDir, 1)
        elif linkPath.startswith('~'):
            homeDir = str(Path.home()).replace('\\', '/')
            linkPath = linkPath.replace('~', homeDir, 1)
        return linkPath

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


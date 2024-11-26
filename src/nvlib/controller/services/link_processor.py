"""Provide a class for processing links.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import glob
import os
from pathlib import Path
import subprocess

from mvclib.controller.service_base import ServiceBase
from nvlib.model.file.doc_open import open_document
from nvlib.novx_globals import _
from nvlib.novx_globals import norm_path


class LinkProcessor(ServiceBase):
    """Strategy class for link processing."""
    ZIM_NOTE_EXTENSION = '.txt'

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

    def open_link_by_index(self, element, linkIndex):
        """Open a linked file.
        
        Positional arguments:
            element: BasicElement or subclass.
            linkIndex: int -- Index of the link to open.
            
        First try to open the link using its relative path.
        If this fails, try to open it using the "full" path. 
        On success, fix the link. 
        Otherwise, show an error message. 
        """
        self._ui.restore_status()
        relativePath = list(element.links)[linkIndex]
        fullPath = element.links[relativePath]
        try:
            self.open_link(relativePath)
        except:

            # The relative link seems to be broken. Try the full path.
            if fullPath is not None:
                newPath = self.shorten_path(fullPath)
            else:
                newPath = ''
            # fixing the link using the full path
            try:
                self.open_link(newPath)
            except Exception as ex:

                # The full path is also broken.
                self._ui.show_error(
                    str(ex),
                    title=_('Cannot open link')
                    )
            else:
                # Replace the broken link with the fixed one.
                links = element.links
                del links[relativePath]
                links[newPath] = fullPath
                element.links = links
                self._ui.set_status(_('Broken link fixed'))
        else:
            # Relative path is o.k. -- now check the full path.
            pathOk = self.expand_path(relativePath)
            if fullPath != pathOk:
                # Replace the broken full path.
                links = element.links
                links[relativePath] = pathOk
                element.links = links
                self._ui.set_status(_('Broken link fixed'))

    def open_link(self, linkPath):
        """Open a link specified by linkPath. Return True on success.
        
        If linkPath is in a Zim wiki subdirectory, 
        start Zim with the specified page.   
        
        Positional arguments:
            linkPath: str -- Link path as stored in novx.
        """
        linkPath = self.expand_path(linkPath)
        extension = None
        try:
            filePath, extension = os.path.splitext(linkPath)
            if extension == self.ZIM_NOTE_EXTENSION:
                launcher = self._ctrl.launchers['.zim']
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
        launcher = self._ctrl.launchers.get(extension, '')
        if os.path.isfile(launcher):
            subprocess.Popen([launcher, linkPath])
            return

        if os.path.isfile(linkPath):
            open_document(linkPath)
            return

        raise FileNotFoundError(f"{_('File not found')}: {norm_path(linkPath)}")


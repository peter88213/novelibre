"""Provide a class for processing links.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import subprocess

from mvclib.controller.service_base import ServiceBase
from nvlib.model.file.doc_open import open_document
from nvlib.novx_globals import norm_path
from nvlib.nv_globals import HOME_DIR
from nvlib.nv_globals import launchers
from nvlib.nv_locale import _


class LinkProcessor(ServiceBase):
    """Strategy class for link processing."""

    def __init__(self, model, view, controller):
        super().__init__(model, view, controller)
        self.externalOpeners = []
        # list of callback functions

    def add_opener(self, method):
        self.externalOpeners.append(method)

    def expand_path(self, linkPath):
        """Return an expanded path string.
        
        Positional arguments:
            linkPath: str -- Link path as stored in novx.

        A leading "~" is substituted with the full home path.            
        A path relative to the project path is expanded to a full path.
        """
        if linkPath.startswith('~'):
            linkPath = linkPath.replace('~', HOME_DIR, 1)
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
                if not self._ctrl.isLocked:
                    # Replace the broken link with the fixed one.
                    links = element.links
                    del links[relativePath]
                    links[newPath] = fullPath
                    element.links = links
                    self._ui.set_status(f"#{_('Broken link fixed')}")
        else:
            if not self._ctrl.isLocked:
                # Relative path is o.k. -- now check the full path.
                pathOk = self.expand_path(relativePath)
                if fullPath != pathOk:
                    # Replace the broken full path.
                    links = element.links
                    links[relativePath] = pathOk
                    element.links = links
                    self._ui.set_status(f"#{_('Broken link fixed')}")

    def open_link(self, linkPath):
        """Open a link specified by linkPath. Return True on success.
        
        Positional arguments:
            linkPath: str -- Link path as stored in novx.
        """
        linkPath = self.expand_path(linkPath)
        for externalOpener in self.externalOpeners:
            try:
                if externalOpener(linkPath):
                    # the link is opened by an external function
                    return

            except:
                pass
        __, extension = os.path.splitext(linkPath)
        launcher = launchers.get(extension, '')
        if os.path.isfile(launcher):
            subprocess.Popen([launcher, linkPath])
            return

        if os.path.isfile(linkPath):
            open_document(linkPath)
            return

        raise FileNotFoundError(f"{_('File not found')}: {norm_path(linkPath)}")

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


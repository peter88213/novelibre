"""Provide a class for Zim link processing.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.view.properties_window.link_processor import LinkProcessor


class ZimLinker(LinkProcessor):

    def to_novx(self, linkPath):
        """Return a path string where the home path is substituted with ~.
        
        Positional arguments:
            linkPath: str -- Full link path.
        
        Extends the superclass method.
        """
        print("Zim in!")
        return super().to_novx(linkPath)

    def open_link(self, linkPath):
        """Open a link specified by linkPath.
        
        Positional arguments:
            linkPath: str -- Link path as stored in novx.

        Extends the superclass method.
        """
        print("Zim out!")
        return super().open_link(linkPath)

"""Provide an abstract Plugin base class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod


class PluginBase(ABC):
    """Abstract Plugin base class.
    
    Public class constants:
        VERSION: str -- Version string.
        NOVELYST_API: str -- API compatibility indicator.
        DESCRIPTION: str -- Description to be diplayed in the noveltree plugin list.
        URL: str -- Plugin project homepage URL.

    Public instance variables:
        filePath: str -- Location of the installed plugin.
        isActive: Boolean -- Acceptance flag.
        isRejected: Boolean --  Rejection flag.
    """
    # Class constants to be overridden by subclasses.
    VERSION = ''
    NOVELYST_API = ''
    DESCRIPTION = ''
    URL = ''

    def __init__(self):
        self.filePath = None
        self.isActive = True
        self.isRejected = False

    @abstractmethod
    def install(self, model, view, controller, prefs):
        """Install the plugin.
        
        Positional arguments:
            view -- reference to the NoveltreeUi instance of the application.
        """
        pass

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        pass

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        pass

    def on_close(self):
        """Actions to be performed when a project is closed."""
        pass

    def on_quit(self):
        """Actions to be performed when noveltree is closed."""
        pass

    def open_node(self):
        """Actions on double-clicking on a node or pressing the Return key."""
        pass

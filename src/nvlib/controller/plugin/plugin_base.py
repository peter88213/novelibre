"""Provide an abstract Plugin base class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod

from nvlib.controller.sub_controller import SubController


class PluginBase(ABC, SubController):
    """Abstract Plugin base class.
    
    Public methods:
        - install
        
    Public methods (inherited from SubController):
        - disable_menu
        - enable_menu
        - lock  
        - on_close
        - on_quit
        - unlock
    
    Public class constants:
        VERSION: str -- Version string.
        API_VERSION: str -- API compatibility indicator.
        DESCRIPTION: str -- Description to be diplayed in the novelibre plugin list.
        URL: str -- Plugin project homepage URL.

    Public instance variables:
        filePath: str -- Location of the installed plugin.
        isActive: Boolean -- Acceptance flag.
        isRejected: Boolean --  Rejection flag.
    """
    # Class constants to be overridden by subclasses.
    VERSION = ''
    API_VERSION = ''
    DESCRIPTION = ''
    URL = ''

    def __init__(self):
        self.filePath = None
        self.isActive = True
        self.isRejected = False

    @abstractmethod
    def install(self, model, view, controller):
        """Install the plugin.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.
        """
        self.initialize_controller(model, view, controller)


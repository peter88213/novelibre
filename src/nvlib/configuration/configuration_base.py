"""Provide an abstract Configuration base class.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod


class ConfigurationBase(ABC):
    """Application configuration.

        Configuration file sections:
        SETTINGS - Strings
        OPTIONS - Boolean values

    Public instance variables:    
        settings - dictionary of strings
        options - dictionary of boolean values
    """

    def __init__(self, settings=None, options=None):
        """Initalize attribute variables.

        Optional arguments:
            settings: dict of str -- default settings
            options: dict of bool -- default options
        """
        self.settings = None
        self.options = None
        self._sLabel = 'SETTINGS'
        self._oLabel = 'OPTIONS'
        self.set(settings, options)

    @abstractmethod
    def read(self, iniFile):
        """Read the configuration from iniFile.
        
        Positional arguments:
            iniFile: str -- configuration file path.
            
        Settings and options that can not be read in, remain unchanged.
        """
        # - Read the configuration file.
        # - If there is a SETTINGS section, get the settings,
        #   using the defaults as fallback.
        # - If there is an OPTIONS section, get the options,
        #   using the defaults as fallback.

    def set(self, settings=None, options=None):
        """Set the entire configuration without writing the file.

        Optional arguments:
            settings: dict of str -- new settings
            options: dict of bool -- new options
        """
        self.settings = (settings or {}).copy()
        self.options = (options or {}).copy()

    @abstractmethod
    def write(self, iniFile):
        """Save the configuration to iniFile.

        Positional arguments:
            iniFile: str -- configuration file path.
        """
        pass
        # - If there are settings, write them to the SETTINGS section.
        # - If there are options, write them to the OPTIONS section.
        # - Do not write empty sections.


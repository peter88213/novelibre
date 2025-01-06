"""Provide a customized Configuration class for reading and writing INI files.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from configparser import ConfigParser
from nvlib.configuration.configuration import Configuration


class NvConfiguration(Configuration):
    """Application configuration, representing an INI file."""

    def read(self, iniFile:str):
        """Read a configuration file.
        
        Positional arguments:
            iniFile -- path configuration file path.
            
        Just read in settings that already exist in the file.
        Overrides the superclass method. 
        """
        config = ConfigParser()
        config.read(iniFile, encoding='utf-8')
        if config.has_section(self._sLabel):
            section = config[self._sLabel]
            for app in section:
                self.settings[app] = section[app]


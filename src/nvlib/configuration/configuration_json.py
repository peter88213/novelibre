"""Provide a Configuration class for reading and writing JSON files.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import json

from nvlib.configuration.configuration_base import ConfigurationBase


class ConfigurationJson(ConfigurationBase):
    """Application configuration, representing a JSON file.

        Configuration file sections:
        SETTINGS - Strings
        OPTIONS - Boolean values

    Public instance variables:    
        settings - dictionary of strings
        options - dictionary of boolean values
    """

    def read(self, iniFile):
        """Read the configuration from iniFile.
        
        Positional arguments:
            iniFile: str -- configuration file path.
            
        Settings and options that can not be read in, remain unchanged.
        """
        try:
            with open(iniFile, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}
        if self._sLabel in config:
            section = config[self._sLabel]
            for setting in self.settings:
                fallback = self.settings[setting]
                self.settings[setting] = section.get(setting, fallback)
        if self._oLabel in config:
            section = config[self._oLabel]
            for option in self.options:
                fallback = self.options[option]
                self.options[option] = section.get(option, fallback)

    def write(self, iniFile):
        """Save the configuration to iniFile.

        Positional arguments:
            iniFile: str -- configuration file path.
        """
        with open(iniFile, 'w', encoding='utf-8') as f:
            config = {}
            if self.settings:
                config[self._sLabel] = self.settings
            if self.options:
                config[self._oLabel] = self.options
            json.dump(
                config,
                f,
                ensure_ascii=False,
                indent=4,
            )

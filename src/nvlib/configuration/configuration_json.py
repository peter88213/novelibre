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

    def read(self, filePath=None):
        """Read the configuration file.
        
        Optional arguments:
            filePath: str -- configuration file path.
            
        Settings and options that can not be read in, remain unchanged.
        """
        filePath = filePath or self.filePath
        try:
            with open(filePath, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}
        if self.strLabel in config:
            section = config[self.strLabel]
            for setting in self.settings:
                fallback = self.settings[setting]
                self.settings[setting] = section.get(setting, fallback)
        if self.boolLabel in config:
            section = config[self.boolLabel]
            for option in self.options:
                fallback = self.options[option]
                self.options[option] = section.get(option, fallback)

    def write(self, filePath=None):
        """Save the configuration.

        Optional arguments:
            filePath: str -- configuration file path.
        """
        filePath = filePath or self.filePath
        with open(filePath, 'w', encoding='utf-8') as f:
            config = {}
            if self.settings:
                config[self.strLabel] = self.settings
            if self.options:
                config[self.boolLabel] = self.options
            json.dump(
                config,
                f,
                ensure_ascii=False,
                indent=4,
            )

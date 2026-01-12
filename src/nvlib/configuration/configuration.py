"""Provide a Configuration class for reading and writing INI files.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from configparser import ConfigParser

from nvlib.configuration.configuration_base import ConfigurationBase


class Configuration(ConfigurationBase):
    """Application configuration, representing an INI file.

        Configuration file sections:
        SETTINGS - Strings
        OPTIONS - Boolean values

    Public instance variables:    
        settings - dictionary of strings
        options - dictionary of boolean values
    """

    def read(self, filePath=None):
        """Read the configuration file.
        
        Positional arguments:
            filePath: str -- configuration file path.
            
        Settings and options that can not be read in, remain unchanged.
        """
        self.filePath = self.filePath or filePath
        # this is for downward compatibility with plugins

        config = ConfigParser()
        config.read(self.filePath, encoding='utf-8')
        if self.strLabel in config:
            section = config[self.strLabel]
            for setting in self.settings:
                fallback = self.settings[setting]
                self.settings[setting] = section.get(setting, fallback)
        if self.boolLabel in config:
            section = config[self.boolLabel]
            for option in self.options:
                fallback = self.options[option]
                self.options[option] = section.getboolean(option, fallback)

    def write(self, filePath=None):
        """Save the configuration.

        Positional arguments:
            filePath: str -- configuration file path.
        """
        self.filePath = self.filePath or filePath
        # this is for downward compatibility with plugins

        config = ConfigParser()
        if self.settings:
            config.add_section(self.strLabel)
            for settingId in self.settings:
                config.set(
                    self.strLabel,
                    settingId,
                    str(self.settings[settingId]),
                )
        if self.options:
            config.add_section(self.boolLabel)
            for settingId in self.options:
                if self.options[settingId]:
                    config.set(self.boolLabel, settingId, 'Yes')
                else:
                    config.set(self.boolLabel, settingId, 'No')
        with open(self.filePath, 'w', encoding='utf-8') as f:
            config.write(f)

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

    def read(self, iniFile):
        """Read a configuration file.
        
        Positional arguments:
            iniFile: str -- path configuration file path.
            
        Settings and options that can not be read in, remain unchanged.
        """
        config = ConfigParser()
        config.read(iniFile, encoding='utf-8')
        self._get_configuration(config)

    def write(self, iniFile):
        """Save the configuration to iniFile.

        Positional arguments:
            iniFile: str -- path configuration file path.
        """
        config = ConfigParser()
        if self.settings:
            config.add_section(self._sLabel)
            for settingId in self.settings:
                config.set(
                    self._sLabel,
                    settingId,
                    str(self.settings[settingId]),
                )
        if self.options:
            config.add_section(self._oLabel)
            for settingId in self.options:
                if self.options[settingId]:
                    config.set(self._oLabel, settingId, 'Yes')
                else:
                    config.set(self._oLabel, settingId, 'No')
        with open(iniFile, 'w', encoding='utf-8') as f:
            config.write(f)

"""Provide a Configuration class for reading and writing INI files.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from configparser import ConfigParser


class Configuration:
    """Application configuration, representing an INI file.

        INI file sections:
        <self._sLabel> - Strings
        <self._oLabel> - Boolean values

    Public instance variables:    
        settings - dictionary of strings
        options - dictionary of boolean values
    """

    def __init__(self, settings={}, options={}):
        """Initalize attribute variables.

        Optional arguments:
            settings -- default settings (dictionary of strings)
            options -- default options (dictionary of boolean values)
        """
        self.settings = None
        self.options = None
        self._sLabel = 'SETTINGS'
        self._oLabel = 'OPTIONS'
        self.set(settings, options)

    def read(self, iniFile):
        """Read a configuration file.
        
        Positional arguments:
            iniFile: str -- path configuration file path.
            
        Settings and options that can not be read in, remain unchanged.
        """
        config = ConfigParser()
        config.read(iniFile, encoding='utf-8')
        if config.has_section(self._sLabel):
            section = config[self._sLabel]
            for setting in self.settings:
                fallback = self.settings[setting]
                self.settings[setting] = section.get(setting, fallback)
        if config.has_section(self._oLabel):
            section = config[self._oLabel]
            for option in self.options:
                fallback = self.options[option]
                self.options[option] = section.getboolean(option, fallback)

    def set(self, settings=None, options=None):
        """Set the entire configuration without writing the INI file.

        Optional arguments:
            settings -- new settings (dictionary of strings)
            options -- new options (dictionary of boolean values)
        """
        if settings is not None:
            self.settings = settings.copy()
        if options is not None:
            self.options = options.copy()

    def write(self, iniFile):
        """Save the configuration to iniFile.

        Positional arguments:
            iniFile: str -- path configuration file path.
        """
        config = ConfigParser()
        if self.settings:
            config.add_section(self._sLabel)
            for settingId in self.settings:
                config.set(self._sLabel, settingId, str(self.settings[settingId]))
        if self.options:
            config.add_section(self._oLabel)
            for settingId in self.options:
                if self.options[settingId]:
                    config.set(self._oLabel, settingId, 'Yes')
                else:
                    config.set(self._oLabel, settingId, 'No')
        with open(iniFile, 'w', encoding='utf-8') as f:
            config.write(f)

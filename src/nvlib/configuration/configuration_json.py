"""Provide a Configuration class for reading and writing JSON files.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import json

from nvlib.configuration.configuration_base import ConfigurationBase


class ConfigurationJson(ConfigurationBase):
    """Application configuration, representing a JSON file.

    Public instance constants:    
        strLabel - Label of the config section containing strings.
        boolLabel - Label of the config section containing boolean values.

    Public instance variables:    
        settings: dict of str - Configuration strings.
        options: dict of bool - Configuration booleans.
        filePath: str - Path to the configuration file.
    """

    def read(self):
        """Read the configuration file.
            
        Settings and options that can not be read in, remain unchanged.
        """
        try:
            with open(self.filePath, 'r', encoding='utf-8') as f:
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

    def write(self):
        """Save the configuration file."""
        with open(self.filePath, 'w', encoding='utf-8') as f:
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

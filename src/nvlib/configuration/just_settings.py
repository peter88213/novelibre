"""Provide a reduced Configuration class for reading and writing INI files.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from configparser import ConfigParser

from nvlib.configuration.configuration import Configuration


class JustSettings(Configuration):
    """Reduced configuration, representing an INI file.
    
    - Only the file's SETTINGS section is used. 
    - The OPTIONS section is not used, if any.
    - The constructor's optional arguments are not considered, if any. 
    """

    def read(self):
        """Read a configuration file.
        
        Just read in settings that exist in the file.
        Do not use default settings as fallback.
        Overrides the superclass method. 
        """
        config = ConfigParser()
        config.read(self.filePath, encoding='utf-8')
        if config.has_section(self.strLabel):
            section = config[self.strLabel]
            for setting in section:
                self.settings[setting] = section[setting]


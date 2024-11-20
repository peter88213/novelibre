"""Provide a substitute for the Plugin class of a rejected module.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class RejectedPlugin:
    """Substitute for the Plugin class of a rejected module.
    
    Class constants:
        VERSION: -- str -- Version string.
        NOVELYST_API: -- str -- API compatibility indicator.
        URL: str -- Plugin project URL substitute.
    
    Public instance variables:
        filePath: str -- Location of the installed plugin.
        isActive: Boolean -- Acceptance flag.
        isRejected: Boolean --  Rejection flag.
        DESCRIPTION: str -- Error message to be displayed instead of the plugin description.   
    """
    VERSION = '-'
    API_VERSION = '-'
    URL = ''

    def __init__(self, filePath, message):
        self.filePath = filePath
        self.isActive = False
        self.isRejected = True
        self.DESCRIPTION = message


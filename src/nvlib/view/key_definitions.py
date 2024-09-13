"""Provide platform specific key definitions for the novelibre application.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.nv_globals import PLATFORM
from nvlib.view.generic_keys import GenericKeys
from nvlib.view.mac_keys import MacKeys
from nvlib.view.windows_keys import WindowsKeys

if PLATFORM == 'win':
    KEYS = WindowsKeys()
elif PLATFORM == 'ix':
    KEYS = GenericKeys()
elif PLATFORM == 'mac':
    KEYS = MacKeys()
else:
    KEYS = GenericKeys()

"""Provide a class with mouse operation definitions for Windows.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.platform.generic_mouse import GenericMouse


class WindowsMouse(GenericMouse):

    BACK_CLICK = '<Button-4>'
    FORWARD_CLICK = '<Button-5>'

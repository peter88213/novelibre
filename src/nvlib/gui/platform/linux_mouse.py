"""Provide a class with mouse operation definitions for Linux.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nvovelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.platform.generic_mouse import GenericMouse


class LinuxMouse(GenericMouse):

    BACK_SCROLL = '<Button-4>'
    FORWARD_SCROLL = '<Button-5>'


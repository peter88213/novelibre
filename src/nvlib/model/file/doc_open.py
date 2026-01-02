"""Helper module for opening documents.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.gui.platform.platform_settings import PLATFORM
from nvlib.novx_globals import norm_path


def open_document(document):
    """Open a document with the operating system's standard application."""
    if PLATFORM == 'win':
        os.startfile(norm_path(document))
        return

    if PLATFORM == 'ix':
        os.system('xdg-open "%s"' % norm_path(document))
        return

    if PLATFORM == 'mac':
        os.system('open "%s"' % norm_path(document))

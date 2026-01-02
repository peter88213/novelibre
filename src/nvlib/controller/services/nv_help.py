"""Provide a service class for the help function.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import webbrowser

from nvlib.nv_locale import _


class NvHelp:

    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/'

    @classmethod
    def open_help_page(cls, page):
        """Show the online help page specified by page."""
        webbrowser.open(f'{cls.HELP_URL}{page}')


"""Provide a service class for the online help function.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import webbrowser

from nvlib.nv_locale import _


class NvOnlineHelp:

    HELP_URL = _("https://peter88213.github.io/nvhelp-en")

    def open_help_page(self, page, site=None):
        """Show the online help page specified by page."""
        webbrowser.open(f'{site or self.HELP_URL}/{page}')


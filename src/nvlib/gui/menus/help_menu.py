"""Provide a class for the "Help" menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.nv_locale import _


class HelpMenu(NvMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)

        self.add_command(
            label=_('Online help'),
            accelerator=KEYS.OPEN_HELP[1],
            command=self._ctrl.open_help,
        )
        self.add_command(
            label=_('About novelibre'),
            command=self._ui._about,
        )
        self.add_command(
            label=f"novelibre {_('Home page')}",
            command=self._ctrl.open_homepage,
        )
        self.add_command(
            label=_('News about novelibre'),
            command=self._ctrl.open_news,
        )
        self.add_separator()

"""Provide a class for the novelibre main menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.nv_locale import _
import tkinter as tk


class MainMenu(tk.Menu, NvMenu):

    def __init__(self, view, controller):
        tk.Menu.__init__(self, tearoff=0)
        NvMenu.__init__(self, view, controller)

        label = _('File')
        self.add_cascade(
            label=label,
            menu=self._ui.fileMenu,
        )

        label = _('View')
        self.add_cascade(
            label=label,
            menu=self._ui.viewMenu
        )

        label = _('Part')
        self.add_cascade(
            label=label,
            menu=self._ui.partMenu,
        )
        self._disableOnClose.append(label)

        label = _('Chapter')
        self.add_cascade(
            label=label,
            menu=self._ui.chapterMenu,
        )
        self._disableOnClose.append(label)

        label = _('Section')
        self.add_cascade(
            label=label,
            menu=self._ui.sectionMenu,
        )
        self._disableOnClose.append(label)

        label = _('Characters')
        self.add_cascade(
            label=label,
            menu=self._ui.characterMenu,
        )
        self._disableOnClose.append(label)

        label = _('Locations')
        self.add_cascade(
            label=label,
            menu=self._ui.locationMenu,
        )
        self._disableOnClose.append(label)

        label = _('Items')
        self.add_cascade(
            label=label,
            menu=self._ui.itemMenu,
        )
        self._disableOnClose.append(label)

        label = _('Plot')
        self.add_cascade(
            label=label,
            menu=self._ui.plotMenu
        )
        self._disableOnClose.append(label)

        label = _('Project notes')
        self.add_cascade(
            label=label,
            menu=self._ui.prjNoteMenu,
        )
        self._disableOnClose.append(label)

        label = _('Import')
        self.add_command(
            label=label,
            command=self._ctrl.open_project_updater
        )
        self._disableOnLock.append(label)
        self._disableOnClose.append(label)

        label = _('Export')
        self.add_cascade(
            label=label,
            menu=self._ui.exportMenu,
        )
        self._disableOnClose.append(label)

        label = _('Tools')
        self.add_cascade(
            label=label,
            menu=self._ui.toolsMenu
        )
        self._disableOnClose.append(label)

        label = _('Help')
        self.add_cascade(
            label=label,
            menu=self._ui.helpMenu,
        )

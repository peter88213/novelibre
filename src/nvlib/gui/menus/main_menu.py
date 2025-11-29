"""Provide a class for the novelibre main menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.nv_locale import _


class MainMenu(NvMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)

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
        self.disableOnClose.append(label)

        label = _('Chapter')
        self.add_cascade(
            label=label,
            menu=self._ui.chapterMenu,
        )
        self.disableOnClose.append(label)

        label = _('Section')
        self.add_cascade(
            label=label,
            menu=self._ui.sectionMenu,
        )
        self.disableOnClose.append(label)

        label = _('Characters')
        self.add_cascade(
            label=label,
            menu=self._ui.characterMenu,
        )
        self.disableOnClose.append(label)

        label = _('Locations')
        self.add_cascade(
            label=label,
            menu=self._ui.locationMenu,
        )
        self.disableOnClose.append(label)

        label = _('Items')
        self.add_cascade(
            label=label,
            menu=self._ui.itemMenu,
        )
        self.disableOnClose.append(label)

        label = _('Plot')
        self.add_cascade(
            label=label,
            menu=self._ui.plotMenu
        )
        self.disableOnClose.append(label)

        label = _('Project notes')
        self.add_cascade(
            label=label,
            menu=self._ui.prjNoteMenu,
        )
        self.disableOnClose.append(label)

        label = _('Import')
        self.add_command(
            label=label,
            command=self._ctrl.open_project_updater
        )
        self.disableOnLock.append(label)
        self.disableOnClose.append(label)

        label = _('Export')
        self.add_cascade(
            label=label,
            menu=self._ui.exportMenu,
        )
        self.disableOnClose.append(label)

        label = _('Tools')
        self.add_cascade(
            label=label,
            menu=self._ui.toolsMenu
        )

        label = _('Help')
        self.add_cascade(
            label=label,
            menu=self._ui.helpMenu,
        )

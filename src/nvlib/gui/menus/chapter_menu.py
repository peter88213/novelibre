"""Provide a class for the "Chapter" menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.nv_locale import _


class ChapterMenu(NvMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)

        label = _('Add')
        self.add_command(
            label=label,
            command=self._ctrl.add_new_chapter,
        )
        self.disableOnLock.append(label)

        label = _('Add multiple chapters...')
        self.add_command(
            label=label,
            command=self._ctrl.add_multiple_new_chapters,
        )
        self.disableOnLock.append(label)

        self.add_separator()

        self._add_set_type_cascade()
        self._add_change_level_cascade()

        self.add_separator()

        label = _('Move selected chapters to new project')
        self.add_command(
            label=label,
            command=self._ctrl.split_file,
        )
        self.disableOnLock.append(label)

        self.add_separator()

        label = _('Export chapter descriptions for editing')
        self.add_command(
            label=label,
            command=self._ctrl.export_chapter_desc,
        )
        self.disableOnLock.append(label)

        label = _('Export chapter table')
        self.add_command(
            label=label,
            command=self._ctrl.export_chapter_list,
        )
        self.disableOnLock.append(label)


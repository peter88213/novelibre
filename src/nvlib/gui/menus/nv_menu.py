"""Provide a base class for novelibre menus.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.sub_controller import SubController
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.nv_locale import _
import tkinter as tk


class NvMenu(tk.Menu, SubController):

    def __init__(self, view, controller):
        super().__init__(tearoff=0)
        self._ui = view
        self._ctrl = controller
        self._disableOnLock = []
        self._disableOnClose = []

    def disable_menu(self):
        for label in self._disableOnClose:
            self.entryconfig(label, state='disabled')

    def enable_menu(self):
        for label in self._disableOnClose:
            self.entryconfig(label, state='normal')

    def lock(self):
        for label in self._disableOnLock:
            self.entryconfig(label, state='disabled')

    def unlock(self):
        for label in self._disableOnLock:
            self.entryconfig(label, state='normal')

    def _add_add_command(self):
        label = _('Add')
        self.add_command(
            label=label,
            command=self._ctrl.add_new_element,
        )
        self._disableOnLock.append(label)

    def _add_clipboard_commands(self):
        label = _('Cut')
        self.add_command(
            label=label,
            accelerator=KEYS.CUT[1],
            command=self._ctrl.cut_element,
        )
        self._disableOnLock.append(label)

        label = _('Copy')
        self.add_command(
            label=label,
            accelerator=KEYS.COPY[1],
            command=self._ctrl.copy_element,
        )
        label = _('Paste')
        self.add_command(
            label=label,
            accelerator=KEYS.PASTE[1],
            command=self._ctrl.paste_element,
        )
        self._disableOnLock.append(label)

    def _add_add_section_command(self):
        label = _('Add Section')
        self.add_command(
            label=label,
            command=self._ctrl.add_new_section,
        )
        self._disableOnLock.append(label)

    def _add_delete_command(self):
        label = _('Delete')
        self.add_command(
            label=label,
            accelerator=KEYS.DELETE[1],
            command=self._ctrl.delete_elements,
        )
        self._disableOnLock.append(label)

    def _add_change_level_cascade(self):
        label = _('Change Level')
        self.add_cascade(
            label=label,
            menu=self._ui.selectLevelMenu,
        )
        self._disableOnLock.append(label)

    def _add_chapter_part_commands(self):
        label = _('Add Chapter')
        self.add_command(
            label=label,
            command=self._ctrl.add_new_chapter
        )
        self._disableOnLock.append(label)

        label = _('Add Part')
        self.add_command(
            label=label,
            command=self._ctrl.add_new_part,
        )
        self._disableOnLock.append(label)

    def _add_insert_stage_command(self):
        label = _('Insert Stage')
        self.add_command(
            label=label,
            command=self._ctrl.add_new_stage,
        )
        self._disableOnLock.append(label)

    def _add_set_cr_status_cascade(self):
        label = _('Set Status')
        self.add_cascade(
            label=label,
            menu=self._ui.selectCharacterStatusMenu,
        )
        self._disableOnLock.append(label)

    def _add_set_status_cascade(self):
        label = _('Set Status')
        self.add_cascade(
            label=label,
            menu=self._ui.selectSectionStatusMenu,
        )
        self._disableOnLock.append(label)

    def _add_set_type_cascade(self):
        label = _('Set Type')
        self.add_cascade(
            label=label,
            menu=self._ui.selectTypeMenu,
        )
        self._disableOnLock.append(label)

    def _add_set_viewpoint_command(self):
        label = _('Set Viewpoint...')
        self.add_command(
            label=label,
            command=self._ctrl.set_viewpoint,
        )
        self._disableOnLock.append(label)

    def _add_view_commands(self):
        label = _('Chapter level')
        self.add_command(
            label=label,
            command=self._ui.tv.show_chapter_level,
        )
        self._disableOnClose.append(label)

        label = _('Expand all')
        self.add_command(
            label=label,
            command=self._ui.tv.expand_all,
        )
        self._disableOnClose.append(label)

        label = _('Collapse all')
        self.add_command(
            label=label,
            command=self._ui.tv.collapse_all,
        )
        self._disableOnClose.append(label)


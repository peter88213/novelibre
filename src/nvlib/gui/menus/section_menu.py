"""Provide a class for the "Section" menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.nv_locale import _
import tkinter as tk


class SectionMenu(tk.Menu, NvMenu):

    def __init__(self, view, controller):
        tk.Menu.__init__(self, tearoff=0)
        NvMenu.__init__(self, view, controller)

        label = _('Add')
        self.add_command(
            label=label,
            command=self._ctrl.add_new_section,
        )
        self._disableOnLock.append(label)

        label = _('Add multiple sections...')
        self.add_command(
            label=label,
            command=self._ctrl.add_multiple_new_sections,
        )
        self._disableOnLock.append(label)

        self.add_separator()

        self._add_set_type_cascade()
        self._add_set_status_cascade()
        self._add_set_viewpoint_command()

        self.add_separator()

        label = _('Export section descriptions for editing')
        self.add_command(
            label=label,
            command=self._ctrl.export_section_desc,
        )
        self._disableOnLock.append(label)

        self.add_separator()

        label = _('Section table (export only)')
        self.add_command(
            label=label,
            command=self._ctrl.export_section_list,
        )

        label = _('Show Time table')
        self.add_command(
            label=label,
            command=self._ctrl.show_timetable,
        )


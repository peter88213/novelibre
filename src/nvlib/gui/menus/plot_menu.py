"""Provide a class for the "Plot" menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.nv_locale import _
import tkinter as tk


class PlotMenu(tk.Menu, NvMenu):

    def __init__(self, view, controller):
        tk.Menu.__init__(self, tearoff=0)
        NvMenu.__init__(self, view, controller)

        label = _('Add Plot line')
        self.add_command(
            label=label,
            command=self._ctrl.add_new_plot_line,
        )
        self._disableOnLock.append(label)

        label = _('Add Plot point')
        self.add_command(
            label=label,
            command=self._ctrl.add_new_plot_point,
        )
        self._disableOnLock.append(label)

        self.add_separator()

        self._add_insert_stage_command()
        self._add_change_level_cascade()

        self.add_separator()

        label = _('Import plot lines')
        self.add_command(
            label=label,
            command=self._ctrl.import_plot_lines,
        )
        self._disableOnLock.append(label)

        self.add_separator()

        label = _('Export plot grid for editing')
        self.add_command(
            label=label,
            command=self._ctrl.export_plot_grid,
        )
        self._disableOnLock.append(label)

        label = _('Export story structure description for editing')
        self.add_command(
            label=label,
            command=self._ctrl.export_story_structure_desc,
        )
        self._disableOnLock.append(label)

        label = _('Export plot line descriptions for editing')
        self.add_command(
            label=label,
            command=self._ctrl.export_plot_lines_desc,
        )
        self._disableOnLock.append(label)

        self.add_separator()

        label = _('Plot table (export only)')
        self.add_command(
            label=label,
            command=self._ctrl.export_plot_list,
        )

        label = _('Show Plot table in browser')
        self.add_command(
            label=label,
            command=self._ctrl.show_plot_list,
        )

"""Provide a context menu class for plot lines.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.tree_window.branch_context_menu import BranchContextMenu
from nvlib.nv_locale import _


class PlotLineContextMenu(BranchContextMenu):

    def __init__(self, master, model, view, controller):
        super().__init__(master, model, view, controller)

        self.add_command(
            label=_('Add Plot line'),
            command=self._ctrl.add_new_plot_line,
        )
        self.add_command(
            label=_('Add Plot point'),
            command=self._ctrl.add_new_plot_point,
        )
        self.add_separator()
        self.add_command(
            label=_('Export manuscript filtered by plot line'),
            command=master._export_manuscript,
        )
        self.add_command(
            label=_('Export synopsis filtered by plot line'),
            command=master._export_synopsis,
        )
        self.add_separator()
        self.add_command(
            label=_('Change sections to Unused'),
            command=self._ctrl.exclude_plot_line,
        )
        self.add_command(
            label=_('Change sections to Normal'),
            command=self._ctrl.include_plot_line
        )
        self.add_separator()
        self.add_command(
            label=_('Delete'), accelerator=KEYS.DELETE[1],
            command=self._ctrl.delete_elements,
        )
        self.add_separator()
        self.add_command(
            label=_('Cut'),
            accelerator=KEYS.CUT[1],
            command=self._ctrl.cut_element,
        )
        self.add_command(
            label=_('Copy'),
            accelerator=KEYS.COPY[1],
            command=self._ctrl.copy_element,
        )
        self.add_command(
            label=_('Paste'),
            accelerator=KEYS.PASTE[1],
            command=self._ctrl.paste_element,
        )
        self._disableOnLock.extend([
            _('Add Plot line'),
            _('Add Plot point'),
            _('Delete'),
            _('Cut'),
            _('Paste'),
            _('Export manuscript filtered by plot line'),
            _('Export synopsis filtered by plot line'),
            _('Change sections to Unused'),
            _('Change sections to Normal'),
        ])


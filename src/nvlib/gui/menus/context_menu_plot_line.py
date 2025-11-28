"""Provide a context menu class for plot lines.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_context_menu import NvContextMenu
from nvlib.nv_locale import _


class ContextMenuPlotLine(NvContextMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)

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
        self._add_delete_command()
        self.add_separator()
        self._add_clipboard_commands()
        self.add_separator()

        label = _('Change sections to Unused')
        self.add_command(
            label=label,
            command=self._ctrl.exclude_plot_line,
        )
        self._disableOnLock.append(label)

        label = _('Change sections to Normal')
        self.add_command(
            label=label,
            command=self._ctrl.include_plot_line
        )
        self._disableOnLock.append(label)

        self.add_separator()

        label = _('Export manuscript filtered by plot line')
        self.add_command(
            label=label,
            command=self._ctrl.export_filtered_manuscript,
        )
        self._disableOnLock.append(label)

        label = _('Export synopsis filtered by plot line')
        self.add_command(
            label=label,
            command=self._ctrl.export_filtered_synopsis,
        )
        self._disableOnLock.append(label)

        self.add_separator()
        self._add_view_commands()


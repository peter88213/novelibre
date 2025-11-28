"""Provide a class for the "Export" menu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.nv_locale import _


class ExportMenu(NvMenu):

    def __init__(self, view, controller):
        super().__init__(view, controller)

        label = _('Manuscript for editing')
        self.add_command(
            label=label,
            command=self._ctrl.export_manuscript,
        )
        self._disableOnLock.append(label)

        label = _('Manuscript for third-party word processing')
        self.add_command(
            label=label,
            command=self._ctrl.export_proofing_manuscript,
        )
        self._disableOnLock.append(label)

        self.add_separator()

        label = _('Final manuscript document (export only)')
        self.add_command(
            label=label,
            command=self._ctrl.export_final_document,
        )

        label = _('Brief synopsis (export only)')
        self.add_command(
            label=label,
            command=self._ctrl.export_brief_synopsis,
        )

        label = _('Cross references (export only)')
        self.add_command(
            label=label,
            command=self._ctrl.export_cross_references,
        )

        self.add_separator()

        label = _('XML data files')
        self.add_command(
            label=label,
            command=self._ctrl.export_xml_data_files,
        )

        self.add_separator()

        label = _('Options')
        self.add_command(
            label=label,
            command=self._ctrl.open_export_options,
        )

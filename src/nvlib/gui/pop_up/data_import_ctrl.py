"""Provide a mixin class to control the data import dialog.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.sub_controller import SubController


class DataImportCtrl(SubController):

    def import_selected_elements(self, selectedIds):
        """Callback function for the data import pick list."""
        self._ctrl.dataImporter.add_elements(selectedIds)

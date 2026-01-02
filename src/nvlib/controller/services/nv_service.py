"""Provide a class with getters and factory methods for data model objects.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from nvlib.configuration.configuration import Configuration
from nvlib.controller.services.novx_service import NovxService
from nvlib.gui.tooltip import Hovertip
from nvlib.model.data.moon import Moon
from nvlib.model.odt.odt_w_export import OdtWExport


class NvService(NovxService):
    """Getters and factory methods for nvlib model objects."""

    def final_document_class(self):
        return OdtWExport

    def get_moon_phase_str(self, isoDate):
        return Moon.get_phase_string(isoDate)

    def new_configuration(self, **kwargs):
        return Configuration(**kwargs)

    def new_hovertip(self, anchor_widget, text):
        return Hovertip(anchor_widget, text)

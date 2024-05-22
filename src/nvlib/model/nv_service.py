"""Provide a class with getters and factory methods for novxlib objects.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from novxlib.config.configuration import Configuration
from novxlib.novx_service import NovxService


class NvService(NovxService):
    """Getters and factory methods for novxlib objects."""

    def make_configuration(self, **kwargs):
        return Configuration(**kwargs)


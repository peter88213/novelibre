"""Provide an abstract command base class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC
from abc import abstractmethod


class Command(ABC):

    @abstractmethod
    def execute(self):
        pass

    def undo(self):
        pass

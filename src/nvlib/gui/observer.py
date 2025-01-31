"""Provide an abstract Observer base class according to the Observer design pattern.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def refresh(self):
        pass

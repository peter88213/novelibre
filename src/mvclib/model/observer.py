"""Provide an abstract Observer base class according to the Observer design pattern.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mvclib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from abc import ABC
from abc import abstractmethod


class Observer(ABC):

    @abstractmethod
    def refresh(self):
        pass

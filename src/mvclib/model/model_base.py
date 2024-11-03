"""Provide a model base class for a MVC framework.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import abstractmethod

from mvclib.model.observable import Observable


class ModelBase(Observable):

    @abstractmethod
    def __init__(self):
        super().__init__()


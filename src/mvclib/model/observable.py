"""Provide an abstract Observable base class according to the Observer design pattern.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC
from abc import abstractmethod


class Observable(ABC):

    @abstractmethod
    def __init__(self):
        self._observers = []
        # list of Observer instance references
        self._isModified = False
        # internal modification flag

    @property
    def isModified(self):
        # Boolean -- True if there are unsaved changes.
        return self._isModified

    @isModified.setter
    def isModified(self, setFlag):
        self._isModified = setFlag
        self.notify_observers()

    def on_element_change(self):
        """Callback function that reports changes."""
        self.isModified = True

    def notify_observers(self):
        for client in self._observers:
            client.refresh()

    def add_observer(self, client):
        """Add an Observer instance to the list."""
        if not client in self._observers:
            self._observers.append(client)

    def delete_observer(self, client):
        """Remove an Observer instance from the list."""
        if client in self._observers:
            self._observers.remove(client)


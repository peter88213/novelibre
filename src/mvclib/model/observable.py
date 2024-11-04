"""Provide an abstract Observable base class according to the Observer design pattern.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC
from abc import abstractmethod


class Observable(ABC):

    @abstractmethod
    def __init__(self):
        self._clients = []
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
        if setFlag:
            self.refresh_clients()

    def on_element_change(self):
        """Callback function that reports changes."""
        self.isModified = True

    def refresh_clients(self):
        for client in self._clients:
            client.refresh()

    def register_client(self, client):
        """Add an Observer instance to the list."""
        if not client in self._clients:
            self._clients.append(client)

    def unregister_client(self, client):
        """Remove an Observer instance from the list."""
        if client in self._clients:
            self._clients.remove(client)


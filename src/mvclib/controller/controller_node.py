"""Provide an abstract controller node class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController


class ControllerNode(SubController):
    """A node in the view composite structure tree.
    
    Subordinate leaves can be registered and unregistered.
    
    Passes down the following commands to the leaves:
        - refresh
        - lock/unlock
        - emable/disable menu    
    """

    def __init__(self):
        self._clients = []

    def disable_menu(self):
        """Disable UI widgets, e.g. when no project is open."""
        for client in self._clients:
            client.disable_menu()

    def enable_menu(self):
        """Enable UI widgets, e.g. when a project is opened."""
        for client in self._clients:
            client.enable_menu()

    def lock(self):
        """Inhibit changes on the model."""
        for client in self._clients:
            client.lock()

    def on_close(self):
        """Actions to be performed when a project is closed."""
        for client in self._clients:
            client.on_close()

    def on_quit(self):
        """Actions to be performed when novelibre is closed."""
        for client in self._clients:
            client.on_quit()

    def register_client(self, client):
        """Add a sub controller instance to the list."""
        if not client in self._clients:
            self._clients.append(client)

    def unlock(self):
        """Enable changes on the model."""
        for client in self._clients:
            client.unlock()

    def unregister_client(self, client):
        """Remove an Observer instance from the list."""
        if client in self._clients:
            self._clients.remove(client)

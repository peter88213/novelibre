"""Provide a controller base class for a MVC framework.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from abc import ABC, abstractmethod


class ControllerBase(ABC):

    @abstractmethod
    def __init__(self, title):
        self._internalLockFlag = False

        #--- Example code:
        # self._mdl = MyModel()
        # self._mdl.add_observer(self)
        # self._ui = MyView(self._mdl, self, title)
        # self.plugins = PluginCollection(self._mdl, self._ui, self)

    @property
    def isLocked(self):
        # Boolean -- True if the project is locked.
        return self._internalLockFlag

    def disable_menu(self):
        """Disable UI widgets when no project is open."""
        self._ui.disable_menu()
        self.plugins.disable_menu()

    def enable_menu(self):
        """Enable UI widgets when a project is open."""
        self._ui.enable_menu()
        self.plugins.enable_menu()

    def get_view(self):
        """Return a reference to the application's main view object."""
        return self._ui

    def lock(self, event=None):
        """Lock the project.
        
        Return True on success, otherwise return False.
        """
        self._internalLockFlag = True
        self._ui.lock()
        self.plugins.lock()
        return True

    def on_quit(self):
        """To be executed before exiting the program."""
        self.plugins.on_quit()
        self._ui.on_quit()

    def refresh(self):
        """Callback function that responds to changes in the model."""
        pass

    def unlock(self, event=None):
        """Unlock the project."""
        self._internalLockFlag = False
        self._ui.unlock()
        self.plugins.unlock()

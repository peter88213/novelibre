"""Provide a controller base class for a MVC framework.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from abc import abstractmethod
from mvclib.controller.controller_node import ControllerNode


class ControllerBase(ControllerNode):

    @abstractmethod
    def __init__(self, title):
        super().__init__()
        self._internalLockFlag = False

        #--- Example code:
        # self._mdl = MyModel()
        # self._mdl.add_observer(self)
        # self._ui = MyView(self._mdl, self, title)
        # self.register_client(self._ui)
        # self.plugins = PluginCollection(self._mdl, self._ui, self)

    @property
    def isLocked(self):
        # Boolean -- True if the project is locked.
        return self._internalLockFlag

    def get_view(self):
        """Return a reference to the application's main view object."""
        return self._ui

    def lock(self, event=None):
        """Lock the project.
        
        Return True on success, otherwise return False.
        Extends the superclass method.
        """
        self._internalLockFlag = True
        super().lock()
        return True

    def unlock(self, event=None):
        """Unlock the project.
        
        Extends the superclass method.
        """
        self._internalLockFlag = False
        super().unlock()

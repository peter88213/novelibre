"""Provide a sub-controller base class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import abstractmethod


class SubController:
    """A leaf in the view composite structure tree."""

    @abstractmethod
    def __init__(self, model=None, view=None, controller=None):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

    def disable_menu(self):
        """Disable UI widgets, e.g. when no project is open."""
        pass

    def enable_menu(self):
        """Enable UI widgets, e.g. when a project is opened."""
        pass

    def lock(self):
        """Inhibit changes on the model."""
        pass

    def on_close(self):
        """Actions to be performed when a project is closed."""
        pass

    def on_quit(self):
        """Actions to be performed when novelibre is closed."""
        pass

    def unlock(self):
        """Enable changes on the model."""
        pass


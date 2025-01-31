"""Provide a sub-controller mixin base class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class SubController:
    """A mixin providing controller methods for views."""

    def initialize_controller(self, model, view, controller):
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


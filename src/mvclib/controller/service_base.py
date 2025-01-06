"""Provide a base class for service classes.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class ServiceBase:

    def __init__(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

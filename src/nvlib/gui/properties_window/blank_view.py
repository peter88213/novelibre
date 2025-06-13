"""Provide a base class for viewing novelibre project element properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.controller.sub_controller import SubController


class BlankView(ttk.Frame, SubController):
    """Class for viewing nothing.
    
    Base class for the element properties views.
    """

    def __init__(self, parent, model, view, controller, **kw):
        """Initialize the view once before element data is available.
        
        Positional arguments:
            parent -- Parent widget to display this widget.
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        """
        super().__init__(parent, **kw)
        self._parent = parent
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self.element = None

    def apply_changes(self, event=None):
        pass

    def configure_display(self):
        pass

    def focus_title(self):
        pass

    def hide(self):
        """Hide the view."""
        self.element = None
        self.pack_forget()

    def set_data(self, elementId):
        pass

    def show(self):
        """Make the view visible."""
        self.pack(expand=True, fill='both')


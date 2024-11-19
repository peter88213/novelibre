""" Provide a class for the properties view window.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.controller.properties_window.properties_viewer_ctrl import PropertiesViewerCtrl


class PropertiesViewer(ttk.Frame, PropertiesViewerCtrl):
    """A window viewing the selected element's properties."""

    def __init__(self, parent, model, view, controller, **kw):
        super().__init__(parent, **kw)
        self.initialize_controller(model, view, controller)


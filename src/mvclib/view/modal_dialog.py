"""Provide an abstract base class for modal dialogs.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mvclib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from abc import abstractmethod
import tkinter as tk


class ModalDialog(tk.Toplevel):
    OFFSET = 300

    @abstractmethod
    def __init__(self, model, view, controller, **kw):
        tk.Toplevel.__init__(self, **kw)
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        __, x, y = self._ui.root.geometry().split('+')
        windowGeometry = f'+{int(x)+self.OFFSET}+{int(y)+self.OFFSET}'
        self.geometry(windowGeometry)
        self.grab_set()
        self.focus()


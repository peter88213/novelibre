"""Provide an abstract base class for modal dialogs.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import abstractmethod

import tkinter as tk


class ModalDialog(tk.Toplevel):
    OFFSET = 300

    @abstractmethod
    def __init__(self, ui, **kw):
        tk.Toplevel.__init__(self, **kw)
        __, x, y = ui.root.geometry().split('+')
        windowGeometry = f'+{int(x)+self.OFFSET}+{int(y)+self.OFFSET}'
        self.geometry(windowGeometry)
        self.grab_set()
        self.focus()


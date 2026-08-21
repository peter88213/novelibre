"""Provide an abstract base class for modal dialogs.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import abstractmethod
import platform

import tkinter as tk


class ModalDialog(tk.Toplevel):
    OFFSET = 300
    RESIZABLE = False

    @abstractmethod
    def __init__(self, ui, **kw):
        tk.Toplevel.__init__(self, **kw)
        __, x, y = ui.root.geometry().split('+')
        windowGeometry = f'+{int(x)+self.OFFSET}+{int(y)+self.OFFSET}'
        self.geometry(windowGeometry)
        if not self.RESIZABLE:
            self.withdraw()
            # this avoids flickering caused by the following commands

            self.wm_resizable(False, False)
            if platform.system() == 'Windows':
                self.attributes('-toolwindow', True)
            self.update()
            self.deiconify()
        self.wait_visibility()
        self.grab_set()
        self.focus()
        self.wm_attributes('-topmost', True)


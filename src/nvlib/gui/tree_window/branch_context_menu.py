"""Provide a context menu class for a tree view branch.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.sub_controller import SubController
from nvlib.gui.widgets.context_menu import ContextMenu


class BranchContextMenu(ContextMenu, SubController):

    def __init__(self, master, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._disableOnLock = []
        super().__init__(master, tearoff=0)

    def lock(self):
        for label in self._disableOnLock:
            self.entryconfig(label, state='disabled')

    def unlock(self):
        for label in self._disableOnLock:
            self.entryconfig(label, state='normal')

    def open(self, event):
        try:
            self.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.grab_release()

"""Provide a base class for novelibre menus.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.sub_controller import SubController
import tkinter as tk


class NvMenu(tk.Menu, SubController):

    def __init__(self):
        super().__init__(tearoff=0)
        self.disableOnLock = []
        self.disableOnClose = []

    def disable_menu(self):
        for label in self.disableOnClose:
            self.entryconfig(label, state='disabled')

    def enable_menu(self):
        for label in self.disableOnClose:
            self.entryconfig(label, state='normal')

    def lock(self):
        for label in self.disableOnLock:
            self.entryconfig(label, state='disabled')

    def unlock(self):
        for label in self.disableOnLock:
            self.entryconfig(label, state='normal')


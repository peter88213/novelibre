"""Provide a menu class for chapter/section type selection.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.nv_locale import _
import tkinter as tk


class TypeMenu(tk.Menu):

    def __init__(self, tree, controller):
        super().__init__(tree, tearoff=0)
        self.add_command(
            label=_('Normal'),
            command=controller.set_type_normal,
        )
        self.add_command(
            label=_('Unused'),
            command=controller.set_type_unused,
        )

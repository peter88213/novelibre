"""Provide a menu class for chapter/stage level selection.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.nv_locale import _
import tkinter as tk


class SelectionMenuLevel(tk.Menu):

    def __init__(self, controller):
        super().__init__(tearoff=0)

        self.add_command(
            label=_('1st Level'),
            command=controller.set_level_1,
        )

        self.add_command(
            label=_('2nd Level'),
            command=controller.set_level_2,
        )

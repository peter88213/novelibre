"""Provide a menu class for character status selection.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.nv_locale import _
import tkinter as tk


class SelectionMenuCharacterStatus(tk.Menu):

    def __init__(self, master, controller):
        super().__init__(master, tearoff=0)
        self.add_command(
            label=_('Major Character'),
            command=controller.set_chr_status_major,
        )
        self.add_command(
            label=_('Minor Character'),
            command=controller.set_chr_status_minor,
        )

"""Provide a class for the "File > New" submenu. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.nv_locale import _
import tkinter as tk


class FileNewSubmenu(tk.Menu):

    def __init__(self, master, controller):
        super().__init__(master, tearoff=0)
        self.add_command(
            label=_('Empty project'),
            command=controller.create_project,
        )
        self.add_command(
            label=_('Create from ODT...'),
            command=controller.import_odf,
        )

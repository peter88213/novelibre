"""Provide a menu class for section status selection.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.nv_locale import _
import tkinter as tk


class ScStatusMenu(tk.Menu):

    def __init__(self, tree, controller):
        super().__init__(tree, tearoff=0)
        self.add_command(
            label=_('Outline'),
            command=controller.set_scn_status_outline,
        )
        self.add_command(
            label=_('Draft'),
            command=controller.set_scn_status_draft,
        )
        self.add_command(
            label=_('1st Edit'),
            command=controller.set_scn_status_1st_edit,
        )
        self.add_command(
            label=_('2nd Edit'),
            command=controller.set_scn_status_2nd_edit,
        )
        self.add_command(
            label=_('Done'),
            command=controller.set_scn_status_done,
        )


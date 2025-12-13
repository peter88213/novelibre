"""Provide a class for character selection.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.widgets.label_combo import LabelCombo
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.novx_globals import CR_ROOT
from nvlib.nv_locale import _


class CharacterSelectionDialog(ModalDialog):

    def __init__(self, model, view, callback, label, **kw):
        super().__init__(view, **kw)
        self._cb = callback
        self._crIdList = [None]
        self.title(_('Characters'))
        preset = ''
        charNames = [preset]
        for crId in model.novel.tree.get_children(CR_ROOT):
            charNames.append(model.novel.characters[crId].title)
            self._crIdList.append(crId)

        characterVar = MyStringVar(value=preset)
        self._characterCombobox = LabelCombo(
            self,
            text=label,
            textvariable=characterVar,
            values=charNames,
        )
        self._characterCombobox.pack(
            anchor='w',
            padx=10,
            pady=10,
        )
        self._characterCombobox.combo.bind(
            '<<ComboboxSelected>>', self.select_string)

        ttk.Separator(self, orient='horizontal').pack(fill='x')

        # "Close" button.
        ttk.Button(
            self,
            text=_('Close'),
            command=self.destroy,
        ).pack(padx=5, pady=5, side='right')

    def select_string(self, event):
        # callback function returning the selected character's ID.
        option = self._characterCombobox.current()
        self.destroy()
        if option >= 0:
            self._cb(self._crIdList[option])

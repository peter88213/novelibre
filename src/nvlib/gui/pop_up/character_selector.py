"""Provide a class for character selection.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.widgets.label_combo import LabelCombo
from nvlib.gui.widgets.modal_dialog import ModalDialog
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.novx_globals import CR_ROOT


class CharacterSelector(ModalDialog):

    def __init__(self, model, view, callback, label, **kw):
        super().__init__(view, **kw)
        self._cb = callback
        self._vpIdList = [None]
        preset = ''
        charNames = [preset]
        for crId in model.novel.tree.get_children(CR_ROOT):
            charNames.append(model.novel.characters[crId].title)
            self._vpIdList.append(crId)

        viewpointVar = MyStringVar(value=preset)
        self._characterCombobox = LabelCombo(
            self,
            text=label,
            textvariable=viewpointVar,
            values=charNames,
        )
        self._characterCombobox.pack(
            anchor='w', padx=5, pady=5)
        self._characterCombobox.combo.bind(
            '<<ComboboxSelected>>', self._apply_changes)

    def _apply_changes(self, event):
        # callback function returning the selected character's ID.
        option = self._characterCombobox.current()
        if option >= 0:
            crId = self._vpIdList[option]
            self._cb(crId)
        self.destroy()

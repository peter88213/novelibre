"""Provide a mixin class for controlling the character properties view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date

from nvlib.controller.properties_window.world_element_view_ctrl import WorldElementViewCtrl
from nvlib.novx_globals import _
from nvlib.nv_globals import prefs


class CharacterViewCtrl(WorldElementViewCtrl):

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        super().apply_changes()

        # 'Full name' entry.
        self.element.fullName = self._fullName.get()

        # 'Bio' frame.
        if self._bioEntry.hasChanged:
            self.element.bio = self._bioEntry.get_text()

        birthDateStr = self._birthDate.get()
        if not birthDateStr:
            self.element.birthDate = None
        elif birthDateStr != self.element.birthDate:
            try:
                date.fromisoformat(birthDateStr)
            except:
                self._birthDate.set(self.element.birthDate)
                self._ui.show_error(
                    f'{_("Wrong date")}: "{birthDateStr}"\n{_("Required")}: {_("YYYY-MM-DD")}',
                    title=_('Input rejected')
                    )
            else:
                self.element.birthDate = birthDateStr

        deathDateStr = self._deathDate.get()
        if not deathDateStr:
            self.element.deathDate = None
        elif deathDateStr != self.element.deathDate:
            try:
                date.fromisoformat(deathDateStr)
            except:
                self._deathDate.set(self.element.deathDate)
                self._ui.show_error(
                    f'{_("Wrong date")}: "{deathDateStr}"\n{_("Required")}: {_("YYYY-MM-DD")}',
                    title=_('Input rejected')
                    )
            else:
                self.element.deathDate = deathDateStr

        # 'Goals' entry.
        if self._goalsEntry.hasChanged:
            self.element.goals = self._goalsEntry.get_text()

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass constructor.
        """
        self.element = self._mdl.novel.characters[elementId]
        super().set_data(elementId)

        # 'Full name' entry.
        self._fullName.set(self.element.fullName)

        #--- 'Bio' entry
        if self._mdl.novel.customChrBio:
            self._bioFrame.buttonText = self._mdl.novel.customChrBio
        else:
            self._bioFrame.buttonText = _('Bio')
        if prefs['show_cr_bio']:
            self._bioFrame.show()
        else:
            self._bioFrame.hide()
        self._bioEntry.set_text(self.element.bio)

        #--- Birth date/death date.
        self._birthDate.set(self.element.birthDate)
        self._deathDate.set(self.element.deathDate)

        #--- 'Goals' entry.
        if self._mdl.novel.customChrGoals:
            self._goalsFrame.buttonText = self._mdl.novel.customChrGoals
        else:
            self._goalsFrame.buttonText = _('Goals')
        if prefs['show_cr_goals']:
            self._goalsFrame.show()
        else:
            self._goalsFrame.hide()
        self._goalsEntry.set_text(self.element.goals)


"""Provide a mixin class for controlling the character properties view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.properties_window.world_element_view_ctrl import WorldElementViewCtrl
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class CharacterViewCtrl(WorldElementViewCtrl):

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        super().apply_changes()

        # 'Full name' entry.
        self.element.fullName = self.fullNameVar.get()

        #--- Character status checkbox.
        self.element.isMajor = self.isMajorVar.get()

        # 'Bio' frame.
        if self.bioEntry.hasChanged:
            self.element.bio = self.bioEntry.get_text()

        birthDateStr = self.birthDateVar.get()
        if not birthDateStr:
            self.element.birthDate = None
        elif birthDateStr != self.element.birthDate:
            try:
                PyCalendar.verified_date(birthDateStr)
            except:
                self.birthDateVar.set(self.element.birthDate)
                self._ui.show_error(
                    message=_('Input rejected'),
                    detail=f'{_("Wrong date")}: "{birthDateStr}"\n{_("Required")}: {PyCalendar.DATE_FORMAT}'
                    )
            else:
                self.element.birthDate = birthDateStr

        deathDateStr = self.deathDateVar.get()
        if not deathDateStr:
            self.element.deathDate = None
        elif deathDateStr != self.element.deathDate:
            try:
                PyCalendar.verified_date(deathDateStr)
            except:
                self.deathDateVar.set(self.element.deathDate)
                self._ui.show_error(
                    message=_('Input rejected'),
                    detail=f'{_("Wrong date")}: "{deathDateStr}"\n{_("Required")}: {PyCalendar.DATE_FORMAT}'
                    )
            else:
                self.element.deathDate = deathDateStr

        # 'Goals' entry.
        if self.goalsEntry.hasChanged:
            self.element.goals = self.goalsEntry.get_text()

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.characters[elementId]
        super().set_data(elementId)

        # 'Full name' entry.
        self.fullNameVar.set(self.element.fullName)

        #--- Character status checkbox.
        self.isMajorVar.set(self.element.isMajor)

        #--- 'Bio' entry
        if self._mdl.novel.customChrBio:
            self.bioFrame.buttonText = self._mdl.novel.customChrBio
        else:
            self.bioFrame.buttonText = _('Bio')
        if prefs['show_cr_bio']:
            self.bioFrame.show()
        else:
            self.bioFrame.hide()
        self.bioEntry.set_text(self.element.bio)

        #--- Birth date/death date.
        self.birthDateVar.set(self.element.birthDate)
        self.deathDateVar.set(self.element.deathDate)

        #--- 'Goals' entry.
        if self._mdl.novel.customChrGoals:
            self.goalsFrame.buttonText = self._mdl.novel.customChrGoals
        else:
            self.goalsFrame.buttonText = _('Goals')
        if prefs['show_cr_goals']:
            self.goalsFrame.show()
        else:
            self.goalsFrame.hide()
        self.goalsEntry.set_text(self.element.goals)


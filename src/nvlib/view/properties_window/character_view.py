"""Provide a class for viewing and editing character properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from tkinter import ttk

from nvlib.nv_globals import prefs
from nvlib.view.properties_window.world_element_view import WorldElementView
from nvlib.widgets.folding_frame import FoldingFrame
from nvlib.widgets.label_entry import LabelEntry
from nvlib.widgets.my_string_var import MyStringVar
from nvlib.widgets.text_box import TextBox
from novxlib.novx_globals import _


class CharacterView(WorldElementView):
    """Class for viewing and editing character properties.

    Adds to the right pane:
    - A "Full name" entry.
    - A "Bio" folding frame.
    - A "Goals" folding frame.
    """
    _LBL_X = 15
    # Width of left-placed labels.

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- 'Full name' entry.
        self._fullName = MyStringVar()
        self._fullNameEntry = LabelEntry(self._fullNameFrame, text=_('Full name'), textvariable=self._fullName, lblWidth=self._LBL_X)
        self._fullNameEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._fullNameEntry)
        self._fullNameEntry.entry.bind('<Return>', self.apply_changes)

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- 'Bio' frame
        self._bioFrame = FoldingFrame(self._elementInfoWindow, '', self._toggle_bio_window)

        self._birthDate = MyStringVar()
        self._birthDateEntry = LabelEntry(self._bioFrame, text=_('Birth date'), textvariable=self._birthDate, lblWidth=self._LBL_X)
        self._birthDateEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._birthDateEntry)

        self._deathDate = MyStringVar()
        self._deathDateEntry = LabelEntry(self._bioFrame, text=_('Death date'), textvariable=self._deathDate, lblWidth=self._LBL_X)
        self._deathDateEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._deathDateEntry)

        self._bioEntry = TextBox(self._bioFrame,
            wrap='word',
            undo=True,
            autoseparators=True,
            maxundo=-1,
            height=10,
            width=10,
            padx=5,
            pady=5,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
            insertbackground=prefs['color_text_fg'],
            )
        self._bioEntry.pack(fill='x')
        inputWidgets.append(self._bioEntry)

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- 'Goals' entry.
        self._goalsFrame = FoldingFrame(self._elementInfoWindow, '', self._toggle_goals_window)
        self._goalsEntry = TextBox(self._goalsFrame,
            wrap='word',
            undo=True,
            autoseparators=True,
            maxundo=-1,
            height=10,
            width=10,
            padx=5,
            pady=5,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
            insertbackground=prefs['color_text_fg'],
            )
        self._goalsEntry.pack(fill='x')
        inputWidgets.append(self._goalsEntry)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self._inputWidgets.append(widget)

        self._prefsShowLinks = 'show_cr_links'

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        super().apply_changes()

        # 'Full name' entry.
        self._element.fullName = self._fullName.get()

        # 'Bio' frame.
        if self._bioEntry.hasChanged:
            self._element.bio = self._bioEntry.get_text()

        birthDateStr = self._birthDate.get()
        if not birthDateStr:
            self._element.birthDate = None
        elif birthDateStr != self._element.birthDate:
            try:
                date.fromisoformat(birthDateStr)
            except:
                self._birthDate.set(self._element.birthDate)
                self._ui.show_error(f'{_("Wrong date")}: "{birthDateStr}"', title=_('Input rejected'))
            else:
                self._element.birthDate = birthDateStr

        deathDateStr = self._deathDate.get()
        if not deathDateStr:
            self._element.deathDate = None
        elif deathDateStr != self._element.deathDate:
            try:
                date.fromisoformat(deathDateStr)
            except:
                self._deathDate.set(self._element.deathDate)
                self._ui.show_error(f'{_("Wrong date")}: "{deathDateStr}"', title=_('Input rejected'))
            else:
                self._element.deathDate = deathDateStr

        # 'Goals' entry.
        if self._goalsEntry.hasChanged:
            self._element.goals = self._goalsEntry.get_text()

    def set_data(self, elementId):
        """Update the view with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.characters[elementId]
        super().set_data(elementId)

        # 'Full name' entry.
        self._fullName.set(self._element.fullName)

        #--- 'Bio' entry
        if self._mdl.novel.customChrBio:
            self._bioFrame.buttonText = self._mdl.novel.customChrBio
        else:
            self._bioFrame.buttonText = _('Bio')
        if prefs['show_cr_bio']:
            self._bioFrame.show()
        else:
            self._bioFrame.hide()
        self._bioEntry.set_text(self._element.bio)

        #--- Birth date/death date.
        self._birthDate.set(self._element.birthDate)
        self._deathDate.set(self._element.deathDate)

        #--- 'Goals' entry.
        if self._mdl.novel.customChrGoals:
            self._goalsFrame.buttonText = self._mdl.novel.customChrGoals
        else:
            self._goalsFrame.buttonText = _('Goals')
        if prefs['show_cr_goals']:
            self._goalsFrame.show()
        else:
            self._goalsFrame.hide()
        self._goalsEntry.set_text(self._element.goals)

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _toggle_bio_window(self, event=None):
        """Hide/show the 'Bio' textbox."""
        if prefs['show_cr_bio']:
            self._bioFrame.hide()
            prefs['show_cr_bio'] = False
        else:
            self._bioFrame.show()
            prefs['show_cr_bio'] = True

    def _toggle_goals_window(self, event=None):
        """Hide/show the 'Goals' textbox."""
        if prefs['show_cr_goals']:
            self._goalsFrame.hide()
            prefs['show_cr_goals'] = False
        else:
            self._goalsFrame.show()
            prefs['show_cr_goals'] = True


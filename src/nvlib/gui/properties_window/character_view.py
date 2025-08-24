"""Provide a class for viewing and editing character properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.world_element_view import WorldElementView
from nvlib.gui.widgets.folding_frame import FoldingFrame
from nvlib.gui.widgets.label_entry import LabelEntry
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.gui.widgets.text_box import TextBox
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.novx_globals import list_to_string
from nvlib.nv_globals import get_locale_date_str
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class CharacterView(WorldElementView):
    """Class for viewing and editing character properties.

    Adds to the right pane:
    - A "Full name" entry.
    - A "Bio" folding frame.
    - A "Character extra field" folding frame.
    """
    _HELP_PAGE = 'character_view.html'
    _LABEL_WIDTH = 15
    # Width of left-placed labels.

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- 'Full name' entry.
        self._fullNameVar = MyStringVar()
        self._fullNameEntry = LabelEntry(
            self._fullNameFrame,
            text=_('Full name'),
            textvariable=self._fullNameVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._fullNameEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._fullNameEntry)

        #--- Character status checkbox.
        self._isMajorVar = tk.BooleanVar()
        self._isMajorCheckbox = ttk.Checkbutton(
            self._elementInfoWindow,
            text=_('Major Character'),
            variable=self._isMajorVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._isMajorCheckbox.pack(anchor='w')
        inputWidgets.append(self._isMajorCheckbox)

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal'
        ).pack(fill='x')

        #--- 'Bio' frame
        self._bioFrame = FoldingFrame(
            self._elementInfoWindow,
            '',
            self._toggle_bio_window,
        )

        # Bio preview.
        self._bioPreviewVar = MyStringVar()
        bioPreview = ttk.Label(
            self._bioFrame.titleBar,
            textvariable=self._bioPreviewVar,
        )
        bioPreview.pack(side='left', padx=2)
        bioPreview.bind('<Button-1>', self._toggle_bio_window)

        self._birthDateVar = MyStringVar()
        self._birthDateEntry = LabelEntry(
            self._bioFrame,
            text=_('Birth date'),
            textvariable=self._birthDateVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._birthDateEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._birthDateEntry)

        self._deathDateVar = MyStringVar()
        self._deathDateEntry = LabelEntry(
            self._bioFrame,
            text=_('Death date'),
            textvariable=self._deathDateVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._deathDateEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._deathDateEntry)

        self._bioBox = TextBox(
            self._bioFrame,
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
        self._bioBox.pack(fill='x')
        inputWidgets.append(self._bioBox)

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal'
        ).pack(fill='x')

        #--- 'Character extra field' entry.
        self._chrExtraFieldFrame = FoldingFrame(
            self._elementInfoWindow,
            '',
            self._toggle_chrExtraField_window,
        )

        # Character extra field preview.
        self._chrExtraFieldPreviewVar = MyStringVar()
        chrExtraFieldPreview = ttk.Label(
            self._chrExtraFieldFrame.titleBar,
            textvariable=self._chrExtraFieldPreviewVar,
        )
        chrExtraFieldPreview.pack(side='left', padx=2)
        chrExtraFieldPreview.bind('<Button-1>', self._toggle_chrExtraField_window)

        self._chrExtraFieldBox = TextBox(self._chrExtraFieldFrame,
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
        self._chrExtraFieldBox.pack(fill='x')
        inputWidgets.append(self._chrExtraFieldBox)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

        self._prefsShowLinks = 'show_cr_links'

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        super().apply_changes()

        #--- "Full name" entry.
        self.element.fullName = self._fullNameVar.get()

        #--- Character status checkbox.
        self.element.isMajor = self._isMajorVar.get()

        #--- "Bio' frame.
        if self._bioBox.hasChanged:
            self.element.bio = self._bioBox.get_text()

        birthDateStr = self._birthDateVar.get()
        if not birthDateStr:
            self.element.birthDate = None
        elif birthDateStr != self.element.birthDate:
            try:
                PyCalendar.verified_date(birthDateStr)
            except:
                self._birthDateVar.set(self.element.birthDate)
                self._ui.show_error(
                    message=_('Input rejected'),
                    detail=(
                        f'{_("Wrong date")}: "{birthDateStr}"\n'
                        f'{_("Required")}: {PyCalendar.DATE_FORMAT}'
                    )
                )
            else:
                self.element.birthDate = birthDateStr

        deathDateStr = self._deathDateVar.get()
        if not deathDateStr:
            self.element.deathDate = None
        elif deathDateStr != self.element.deathDate:
            try:
                PyCalendar.verified_date(deathDateStr)
            except:
                self._deathDateVar.set(self.element.deathDate)
                self._ui.show_error(
                    message=_('Input rejected'),
                    detail=(
                        f'{_("Wrong date")}: "{deathDateStr}"\n'
                        f'{_("Required")}: {PyCalendar.DATE_FORMAT}'
                    )
                )
            else:
                self.element.deathDate = deathDateStr

        #--- "Character extra field" entry.
        if self._chrExtraFieldBox.hasChanged:
            self.element.goals = self._chrExtraFieldBox.get_text()

    def configure_display(self):
        """Expand or collapse the property frames."""
        super().configure_display()

        #--- Bio frame.
        self._bioFrame.buttonText = _('Bio')
        if prefs['show_cr_bio']:
            self._bioFrame.show()
            self._bioPreviewVar.set('')
        else:
            self._bioFrame.hide()
            bio = []
            if self.element.birthDate:
                bio.append(f'* {get_locale_date_str(self.element.birthDate)}')
            if self.element.deathDate:
                bio.append(f'† {get_locale_date_str(self.element.deathDate)}')
            if self.element.bio:
                bio.append(self._CHECK)
            self._bioPreviewVar.set(
                list_to_string(bio, divider=' '))

        #--- Character extra field frame.
        if self._mdl.novel.chrExtraField:
            self._chrExtraFieldFrame.buttonText = self._mdl.novel.chrExtraField
        else:
            self._chrExtraFieldFrame.buttonText = _('Extra field')
        if prefs['show_chr_extra_field']:
            self._chrExtraFieldFrame.show()
            self._chrExtraFieldPreviewVar.set('')
        else:
            self._chrExtraFieldFrame.hide()
            if self.element.goals:
                self._chrExtraFieldPreviewVar.set(self._CHECK)
            else:
                self._chrExtraFieldPreviewVar.set('')

    def set_data(self, elementId):
        """Update the view with element data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.characters[elementId]
        super().set_data(elementId)

        #--- "Full name" entry.
        self._fullNameVar.set(self.element.fullName)

        #--- Character status checkbox.
        self._isMajorVar.set(self.element.isMajor)

        #--- Bio frame.

        # "Bio" entry.
        self._bioBox.set_text(self.element.bio)

        # Birth date/death date.
        self._birthDateVar.set(self.element.birthDate)
        self._deathDateVar.set(self.element.deathDate)

        #--- "Character extra field" entry.
        self._chrExtraFieldBox.set_text(self.element.goals)

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _toggle_bio_window(self, event=None):
        # Hide/show the 'Bio' textbox.
        if prefs['show_cr_bio']:
            self._bioFrame.hide()
            prefs['show_cr_bio'] = False
        else:
            self._bioFrame.show()
            prefs['show_cr_bio'] = True
        self._toggle_folding_frame()

    def _toggle_chrExtraField_window(self, event=None):
        # Hide/show the 'Character extra field' textbox.
        if prefs['show_chr_extra_field']:
            self._chrExtraFieldFrame.hide()
            prefs['show_chr_extra_field'] = False
        else:
            self._chrExtraFieldFrame.show()
            prefs['show_chr_extra_field'] = True
        self._toggle_folding_frame()


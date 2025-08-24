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
    - A "Character extra field 1" folding frame.
    - A "Character extra field 2" folding frame.
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

        #--- Birth and death date entries.
        self._birthDateVar = MyStringVar()
        self._birthDateEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('Birth date'),
            textvariable=self._birthDateVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._birthDateEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._birthDateEntry)

        self._deathDateVar = MyStringVar()
        self._deathDateEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('Death date'),
            textvariable=self._deathDateVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._deathDateEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._deathDateEntry)

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal'
        ).pack(fill='x')

        #--- Character field 1 frame.
        self._crField1Frame = FoldingFrame(
            self._elementInfoWindow,
            '',
            self._toggle_crField1_window,
        )

        self._crField1PreviewVar = MyStringVar()
        crField1Preview = ttk.Label(
            self._crField1Frame.titleBar,
            textvariable=self._crField1PreviewVar,
        )
        crField1Preview.pack(side='left', padx=2)
        crField1Preview.bind('<Button-1>', self._toggle_crField1_window)

        self._crField1Box = TextBox(
            self._crField1Frame,
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
        self._crField1Box.pack(fill='x')
        inputWidgets.append(self._crField1Box)

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal'
        ).pack(fill='x')

        #--- Character field 2 frame.
        self._crField2Frame = FoldingFrame(
            self._elementInfoWindow,
            '',
            self._toggle_crField2_window,
        )

        self._crField2PreviewVar = MyStringVar()
        crField2Preview = ttk.Label(
            self._crField2Frame.titleBar,
            textvariable=self._crField2PreviewVar,
        )
        crField2Preview.pack(side='left', padx=2)
        crField2Preview.bind('<Button-1>', self._toggle_crField2_window)

        self._crField2Box = TextBox(self._crField2Frame,
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
        self._crField2Box.pack(fill='x')
        inputWidgets.append(self._crField2Box)

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal'
        ).pack(fill='x')

        #--- Character field 3 frame.
        self._crField3Frame = FoldingFrame(
            self._elementInfoWindow,
            '',
            self._toggle_crField3_window,
        )

        self._crField3PreviewVar = MyStringVar()
        crField3Preview = ttk.Label(
            self._crField3Frame.titleBar,
            textvariable=self._crField3PreviewVar,
        )
        crField3Preview.pack(side='left', padx=2)
        crField3Preview.bind('<Button-1>', self._toggle_crField3_window)

        self._crField3Box = TextBox(self._crField3Frame,
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
        self._crField3Box.pack(fill='x')
        inputWidgets.append(self._crField3Box)

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

        #--- Birth and death date entries.
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

        #--- Character field 1 entry.
        if self._crField1Box.hasChanged:
            self.element.bio = self._crField1Box.get_text()

        #--- Character field 2 entry.
        if self._crField2Box.hasChanged:
            self.element.goals = self._crField2Box.get_text()

        #--- Character field 3 entry.
        if self._crField3Box.hasChanged:
            self.element.field2 = self._crField3Box.get_text()

    def configure_display(self):
        """Expand or collapse the property frames."""
        super().configure_display()

        #--- Character field 1 frame.
        if self._mdl.novel.crField1:
            self._crField1Frame.buttonText = self._mdl.novel.crField1
        else:
            self._crField1Frame.buttonText = f"{_('Field')} 1"
        if prefs['show_cr_field_1']:
            self._crField1Frame.show()
            self._crField1PreviewVar.set('')
        else:
            self._crField1Frame.hide()
            if self.element.bio:
                self._crField1PreviewVar.set(self._CHECK)
            else:
                self._crField1PreviewVar.set('')

        #--- Character field 2 frame.
        if self._mdl.novel.crField2:
            self._crField2Frame.buttonText = self._mdl.novel.crField2
        else:
            self._crField2Frame.buttonText = f"{_('Field')} 2"
        if prefs['show_cr_field_2']:
            self._crField2Frame.show()
            self._crField2PreviewVar.set('')
        else:
            self._crField2Frame.hide()
            if self.element.goals:
                self._crField2PreviewVar.set(self._CHECK)
            else:
                self._crField2PreviewVar.set('')

        #--- Character field 3 frame.
        if self._mdl.novel.crField3:
            self._crField3Frame.buttonText = self._mdl.novel.crField3
        else:
            self._crField3Frame.buttonText = f"{_('Extra field')} 2"
        if prefs['show_cr_field_3']:
            self._crField3Frame.show()
            self._crField3PreviewVar.set('')
        else:
            self._crField3Frame.hide()
            if self.element.field2:
                self._crField3PreviewVar.set(self._CHECK)
            else:
                self._crField3PreviewVar.set('')

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

        #--- Birth and death date entries.
        self._birthDateVar.set(self.element.birthDate)
        self._deathDateVar.set(self.element.deathDate)

        #--- Character field 1 entry.
        self._crField1Box.set_text(self.element.bio)

        #--- Character field 2 entry.
        self._crField2Box.set_text(self.element.goals)

        #--- Character field 3 entry.
        self._crField3Box.set_text(self.element.field2)

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _toggle_crField1_window(self, event=None):
        # Hide/show the 'Character field 1' textbox.
        if prefs['show_cr_field_1']:
            self._crField1Frame.hide()
            prefs['show_cr_field_1'] = False
        else:
            self._crField1Frame.show()
            prefs['show_cr_field_1'] = True
        self._toggle_folding_frame()

    def _toggle_crField2_window(self, event=None):
        # Hide/show the 'Character field 2' textbox.
        if prefs['show_cr_field_2']:
            self._crField2Frame.hide()
            prefs['show_cr_field_2'] = False
        else:
            self._crField2Frame.show()
            prefs['show_cr_field_2'] = True
        self._toggle_folding_frame()

    def _toggle_crField3_window(self, event=None):
        # Hide/show the 'Character field 3' textbox.
        if prefs['show_cr_field_3']:
            self._crField3Frame.hide()
            prefs['show_cr_field_3'] = False
        else:
            self._crField3Frame.show()
            prefs['show_cr_field_3'] = True
        self._toggle_folding_frame()


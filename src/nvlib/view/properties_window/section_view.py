"""Provide a tkinter based class for viewing and editing all section properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from tkinter import ttk

from mvclib.widgets.folding_frame import FoldingFrame
from mvclib.widgets.label_combo import LabelCombo
from mvclib.widgets.label_entry import LabelEntry
from mvclib.widgets.my_string_var import MyStringVar
from mvclib.widgets.text_box import TextBox
from nvlib.model.data.date_time_tools import get_age
from nvlib.model.data.date_time_tools import get_specific_date
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import WEEKDAYS
from nvlib.novx_globals import _
from nvlib.novx_globals import list_to_string
from nvlib.novx_globals import string_to_list
from nvlib.nv_globals import datestr
from nvlib.nv_globals import get_section_date_str
from nvlib.nv_globals import prefs
from nvlib.view.properties_window.basic_view import BasicView
from nvlib.view.widgets.collection_box import CollectionBox
import tkinter as tk


class SectionView(BasicView):
    """Class for viewing and editing section properties.
       
    Adds to the right pane:
    - A "Tags" entry.
    - A folding frame for relationships (characters/locations/items)
    - A folding frame for date/time.
    - A combobox for viewpoint character selection.
    - A checkbox "unused".
    - A checkbox "append to previous".
    - A "Plot" folding frame for plotLines and plot point associations.
    - A "Scene" folding frame for Goal/Reaction/Outcome.
    """
    _HEIGHT_LIMIT = 10
    _DATE_TIME_LBL_X = 15
    # Width of left-placed labels.

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- 'Tags' entry.
        self._tags = MyStringVar()
        self._tagsEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('Tags'),
            textvariable=self._tags,
            command=self.apply_changes,
            lblWidth=self._LBL_X
            )
        self._tagsEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._tagsEntry)

        #--- Frame for section specific properties.
        self._sectionExtraFrame = ttk.Frame(self._elementInfoWindow)
        self._sectionExtraFrame.pack(anchor='w', fill='x')

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- Frame for 'Relationships'.
        # updating the character list before the viewpoints
        self._relationFrame = FoldingFrame(self._elementInfoWindow, _('Relationships'), self._toggle_relation_frame)

        # 'Characters' listbox.
        self._crTitles = ''
        crHeading = ttk.Frame(self._relationFrame)
        self._characterLabel = ttk.Label(crHeading, text=_('Characters'))
        self._characterLabel.pack(anchor='w', side='left')
        ttk.Button(crHeading, text=_('Show ages'), command=self._show_ages).pack(anchor='e')
        crHeading.pack(fill='x')
        self._characterCollection = CollectionBox(
            self._relationFrame,
            cmdAdd=self._pick_character,
            cmdRemove=self._remove_character,
            cmdOpen=self._go_to_character,
            cmdActivate=self._activate_character_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self._characterCollection.pack(fill='x')
        inputWidgets.extend(self._characterCollection.inputWidgets)

        # 'Locations' listbox.
        self._lcTitles = ''
        self._locationLabel = ttk.Label(self._relationFrame, text=_('Locations'))
        self._locationLabel.pack(anchor='w')
        self._locationCollection = CollectionBox(
            self._relationFrame,
            cmdAdd=self._pick_location,
            cmdRemove=self._remove_location,
            cmdOpen=self._go_to_location,
            cmdActivate=self._activate_location_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self._locationCollection.pack(fill='x')
        inputWidgets.extend(self._locationCollection.inputWidgets)

        # 'Items' listbox.
        self._itTitles = ''
        self._itemLabel = ttk.Label(self._relationFrame, text=_('Items'))
        self._itemLabel.pack(anchor='w')
        self._itemCollection = CollectionBox(
            self._relationFrame,
            cmdAdd=self._pick_item,
            cmdRemove=self._remove_item,
            cmdOpen=self._go_to_item,
            cmdActivate=self._activate_item_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self._itemCollection.pack(fill='x')
        inputWidgets.extend(self._itemCollection.inputWidgets)

        self._prefsShowLinks = 'show_sc_links'

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- Frame for date/time/duration.
        self._dateTimeFrame = FoldingFrame(
            self._elementInfoWindow,
            _('Date/Time'),
            self._toggle_date_time_frame)
        sectionStartFrame = ttk.Frame(self._dateTimeFrame
                                      )
        sectionStartFrame.pack(fill='x')
        localeDateFrame = ttk.Frame(sectionStartFrame)
        localeDateFrame.pack(fill='x')
        ttk.Label(localeDateFrame, text=_('Start'), width=self._DATE_TIME_LBL_X).pack(side='left')

        # 'Start date' entry.
        self._startDate = MyStringVar()
        self._startDateEntry = LabelEntry(
            sectionStartFrame,
            text=_('Date'),
            textvariable=self._startDate,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._startDateEntry.pack(anchor='w')
        inputWidgets.append(self._startDateEntry)

        # 'Start time' entry.
        self._startTime = MyStringVar()
        self._startTimeEntry = LabelEntry(
            sectionStartFrame,
            text=_('Time'),
            textvariable=self._startTime,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._startTimeEntry.pack(anchor='w')
        inputWidgets.append(self._startTimeEntry)

        # 'Start day' entry.
        self._startDay = MyStringVar()
        self._startDayEntry = LabelEntry(
            sectionStartFrame,
            text=_('Day'),
            textvariable=self._startDay,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._startDayEntry.pack(anchor='w')
        inputWidgets.append(self._startDayEntry)
        self._startDayEntry.entry.bind('<Return>', self._change_day)

        # Day of the week display.
        self._weekDay = MyStringVar()
        ttk.Label(localeDateFrame, textvariable=self._weekDay).pack(side='left')

        # Localized date display.
        self._localeDate = MyStringVar()
        ttk.Label(localeDateFrame, textvariable=self._localeDate).pack(side='left')

        # Time display.
        ttk.Label(localeDateFrame, textvariable=self._startTime).pack(side='left')

        # 'Moon phase' button.
        ttk.Button(
            localeDateFrame,
            text=_('Moon phase'),
            command=self._show_moonphase
            ).pack(anchor='e')

        # 'Clear date/time' button.
        self._clearDateButton = ttk.Button(
            sectionStartFrame,
            text=_('Clear date/time'),
            command=self._clear_start
            )
        self._clearDateButton.pack(side='left', fill='x', expand=True, padx=1, pady=2)
        inputWidgets.append(self._clearDateButton)

        # 'Generate' button.
        self._generateDateButton = ttk.Button(
            sectionStartFrame,
            text=_('Generate'),
            command=self._auto_set_date
            )
        self._generateDateButton.pack(side='left', fill='x', expand=True, padx=1, pady=2)
        inputWidgets.append(self._generateDateButton)

        # 'Toggle date' button.
        self._toggleDateButton = ttk.Button(
            sectionStartFrame,
            text=_('Convert date/day'),
            command=self._toggle_date
            )
        self._toggleDateButton.pack(side='left', fill='x', expand=True, padx=1, pady=2)
        inputWidgets.append(self._toggleDateButton)

        ttk.Separator(self._dateTimeFrame, orient='horizontal').pack(fill='x', pady=2)

        sectionDurationFrame = ttk.Frame(self._dateTimeFrame)
        sectionDurationFrame.pack(fill='x')
        ttk.Label(sectionDurationFrame, text=_('Duration')).pack(anchor='w')

        # 'Duration days' entry.
        self._lastsDays = MyStringVar()
        self._lastsDaysEntry = LabelEntry(
            sectionDurationFrame,
            text=_('Days'),
            textvariable=self._lastsDays,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._lastsDaysEntry.pack(anchor='w')
        inputWidgets.append(self._lastsDaysEntry)

        # 'Duration hours' entry.
        self._lastsHours = MyStringVar()
        self._lastsHoursEntry = LabelEntry(
            sectionDurationFrame,
            text=_('Hours'),
            textvariable=self._lastsHours,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._lastsHoursEntry.pack(anchor='w')
        inputWidgets.append(self._lastsHoursEntry)

        # 'Duration minutes' entry.
        self._lastsMinutes = MyStringVar()
        self._lastsMinutesEntry = LabelEntry(
            sectionDurationFrame,
            text=_('Minutes'),
            textvariable=self._lastsMinutes,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._lastsMinutesEntry.pack(anchor='w')
        inputWidgets.append(self._lastsMinutesEntry)

        # 'Clear duration' button.
        self._clearDurationButton = ttk.Button(
            sectionDurationFrame,
            text=_('Clear duration'),
            command=self._clear_duration
            )
        self._clearDurationButton.pack(side='left', padx=1, pady=2)
        inputWidgets.append(self._clearDurationButton)

        # 'Generate' button.
        self._generatDurationButton = ttk.Button(
            sectionDurationFrame,
            text=_('Generate'),
            command=self._auto_set_duration
            )
        self._generatDurationButton.pack(side='left', padx=1, pady=2)
        inputWidgets.append(self._generatDurationButton)

        # ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- 'Viewpoint' combobox.
        self._viewpoint = MyStringVar()
        self._characterCombobox = LabelCombo(
            self._sectionExtraFrame,
            text=_('Viewpoint'),
            textvariable=self._viewpoint,
            values=[],
            )
        self._characterCombobox.pack(anchor='w', pady=2)
        inputWidgets.append(self._characterCombobox)
        self._characterCombobox.combo.bind('<<ComboboxSelected>>', self.apply_changes)
        self._vpList = []

        #--- 'Unused' checkbox.
        self._isUnused = tk.BooleanVar()
        self._isUnusedCheckbox = ttk.Checkbutton(
            self._sectionExtraFrame,
            text=_('Unused'),
            variable=self._isUnused,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._isUnusedCheckbox.pack(anchor='w')
        inputWidgets.append(self._isUnusedCheckbox)

        #--- 'Append to previous section' checkbox.
        self._appendToPrev = tk.BooleanVar()
        self._appendToPrevCheckbox = ttk.Checkbutton(
            self._sectionExtraFrame,
            text=_('Append to previous section'),
            variable=self._appendToPrev,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._appendToPrevCheckbox.pack(anchor='w')
        inputWidgets.append(self._appendToPrevCheckbox)

        ttk.Separator(self._sectionExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for 'Plot'.
        self._plotFrame = FoldingFrame(self._sectionExtraFrame, _('Plot'), self._toggle_plot_frame)

        # 'Plot lines' listbox.
        self._plotlineTitles = ''
        self._plotlineLabel = ttk.Label(self._plotFrame, text=_('Plot lines'))
        self._plotlineLabel.pack(anchor='w')
        self._plotlineCollection = CollectionBox(
            self._plotFrame,
            cmdAdd=self._pick_plotline,
            cmdRemove=self._remove_plotline,
            cmdOpen=self._go_to_arc,
            cmdActivate=self._activate_arc_buttons,
            cmdSelect=self._on_select_plotline,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self._plotlineCollection.pack(fill='x')
        inputWidgets.extend(self._plotlineCollection.inputWidgets)
        self._selectedPlotline = None

        #--- 'Plot line notes' text box for entering self._element.plotlineNotes[plId],
        #    where plId is the ID of the selected plot line in the'Plot lines' listbox.
        ttk.Label(self._plotFrame, text=_('Notes on the selected plot line')).pack(anchor='w')
        self._plotNotesWindow = TextBox(
            self._plotFrame,
            wrap='word',
            undo=True,
            autoseparators=True,
            maxundo=-1,
            height=prefs['gco_height'],
            padx=5,
            pady=5,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
            insertbackground=prefs['color_text_fg'],
            )
        self._plotNotesWindow.pack(fill='x')
        inputWidgets.append(self._plotNotesWindow)

        #--- 'Plot points' label.
        ttk.Label(self._plotFrame, text=_('Plot points')).pack(anchor='w')
        self._plotPointsDisplay = tk.Label(self._plotFrame, anchor='w', bg='white')
        self._plotPointsDisplay.pack(anchor='w', fill='x')

        ttk.Separator(self._sectionExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for 'Scene'.
        self._sceneFrame = FoldingFrame(self._sectionExtraFrame, _('Scene'), self._toggle_scene_frame)

        # Scene radiobuttons.
        selectionFrame = ttk.Frame(self._sceneFrame)
        self._customPlotProgress = ''
        self._customCharacterization = ''
        self._customWorldBuilding = ''
        self._customGoal = ''
        self._customConflict = ''
        self._customOutcome = ''
        self._scene = tk.IntVar()

        self._notApplicableRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Not a scene'),
            variable=self._scene,
            value=0, command=self._set_not_applicable,
            )
        self._notApplicableRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._notApplicableRadiobutton)

        self._actionRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Action'),
            variable=self._scene,
            value=1, command=self._set_action_scene,
            )
        self._actionRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._actionRadiobutton)

        self._reactionRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Reaction'),
            variable=self._scene,
            value=2,
            command=self._set_reaction_scene,
            )
        self._reactionRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._reactionRadiobutton)

        self._customRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Other'),
            variable=self._scene,
            value=3,
            command=self._set_custom_scene
            )
        self._customRadiobutton.pack(anchor='w')
        inputWidgets.append(self._customRadiobutton)

        selectionFrame.pack(fill='x')

        # 'Goal/Reaction' window. The labels are configured dynamically.
        self._goalLabel = ttk.Label(self._sceneFrame)
        self._goalLabel.pack(anchor='w')
        self._goalWindow = TextBox(
            self._sceneFrame,
            wrap='word',
            undo=True,
            autoseparators=True,
            maxundo=-1,
            height=prefs['gco_height'],
            padx=5,
            pady=5,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
            insertbackground=prefs['color_text_fg'],
            )
        self._goalWindow.pack(fill='x')
        inputWidgets.append(self._goalWindow)

        # 'Conflict/Dilemma' window. The labels are configured dynamically.
        self._conflictLabel = ttk.Label(self._sceneFrame)
        self._conflictLabel.pack(anchor='w')
        self._conflictWindow = TextBox(
            self._sceneFrame,
            wrap='word',
            undo=True,
            autoseparators=True,
            maxundo=-1,
            height=prefs['gco_height'],
            padx=5,
            pady=5,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
            insertbackground=prefs['color_text_fg'],
            )
        self._conflictWindow.pack(fill='x')
        inputWidgets.append(self._conflictWindow)

        # 'Outcome/Choice' window. The labels are configured dynamically.
        self._outcomeLabel = ttk.Label(self._sceneFrame)
        self._outcomeLabel.pack(anchor='w')
        self._outcomeWindow = TextBox(
            self._sceneFrame,
            wrap='word',
            undo=True,
            autoseparators=True,
            maxundo=-1,
            height=prefs['gco_height'],
            padx=5,
            pady=5,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
            insertbackground=prefs['color_text_fg'],
            )
        self._outcomeWindow.pack(fill='x')
        inputWidgets.append(self._outcomeWindow)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self._inputWidgets.append(widget)

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self._element is None:
            return

        super().apply_changes()

        #--- Section start.

        # 'Tags' entry.
        newTags = self._tags.get()
        if self._tagsStr or newTags:
            self._element.tags = string_to_list(newTags)

        # Date and time are checked separately.
        # If an invalid date is entered, the old value is kept.
        # If an invalid time is entered, the old value is kept.
        # If a valid date is entered, the day is cleared, if any.
        # Otherwise, if a valid day is entered, the date is cleared, if any.

        # 'Date' entry.
        dateStr = self._startDate.get()
        if not dateStr:
            self._element.date = None
        elif dateStr != self._element.date:
            try:
                date.fromisoformat(dateStr)
            except ValueError:
                self._startDate.set(self._element.date)
                self._ui.show_error(
                    f'{_("Wrong date")}: "{dateStr}"\n{_("Required")}: {_("YYYY-MM-DD")}',
                    title=_('Input rejected')
                    )
            else:
                self._element.date = dateStr

        # 'Time' entry.
        timeStr = self._startTime.get()
        if not timeStr:
            self._element.time = None
        else:
            if self._element.time:
                dispTime = self._element.time.rsplit(':', 1)[0]
            else:
                dispTime = ''
            if timeStr != dispTime:
                try:
                    time.fromisoformat(timeStr)
                except ValueError:
                    self._startTime.set(dispTime)
                    self._ui.show_error(
                        f'{_("Wrong time")}: "{timeStr}"\n{_("Required")}: {_("hh:mm")}',
                        title=_('Input rejected')
                        )
                else:
                    while timeStr.count(':') < 2:
                        timeStr = f'{timeStr}:00'
                    self._element.time = timeStr
                    dispTime = self._element.time.rsplit(':', 1)[0]
                    self._startTime.set(dispTime)

        # 'Day' entry.
        if self._element.date:
            self._element.day = None
        else:
            self._change_day()

        #--- Section duration.
        # Section duration changes are applied as a whole.
        # That is, days, hours and minutes entries must all be correct numbers.
        # Otherwise, the old values are kept.
        # If more than 60 minutes are entered in the "Minutes" field,
        # the hours are incremented accordingly.
        # If more than 24 hours are entered in the "Hours" field,
        # the days are incremented accordingly.
        wrongEntry = False
        newEntry = False

        # 'Duration minutes' entry.
        hoursLeft = 0
        lastsMinutesStr = self._lastsMinutes.get()
        if lastsMinutesStr or self._element.lastsMinutes:
            if lastsMinutesStr != self._element.lastsMinutes:
                if not lastsMinutesStr:
                    lastsMinutesStr = 0
                try:
                    minutes = int(lastsMinutesStr)
                except ValueError:
                    wrongEntry = True
                else:
                    hoursLeft, minutes = divmod(minutes, 60)
                    if minutes > 0:
                        lastsMinutesStr = str(minutes)
                    else:
                        lastsMinutesStr = None
                    self._lastsMinutes.set(lastsMinutesStr)
                    newEntry = True

        # 'Duration hours' entry.
        daysLeft = 0
        lastsHoursStr = self._lastsHours.get()
        if hoursLeft or lastsHoursStr or self._element.lastsHours:
            if hoursLeft or lastsHoursStr != self._element.lastsHours:
                try:
                    if lastsHoursStr:
                        hoursLeft += int(lastsHoursStr)
                    daysLeft, hoursLeft = divmod(hoursLeft, 24)
                    if hoursLeft > 0:
                        lastsHoursStr = str(hoursLeft)
                    else:
                        lastsHoursStr = None
                    self._lastsHours.set(lastsHoursStr)
                except ValueError:
                    wrongEntry = True
                else:
                    newEntry = True

        # 'Duration days' entry.
        lastsDaysStr = self._lastsDays.get()
        if daysLeft or lastsDaysStr or self._element.lastsDays:
            if daysLeft or lastsDaysStr != self._element.lastsDays:
                try:
                    if lastsDaysStr:
                        daysLeft += int(lastsDaysStr)
                    if daysLeft > 0:
                        lastsDaysStr = str(daysLeft)
                    else:
                        lastsDaysStr = None
                    self._lastsDays.set(lastsDaysStr)
                except ValueError:
                    wrongEntry = True
                else:
                    newEntry = True

        if wrongEntry:
            self._lastsMinutes.set(self._element.lastsMinutes)
            self._lastsHours.set(self._element.lastsHours)
            self._lastsDays.set(self._element.lastsDays)
            self._ui.show_error(f'{_("Wrong entry: number required")}.', title=_('Input rejected'))
        elif newEntry:
            self._element.lastsMinutes = lastsMinutesStr
            self._element.lastsHours = lastsHoursStr
            self._element.lastsDays = lastsDaysStr

        #--- 'Viewpoint' combobox.
        option = self._characterCombobox.current()
        if option >= 0:
            # Put the selected character at the first position of related characters.
            vpId = self._vpList[option]
            scCharacters = self._element.characters
            if scCharacters:
                    if vpId in scCharacters:
                        scCharacters.remove(vpId)
                    scCharacters.insert(0, vpId)
            else:
                scCharacters = [vpId]
            self._element.characters = scCharacters

        #--- 'Unused' checkbox.
        if self._isUnused.get():
            self._element.scType = 1
        else:
            self._element.scType = 0

        #--- 'Append to previous section' checkbox.
        self._element.appendToPrev = self._appendToPrev.get()

        #--- 'Plot line notes' text box.
        self._save_plot_notes()

        #--- 'Goal/Reaction' window.
        if self._goalWindow.hasChanged:
            self._element.goal = self._goalWindow.get_text()
        #--- 'Conflict/Dilemma' window.
        if self._conflictWindow.hasChanged:
            self._element.conflict = self._conflictWindow.get_text()

        #--- 'Outcome/Choice' window.
        if self._outcomeWindow.hasChanged:
            self._element.outcome = self._outcomeWindow.get_text()

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.sections[elementId]
        super().set_data(elementId)

        # 'Tags' entry.
        self._tagsStr = list_to_string(self._element.tags)
        self._tags.set(self._tagsStr)

        #--- Frame for 'Relationships'.
        if prefs['show_relationships']:
            self._relationFrame.show()
        else:
            self._relationFrame.hide()

        # 'Characters' window.
        self._crTitles = self._get_element_titles(self._element.characters, self._mdl.novel.characters)
        self._characterCollection.cList.set(self._crTitles)
        listboxSize = len(self._crTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._characterCollection.cListbox.config(height=listboxSize)
        if not self._characterCollection.cListbox.curselection() or not self._characterCollection.cListbox.focus_get():
            self._characterCollection.disable_buttons()

        # 'Locations' window.
        self._lcTitles = self._get_element_titles(self._element.locations, self._mdl.novel.locations)
        self._locationCollection.cList.set(self._lcTitles)
        listboxSize = len(self._lcTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._locationCollection.cListbox.config(height=listboxSize)
        if not self._locationCollection.cListbox.curselection() or not self._locationCollection.cListbox.focus_get():
            self._locationCollection.disable_buttons()

        # 'Items' window.
        self._itTitles = self._get_element_titles(self._element.items, self._mdl.novel.items)
        self._itemCollection.cList.set(self._itTitles)
        listboxSize = len(self._itTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._itemCollection.cListbox.config(height=listboxSize)
        if not self._itemCollection.cListbox.curselection() or not self._itemCollection.cListbox.focus_get():
            self._itemCollection.disable_buttons()

        #--- Frame for date/time/duration.
        if self._element.date and self._element.weekDay is not None:
            self._weekDay.set(WEEKDAYS[self._element.weekDay])
        elif self._element.day and self._mdl.novel.referenceWeekDay is not None:
            self._weekDay.set(WEEKDAYS[(int(self._element.day) + self._mdl.novel.referenceWeekDay) % 7])
        else:
            self._weekDay.set('')
        self._startDate.set(self._element.date)
        if self._element.localeDate:
            displayDate = get_section_date_str(self._element)
        elif self._element.day:
            displayDate = f'{_("Day")} {self._element.day}'
        else:
            displayDate = ''
        self._localeDate.set(displayDate)

        # Remove the seconds for the display.
        if self._element.time:
            dispTime = self._element.time.rsplit(':', 1)[0]
        else:
            dispTime = ''
        self._startTime.set(dispTime)

        self._startDay.set(self._element.day)
        self._lastsDays.set(self._element.lastsDays)
        self._lastsHours.set(self._element.lastsHours)
        self._lastsMinutes.set(self._element.lastsMinutes)

        #--- Frame for date/time.
        if prefs['show_date_time']:
            self._dateTimeFrame.show()
        else:
            self._dateTimeFrame.hide()

        #--- 'Viewpoint' combobox.
        charNames = []
        self._vpList = []
        for crId in self._mdl.novel.tree.get_children(CR_ROOT):
            charNames.append(self._mdl.novel.characters[crId].title)
            self._vpList.append(crId)
        self._characterCombobox.configure(values=charNames)
        if self._element.characters:
            vp = self._mdl.novel.characters[self._element.characters[0]].title
        else:
            vp = ''
        self._viewpoint.set(value=vp)

        #--- 'Plot lines' listbox.
        self._plotlineTitles = self._get_plotline_titles(self._element.scPlotLines, self._mdl.novel.plotLines)
        self._plotlineCollection.cList.set(self._plotlineTitles)
        listboxSize = len(self._plotlineTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._plotlineCollection.cListbox.config(height=listboxSize)
        if not self._plotlineCollection.cListbox.curselection() or not self._plotlineCollection.cListbox.focus_get():
            self._plotlineCollection.disable_buttons()

        #--- 'Plot notes' text box.
        self._plotNotesWindow.clear()
        self._plotNotesWindow.config(state='disabled')
        self._plotNotesWindow.config(bg='light gray')
        if self._plotlineTitles:
            self._plotlineCollection.cListbox.select_clear(0, 'end')
            self._plotlineCollection.cListbox.select_set('end')
            self._selectedPlotline = -1
            self._on_select_plotline(-1)
        else:
            self._selectedPlotline = None

        #--- "Plot points" label
        plotPointTitles = []
        for ppId in self._element.scPlotPoints:
            plId = self._element.scPlotPoints[ppId]
            plotPointTitles.append(f'{self._mdl.novel.plotLines[plId].shortName}: {self._mdl.novel.plotPoints[ppId].title}')
        self._plotPointsDisplay.config(text=list_to_string(plotPointTitles))

        #--- 'Unused' checkbox.
        if self._element.scType > 0:
            self._isUnused.set(True)
        else:
            self._isUnused.set(False)

        #--- 'Append to previous section' checkbox.
        if self._element.appendToPrev:
            self._appendToPrev.set(True)
        else:
            self._appendToPrev.set(False)

        # Customized Goal/Conflict/Outcome configuration.
        if self._mdl.novel.customPlotProgress:
            self._customPlotProgress = self._mdl.novel.customPlotProgress
        else:
            self._customPlotProgress = ''

        if self._mdl.novel.customCharacterization:
            self._customCharacterization = self._mdl.novel.customCharacterization
        else:
            self._customCharacterization = ''

        if self._mdl.novel.customWorldBuilding:
            self._customWorldBuilding = self._mdl.novel.customWorldBuilding
        else:
            self._customWorldBuilding = ''

        if self._mdl.novel.customGoal:
            self._customGoal = self._mdl.novel.customGoal
        else:
            self._customGoal = ''

        if self._mdl.novel.customConflict:
            self._customConflict = self._mdl.novel.customConflict
        else:
            self._customConflict = ''

        if self._mdl.novel.customOutcome:
            self._customOutcome = self._mdl.novel.customOutcome
        else:
            self._customOutcome = ''

        #--- Frame for 'Plot'.
        if prefs['show_plot']:
            self._plotFrame.show()
        else:
            self._plotFrame.hide()

        #--- Frame for 'Scene'.
        if prefs['show_scene']:
            self._sceneFrame.show()
        else:
            self._sceneFrame.hide()

        #--- Scene radiobuttons.
        self._scene.set(self._element.scene)

        #--- 'Goal/Reaction' window.
        self._goalWindow.set_text(self._element.goal)

        #--- 'Conflict/Dilemma' window.
        self._conflictWindow.set_text(self._element.conflict)

        #--- 'Outcome/Choice' window.
        self._outcomeWindow.set_text(self._element.outcome)

        # Configure the labels.
        if self._element.scene == 3:
            self._set_custom_scene()
        elif self._element.scene == 2:
            self._set_reaction_scene()
        elif self._element.scene == 1:
            self._set_action_scene()
        else:
            self._set_not_applicable()

    def unlock(self):
        """Enable plot line notes only if a plot line is selected."""
        super().unlock()
        if self._selectedPlotline is None:
            self._plotNotesWindow.config(state='disabled')

    def _activate_arc_buttons(self, event=None):
        if self._element.scPlotLines:
            self._plotlineCollection.enable_buttons()
        else:
            self._plotlineCollection.disable_buttons()

    def _activate_character_buttons(self, event=None):
        if self._element.characters:
            self._characterCollection.enable_buttons()
        else:
            self._characterCollection.disable_buttons()

    def _activate_item_buttons(self, event=None):
        if self._element.items:
            self._itemCollection.enable_buttons()
        else:
            self._itemCollection.disable_buttons()

    def _activate_location_buttons(self, event=None):
        if self._element.locations:
            self._locationCollection.enable_buttons()
        else:
            self._locationCollection.disable_buttons()

    def _add_character(self, event=None):
        # Add the selected element to the collection, if applicable.
        crList = self._element.characters
        crId = self._ui.tv.tree.selection()[0]
        if crId.startswith(CHARACTER_PREFIX) and not crId in crList:
            crList.append(crId)
            self._element.characters = crList

    def _add_item(self, event=None):
        # Add the selected element to the collection, if applicable.
        itList = self._element.items
        itId = self._ui.tv.tree.selection()[0]
        if itId.startswith(ITEM_PREFIX)and not itId in itList:
            itList.append(itId)
            self._element.items = itList

    def _add_location(self, event=None):
        # Add the selected element to the collection, if applicable.
        lcList = self._element.locations
        lcId = self._ui.tv.tree.selection()[0]
        if lcId.startswith(LOCATION_PREFIX)and not lcId in lcList:
            lcList.append(lcId)
            self._element.locations = lcList

    def _add_plotline(self, event=None):
        # Add the selected element to the collection, if applicable.
        plotlineList = self._element.scPlotLines
        plId = self._ui.tv.tree.selection()[0]
        if plId.startswith(PLOT_LINE_PREFIX) and not plId in plotlineList:
            plotlineList.append(plId)
            self._element.scPlotLines = plotlineList
            plotlineSections = self._mdl.novel.plotLines[plId].sections
            if not self._elementId in plotlineSections:
                plotlineSections.append(self._elementId)
                self._mdl.novel.plotLines[plId].sections = plotlineSections

            # TODO: Select the new plot line entry.

    def _auto_set_date(self):
        """Set section start to the end of the previous section."""
        prevScId = self._ui.tv.prev_node(self._elementId)
        if not prevScId:
            return

        newDate, newTime, newDay = self._mdl.novel.sections[prevScId].get_end_date_time()
        if newTime is None:
            self._ui.show_error(
                _('The previous section has no time set.'),
                title=_('Cannot generate date/time')
                )
            return

        # self.doNotUpdate = True
        self._element.date = newDate
        self._element.time = newTime
        self._element.day = newDay
        # self.doNotUpdate = False
        self._startDate.set(newDate)
        self._startTime.set(newTime.rsplit(':', 1)[0])
        self._startDay.set(newDay)

    def _auto_set_duration(self):
        """Calculate section duration from the start of the next section."""

        def day_to_date(day, refDate):
            deltaDays = timedelta(days=int(day))
            return date.isoformat(refDate + deltaDays)

        nextScId = self._ui.tv.next_node(self._elementId)
        if not nextScId:
            return

        thisTimeIso = self._element.time
        if not thisTimeIso:
            self._ui.show_error(
                _('This section has no time set.'),
                title=_('Cannot generate duration')
                )
            return

        nextTimeIso = self._mdl.novel.sections[nextScId].time
        if not nextTimeIso:
            self._ui.show_error(
                _('The next section has no time set.'),
                title=_('Cannot generate duration')
                )
            return

        try:
            refDateIso = self._mdl.novel.referenceDate
            refDate = date.fromisoformat(refDateIso)
        except:
            refDate = date.today()
            refDateIso = date.isoformat(refDate)
        if self._mdl.novel.sections[nextScId].date:
            nextDateIso = self._mdl.novel.sections[nextScId].date
        elif self._mdl.novel.sections[nextScId].day:
            nextDateIso = day_to_date(self._mdl.novel.sections[nextScId].day, refDate)
        elif self._element.day:
            nextDateIso = self._element.day
        else:
            nextDateIso = refDateIso
        if self._element.date:
            thisDateIso = self._element.date
        elif self._element.day:
            thisDateIso = day_to_date(self._element.day, refDate)
        else:
            thisDateIso = nextDateIso

        StartDateTime = datetime.fromisoformat(f'{thisDateIso}T{thisTimeIso}')
        endDateTime = datetime.fromisoformat(f'{nextDateIso}T{nextTimeIso}')
        sectionDuration = endDateTime - StartDateTime
        lastsHours = sectionDuration.seconds // 3600
        lastsMinutes = (sectionDuration.seconds % 3600) // 60
        if sectionDuration.days:
            newDays = str(sectionDuration.days)
        else:
            newDays = None
        if lastsHours:
            newHours = str(lastsHours)
        else:
            newHours = None
        if lastsMinutes:
            newMinutes = str(lastsMinutes)
        else:
            newMinutes = None

        self.doNotUpdate = True
        self._element.lastsDays = newDays
        self._element.lastsHours = newHours
        self._element.lastsMinutes = newMinutes
        self.doNotUpdate = False
        self._lastsDays.set(newDays)
        self._lastsHours.set(newHours)
        self._lastsMinutes.set(newMinutes)

    def _clear_duration(self):
        """Remove duration data from the section."""
        durationData = [
            self._element.lastsDays,
            self._element.lastsHours,
            self._element.lastsMinutes,
            ]
        hasData = False
        for dataElement in durationData:
            if dataElement:
                hasData = True
        if hasData and self._ui.ask_yes_no(_('Clear duration from this section?')):
            self._element.lastsDays = None
            self._element.lastsHours = None
            self._element.lastsMinutes = None

    def _change_day(self, event=None):
        # 'Day' entry. If valid, clear the start date.
            dayStr = self._startDay.get()
            if dayStr or self._element.day:
                if dayStr != self._element.day:
                    if not dayStr:
                        self._element.day = None
                    else:
                        try:
                            int(dayStr)
                        except ValueError:
                            self._startDay.set(self._element.day)
                            self._ui.show_error(
                                f'{_("Wrong entry: number required")}.',
                                title=_('Input rejected')
                                )
                        else:
                            self._element.day = dayStr
                            self._element.date = None

    def _clear_start(self):
        """Remove start data from the section."""
        startData = [
            self._element.date,
            self._element.time,
            self._element.day,
            ]
        hasData = False
        for dataElement in startData:
            if dataElement:
                hasData = True
        if hasData and self._ui.ask_yes_no(_('Clear date/time from this section?')):
            self._element.date = None
            self._element.time = None
            self._element.day = None

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _get_element_titles(self, elemIds, elements):
        """Return a list of element titles.
        
        Positional arguments:
            elemIds -- list of element IDs.
            elements -- list of element objects.          
        """
        elemTitles = []
        if elemIds:
            for elemId in elemIds:
                try:
                    elemTitles.append(elements[elemId].title)
                except:
                    pass
        return elemTitles

    def _get_plotline_titles(self, elemIds, elements):
        """Return a list of plot line titles, preceded by the short names.
        
        Positional arguments:
            elemIds -- list of element IDs.
            elements -- list of element objects.          
        """
        elemTitles = []
        if elemIds:
            for elemId in elemIds:
                try:
                    elemTitles.append(f'({elements[elemId].shortName}) {elements[elemId].title}')
                except:
                    pass
        return elemTitles

    def _get_relation_id_list(self, newTitleStr, oldTitleStr, elements):
        """Return a list of valid IDs from a string containing semicolon-separated titles."""
        if newTitleStr or oldTitleStr:
            if oldTitleStr != newTitleStr:
                elemIds = []
                for elemTitle in string_to_list(newTitleStr):
                    for elemId in elements:
                        if elements[elemId].title == elemTitle:
                            elemIds.append(elemId)
                            break
                    else:
                        # No break occurred: there is no element with the specified title
                        self._ui.show_error(f'{_("Wrong name")}: "{elemTitle}"', title=_('Input rejected'))
                return elemIds

        return None

    def _go_to_arc(self, event=None):
        """Go to the plot line selected in the listbox."""
        try:
            selection = self._plotlineCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self._element.scPlotLines[selection])

    def _go_to_character(self, event=None):
        """Go to the character selected in the listbox."""
        try:
            selection = self._characterCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self._element.characters[selection])

    def _go_to_location(self, event=None):
        """Go to the location selected in the listbox."""
        try:
            selection = self._locationCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self._element.locations[selection])

    def _go_to_item(self, event=None):
        """Go to the item selected in the listbox."""
        try:
            selection = self._itemCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self._element.items[selection])

    def _on_select_plotline(self, selection):
        """Callback routine for section plot line list selection."""
        self._save_plot_notes()
        self._selectedPlotline = self._element.scPlotLines[selection]
        self._plotNotesWindow.config(state='normal')
        if self._element.plotlineNotes:
            self._plotNotesWindow.set_text(self._element.plotlineNotes.get(self._selectedPlotline, ''))
        else:
            self._plotNotesWindow.clear()
        if self._isLocked:
            self._plotNotesWindow.config(state='disabled')
        self._plotNotesWindow.config(bg='white')

    def _pick_character(self, event=None):
        """Enter the "add character" selection mode."""
        self._start_picking_mode(command=self._add_character)
        self._ui.tv.see_node(CR_ROOT)

    def _pick_item(self, event=None):
        """Enter the "add item" selection mode."""
        self._start_picking_mode(command=self._add_item)
        self._ui.tv.see_node(IT_ROOT)

    def _pick_location(self, event=None):
        """Enter the "add location" selection mode."""
        self._start_picking_mode(command=self._add_location)
        self._ui.tv.see_node(LC_ROOT)

    def _pick_plotline(self, event=None):
        """Enter the "add plot line" selection mode."""
        self._start_picking_mode(command=self._add_plotline)
        self._ui.tv.see_node(PL_ROOT)

    def _remove_character(self, event=None):
        """Remove the character selected in the listbox from the section characters."""
        try:
            selection = self._characterCollection.cListbox.curselection()[0]
        except:
            return

        crId = self._element.characters[selection]
        title = self._mdl.novel.characters[crId].title
        if self._ui.ask_yes_no(f'{_("Remove character")}: "{title}"?'):
            crList = self._element.characters
            del crList[selection]
            self._element.characters = crList

    def _remove_item(self, event=None):
        """Remove the item selected in the listbox from the section items."""
        try:
            selection = self._itemCollection.cListbox.curselection()[0]
        except:
            return

        itId = self._element.items[selection]
        title = self._mdl.novel.items[itId].title
        if self._ui.ask_yes_no(f'{_("Remove item")}: "{title}"?'):
            itList = self._element.items
            del itList[selection]
            self._element.items = itList

    def _remove_location(self, event=None):
        """Remove the location selected in the listbox from the section locations."""
        try:
            selection = self._locationCollection.cListbox.curselection()[0]
        except:
            return

        lcId = self._element.locations[selection]
        title = self._mdl.novel.locations[lcId].title
        if self._ui.ask_yes_no(f'{_("Remove location")}: "{title}"?'):
            lcList = self._element.locations
            del lcList[selection]
            self._element.locations = lcList

    def _remove_plotline(self, event=None):
        """Remove the plot line selected in the listbox from the section associations."""
        try:
            selection = self._plotlineCollection.cListbox.curselection()[0]
        except:
            return

        plId = self._element.scPlotLines[selection]
        title = self._mdl.novel.plotLines[plId].title
        if not self._ui.ask_yes_no(f'{_("Remove plot line")}: "{title}"?'):
            return

        # Remove the plot line from the section's list.
        arcList = self._element.scPlotLines
        del arcList[selection]
        self._element.scPlotLines = arcList

        # Remove the section from the plot line's list.
        arcSections = self._mdl.novel.plotLines[plId].sections
        if self._elementId in arcSections:
            arcSections.remove(self._elementId)
            self._mdl.novel.plotLines[plId].sections = arcSections

            # Remove plot point assignments, if any.
            for ppId in list(self._element.scPlotPoints):
                if self._element.scPlotPoints[ppId] == plId:
                    del(self._element.scPlotPoints[ppId])
                    # removing the plot line's plot point from the section's list
                    # Note: this doesn't trigger the refreshing method
                    self._mdl.novel.plotPoints[ppId].sectionAssoc = None
                    # un-assigning the section from the plot line's plot point

    def _save_plot_notes(self):
        if self._selectedPlotline and self._plotNotesWindow.hasChanged:
            plotlineNotes = self._element.plotlineNotes
            if plotlineNotes is None:
                plotlineNotes = {}
            plotlineNotes[self._selectedPlotline] = self._plotNotesWindow.get_text()
            self.doNotUpdate = True
            self._element.plotlineNotes = plotlineNotes
            self.doNotUpdate = False

    def _set_action_scene(self, event=None):
        self._goalLabel.config(text=_('Goal'))
        self._conflictLabel.config(text=_('Conflict'))
        self._outcomeLabel.config(text=_('Outcome'))
        self._element.scene = self._scene.get()

    def _set_custom_scene(self, event=None):
        if self._customGoal:
            self._goalLabel.config(text=self._customGoal)
        else:
            self._goalLabel.config(text=_('Opening'))

        if self._customConflict:
            self._conflictLabel.config(text=self._customConflict)
        else:
            self._conflictLabel.config(text=_('Peak emotional moment'))

        if self._customOutcome:
            self._outcomeLabel.config(text=self._customOutcome)
        else:
            self._outcomeLabel.config(text=_('Ending'))

        self._element.scene = self._scene.get()

    def _set_not_applicable(self, event=None):
        if self._customPlotProgress:
            self._goalLabel.config(text=self._customPlotProgress)
        else:
            self._goalLabel.config(text=_('Plot progress'))

        if self._customCharacterization:
            self._conflictLabel.config(text=self._customCharacterization)
        else:
            self._conflictLabel.config(text=_('Characterization'))

        if self._customWorldBuilding:
            self._outcomeLabel.config(text=self._customWorldBuilding)
        else:
            self._outcomeLabel.config(text=_('World building'))

        self._element.scene = self._scene.get()

    def _set_reaction_scene(self, event=None):
        self._goalLabel.config(text=_('Reaction'))
        self._conflictLabel.config(text=_('Dilemma'))
        self._outcomeLabel.config(text=_('Choice'))
        self._element.scene = self._scene.get()

    def _show_ages(self, event=None):
        """Display the ages of the related characters."""
        if self._element.date is not None:
            now = self._element.date
        else:
            try:
                now = get_specific_date(
                    self._element.day,
                    self._mdl.novel.referenceDate
                    )
            except:
                self._show_missing_date_message()
                return

        charList = []
        for crId in self._element.characters:
            birthDate = self._mdl.novel.characters[crId].birthDate
            deathDate = self._mdl.novel.characters[crId].deathDate
            try:
                years = get_age(now, birthDate, deathDate)
                if years < 0:
                    years *= -1
                    suffix = _('years after death')
                else:
                    suffix = _('years old')
                charList.append(f'{self._mdl.novel.characters[crId].title}: {years} {suffix}')
            except:
                charList.append(f'{self._mdl.novel.characters[crId].title}: ({_("no data")})')

        if charList:
            self._ui.show_info(
                '\n'.join(charList),
                title=f'{_("Date")}: {datestr(now)}'
                )

    def _show_moonphase(self, event=None):
        """Display the moon phase of the section start date."""
        if self._element.date is not None:
            now = self._element.date
        else:
            try:
                now = get_specific_date(
                    self._element.day,
                    self._mdl.novel.referenceDate
                    )
            except:
                self._show_missing_date_message()
                return

        self._ui.show_info(
            f'{_("Moon phase")}: '\
            f'{self._mdl.nvService.get_moon_phase_str(now)}',
            title=f'{_("Date")}: {datestr(now)}'
            )

    def _toggle_date(self, event=None):
        """Toggle specific/unspecific date."""
        if not self._mdl.novel.referenceDate:
            self._show_missing_reference_date_message()
            return

        self.doNotUpdate = True
        if self._element.date:
            self._element.date_to_day(self._mdl.novel.referenceDate)
        elif self._element.day:
            self._element.day_to_date(self._mdl.novel.referenceDate)
        else:
            self._show_missing_date_message()
            return

        self.doNotUpdate = False
        self.set_data(self._elementId)

    def _toggle_date_time_frame(self, event=None):
        """Hide/show the 'Date/Time' frame."""
        if prefs['show_date_time']:
            self._dateTimeFrame.hide()
            prefs['show_date_time'] = False
        else:
            self._dateTimeFrame.show()
            prefs['show_date_time'] = True

    def _toggle_plot_frame(self, event=None):
        """Hide/show the 'Plot' frame."""
        if prefs['show_plot']:
            self._plotFrame.hide()
            prefs['show_plot'] = False
        else:
            self._plotFrame.show()
            prefs['show_plot'] = True

    def _toggle_relation_frame(self, event=None):
        """Hide/show the 'Relationships' frame."""
        if prefs['show_relationships']:
            self._relationFrame.hide()
            prefs['show_relationships'] = False
        else:
            self._relationFrame.show()
            prefs['show_relationships'] = True

    def _toggle_scene_frame(self, event=None):
        """Hide/show the 'Scene' frame."""
        if prefs['show_scene']:
            self._sceneFrame.hide()
            prefs['show_scene'] = False
        else:
            self._sceneFrame.show()
            prefs['show_scene'] = True


"""Provide a tkinter based class for viewing and editing all section properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.element_view import ElementView
from nvlib.gui.widgets.collection_box import CollectionBox
from nvlib.gui.widgets.folding_frame import FoldingFrame
from nvlib.gui.widgets.label_combo import LabelCombo
from nvlib.gui.widgets.label_entry import LabelEntry
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.gui.widgets.text_box import TextBox
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import list_to_string
from nvlib.novx_globals import string_to_list
from nvlib.nv_globals import NOT_ASSIGNED
from nvlib.nv_globals import get_duration_str
from nvlib.nv_globals import get_locale_date_str
from nvlib.nv_globals import get_section_date_str
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class SectionView(ElementView):
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
    _HELP_PAGE = 'section_view.html'
    _HEIGHT_LIMIT = 10
    _DT_LABEL_WIDTH = 15

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- 'Tags' entry.
        self._tagsVar = MyStringVar()
        self._tagsEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('Tags'),
            textvariable=self._tagsVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._tagsEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._tagsEntry)

        #--- Frame for section specific properties.
        self._sectionExtraFrame = ttk.Frame(self._elementInfoWindow)
        self._sectionExtraFrame.pack(anchor='w', fill='x')

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal'
        ).pack(fill='x')

        #--- Frame for 'Relationships'.
        # updating the character list before the viewpoints
        self._relationFrame = FoldingFrame(
            self._elementInfoWindow,
            _('Relationships'),
            self._toggle_relation_frame,
        )

        # Relationships preview.
        self._relationsPreviewVar = MyStringVar()
        relationsPreview = ttk.Label(
            self._relationFrame.titleBar,
            textvariable=self._relationsPreviewVar,
        )
        relationsPreview.pack(side='left', padx=2)
        relationsPreview.bind('<Button-1>', self._toggle_relation_frame)

        # 'Characters' listbox.
        self._crTitles = ''
        crHeading = ttk.Frame(self._relationFrame)
        self._characterLabel = ttk.Label(crHeading, text=_('Characters'))
        self._characterLabel.pack(anchor='w', side='left')
        ttk.Button(
            crHeading,
            text=_('Show ages'),
            command=self.show_ages,
        ).pack(anchor='e')
        crHeading.pack(fill='x')
        self._characterCollection = CollectionBox(
            self._relationFrame,
            cmdAdd=self.pick_character,
            cmdRemove=self.remove_character,
            cmdOpen=self.go_to_character,
            cmdActivate=self._activate_character_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
        )
        self._characterCollection.pack(fill='x')
        inputWidgets.extend(self._characterCollection.inputWidgets)

        # 'Locations' listbox.
        self._lcTitles = ''
        self._locationLabel = ttk.Label(
            self._relationFrame,
            text=_('Locations')
        )
        self._locationLabel.pack(anchor='w')
        self._locationCollection = CollectionBox(
            self._relationFrame,
            cmdAdd=self.pick_location,
            cmdRemove=self.remove_location,
            cmdOpen=self.go_to_location,
            cmdActivate=self._activate_location_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
        )
        self._locationCollection.pack(fill='x')
        inputWidgets.extend(self._locationCollection.inputWidgets)

        # 'Items' listbox.
        self._itTitles = ''
        self._itemLabel = ttk.Label(self._relationFrame, text=_('Items'))
        self._itemLabel.pack(anchor='w')
        self._itemCollection = CollectionBox(
            self._relationFrame,
            cmdAdd=self.pick_item,
            cmdRemove=self.remove_item,
            cmdOpen=self.go_to_item,
            cmdActivate=self._activate_item_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
        )
        self._itemCollection.pack(fill='x')
        inputWidgets.extend(self._itemCollection.inputWidgets)

        self._prefsShowLinks = 'show_sc_links'

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal'
        ).pack(fill='x')

        #--- Frame for date/time/duration.
        self._dateTimeFrame = FoldingFrame(
            self._elementInfoWindow,
            _('Date/Time'),
            self._toggle_date_time_frame,
        )

        # Preview start date.
        self._datePreviewVar = MyStringVar()
        datePreview = ttk.Label(
            self._dateTimeFrame.titleBar,
            textvariable=self._datePreviewVar,
        )
        datePreview.pack(side='left', padx=2)
        datePreview.bind('<Button-1>', self._toggle_date_time_frame)

        sectionStartFrame = ttk.Frame(self._dateTimeFrame)
        sectionStartFrame.pack(fill='x')

        # Frame for localized date/time display.
        displayDateFrame = ttk.Frame(sectionStartFrame)
        displayDateFrame.pack(fill='x')
        ttk.Label(
            displayDateFrame,
            text=_('Start'),
            width=self._DT_LABEL_WIDTH,
        ).pack(side='left')

        # Display date.
        self._displayDateVar = MyStringVar()
        displayDate = ttk.Label(
            displayDateFrame,
            textvariable=self._displayDateVar,
        )
        displayDate.pack(side='left')

        # 'Moon phase' button.
        ttk.Button(
            displayDateFrame,
            text=_('Moon phase'),
            command=self.show_moonphase,
        ).pack(anchor='e')

        # 'Start date' entry.
        self._startDateVar = MyStringVar()
        self._startDateEntry = LabelEntry(
            sectionStartFrame,
            text=_('Date'),
            textvariable=self._startDateVar,
            command=self.apply_changes,
            lblWidth=self._DT_LABEL_WIDTH,
        )
        self._startDateEntry.pack(anchor='w')
        inputWidgets.append(self._startDateEntry)

        # 'Start time' entry.
        self._startTimeVar = MyStringVar()
        self._startTimeEntry = LabelEntry(
            sectionStartFrame,
            text=_('Time'),
            textvariable=self._startTimeVar,
            command=self.apply_changes,
            lblWidth=self._DT_LABEL_WIDTH,
        )
        self._startTimeEntry.pack(anchor='w')
        inputWidgets.append(self._startTimeEntry)

        # 'Start day' entry.
        self._startDayVar = MyStringVar()
        self._startDayEntry = LabelEntry(
            sectionStartFrame,
            text=_('Day'),
            textvariable=self._startDayVar,
            command=self.apply_changes,
            lblWidth=self._DT_LABEL_WIDTH,
        )
        self._startDayEntry.pack(anchor='w')
        inputWidgets.append(self._startDayEntry)
        self._startDayEntry.entry.bind('<Return>', self.change_day)

        # 'Clear date/time' button.
        self._clearDateButton = ttk.Button(
            sectionStartFrame,
            text=_('Clear date/time'),
            command=self.clear_start,
        )
        self._clearDateButton.pack(
            side='left',
            fill='x',
            expand=True,
            padx=1,
            pady=2,
            )
        inputWidgets.append(self._clearDateButton)

        # 'Generate' button.
        self._generateDateButton = ttk.Button(
            sectionStartFrame,
            text=_('Generate'),
            command=self.auto_set_date,
        )
        self._generateDateButton.pack(
            side='left',
            fill='x',
            expand=True,
            padx=1,
            pady=2,
        )
        inputWidgets.append(self._generateDateButton)

        # 'Toggle date' button.
        self._toggleDateButton = ttk.Button(
            sectionStartFrame,
            text=_('Convert date/day'),
            command=self.toggle_date,
        )
        self._toggleDateButton.pack(
            side='left',
            fill='x',
            expand=True,
            padx=1,
            pady=2,
        )
        inputWidgets.append(self._toggleDateButton)

        ttk.Separator(
            self._dateTimeFrame,
            orient='horizontal'
        ).pack(fill='x', pady=2)

        sectionDurationFrame = ttk.Frame(self._dateTimeFrame)
        sectionDurationFrame.pack(fill='x')

        displayDurationFrame = ttk.Frame(sectionDurationFrame)
        displayDurationFrame.pack(fill='x')
        ttk.Label(
            displayDurationFrame,
            text=_('Duration'),
            width=self._DT_LABEL_WIDTH,
        ).pack(side='left')

        # Display duration.
        self.displayDurationVar = MyStringVar()
        displayDuration = ttk.Label(
            displayDurationFrame,
            textvariable=self.displayDurationVar,
        )
        displayDuration.pack(side='left', padx=2)

        # 'Duration days' entry.
        self._lastsDaysVar = MyStringVar()
        self._lastsDaysEntry = LabelEntry(
            sectionDurationFrame,
            text=_('Days'),
            textvariable=self._lastsDaysVar,
            command=self.apply_changes,
            lblWidth=self._DT_LABEL_WIDTH,
        )
        self._lastsDaysEntry.pack(anchor='w')
        inputWidgets.append(self._lastsDaysEntry)

        # 'Duration hours' entry.
        self._lastsHoursVar = MyStringVar()
        self._lastsHoursEntry = LabelEntry(
            sectionDurationFrame,
            text=_('Hours'),
            textvariable=self._lastsHoursVar,
            command=self.apply_changes,
            lblWidth=self._DT_LABEL_WIDTH,
        )
        self._lastsHoursEntry.pack(anchor='w')
        inputWidgets.append(self._lastsHoursEntry)

        # 'Duration minutes' entry.
        self._lastsMinutesVar = MyStringVar()
        self._lastsMinutesEntry = LabelEntry(
            sectionDurationFrame,
            text=_('Minutes'),
            textvariable=self._lastsMinutesVar,
            command=self.apply_changes,
            lblWidth=self._DT_LABEL_WIDTH,
        )
        self._lastsMinutesEntry.pack(anchor='w')
        inputWidgets.append(self._lastsMinutesEntry)

        # 'Clear duration' button.
        self._clearDurationButton = ttk.Button(
            sectionDurationFrame,
            text=_('Clear duration'),
            command=self.clear_duration,
        )
        self._clearDurationButton.pack(side='left', padx=1, pady=2)
        inputWidgets.append(self._clearDurationButton)

        # 'Generate' button.
        self._generatDurationButton = ttk.Button(
            sectionDurationFrame,
            text=_('Generate'),
            command=self.auto_set_duration,
        )
        self._generatDurationButton.pack(side='left', padx=1, pady=2)
        inputWidgets.append(self._generatDurationButton)

        #--- 'Viewpoint' combobox.
        self._viewpointVar = MyStringVar()
        self._characterCombobox = LabelCombo(
            self._sectionExtraFrame,
            text=_('Viewpoint'),
            textvariable=self._viewpointVar,
            values=[],
            lblWidth=self._LABEL_WIDTH,
        )
        self._characterCombobox.pack(anchor='w', pady=2)
        inputWidgets.append(self._characterCombobox)
        self._characterCombobox.combo.bind(
            '<<ComboboxSelected>>', self.apply_changes)
        self._vpIdList = []

        #--- 'Unused' checkbox.
        self._isUnusedVar = tk.BooleanVar()
        self._isUnusedCheckbox = ttk.Checkbutton(
            self._sectionExtraFrame,
            text=_('Unused'),
            variable=self._isUnusedVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._isUnusedCheckbox.pack(anchor='w')
        inputWidgets.append(self._isUnusedCheckbox)

        #--- 'Append to previous section' checkbox.
        self._appendToPrevVar = tk.BooleanVar()
        self._appendToPrevCheckbox = ttk.Checkbutton(
            self._sectionExtraFrame,
            text=_('Append to previous section'),
            variable=self._appendToPrevVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._appendToPrevCheckbox.pack(anchor='w')
        inputWidgets.append(self._appendToPrevCheckbox)

        ttk.Separator(
            self._sectionExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for 'Plot'.
        self._plotFrame = FoldingFrame(
            self._sectionExtraFrame,
            _('Plot'),
            self._toggle_plot_frame,
        )

        # Plot lines preview.
        self._plotPreviewVar = MyStringVar()
        plotlinesPreview = ttk.Label(
            self._plotFrame.titleBar,
            textvariable=self._plotPreviewVar,
        )
        plotlinesPreview.pack(side='left', padx=2)
        plotlinesPreview.bind('<Button-1>', self._toggle_plot_frame)

        # 'Plot lines' listbox.
        self._plotlineTitles = ''
        self._plotlineLabel = ttk.Label(self._plotFrame, text=_('Plot lines'))
        self._plotlineLabel.pack(anchor='w')
        self._plotlineCollection = CollectionBox(
            self._plotFrame,
            cmdAdd=self.pick_plotline,
            cmdRemove=self.remove_plotline,
            cmdOpen=self.go_to_plotline,
            cmdActivate=self._activate_plotline_buttons,
            cmdSelect=self.on_select_plotline,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon,
            bg=prefs['color_text_bg'],
            fg=prefs['color_text_fg'],
        )
        self._plotlineCollection.pack(fill='x')
        inputWidgets.extend(self._plotlineCollection.inputWidgets)
        self.selectedPlotline = None

        # 'Plot line notes' text box for entering element.plotlineNotes[plId],
        #  where plId is the ID of the selected plot line
        #  in the'Plot lines' listbox.
        ttk.Label(
            self._plotFrame,
            text=_('Notes on the selected plot line'),
        ).pack(anchor='w')
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
        self._plotPointsDisplay = tk.Label(
            self._plotFrame,
            anchor='w',
            bg='white',
        )
        self._plotPointsDisplay.pack(anchor='w', fill='x')

        ttk.Separator(
            self._sectionExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for 'Scene'.
        self._sceneFrame = FoldingFrame(
            self._sectionExtraFrame,
            _('Scene'),
            self._toggle_scene_frame,
        )

        # Kind of scene preview.
        self._scenePreviewVar = MyStringVar()
        scenePreview = ttk.Label(
            self._sceneFrame.titleBar,
            textvariable=self._scenePreviewVar,
        )
        scenePreview.pack(side='left', padx=2)
        scenePreview.bind('<Button-1>', self._toggle_scene_frame)

        # Scene radiobuttons.
        selectionFrame = ttk.Frame(self._sceneFrame)
        self._noSceneField1Var = ''
        self._noSceneField2Var = ''
        self._noSceneField3Var = ''
        self._otherSceneField1Var = ''
        self._otherSceneField2Var = ''
        self._otherSceneField3Var = ''
        self.sceneVar = tk.IntVar()

        self._kindsOfScene = [
            _('Not a scene'),
            _('Action'),
            _('Reaction'),
            _('Other'),
        ]
        sceneChoice = 0
        self._notApplicableRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=self._kindsOfScene[sceneChoice],
            variable=self.sceneVar,
            value=sceneChoice,
            command=self.set_not_applicable,
        )
        self._notApplicableRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._notApplicableRadiobutton)

        sceneChoice += 1
        self._actionRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=self._kindsOfScene[sceneChoice],
            variable=self.sceneVar,
            value=sceneChoice,
            command=self.set_action_scene,
        )
        self._actionRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._actionRadiobutton)

        sceneChoice += 1
        self._reactionRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=self._kindsOfScene[sceneChoice],
            variable=self.sceneVar,
            value=sceneChoice,
            command=self.set_reaction_scene,
        )
        self._reactionRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._reactionRadiobutton)

        sceneChoice += 1
        self._customRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=self._kindsOfScene[sceneChoice],
            variable=self.sceneVar,
            value=sceneChoice,
            command=self.set_custom_scene,
        )
        self._customRadiobutton.pack(anchor='w')
        inputWidgets.append(self._customRadiobutton)

        selectionFrame.pack(fill='x')

        # 'Goal/Reaction' window. The labels are configured dynamically.
        self._goalLabel = ttk.Label(self._sceneFrame)
        self._goalLabel.pack(anchor='w')
        self._goalBox = TextBox(
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
        self._goalBox.pack(fill='x')
        inputWidgets.append(self._goalBox)

        # 'Conflict/Dilemma' window. The labels are configured dynamically.
        self._conflictLabel = ttk.Label(self._sceneFrame)
        self._conflictLabel.pack(anchor='w')
        self._conflictBox = TextBox(
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
        self._conflictBox.pack(fill='x')
        inputWidgets.append(self._conflictBox)

        # 'Outcome/Choice' window. The labels are configured dynamically.
        self._outcomeLabel = ttk.Label(self._sceneFrame)
        self._outcomeLabel.pack(anchor='w')
        self._outcomeBox = TextBox(
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
        self._outcomeBox.pack(fill='x')
        inputWidgets.append(self._outcomeBox)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        super().apply_changes()

        #--- Section start.

        # 'Tags' entry.
        self.element.tags = string_to_list(self._tagsVar.get())

        # Date and time are checked separately.
        # If an invalid date is entered, the old value is kept.
        # If an invalid time is entered, the old value is kept.
        # If a valid date is entered, the day is cleared, if any.
        # Otherwise, if a valid day is entered, the date is cleared, if any.

        # 'Date' entry.
        dateStr = self._startDateVar.get()
        if not dateStr:
            self.element.date = None
        elif dateStr != self.element.date:
            try:
                dateStr = PyCalendar.verified_date(dateStr)
            except ValueError:
                self._startDateVar.set(self.element.date)
                self._ui.show_error(
                    message=_('Input rejected'),
                    detail=(
                        f'{_("Wrong date")}: '
                        f'"{dateStr}"\n{_("Required")}: '
                        f'{PyCalendar.DATE_FORMAT}'
                    ),
                )
            else:
                self.element.date = dateStr

        # 'Time' entry.
        timeStr = self._startTimeVar.get()
        if not timeStr:
            self.element.time = None
        else:
            if self.element.time:
                dispTime = PyCalendar.display_time(self.element.time)
            else:
                dispTime = ''
            if timeStr != dispTime:
                try:
                    timeStr = PyCalendar.verified_time(timeStr)
                except ValueError:
                    self._startTimeVar.set(dispTime)
                    self._ui.show_error(
                        message=_('Input rejected'),
                        detail=(
                            f'{_("Wrong time")}: '
                            f'"{timeStr}"\n{_("Required")}: '
                            f'{PyCalendar.TIME_FORMAT}'
                        ),
                    )
                else:
                    self.element.time = timeStr
                    dispTime = PyCalendar.display_time(self.element.time)
                    self._startTimeVar.set(dispTime)

        # 'Day' entry.
        if self.element.date:
            self.element.day = None
        else:
            self.change_day()

        #--- Section duration.
        # Section duration changes are applied as a whole.
        # That is, days, hours and minutes entries
        # must all be correct numbers.
        # Otherwise, the old values are kept.
        # If more than 60 minutes are entered in the "Minutes" field,
        # the hours are incremented accordingly.
        # If more than 24 hours are entered in the "Hours" field,
        # the days are incremented accordingly.
        wrongEntry = False
        newEntry = False

        # 'Duration minutes' entry.
        hoursLeft = 0
        lastsMinutesStr = self._lastsMinutesVar.get()
        if lastsMinutesStr or self.element.lastsMinutes:
            if lastsMinutesStr != self.element.lastsMinutes:
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
                    self._lastsMinutesVar.set(lastsMinutesStr)
                    newEntry = True

        # 'Duration hours' entry.
        daysLeft = 0
        lastsHoursStr = self._lastsHoursVar.get()
        if hoursLeft or lastsHoursStr or self.element.lastsHours:
            if hoursLeft or lastsHoursStr != self.element.lastsHours:
                try:
                    if lastsHoursStr:
                        hoursLeft += int(lastsHoursStr)
                    daysLeft, hoursLeft = divmod(hoursLeft, 24)
                    if hoursLeft > 0:
                        lastsHoursStr = str(hoursLeft)
                    else:
                        lastsHoursStr = None
                    self._lastsHoursVar.set(lastsHoursStr)
                except ValueError:
                    wrongEntry = True
                else:
                    newEntry = True

        # 'Duration days' entry.
        lastsDaysStr = self._lastsDaysVar.get()
        if daysLeft or lastsDaysStr or self.element.lastsDays:
            if daysLeft or lastsDaysStr != self.element.lastsDays:
                try:
                    if lastsDaysStr:
                        daysLeft += int(lastsDaysStr)
                    if daysLeft > 0:
                        lastsDaysStr = str(daysLeft)
                    else:
                        lastsDaysStr = None
                    self._lastsDaysVar.set(lastsDaysStr)
                except ValueError:
                    wrongEntry = True
                else:
                    newEntry = True

        if wrongEntry:
            self._lastsMinutesVar.set(self.element.lastsMinutes)
            self._lastsHoursVar.set(self.element.lastsHours)
            self._lastsDaysVar.set(self.element.lastsDays)
            self._ui.show_error(
                message=_('Input rejected'),
                detail=f'{_("Wrong entry: number required")}.'
            )
        elif newEntry:
            self.element.lastsMinutes = lastsMinutesStr
            self.element.lastsHours = lastsHoursStr
            self.element.lastsDays = lastsDaysStr

        #--- 'Viewpoint' combobox.
        option = self._characterCombobox.current()
        if option >= 0:
            # Put the selected character at the first position
            # of related characters.
            vpId = self._vpIdList[option]
            self.element.viewpoint = vpId

        #--- 'Unused' checkbox.
        if self._isUnusedVar.get():
            self._ctrl.set_type_unused()
        else:
            self._ctrl.set_type_normal()
        if self.element.scType > 0:
            self._isUnusedVar.set(True)
            # adjustment for section in an unused chapter

        #--- 'Append to previous section' checkbox.
        self.element.appendToPrev = self._appendToPrevVar.get()

        #--- 'Plot line notes' text box.
        self.save_plot_notes()

        #--- 'Goal/Reaction' window.
        if self._goalBox.hasChanged:
            self.element.goal = self._goalBox.get_text()
        #--- 'Conflict/Dilemma' window.
        if self._conflictBox.hasChanged:
            self.element.conflict = self._conflictBox.get_text()

        #--- 'Outcome/Choice' window.
        if self._outcomeBox.hasChanged:
            self.element.outcome = self._outcomeBox.get_text()

    def auto_set_date(self):
        """Set section start to the end of the previous section."""
        prevScId = self._ui.tv.prev_node(self.elementId)
        if not prevScId:
            self._ui.show_error(
                message=_('Cannot generate date/time'),
                detail=f"{_('There is no previous section')}."
            )
            return

        (
            newDate,
            newTime,
            newDay
        ) = self._mdl.novel.sections[prevScId].get_end_date_time()
        if newTime is None:
            self._ui.show_error(
                message=_('Cannot generate date/time'),
                detail=f"{_('The previous section has no time set')}."
            )
            return

        # self._doNotUpdate = True
        self.element.date = newDate
        self.element.time = newTime
        self.element.day = newDay
        # self._doNotUpdate = False
        self._startDateVar.set(newDate)
        self._startTimeVar.set(PyCalendar.display_time(newTime))
        self._startDayVar.set(newDay)

    def auto_set_duration(self):
        """Calculate section duration from the start of the next section."""

        nextScId = self._ui.tv.next_node(self.elementId)
        if not nextScId:
            self._ui.show_error(
                message=_('Cannot generate duration'),
                detail=f"{_('There is no next section')}."
            )
            return

        thisTimeIso = self.element.time
        if not thisTimeIso:
            self._ui.show_error(
                message=_('Cannot generate duration'),
                detail=f"{_('This section has no time set')}."
            )
            return

        nextTimeIso = self._mdl.novel.sections[nextScId].time
        if not nextTimeIso:
            self._ui.show_error(
                message=_('Cannot generate duration'),
                detail=f"{_('The next section has no time set')}."
            )
            return

        refDateIso = self._mdl.novel.referenceDate
        if not refDateIso:
            refDateIso = PyCalendar.min
        if self._mdl.novel.sections[nextScId].date:
            nextDateIso = self._mdl.novel.sections[nextScId].date
        elif self._mdl.novel.sections[nextScId].day:
            nextDateIso = PyCalendar.specific_date(
                self._mdl.novel.sections[nextScId].day, refDateIso,)
        elif self.element.day:
            nextDateIso = self.element.day
        else:
            nextDateIso = None

        if self.element.date:
            thisDateIso = self.element.date
            if nextDateIso is None:
                nextDateIso = thisDateIso
        elif self.element.day:
            thisDateIso = PyCalendar.specific_date(
                self.element.day, refDateIso)
            if nextDateIso is None:
                nextDateIso = thisDateIso
        else:
            if nextDateIso is not None:
                thisDateIso = nextDateIso
            else:
                nextDateIso = thisDateIso = PyCalendar.min
        newDays, newHours, newMinutes = PyCalendar.duration(
            thisDateIso,
            thisTimeIso,
            nextDateIso,
            nextTimeIso,
        )
        self._doNotUpdate = True
        self.element.lastsDays = newDays
        self.element.lastsHours = newHours
        self.element.lastsMinutes = newMinutes
        self._doNotUpdate = False
        self._lastsDaysVar.set(newDays)
        self._lastsHoursVar.set(newHours)
        self._lastsMinutesVar.set(newMinutes)

    def change_day(self, event=None):
        # 'Day' entry. If valid, clear the start date.
        dayStr = self._startDayVar.get()
        if dayStr or self.element.day:
            if dayStr != self.element.day:
                if not dayStr:
                    self.element.day = None
                else:
                    try:
                        int(dayStr)
                    except ValueError:
                        self._startDayVar.set(self.element.day)
                        self._ui.show_error(
                            message=_('Input rejected'),
                            detail=f'{_("Wrong entry: number required")}.'
                        )
                    else:
                        self.element.day = dayStr
                        self.element.date = None

    def clear_duration(self):
        """Remove duration data from the section."""
        durationData = [
            self.element.lastsDays,
            self.element.lastsHours,
            self.element.lastsMinutes,
            ]
        hasData = False
        for dataElement in durationData:
            if dataElement:
                hasData = True
        if hasData and self._ui.ask_yes_no(
            message=_('Clear duration from this section?')
        ):
            self.element.lastsDays = None
            self.element.lastsHours = None
            self.element.lastsMinutes = None

    def clear_start(self):
        """Remove start data from the section."""
        startData = [
            self.element.date,
            self.element.time,
            self.element.day,
            ]
        hasData = False
        for dataElement in startData:
            if dataElement:
                hasData = True
        if hasData and self._ui.ask_yes_no(
            message=_('Clear date/time from this section?')
        ):
            self.element.date = None
            self.element.time = None
            self.element.day = None

    def configure_display(self):
        """Expand or collapse the property frames."""
        super().configure_display()

        #--- Frame for 'Relationships'.
        if prefs['show_relationships']:
            self._relationFrame.show()
            self._relationsPreviewVar.set('')
        else:
            self._relationFrame.hide()
            relationsPreview = []
            relationCounts = {
                _('Characters'): len(self.element.characters),
                _('Locations'):len(self.element.locations),
                _('Items'):len(self.element.items),
            }
            for elementType in relationCounts:
                if relationCounts[elementType]:
                    relationsPreview.append(
                        f"{elementType}: {relationCounts[elementType]}"
                    )
            self._relationsPreviewVar.set(
                list_to_string(relationsPreview, divider=', ')
            )

        #--- Frame for date/time/duration.
        dispDateTime = []
        if self.element.date and self.element.weekDay is not None:
            dispDateTime.append(
                PyCalendar.WEEKDAYS[self.element.weekDay])
        elif (
            self.element.day
            and self._mdl.novel.referenceWeekDay is not None
        ):
            wd = (int(self.element.day) + self._mdl.novel.referenceWeekDay) % 7
            dispDateTime.append(PyCalendar.WEEKDAYS[wd])
        self._startDateVar.set(self.element.date)
        if self.element.localeDate:
            dispDateTime.append(get_section_date_str(self.element))
        elif self.element.day:
            dispDateTime.append(f'{_("Day")} {self.element.day}')

        # Remove the seconds for the display.
        if self.element.time:
            dispDateTime.append(PyCalendar.display_time(self.element.time))

        if prefs['show_date_time']:
            self._dateTimeFrame.show()
            self._displayDateVar.set(
                list_to_string(dispDateTime, divider=' ')
            )
            self._datePreviewVar.set('')
            self.displayDurationVar.set(
                get_duration_str(self.element))
        else:
            self._dateTimeFrame.hide()
            self._datePreviewVar.set(
                list_to_string(dispDateTime, divider=' ')
            )

        #--- Frame for 'Plot'.
        if prefs['show_plot']:
            self._plotFrame.show()
            self._plotPreviewVar.set('')
        else:
            self._plotFrame.hide()
            plotPreview = []
            plotCounts = {
                _('Plot lines'): len(self.element.scPlotLines),
                _('Plot points'):len(self.element.scPlotPoints),
            }
            for elementType in plotCounts:
                if plotCounts[elementType]:
                    plotPreview.append(
                        f"{elementType}: {plotCounts[elementType]}"
                    )
            self._plotPreviewVar.set(
                list_to_string(plotPreview, divider=', '))

        #--- Frame for 'Scene'.
        if prefs['show_scene']:
            self._sceneFrame.show()
            self._scenePreviewVar.set('')
        else:
            self._sceneFrame.hide()
            if (self.element.scene
                or self.element.goal
                or self.element.conflict
                or self.element.outcome
            ):
                self._scenePreviewVar.set(
                    self._kindsOfScene[self.element.scene])
            else:
                self._scenePreviewVar.set('')

    def go_to_character(self, event=None):
        """Go to the character selected in the listbox."""
        try:
            selection = self._characterCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.characters[selection])

    def go_to_item(self, event=None):
        """Go to the item selected in the listbox."""
        try:
            selection = self._itemCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.items[selection])

    def go_to_location(self, event=None):
        """Go to the location selected in the listbox."""
        try:
            selection = self._locationCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.locations[selection])

    def go_to_plotline(self, event=None):
        """Go to the plot line selected in the listbox."""
        try:
            selection = self._plotlineCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.scPlotLines[selection])

    def on_select_plotline(self, selection):
        """Callback routine for section plot line list selection."""
        self.save_plot_notes()
        self.selectedPlotline = self.element.scPlotLines[selection]
        self._plotNotesWindow.config(state='normal')
        if self.element.plotlineNotes:
            self._plotNotesWindow.set_text(
                self.element.plotlineNotes.get(self.selectedPlotline, '')
            )
        else:
            self._plotNotesWindow.clear()
        if self._isLocked:
            self._plotNotesWindow.config(state='disabled')
        self._plotNotesWindow.config(bg='white')

    def pick_character(self, event=None):
        """Enter the "add character" selection mode."""
        self._ui.tv.save_branch_status()
        self._ui.tv.close_children('')
        self._ui.tv.open_children(CR_ROOT)
        self._start_picking_mode(command=self._add_character)
        self._ui.tv.see_node(CR_ROOT)

    def pick_item(self, event=None):
        """Enter the "add item" selection mode."""
        self._ui.tv.save_branch_status()
        self._ui.tv.close_children('')
        self._ui.tv.open_children(IT_ROOT)
        self._start_picking_mode(command=self._add_item)
        self._ui.tv.see_node(IT_ROOT)

    def pick_location(self, event=None):
        """Enter the "add location" selection mode."""
        self._ui.tv.save_branch_status()
        self._ui.tv.close_children('')
        self._ui.tv.open_children(LC_ROOT)
        self._start_picking_mode(command=self._add_location)
        self._ui.tv.see_node(LC_ROOT)

    def pick_plotline(self, event=None):
        """Enter the "add plot line" selection mode."""
        self._ui.tv.save_branch_status()
        self._ui.tv.close_children('')
        self._ui.tv.open_children(PL_ROOT)
        self._start_picking_mode(command=self._add_plotline)
        self._ui.tv.see_node(PL_ROOT)

    def remove_character(self, event=None):
        """Remove the character selected in the listbox 
        from the section characters."""
        try:
            selection = self._characterCollection.cListbox.curselection()[0]
        except:
            return

        crId = self.element.characters[selection]
        if self._ui.ask_yes_no(
            message=_('Remove character from the list?'),
            detail=self._mdl.novel.characters[crId].title
        ):
            crList = self.element.characters
            del crList[selection]
            self.element.characters = crList

    def remove_item(self, event=None):
        """Remove the item selected in the listbox from the section items."""
        try:
            selection = self._itemCollection.cListbox.curselection()[0]
        except:
            return

        itId = self.element.items[selection]
        if self._ui.ask_yes_no(
            message=_('Remove item from the list?'),
            detail=self._mdl.novel.items[itId].title
        ):
            itList = self.element.items
            del itList[selection]
            self.element.items = itList

    def remove_location(self, event=None):
        """Remove the location selected in the listbox 
        from the section locations."""
        try:
            selection = self._locationCollection.cListbox.curselection()[0]
        except:
            return

        lcId = self.element.locations[selection]
        if self._ui.ask_yes_no(
            message=_('Remove location from the list?'),
            detail=self._mdl.novel.locations[lcId].title
        ):
            lcList = self.element.locations
            del lcList[selection]
            self.element.locations = lcList

    def remove_plotline(self, event=None):
        """Remove the plot line selected in the listbox 
        from the section associations."""
        try:
            selection = self._plotlineCollection.cListbox.curselection()[0]
        except:
            return

        plId = self.element.scPlotLines[selection]
        if not self._ui.ask_yes_no(
            message=_('Remove plot line from the list?'),
            detail=(
                f"({self._mdl.novel.plotLines[plId].shortName}) "
                f"{self._mdl.novel.plotLines[plId].title}"
            )
        ):
            return

        # Remove the plot line from the section's list.
        arcList = self.element.scPlotLines
        del arcList[selection]
        self.element.scPlotLines = arcList

        # Remove the section from the plot line's list.
        arcSections = self._mdl.novel.plotLines[plId].sections
        if self.elementId in arcSections:
            arcSections.remove(self.elementId)
            self._mdl.novel.plotLines[plId].sections = arcSections

            # Remove plot point assignments, if any.
            for ppId in list(self.element.scPlotPoints):
                if self.element.scPlotPoints[ppId] == plId:
                    del(self.element.scPlotPoints[ppId])
                    # removing the plot line's plot point
                    # from the section's list
                    # Note: this doesn't trigger the refreshing method
                    self._mdl.novel.plotPoints[ppId].sectionAssoc = None
                    # un-assigning the section from the plot line's plot point

    def save_plot_notes(self):
        if self.selectedPlotline and self._plotNotesWindow.hasChanged:
            plotlineNotes = self.element.plotlineNotes
            if plotlineNotes is None:
                plotlineNotes = {}
            plotlineNotes[self.selectedPlotline] = (
                self._plotNotesWindow.get_text()
            )
            self._doNotUpdate = True
            self.element.plotlineNotes = plotlineNotes
            self._doNotUpdate = False

    def set_action_scene(self, event=None):
        self._goalLabel.config(text=_('Goal'))
        self._conflictLabel.config(text=_('Conflict'))
        self._outcomeLabel.config(text=_('Outcome'))
        self.element.scene = self.sceneVar.get()

    def set_custom_scene(self, event=None):
        if self._otherSceneField1Var:
            self._goalLabel.config(text=self._otherSceneField1Var)
        else:
            self._goalLabel.config(text=f"{_('Field')} 1")

        if self._otherSceneField2Var:
            self._conflictLabel.config(text=self._otherSceneField2Var)
        else:
            self._conflictLabel.config(text=f"{_('Field')} 2")

        if self._otherSceneField3Var:
            self._outcomeLabel.config(text=self._otherSceneField3Var)
        else:
            self._outcomeLabel.config(text=f"{_('Field')} 3")

        self.element.scene = self.sceneVar.get()

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.sections[elementId]
        super().set_data(elementId)

        # 'Tags' entry.
        self._tagsVar.set(list_to_string(self.element.tags))

        #--- Frame for 'Relationships'.

        # 'Characters' window.
        self._crTitles = self._get_element_titles(
            self.element.characters, self._mdl.novel.characters
        )
        self._characterCollection.cList.set(self._crTitles)
        listboxSize = len(self._crTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._characterCollection.cListbox.config(height=listboxSize)
        if (not self._characterCollection.cListbox.curselection()
            or not self._characterCollection.cListbox.focus_get()
        ):
            self._characterCollection.disable_buttons()

        # 'Locations' window.
        self._lcTitles = self._get_element_titles(
            self.element.locations, self._mdl.novel.locations
        )
        self._locationCollection.cList.set(self._lcTitles)
        listboxSize = len(self._lcTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._locationCollection.cListbox.config(height=listboxSize)
        if (not self._locationCollection.cListbox.curselection()
            or not self._locationCollection.cListbox.focus_get()
        ):
            self._locationCollection.disable_buttons()

        # 'Items' window.
        self._itTitles = self._get_element_titles(
            self.element.items, self._mdl.novel.items
        )
        self._itemCollection.cList.set(self._itTitles)
        listboxSize = len(self._itTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._itemCollection.cListbox.config(height=listboxSize)
        if (not self._itemCollection.cListbox.curselection()
            or not self._itemCollection.cListbox.focus_get()
        ):
            self._itemCollection.disable_buttons()

        #--- Frame for date/time/duration.

        # Remove the seconds for the display.
        if self.element.time:
            self._startTimeVar.set(
                PyCalendar.display_time(self.element.time)
            )
        else:
            self._startTimeVar.set('')

        self._startDayVar.set(self.element.day)
        self._lastsDaysVar.set(self.element.lastsDays)
        self._lastsHoursVar.set(self.element.lastsHours)
        self._lastsMinutesVar.set(self.element.lastsMinutes)

        #--- 'Viewpoint' combobox.
        if self.element.viewpoint:
            charNames = [f"({_('Clear assignment')})"]
            preset = self._mdl.novel.characters[self.element.viewpoint].title
        else:
            charNames = [NOT_ASSIGNED]
            preset = NOT_ASSIGNED
        self._vpIdList = [None]
        for crId in self._mdl.novel.tree.get_children(CR_ROOT):
            charNames.append(self._mdl.novel.characters[crId].title)
            self._vpIdList.append(crId)
        self._characterCombobox.configure(values=charNames)
        self._viewpointVar.set(value=preset)

        #--- 'Unused' checkbox.
        if self.element.scType > 0:
            self._isUnusedVar.set(True)
        else:
            self._isUnusedVar.set(False)

        #--- 'Append to previous section' checkbox.
        self._appendToPrevVar.set(self.element.appendToPrev)

        # Customized Goal/Conflict/Outcome configuration.
        if self._mdl.novel.noSceneField1:
            self._noSceneField1Var = self._mdl.novel.noSceneField1
        else:
            self._noSceneField1Var = ''

        if self._mdl.novel.noSceneField2:
            self._noSceneField2Var = (
                self._mdl.novel.noSceneField2
            )
        else:
            self._noSceneField2Var = ''

        if self._mdl.novel.noSceneField3:
            self._noSceneField3Var = self._mdl.novel.noSceneField3
        else:
            self._noSceneField3Var = ''

        if self._mdl.novel.otherSceneField1:
            self._otherSceneField1Var = self._mdl.novel.otherSceneField1
        else:
            self._otherSceneField1Var = ''

        if self._mdl.novel.otherSceneField2:
            self._otherSceneField2Var = self._mdl.novel.otherSceneField2
        else:
            self._otherSceneField2Var = ''

        if self._mdl.novel.otherSceneField3:
            self._otherSceneField3Var = self._mdl.novel.otherSceneField3
        else:
            self._otherSceneField3Var = ''

        #--- Frame for 'Plot'.

        #  'Plot lines' listbox.
        self._plotlineTitles = self._get_plotline_titles(
            self.element.scPlotLines,
            self._mdl.novel.plotLines
        )
        self._plotlineCollection.cList.set(self._plotlineTitles)
        listboxSize = len(self._plotlineTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._plotlineCollection.cListbox.config(height=listboxSize)
        if (not self._plotlineCollection.cListbox.curselection()
            or not self._plotlineCollection.cListbox.focus_get()
        ):
            self._plotlineCollection.disable_buttons()

        # 'Plot notes' text box.
        self._plotNotesWindow.clear()
        self._plotNotesWindow.config(state='disabled')
        self._plotNotesWindow.config(bg='light gray')
        if self._plotlineTitles:
            self._plotlineCollection.cListbox.select_clear(0, 'end')
            self._plotlineCollection.cListbox.select_set('end')
            self.selectedPlotline = -1
            self.on_select_plotline(-1)
        else:
            self.selectedPlotline = None

        # "Plot points" label
        plotPointTitles = []
        for ppId in self.element.scPlotPoints:
            plId = self.element.scPlotPoints[ppId]
            plotPointTitles.append(
                (
                    f'{self._mdl.novel.plotLines[plId].shortName}: '
                    f'{self._mdl.novel.plotPoints[ppId].title}'
                )
            )
        self._plotPointsDisplay.config(text=list_to_string(plotPointTitles))

        #--- Frame for 'Scene'.

        # Scene radiobuttons.
        self.sceneVar.set(self.element.scene)

        # 'Goal/Reaction' window.
        self._goalBox.set_text(self.element.goal)

        # 'Conflict/Dilemma' window.
        self._conflictBox.set_text(self.element.conflict)

        # 'Outcome/Choice' window.
        self._outcomeBox.set_text(self.element.outcome)

        # Configure the labels.
        if self.element.scene == 3:
            self.set_custom_scene()
        elif self.element.scene == 2:
            self.set_reaction_scene()
        elif self.element.scene == 1:
            self.set_action_scene()
        else:
            self.set_not_applicable()

    def set_not_applicable(self, event=None):
        if self._noSceneField1Var:
            self._goalLabel.config(text=self._noSceneField1Var)
        else:
            self._goalLabel.config(text=f"{_('Field')} 1")

        if self._noSceneField2Var:
            self._conflictLabel.config(text=self._noSceneField2Var)
        else:
            self._conflictLabel.config(text=f"{_('Field')} 2")

        if self._noSceneField3Var:
            self._outcomeLabel.config(text=self._noSceneField3Var)
        else:
            self._outcomeLabel.config(text=f"{_('Field')} 3")

        self.element.scene = self.sceneVar.get()

    def set_reaction_scene(self, event=None):
        self._goalLabel.config(text=_('Reaction'))
        self._conflictLabel.config(text=_('Dilemma'))
        self._outcomeLabel.config(text=_('Choice'))
        self.element.scene = self.sceneVar.get()

    def show_ages(self, event=None):
        """Display the ages of the related characters."""
        if self.element.date is not None:
            now = self.element.date
        else:
            try:
                now = PyCalendar.specific_date(
                    self.element.day,
                    self._mdl.novel.referenceDate
                    )
            except Exception:
                self._report_missing_date()
                return

        charList = []
        for crId in self.element.characters:
            birthDate = self._mdl.novel.characters[crId].birthDate
            deathDate = self._mdl.novel.characters[crId].deathDate
            try:
                yearsOld, yearsDead, daysOld, daysDead = PyCalendar.age(
                    now,
                    birthDate,
                    deathDate
                )
                if yearsDead is not None:
                    if yearsDead:
                        time = yearsDead
                        suffix = _('years after death')
                    else:
                        time = daysDead
                        suffix = _('days after death')
                    if yearsOld:
                        suffix = f"{suffix} {_('at age')} {yearsOld}"

                elif yearsOld:
                    suffix = _('years old')
                    time = yearsOld
                else:
                    suffix = _('days old')
                    time = daysOld
                charList.append(
                    (
                        f'{self._mdl.novel.characters[crId].title}: '
                        f'{time} {suffix}'
                    )
                )
            except Exception:
                charList.append(
                    (
                        f'{self._mdl.novel.characters[crId].title}: '
                        f'({_("no data")})'
                    )
                )

        if charList:
            self._ui.show_info(
                message=f'{_("Date")}: {get_locale_date_str(now)}',
                detail='\n'.join(charList),
                title=_('Show ages')
            )

    def show_moonphase(self, event=None):
        """Display the moon phase of the section start date."""
        if self.element.date is not None:
            now = self.element.date
        else:
            try:
                now = PyCalendar.specific_date(
                    self.element.day,
                    self._mdl.novel.referenceDate
                )
            except:
                self._report_missing_date()
                return

        self._ui.show_info(
            message=f'{_("Date")}: {get_locale_date_str(now)}',
            detail=f'{self._mdl.nvService.get_moon_phase_str(now)}',
            title=_("Moon phase")
        )

    def toggle_date(self, event=None):
        """Toggle specific/unspecific date."""
        if not self._mdl.novel.referenceDate:
            self._report_missing_reference_date()
            return

        self._doNotUpdate = True
        if self.element.date:
            self.element.date_to_day(self._mdl.novel.referenceDate)
        elif self.element.day:
            self.element.day_to_date(self._mdl.novel.referenceDate)
        else:
            self._report_missing_date()
            return

        self._doNotUpdate = False
        self.set_data(self.elementId)

    def unlock(self):
        """Enable plot line notes only if a plot line is selected."""
        super().unlock()
        if self.selectedPlotline is None:
            self._plotNotesWindow.config(state='disabled')

    def _activate_plotline_buttons(self, event=None):
        if self.element.scPlotLines:
            self._plotlineCollection.enable_buttons()
        else:
            self._plotlineCollection.disable_buttons()

    def _activate_character_buttons(self, event=None):
        if self.element.characters:
            self._characterCollection.enable_buttons()
        else:
            self._characterCollection.disable_buttons()

    def _activate_item_buttons(self, event=None):
        if self.element.items:
            self._itemCollection.enable_buttons()
        else:
            self._itemCollection.disable_buttons()

    def _activate_location_buttons(self, event=None):
        if self.element.locations:
            self._locationCollection.enable_buttons()
        else:
            self._locationCollection.disable_buttons()

    def _add_character(self, event=None):
        # Add the selected element to the collection, if applicable.
        crList = self.element.characters
        crId = self._ui.tv.tree.selection()[0]
        if crId.startswith(CHARACTER_PREFIX) and not crId in crList:
            crList.append(crId)
            self.element.characters = crList
        self._ui.tv.restore_branch_status()

    def _add_item(self, event=None):
        # Add the selected element to the collection, if applicable.
        itList = self.element.items
        itId = self._ui.tv.tree.selection()[0]
        if itId.startswith(ITEM_PREFIX)and not itId in itList:
            itList.append(itId)
            self.element.items = itList
        self._ui.tv.restore_branch_status()

    def _add_location(self, event=None):
        # Add the selected element to the collection, if applicable.
        lcList = self.element.locations
        lcId = self._ui.tv.tree.selection()[0]
        if lcId.startswith(LOCATION_PREFIX)and not lcId in lcList:
            lcList.append(lcId)
            self.element.locations = lcList
        self._ui.tv.restore_branch_status()

    def _add_plotline(self, event=None):
        # Add the selected element to the collection, if applicable.
        plotlineList = self.element.scPlotLines
        plId = self._ui.tv.tree.selection()[0]
        if plId.startswith(PLOT_LINE_PREFIX) and not plId in plotlineList:
            plotlineList.append(plId)
            self.element.scPlotLines = plotlineList
            plotlineSections = self._mdl.novel.plotLines[plId].sections
            if not self.elementId in plotlineSections:
                plotlineSections.append(self.elementId)
                self._mdl.novel.plotLines[plId].sections = plotlineSections

            # TODO: Select the new plot line entry.
        self._ui.tv.restore_branch_status()

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _get_element_titles(self, elemIds, elements):
        # Return a list of element titles.
        #   elemIds -- list of element IDs.
        #   elements -- list of element objects.
        elemTitles = []
        if elemIds:
            for elemId in elemIds:
                try:
                    elemTitles.append(elements[elemId].title)
                except:
                    pass
        return elemTitles

    def _get_plotline_titles(self, elemIds, elements):
        # Return a list of plot line titles, preceded by the short names.
        #    elemIds -- list of element IDs.
        #    elements -- list of element objects.
        elemTitles = []
        if elemIds:
            for elemId in elemIds:
                try:
                    elemTitles.append(
                        (
                            f'({elements[elemId].shortName}) '
                            f'{elements[elemId].title}'
                        )
                    )
                except:
                    pass
        return elemTitles

    def _get_relation_id_list(self, newTitleStr, oldTitleStr, elements):
        # Return a list of valid IDs from a string
        # containing semicolon-separated titles.
        if newTitleStr or oldTitleStr:
            if oldTitleStr != newTitleStr:
                elemIds = []
                for elemTitle in string_to_list(newTitleStr):
                    for elemId in elements:
                        if elements[elemId].title == elemTitle:
                            elemIds.append(elemId)
                            break
                    else:
                        # No break occurred:
                        # there is no element with the specified title
                        self._ui.show_error(
                            message=_('Input rejected'),
                            detail=f'{_("Wrong name")}: "{elemTitle}".'
                        )
                return elemIds

        return None

    def _report_missing_date(self):
        self._ui.show_error(
            message=_('Date information is missing'),
            detail=f"{_('Please enter either a section date or a day and a reference date')}.",
        )

    def _toggle_date_time_frame(self, event=None):
        # Hide/show the 'Date/Time' frame.
        if prefs['show_date_time']:
            self._dateTimeFrame.hide()
            prefs['show_date_time'] = False
        else:
            self._dateTimeFrame.show()
            prefs['show_date_time'] = True
        self._toggle_folding_frame()

    def _toggle_plot_frame(self, event=None):
        # Hide/show the 'Plot' frame.
        if prefs['show_plot']:
            self._plotFrame.hide()
            prefs['show_plot'] = False
        else:
            self._plotFrame.show()
            prefs['show_plot'] = True
        self._toggle_folding_frame()

    def _toggle_relation_frame(self, event=None):
        # Hide/show the 'Relationships' frame.
        if prefs['show_relationships']:
            self._relationFrame.hide()
            prefs['show_relationships'] = False
        else:
            self._relationFrame.show()
            prefs['show_relationships'] = True
        self._toggle_folding_frame()

    def _toggle_scene_frame(self, event=None):
        # Hide/show the 'Scene' frame.
        if prefs['show_scene']:
            self._sceneFrame.hide()
            prefs['show_scene'] = False
        else:
            self._sceneFrame.show()
            prefs['show_scene'] = True
        self._toggle_folding_frame()


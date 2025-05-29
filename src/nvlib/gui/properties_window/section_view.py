"""Provide a tkinter based class for viewing and editing all section properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.properties_window.basic_view import BasicView
from nvlib.gui.properties_window.section_view_ctrl import SectionViewCtrl
from nvlib.gui.widgets.collection_box import CollectionBox
from nvlib.gui.widgets.folding_frame import FoldingFrame
from nvlib.gui.widgets.label_combo import LabelCombo
from nvlib.gui.widgets.label_entry import LabelEntry
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.gui.widgets.text_box import TextBox
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class SectionView(BasicView, SectionViewCtrl):
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
        self.tagsVar = MyStringVar()
        self._tagsEntry = LabelEntry(
            self.elementInfoWindow,
            text=_('Tags'),
            textvariable=self.tagsVar,
            command=self.apply_changes,
            lblWidth=self._LBL_X
            )
        self._tagsEntry.pack(anchor='w', pady=2)
        inputWidgets.append(self._tagsEntry)

        #--- Frame for section specific properties.
        self._sectionExtraFrame = ttk.Frame(self.elementInfoWindow)
        self._sectionExtraFrame.pack(anchor='w', fill='x')

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- Frame for 'Relationships'.
        # updating the character list before the viewpoints
        self.relationFrame = FoldingFrame(self.elementInfoWindow, _('Relationships'), self._toggle_relation_frame)

        # 'Characters' listbox.
        self.crTitles = ''
        crHeading = ttk.Frame(self.relationFrame)
        self._characterLabel = ttk.Label(crHeading, text=_('Characters'))
        self._characterLabel.pack(anchor='w', side='left')
        ttk.Button(crHeading, text=_('Show ages'), command=self.show_ages).pack(anchor='e')
        crHeading.pack(fill='x')
        self.characterCollection = CollectionBox(
            self.relationFrame,
            cmdAdd=self.pick_character,
            cmdRemove=self.remove_character,
            cmdOpen=self.go_to_character,
            cmdActivate=self.activate_character_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self.characterCollection.pack(fill='x')
        inputWidgets.extend(self.characterCollection.inputWidgets)

        # 'Locations' listbox.
        self.lcTitles = ''
        self._locationLabel = ttk.Label(self.relationFrame, text=_('Locations'))
        self._locationLabel.pack(anchor='w')
        self.locationCollection = CollectionBox(
            self.relationFrame,
            cmdAdd=self.pick_location,
            cmdRemove=self.remove_location,
            cmdOpen=self.go_to_location,
            cmdActivate=self.activate_location_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self.locationCollection.pack(fill='x')
        inputWidgets.extend(self.locationCollection.inputWidgets)

        # 'Items' listbox.
        self.itTitles = ''
        self._itemLabel = ttk.Label(self.relationFrame, text=_('Items'))
        self._itemLabel.pack(anchor='w')
        self.itemCollection = CollectionBox(
            self.relationFrame,
            cmdAdd=self.pick_item,
            cmdRemove=self.remove_item,
            cmdOpen=self.go_to_item,
            cmdActivate=self.activate_item_buttons,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self.itemCollection.pack(fill='x')
        inputWidgets.extend(self.itemCollection.inputWidgets)

        self._prefsShowLinks = 'show_sc_links'

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- Frame for date/time/duration.
        self.dateTimeFrame = FoldingFrame(
            self.elementInfoWindow,
            _('Date/Time'),
            self._toggle_date_time_frame)
        sectionStartFrame = ttk.Frame(self.dateTimeFrame)
        sectionStartFrame.pack(fill='x')
        localeDateFrame = ttk.Frame(sectionStartFrame)
        localeDateFrame.pack(fill='x')
        ttk.Label(
            localeDateFrame,
            text=_('Start'),
            width=self._DATE_TIME_LBL_X
            ).pack(side='left')

        # 'Start date' entry.
        self.startDateVar = MyStringVar()
        self._startDateEntry = LabelEntry(
            sectionStartFrame,
            text=_('Date'),
            textvariable=self.startDateVar,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._startDateEntry.pack(anchor='w')
        inputWidgets.append(self._startDateEntry)

        # 'Start time' entry.
        self.startTimeVar = MyStringVar()
        self._startTimeEntry = LabelEntry(
            sectionStartFrame,
            text=_('Time'),
            textvariable=self.startTimeVar,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._startTimeEntry.pack(anchor='w')
        inputWidgets.append(self._startTimeEntry)

        # 'Start day' entry.
        self.startDayVar = MyStringVar()
        self._startDayEntry = LabelEntry(
            sectionStartFrame,
            text=_('Day'),
            textvariable=self.startDayVar,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._startDayEntry.pack(anchor='w')
        inputWidgets.append(self._startDayEntry)
        self._startDayEntry.entry.bind('<Return>', self.change_day)

        # Day of the week display.
        self.weekDayVar = MyStringVar()
        weekDayDisplay = ttk.Label(
            self.dateTimeFrame.titleBar,
            textvariable=self.weekDayVar
            )
        weekDayDisplay.pack(side='left')
        weekDayDisplay.bind('<Button-1>', self._toggle_date_time_frame)

        # Localized date display.
        self.localeDateVar = MyStringVar()
        localeDateDisplay = ttk.Label(
            self.dateTimeFrame.titleBar,
            textvariable=self.localeDateVar
            )
        localeDateDisplay.pack(side='left')
        localeDateDisplay.bind('<Button-1>', self._toggle_date_time_frame)

        # Time display.
        timeDisplay = ttk.Label(
            self.dateTimeFrame.titleBar,
            textvariable=self.startTimeVar
            )
        timeDisplay.pack(side='left', padx='2')
        timeDisplay.bind('<Button-1>', self._toggle_date_time_frame)

        # 'Moon phase' button.
        ttk.Button(
            localeDateFrame,
            text=_('Moon phase'),
            command=self.show_moonphase
            ).pack(anchor='e')

        # 'Clear date/time' button.
        self._clearDateButton = ttk.Button(
            sectionStartFrame,
            text=_('Clear date/time'),
            command=self.clear_start
            )
        self._clearDateButton.pack(side='left', fill='x', expand=True, padx=1, pady=2)
        inputWidgets.append(self._clearDateButton)

        # 'Generate' button.
        self._generateDateButton = ttk.Button(
            sectionStartFrame,
            text=_('Generate'),
            command=self.auto_set_date
            )
        self._generateDateButton.pack(side='left', fill='x', expand=True, padx=1, pady=2)
        inputWidgets.append(self._generateDateButton)

        # 'Toggle date' button.
        self._toggleDateButton = ttk.Button(
            sectionStartFrame,
            text=_('Convert date/day'),
            command=self.toggle_date
            )
        self._toggleDateButton.pack(side='left', fill='x', expand=True, padx=1, pady=2)
        inputWidgets.append(self._toggleDateButton)

        ttk.Separator(self.dateTimeFrame, orient='horizontal').pack(fill='x', pady=2)

        sectionDurationFrame = ttk.Frame(self.dateTimeFrame)
        sectionDurationFrame.pack(fill='x')
        ttk.Label(sectionDurationFrame, text=_('Duration')).pack(anchor='w')

        # 'Duration days' entry.
        self.lastsDaysVar = MyStringVar()
        self._lastsDaysEntry = LabelEntry(
            sectionDurationFrame,
            text=_('Days'),
            textvariable=self.lastsDaysVar,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._lastsDaysEntry.pack(anchor='w')
        inputWidgets.append(self._lastsDaysEntry)

        # 'Duration hours' entry.
        self.lastsHoursVar = MyStringVar()
        self._lastsHoursEntry = LabelEntry(
            sectionDurationFrame,
            text=_('Hours'),
            textvariable=self.lastsHoursVar,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._lastsHoursEntry.pack(anchor='w')
        inputWidgets.append(self._lastsHoursEntry)

        # 'Duration minutes' entry.
        self.lastsMinutesVar = MyStringVar()
        self._lastsMinutesEntry = LabelEntry(
            sectionDurationFrame,
            text=_('Minutes'),
            textvariable=self.lastsMinutesVar,
            command=self.apply_changes,
            lblWidth=self._DATE_TIME_LBL_X
            )
        self._lastsMinutesEntry.pack(anchor='w')
        inputWidgets.append(self._lastsMinutesEntry)

        # 'Clear duration' button.
        self._clearDurationButton = ttk.Button(
            sectionDurationFrame,
            text=_('Clear duration'),
            command=self.clear_duration
            )
        self._clearDurationButton.pack(side='left', padx=1, pady=2)
        inputWidgets.append(self._clearDurationButton)

        # 'Generate' button.
        self._generatDurationButton = ttk.Button(
            sectionDurationFrame,
            text=_('Generate'),
            command=self.auto_set_duration
            )
        self._generatDurationButton.pack(side='left', padx=1, pady=2)
        inputWidgets.append(self._generatDurationButton)

        # ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- 'Viewpoint' combobox.
        self.viewpointVar = MyStringVar()
        self.characterCombobox = LabelCombo(
            self._sectionExtraFrame,
            text=_('Viewpoint'),
            textvariable=self.viewpointVar,
            values=[],
            lblWidth=self._LBL_X
            )
        self.characterCombobox.pack(anchor='w', pady=2)
        inputWidgets.append(self.characterCombobox)
        self.characterCombobox.combo.bind('<<ComboboxSelected>>', self.apply_changes)
        self._vpList = []

        #--- 'Unused' checkbox.
        self.isUnusedVar = tk.BooleanVar()
        self._isUnusedCheckbox = ttk.Checkbutton(
            self._sectionExtraFrame,
            text=_('Unused'),
            variable=self.isUnusedVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._isUnusedCheckbox.pack(anchor='w')
        inputWidgets.append(self._isUnusedCheckbox)

        #--- 'Append to previous section' checkbox.
        self.appendToPrevVar = tk.BooleanVar()
        self._appendToPrevCheckbox = ttk.Checkbutton(
            self._sectionExtraFrame,
            text=_('Append to previous section'),
            variable=self.appendToPrevVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._appendToPrevCheckbox.pack(anchor='w')
        inputWidgets.append(self._appendToPrevCheckbox)

        ttk.Separator(self._sectionExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for 'Plot'.
        self.plotFrame = FoldingFrame(self._sectionExtraFrame, _('Plot'), self._toggle_plot_frame)

        # 'Plot lines' listbox.
        self.plotlineTitles = ''
        self._plotlineLabel = ttk.Label(self.plotFrame, text=_('Plot lines'))
        self._plotlineLabel.pack(anchor='w')
        self.plotlineCollection = CollectionBox(
            self.plotFrame,
            cmdAdd=self.pick_plotline,
            cmdRemove=self.remove_plotline,
            cmdOpen=self.go_to_plotline,
            cmdActivate=self.activate_arc_buttons,
            cmdSelect=self.on_select_plotline,
            lblOpen=_('Go to'),
            iconAdd=self._ui.icons.addIcon,
            iconRemove=self._ui.icons.removeIcon,
            iconOpen=self._ui.icons.gotoIcon
            )
        self.plotlineCollection.pack(fill='x')
        inputWidgets.extend(self.plotlineCollection.inputWidgets)
        self.selectedPlotline = None

        #--- 'Plot line notes' text box for entering element.plotlineNotes[plId],
        #    where plId is the ID of the selected plot line in the'Plot lines' listbox.
        ttk.Label(self.plotFrame, text=_('Notes on the selected plot line')).pack(anchor='w')
        self.plotNotesWindow = TextBox(
            self.plotFrame,
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
        self.plotNotesWindow.pack(fill='x')
        inputWidgets.append(self.plotNotesWindow)

        #--- 'Plot points' label.
        ttk.Label(self.plotFrame, text=_('Plot points')).pack(anchor='w')
        self.plotPointsDisplay = tk.Label(self.plotFrame, anchor='w', bg='white')
        self.plotPointsDisplay.pack(anchor='w', fill='x')

        ttk.Separator(self._sectionExtraFrame, orient='horizontal').pack(fill='x')

        #--- Frame for 'Scene'.
        self.sceneFrame = FoldingFrame(self._sectionExtraFrame, _('Scene'), self._toggle_scene_frame)

        # Scene radiobuttons.
        selectionFrame = ttk.Frame(self.sceneFrame)
        self.customPlotProgressVar = ''
        self.customCharacterizationVar = ''
        self.customWorldBuildingVar = ''
        self.customGoalVar = ''
        self.customConflictVar = ''
        self.customOutcomeVar = ''
        self.sceneVar = tk.IntVar()

        self._notApplicableRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Not a scene'),
            variable=self.sceneVar,
            value=0, command=self.set_not_applicable,
            )
        self._notApplicableRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._notApplicableRadiobutton)

        self._actionRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Action'),
            variable=self.sceneVar,
            value=1, command=self.set_action_scene,
            )
        self._actionRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._actionRadiobutton)

        self._reactionRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Reaction'),
            variable=self.sceneVar,
            value=2,
            command=self.set_reaction_scene,
            )
        self._reactionRadiobutton.pack(side='left', anchor='w')
        inputWidgets.append(self._reactionRadiobutton)

        self._customRadiobutton = ttk.Radiobutton(
            selectionFrame,
            text=_('Other'),
            variable=self.sceneVar,
            value=3,
            command=self.set_custom_scene
            )
        self._customRadiobutton.pack(anchor='w')
        inputWidgets.append(self._customRadiobutton)

        selectionFrame.pack(fill='x')

        # 'Goal/Reaction' window. The labels are configured dynamically.
        self.goalLabel = ttk.Label(self.sceneFrame)
        self.goalLabel.pack(anchor='w')
        self.goalWindow = TextBox(
            self.sceneFrame,
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
        self.goalWindow.pack(fill='x')
        inputWidgets.append(self.goalWindow)

        # 'Conflict/Dilemma' window. The labels are configured dynamically.
        self.conflictLabel = ttk.Label(self.sceneFrame)
        self.conflictLabel.pack(anchor='w')
        self.conflictWindow = TextBox(
            self.sceneFrame,
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
        self.conflictWindow.pack(fill='x')
        inputWidgets.append(self.conflictWindow)

        # 'Outcome/Choice' window. The labels are configured dynamically.
        self.outcomeLabel = ttk.Label(self.sceneFrame)
        self.outcomeLabel.pack(anchor='w')
        self.outcomeWindow = TextBox(
            self.sceneFrame,
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
        self.outcomeWindow.pack(fill='x')
        inputWidgets.append(self.outcomeWindow)

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _toggle_date_time_frame(self, event=None):
        """Hide/show the 'Date/Time' frame."""
        if prefs['show_date_time']:
            self.dateTimeFrame.hide()
            prefs['show_date_time'] = False
        else:
            self.dateTimeFrame.show()
            prefs['show_date_time'] = True

    def _toggle_plot_frame(self, event=None):
        """Hide/show the 'Plot' frame."""
        if prefs['show_plot']:
            self.plotFrame.hide()
            prefs['show_plot'] = False
        else:
            self.plotFrame.show()
            prefs['show_plot'] = True

    def _toggle_relation_frame(self, event=None):
        """Hide/show the 'Relationships' frame."""
        if prefs['show_relationships']:
            self.relationFrame.hide()
            prefs['show_relationships'] = False
        else:
            self.relationFrame.show()
            prefs['show_relationships'] = True

    def _toggle_scene_frame(self, event=None):
        """Hide/show the 'Scene' frame."""
        if prefs['show_scene']:
            self.sceneFrame.hide()
            prefs['show_scene'] = False
        else:
            self.sceneFrame.show()
            prefs['show_scene'] = True


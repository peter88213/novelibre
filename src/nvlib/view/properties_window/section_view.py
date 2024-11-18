"""Provide a tkinter based class for viewing and editing all section properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.widgets.folding_frame import FoldingFrame
from mvclib.widgets.label_combo import LabelCombo
from mvclib.widgets.label_entry import LabelEntry
from mvclib.widgets.my_string_var import MyStringVar
from mvclib.widgets.text_box import TextBox
from nvlib.controller.properties_window.section_view_ctrl import SectionViewCtrl
from nvlib.novx_globals import _
from nvlib.nv_globals import prefs
from nvlib.view.properties_window.basic_view import BasicView
from nvlib.view.widgets.collection_box import CollectionBox
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
        self.tags = MyStringVar()
        self._tagsEntry = LabelEntry(
            self.elementInfoWindow,
            text=_('Tags'),
            textvariable=self.tags,
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
        self._relationFrame = FoldingFrame(self.elementInfoWindow, _('Relationships'), self._toggle_relation_frame)

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

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- Frame for date/time/duration.
        self._dateTimeFrame = FoldingFrame(
            self.elementInfoWindow,
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

        # ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

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

        #--- 'Plot line notes' text box for entering self.element.plotlineNotes[plId],
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
            self.inputWidgets.append(widget)

    def _activate_arc_buttons(self, event=None):
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

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_notes_window()
        self._create_button_bar()

    def _go_to_arc(self, event=None):
        """Go to the plot line selected in the listbox."""
        try:
            selection = self._plotlineCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.scPlotLines[selection])

    def _go_to_character(self, event=None):
        """Go to the character selected in the listbox."""
        try:
            selection = self._characterCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.characters[selection])

    def _go_to_location(self, event=None):
        """Go to the location selected in the listbox."""
        try:
            selection = self._locationCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.locations[selection])

    def _go_to_item(self, event=None):
        """Go to the item selected in the listbox."""
        try:
            selection = self._itemCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.items[selection])

    def _on_select_plotline(self, selection):
        """Callback routine for section plot line list selection."""
        self._save_plot_notes()
        self._selectedPlotline = self.element.scPlotLines[selection]
        self._plotNotesWindow.config(state='normal')
        if self.element.plotlineNotes:
            self._plotNotesWindow.set_text(self.element.plotlineNotes.get(self._selectedPlotline, ''))
        else:
            self._plotNotesWindow.clear()
        if self.isLocked:
            self._plotNotesWindow.config(state='disabled')
        self._plotNotesWindow.config(bg='white')

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


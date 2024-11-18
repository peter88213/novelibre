"""Provide a tkinter based class for viewing and editing project properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import ttk

from mvclib.widgets.folding_frame import FoldingFrame
from mvclib.widgets.label_combo import LabelCombo
from mvclib.widgets.label_disp import LabelDisp
from mvclib.widgets.label_entry import LabelEntry
from mvclib.widgets.my_string_var import MyStringVar
from nvlib.controller.properties_window.project_view_ctrl import ProjectViewCtrl
from nvlib.novx_globals import _
from nvlib.nv_globals import prefs
from nvlib.view.properties_window.basic_view import BasicView
import tkinter as tk


class ProjectView(BasicView, ProjectViewCtrl):
    """Class for viewing and editing project properties."""

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- Author entry.
        self._authorName = MyStringVar()
        self._authorNameEntry = LabelEntry(
            self.elementInfoWindow,
            text=_('Author'),
            textvariable=self._authorName,
            command=self.apply_changes,
            lblWidth=20
            )
        self._authorNameEntry.pack(anchor='w')
        inputWidgets.append(self._authorNameEntry)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- "Language settings" frame.
        self._languageFrame = FoldingFrame(self.elementInfoWindow, _('Document language'), self._toggle_language_frame)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        # Language and country code.
        self._languageCode = MyStringVar()
        self._languageCodeEntry = LabelEntry(
            self._languageFrame,
            text=_('Language code'),
            textvariable=self._languageCode,
            command=self.apply_changes,
            lblWidth=20
            )
        self._languageCodeEntry.pack(anchor='w')
        inputWidgets.append(self._languageCodeEntry)

        self._countryCode = MyStringVar()
        self._countryCodeEntry = LabelEntry(
            self._languageFrame,
            text=_('Country code'),
            textvariable=self._countryCode,
            command=self.apply_changes,
            lblWidth=20
            )
        self._countryCodeEntry.pack(anchor='w')
        inputWidgets.append(self._countryCodeEntry)

        #--- "Auto numbering" frame.
        self._numberingFrame = FoldingFrame(self.elementInfoWindow, _('Auto numbering'), self._toggle_numbering_frame)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        # 'Auto number chapters...' checkbox.
        self._renumberChapters = tk.BooleanVar(value=False)
        self._renumberChaptersCheckbox = ttk.Checkbutton(
            self._numberingFrame,
            text=_('Auto number chapters when refreshing the tree'),
            variable=self._renumberChapters,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._renumberChaptersCheckbox.pack(anchor='w')
        inputWidgets.append(self._renumberChaptersCheckbox)

        # 'Chapter number prefix' entry.
        self._chapterHeadingPrefix = MyStringVar()
        self._chapterHeadingPrefixEntry = LabelEntry(
            self._numberingFrame,
            text=_('Chapter number prefix'),
            textvariable=self._chapterHeadingPrefix,
            command=self.apply_changes,
            lblWidth=20
            )
        self._chapterHeadingPrefixEntry.pack(anchor='w')
        inputWidgets.append(self._chapterHeadingPrefixEntry)

        # 'Chapter number suffix' entry.
        self._chapterHeadingSuffix = MyStringVar()
        self._chapterHeadingSuffixEntry = LabelEntry(
            self._numberingFrame,
            text=_('Chapter number suffix'),
            textvariable=self._chapterHeadingSuffix,
            command=self.apply_changes,
            lblWidth=20
            )
        self._chapterHeadingSuffixEntry.pack(anchor='w')
        inputWidgets.append(self._chapterHeadingSuffixEntry)

        # 'Use Roman chapter numbers' checkbox.
        self._romanChapterNumbers = tk.BooleanVar()
        self._romanChapterNumbersCheckbox = ttk.Checkbutton(
            self._numberingFrame,
            text=_('Use Roman chapter numbers'),
            variable=self._romanChapterNumbers,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._romanChapterNumbersCheckbox.pack(anchor='w')
        inputWidgets.append(self._romanChapterNumbersCheckbox)

        # 'Reset chapter number..." checkbox
        self._renumberWithinParts = tk.BooleanVar()
        self._renumberWithinPartsCheckbox = ttk.Checkbutton(
            self._numberingFrame,
            text=_('Restart chapter numbering at part beginning'),
            variable=self._renumberWithinParts,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._renumberWithinPartsCheckbox.pack(anchor='w')
        inputWidgets.append(self._renumberWithinPartsCheckbox)

        # 'Auto number parts' checkbox.
        self._renumberParts = tk.BooleanVar()
        self._renumberPartsCheckbox = ttk.Checkbutton(
            self._numberingFrame,
            text=_('Auto number parts when refreshing the tree'),
            variable=self._renumberParts,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._renumberPartsCheckbox.pack(anchor='w')
        inputWidgets.append(self._renumberPartsCheckbox)

        # 'Part number prefix' entry.
        self._partHeadingPrefix = MyStringVar()
        self._partHeadingPrefixEntry = LabelEntry(
            self._numberingFrame,
            text=_('Part number prefix'),
            textvariable=self._partHeadingPrefix,
            command=self.apply_changes,
            lblWidth=20
            )
        self._partHeadingPrefixEntry.pack(anchor='w')
        inputWidgets.append(self._partHeadingPrefixEntry)

        # 'Part number suffix' entry.
        self._partHeadingSuffix = MyStringVar()
        self._partHeadingSuffixEntry = LabelEntry(
            self._numberingFrame,
            text=_('Part number suffix'),
            textvariable=self._partHeadingSuffix,
            command=self.apply_changes,
            lblWidth=20
            )
        self._partHeadingSuffixEntry.pack(anchor='w')
        inputWidgets.append(self._partHeadingSuffixEntry)

        # 'Use Roman part numbers' checkbox.
        self._romanPartNumbers = tk.BooleanVar()
        self._romanPartNumbersCheckbox = ttk.Checkbutton(
            self._numberingFrame,
            text=_('Use Roman part numbers'),
            variable=self._romanPartNumbers,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._romanPartNumbersCheckbox.pack(anchor='w')
        inputWidgets.append(self._romanPartNumbersCheckbox)

        #--- "Renamings" frame.
        self._renamingsFrame = FoldingFrame(self.elementInfoWindow, _('Renamings'), self._toggle_renamings_frame)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')
        ttk.Label(self._renamingsFrame, text=_('Not a scene')).pack(anchor='w')

        # Custom 'Plot progress' entry.
        self._customPlotProgress = MyStringVar()
        self._customPlotProgressEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Plot progress'),
            textvariable=self._customPlotProgress,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customPlotProgressEntry.pack(anchor='w')
        inputWidgets.append(self._customPlotProgressEntry)

        # Custom 'Characterization' entry.
        self._customCharacterization = MyStringVar()
        self._customCharacterizationEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Characterization'),
            textvariable=self._customCharacterization,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customCharacterizationEntry.pack(anchor='w')
        inputWidgets.append(self._customCharacterizationEntry)

        # Custom 'World building' entry.
        self._customWorldBuilding = MyStringVar()
        self.__customWorldBuildingEntry = LabelEntry(
            self._renamingsFrame,
            text=_('World building'),
            textvariable=self._customWorldBuilding,
            command=self.apply_changes,
            lblWidth=20
            )
        self.__customWorldBuildingEntry.pack(anchor='w')
        inputWidgets.append(self.__customWorldBuildingEntry)

        ttk.Separator(self._renamingsFrame, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(self._renamingsFrame, text=_('Other scene')).pack(anchor='w')

        # 'Opening' entry.
        self._customGoal = MyStringVar()
        self._customGoalEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Opening'),
            textvariable=self._customGoal,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customGoalEntry.pack(anchor='w')
        inputWidgets.append(self._customGoalEntry)

        # 'Peak emotional moment' entry.
        self._customConflict = MyStringVar()
        self._customConflictEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Peak em. moment'),
            textvariable=self._customConflict,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customConflictEntry.pack(anchor='w')
        inputWidgets.append(self._customConflictEntry)

        # 'Ending' entry.
        self._customOutcome = MyStringVar()
        self._customOutcomeEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Ending'),
            textvariable=self._customOutcome,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customOutcomeEntry.pack(anchor='w')
        inputWidgets.append(self._customOutcomeEntry)

        ttk.Separator(self._renamingsFrame, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(self._renamingsFrame, text=_('Character')).pack(anchor='w')

        # 'Bio' entry.
        self._customChrBio = MyStringVar()
        self._customChrBioEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Bio'),
            textvariable=self._customChrBio,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customChrBioEntry.pack(anchor='w')
        inputWidgets.append(self._customChrBioEntry)

        # 'Goals' entry.
        self._customChrGoals = MyStringVar()
        self._customChrGoalsEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Goals'),
            textvariable=self._customChrGoals,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customChrGoalsEntry.pack(anchor='w')
        inputWidgets.append(self._customChrGoalsEntry)

        #--- "Narrative time" frame.
        self._narrativeTimeFrame = FoldingFrame(self.elementInfoWindow, _('Narrative time'), self._toggle_narrative_time_frame)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        # 'Reference date' entry.
        self._referenceDate = MyStringVar()
        self._referenceDateEntry = LabelEntry(
            self._narrativeTimeFrame,
            text=_('Reference date'),
            textvariable=self._referenceDate,
            command=self.apply_changes,
            lblWidth=20
            )
        self._referenceDateEntry.pack(anchor='w')
        inputWidgets.append(self._referenceDateEntry)

        # Day of the week display.
        localeDateFrame = ttk.Frame(self._narrativeTimeFrame)
        localeDateFrame.pack(fill='x')
        ttk.Label(localeDateFrame, width=20).pack(side='left')
        self._referenceWeekDay = MyStringVar()
        ttk.Label(localeDateFrame, textvariable=self._referenceWeekDay).pack(side='left')
        self._localeDate = MyStringVar()
        ttk.Label(localeDateFrame, textvariable=self._localeDate).pack(anchor='w')

        # Convert date/day buttons.
        self._datesToDaysButton = ttk.Button(self._narrativeTimeFrame, text=_('Convert dates to days'), command=self._dates_to_days)
        self._datesToDaysButton.pack(side='left', fill='x', expand=True, padx=1, pady=2)
        inputWidgets.append(self._datesToDaysButton)

        self._daysToDatesButton = ttk.Button(self._narrativeTimeFrame, text=_('Convert days to dates'), command=self._days_to_dates)
        self._daysToDatesButton.pack(side='left', fill='x', expand=True, padx=1, pady=2)
        inputWidgets.append(self._daysToDatesButton)

        #--- "Writing progress" frame.
        self._progressFrame = FoldingFrame(self.elementInfoWindow, _('Writing progress'), self._toggle_progress_frame)

        # 'Log writing progress' checkbox.
        self._saveWordCount = tk.BooleanVar()
        self._saveWordCountEntry = ttk.Checkbutton(
            self._progressFrame,
            text=_('Log writing progress'),
            variable=self._saveWordCount,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._saveWordCountEntry.pack(anchor='w')
        inputWidgets.append(self._saveWordCountEntry)

        ttk.Separator(self._progressFrame, orient='horizontal').pack(fill='x')

        # 'Words to write' entry.
        self._wordTarget = tk.IntVar()
        self._wordTargetEntry = LabelEntry(
            self._progressFrame,
            text=_('Words to write'),
            textvariable=self._wordTarget,
            command=self.apply_changes,
            lblWidth=20
            )
        self._wordTargetEntry.pack(anchor='w')
        inputWidgets.append(self._wordTargetEntry)

        # 'Starting count' entry.
        self._wordCountStart = tk.IntVar()
        self._wordCountStartEntry = LabelEntry(
            self._progressFrame,
            text=_('Starting count'),
            textvariable=self._wordCountStart,
            command=self.apply_changes,
            lblWidth=20
            )
        self._wordCountStartEntry.pack(anchor='w')
        inputWidgets.append(self._wordCountStartEntry)

        # 'Set actual wordcount as start' button.
        self._setInitialWcButton = ttk.Button(self._progressFrame, text=_('Set actual wordcount as start'), command=self._set_initial_wc)
        self._setInitialWcButton.pack(pady=2)
        inputWidgets.append(self._setInitialWcButton)

        # 'Words written' display.
        self._wordsWritten = MyStringVar()
        self._wordTarget.trace_add('write', self._update_words_written)
        self._wordCountStart.trace_add('write', self._update_words_written)
        LabelDisp(self._progressFrame, text=_('Words written'),
                  textvariable=self._wordsWritten, lblWidth=20).pack(anchor='w')

        ttk.Separator(self._progressFrame, orient='horizontal').pack(fill='x')

        self._totalUsed = MyStringVar()
        LabelDisp(self._progressFrame, text=_('Used'), textvariable=self._totalUsed, lblWidth=20).pack(anchor='w')
        self._totalOutline = MyStringVar()
        LabelDisp(self._progressFrame, text=_('Outline'), textvariable=self._totalOutline, lblWidth=20).pack(anchor='w')
        self._totalDraft = MyStringVar()
        LabelDisp(self._progressFrame, text=_('Draft'), textvariable=self._totalDraft, lblWidth=20).pack(anchor='w')
        self._total1stEdit = MyStringVar()
        LabelDisp(self._progressFrame, text=_('1st Edit'), textvariable=self._total1stEdit, lblWidth=20).pack(anchor='w')
        self._total2ndEdit = MyStringVar()
        LabelDisp(self._progressFrame, text=_('2nd Edit'), textvariable=self._total2ndEdit, lblWidth=20).pack(anchor='w')
        self._totalDone = MyStringVar()
        LabelDisp(self._progressFrame, text=_('Done'), textvariable=self._totalDone, lblWidth=20).pack(anchor='w')
        self._totalUnused = MyStringVar()
        LabelDisp(self._progressFrame, text=_('Unused'), textvariable=self._totalUnused, lblWidth=20).pack(anchor='w')
        self._totalWords = MyStringVar()
        LabelDisp(self._progressFrame, text=_('All'), textvariable=self._totalWords, lblWidth=20).pack(anchor='w')

        #--- 'phase' combobox.
        self._phase = MyStringVar()
        self._phaseCombobox = LabelCombo(self._progressFrame, lblWidth=20, text=_('Work phase'), textvariable=self._phase, values=[])
        self._phaseCombobox.pack(anchor='w')
        inputWidgets.append(self._phaseCombobox)
        self._phaseCombobox.bind('<Return>', self.apply_changes)

        #--- Cover display
        self._coverFile = None

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

        self._prefsShowLinks = 'show_pr_links'

    def show(self):
        """Display the cover.
        
        Extends the superclass constructor.
        """
        try:
            coverFile = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}.png'
            if self._coverFile != coverFile:
                self._coverFile = coverFile
                coverPic = tk.PhotoImage(file=coverFile)
                self._cover.configure(image=coverPic)
                self._cover.image = coverPic
                # avoid garbage collection
        except:
            self._cover.configure(image=None)
            self._cover.image = None
        super().show()

    def _create_cover_window(self):
        """Create a text box for element notes."""
        self._cover = tk.Label(self._propertiesFrame)
        self._cover.pack()

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_cover_window()

    def _toggle_language_frame(self, event=None):
        """Hide/show the "Document language" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs['show_language_settings']:
            self._languageFrame.hide()
            prefs['show_language_settings'] = False
        else:
            self._languageFrame.show()
            prefs['show_language_settings'] = True

    def _toggle_numbering_frame(self, event=None):
        """Hide/show the "Auto numbering" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs['show_auto_numbering']:
            self._numberingFrame.hide()
            prefs['show_auto_numbering'] = False
        else:
            self._numberingFrame.show()
            prefs['show_auto_numbering'] = True

    def _toggle_narrative_time_frame(self, event=None):
        """Hide/show the "Narrative time" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs['show_narrative_time']:
            self._narrativeTimeFrame.hide()
            prefs['show_narrative_time'] = False
        else:
            self._narrativeTimeFrame.show()
            prefs['show_narrative_time'] = True

    def _toggle_progress_frame(self, event=None):
        """Hide/show the "Writing progress" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs['show_writing_progress']:
            self._progressFrame.hide()
            prefs['show_writing_progress'] = False
        else:
            self._progressFrame.show()
            prefs['show_writing_progress'] = True

    def _toggle_renamings_frame(self, event=None):
        """Hide/show the "Renamings" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs['show_renamings']:
            self._renamingsFrame.hide()
            prefs['show_renamings'] = False
        else:
            self._renamingsFrame.show()
            prefs['show_renamings'] = True


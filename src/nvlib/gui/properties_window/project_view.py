"""Provide a tkinter based class for viewing and editing project properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import ttk

from nvlib.gui.properties_window.basic_view import BasicView
from nvlib.gui.properties_window.project_view_ctrl import ProjectViewCtrl
from nvlib.gui.widgets.folding_frame import FoldingFrame
from nvlib.gui.widgets.label_combo import LabelCombo
from nvlib.gui.widgets.label_disp import LabelDisp
from nvlib.gui.widgets.label_entry import LabelEntry
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
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
        self.authorNameVar = MyStringVar()
        self._authorNameEntry = LabelEntry(
            self.elementInfoWindow,
            text=_('Author'),
            textvariable=self.authorNameVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._authorNameEntry.pack(anchor='w')
        inputWidgets.append(self._authorNameEntry)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- "Language settings" frame.
        self.languageFrame = FoldingFrame(self.elementInfoWindow, _('Document language'), self._toggle_language_frame)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        # Language and country code.
        self.languageCodeVar = MyStringVar()
        self._languageCodeEntry = LabelEntry(
            self.languageFrame,
            text=_('Language code'),
            textvariable=self.languageCodeVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._languageCodeEntry.pack(anchor='w')
        inputWidgets.append(self._languageCodeEntry)

        self.countryCodeVar = MyStringVar()
        self._countryCodeEntry = LabelEntry(
            self.languageFrame,
            text=_('Country code'),
            textvariable=self.countryCodeVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._countryCodeEntry.pack(anchor='w')
        inputWidgets.append(self._countryCodeEntry)

        #--- "Auto numbering" frame.
        self.numberingFrame = FoldingFrame(self.elementInfoWindow, _('Auto numbering'), self._toggle_numbering_frame)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        # 'Auto number chapters...' checkbox.
        self.renumberChaptersVar = tk.BooleanVar(value=False)
        self._renumberChaptersCheckbox = ttk.Checkbutton(
            self.numberingFrame,
            text=_('Auto number chapters when refreshing the tree'),
            variable=self.renumberChaptersVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._renumberChaptersCheckbox.pack(anchor='w')
        inputWidgets.append(self._renumberChaptersCheckbox)

        # 'Chapter number prefix' entry.
        self.chapterHeadingPrefixVar = MyStringVar()
        self._chapterHeadingPrefixEntry = LabelEntry(
            self.numberingFrame,
            text=_('Chapter number prefix'),
            textvariable=self.chapterHeadingPrefixVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._chapterHeadingPrefixEntry.pack(anchor='w')
        inputWidgets.append(self._chapterHeadingPrefixEntry)

        # 'Chapter number suffix' entry.
        self.chapterHeadingSuffixVar = MyStringVar()
        self._chapterHeadingSuffixEntry = LabelEntry(
            self.numberingFrame,
            text=_('Chapter number suffix'),
            textvariable=self.chapterHeadingSuffixVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._chapterHeadingSuffixEntry.pack(anchor='w')
        inputWidgets.append(self._chapterHeadingSuffixEntry)

        # 'Use Roman chapter numbers' checkbox.
        self.romanChapterNumbersVar = tk.BooleanVar()
        self._romanChapterNumbersCheckbox = ttk.Checkbutton(
            self.numberingFrame,
            text=_('Use Roman chapter numbers'),
            variable=self.romanChapterNumbersVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._romanChapterNumbersCheckbox.pack(anchor='w')
        inputWidgets.append(self._romanChapterNumbersCheckbox)

        # 'Reset chapter number..." checkbox
        self.renumberWithinPartsVar = tk.BooleanVar()
        self._renumberWithinPartsCheckbox = ttk.Checkbutton(
            self.numberingFrame,
            text=_('Restart chapter numbering at part beginning'),
            variable=self.renumberWithinPartsVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._renumberWithinPartsCheckbox.pack(anchor='w')
        inputWidgets.append(self._renumberWithinPartsCheckbox)

        # 'Auto number parts' checkbox.
        self.renumberPartsVar = tk.BooleanVar()
        self._renumberPartsCheckbox = ttk.Checkbutton(
            self.numberingFrame,
            text=_('Auto number parts when refreshing the tree'),
            variable=self.renumberPartsVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._renumberPartsCheckbox.pack(anchor='w')
        inputWidgets.append(self._renumberPartsCheckbox)

        # 'Part number prefix' entry.
        self.partHeadingPrefixVar = MyStringVar()
        self._partHeadingPrefixEntry = LabelEntry(
            self.numberingFrame,
            text=_('Part number prefix'),
            textvariable=self.partHeadingPrefixVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._partHeadingPrefixEntry.pack(anchor='w')
        inputWidgets.append(self._partHeadingPrefixEntry)

        # 'Part number suffix' entry.
        self.partHeadingSuffixVar = MyStringVar()
        self._partHeadingSuffixEntry = LabelEntry(
            self.numberingFrame,
            text=_('Part number suffix'),
            textvariable=self.partHeadingSuffixVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._partHeadingSuffixEntry.pack(anchor='w')
        inputWidgets.append(self._partHeadingSuffixEntry)

        # 'Use Roman part numbers' checkbox.
        self.romanPartNumbersVar = tk.BooleanVar()
        self._romanPartNumbersCheckbox = ttk.Checkbutton(
            self.numberingFrame,
            text=_('Use Roman part numbers'),
            variable=self.romanPartNumbersVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._romanPartNumbersCheckbox.pack(anchor='w')
        inputWidgets.append(self._romanPartNumbersCheckbox)

        #--- "Renamings" frame.
        self.renamingsFrame = FoldingFrame(self.elementInfoWindow, _('Renamings'), self._toggle_renamings_frame)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')
        ttk.Label(self.renamingsFrame, text=_('Not a scene')).pack(anchor='w')

        # Custom 'Plot progress' entry.
        self.customPlotProgressVar = MyStringVar()
        self._customPlotProgressEntry = LabelEntry(
            self.renamingsFrame,
            text=_('Plot progress'),
            textvariable=self.customPlotProgressVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customPlotProgressEntry.pack(anchor='w')
        inputWidgets.append(self._customPlotProgressEntry)

        # Custom 'Characterization' entry.
        self.customCharacterizationVar = MyStringVar()
        self._customCharacterizationEntry = LabelEntry(
            self.renamingsFrame,
            text=_('Characterization'),
            textvariable=self.customCharacterizationVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customCharacterizationEntry.pack(anchor='w')
        inputWidgets.append(self._customCharacterizationEntry)

        # Custom 'World building' entry.
        self.customWorldBuildingVar = MyStringVar()
        self._customWorldBuildingEntry = LabelEntry(
            self.renamingsFrame,
            text=_('World building'),
            textvariable=self.customWorldBuildingVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customWorldBuildingEntry.pack(anchor='w')
        inputWidgets.append(self._customWorldBuildingEntry)

        ttk.Separator(self.renamingsFrame, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(self.renamingsFrame, text=_('Other scene')).pack(anchor='w')

        # 'Opening' entry.
        self.customGoalVar = MyStringVar()
        self._customGoalEntry = LabelEntry(
            self.renamingsFrame,
            text=_('Opening'),
            textvariable=self.customGoalVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customGoalEntry.pack(anchor='w')
        inputWidgets.append(self._customGoalEntry)

        # 'Peak emotional moment' entry.
        self.customConflictVar = MyStringVar()
        self._customConflictEntry = LabelEntry(
            self.renamingsFrame,
            text=_('Peak em. moment'),
            textvariable=self.customConflictVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customConflictEntry.pack(anchor='w')
        inputWidgets.append(self._customConflictEntry)

        # 'Ending' entry.
        self.customOutcomeVar = MyStringVar()
        self._customOutcomeEntry = LabelEntry(
            self.renamingsFrame,
            text=_('Ending'),
            textvariable=self.customOutcomeVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customOutcomeEntry.pack(anchor='w')
        inputWidgets.append(self._customOutcomeEntry)

        ttk.Separator(self.renamingsFrame, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(self.renamingsFrame, text=_('Character')).pack(anchor='w')

        # 'Bio' entry.
        self.customChrBioVar = MyStringVar()
        self._customChrBioEntry = LabelEntry(
            self.renamingsFrame,
            text=_('Bio'),
            textvariable=self.customChrBioVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customChrBioEntry.pack(anchor='w')
        inputWidgets.append(self._customChrBioEntry)

        # 'Goals' entry.
        self.customChrGoalsVar = MyStringVar()
        self._customChrGoalsEntry = LabelEntry(
            self.renamingsFrame,
            text=_('Goals'),
            textvariable=self.customChrGoalsVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customChrGoalsEntry.pack(anchor='w')
        inputWidgets.append(self._customChrGoalsEntry)

        #--- "Narrative time" frame.
        self.narrativeTimeFrame = FoldingFrame(self.elementInfoWindow, _('Narrative time'), self._toggle_narrative_time_frame)

        ttk.Separator(self.elementInfoWindow, orient='horizontal').pack(fill='x')

        # 'Reference date' entry.
        self.referenceDateVar = MyStringVar()
        self._referenceDateEntry = LabelEntry(
            self.narrativeTimeFrame,
            text=_('Reference date'),
            textvariable=self.referenceDateVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._referenceDateEntry.pack(anchor='w')
        inputWidgets.append(self._referenceDateEntry)

        # Day of the week display.
        localeDateFrame = ttk.Frame(self.narrativeTimeFrame)
        localeDateFrame.pack(fill='x')
        ttk.Label(localeDateFrame, width=20).pack(side='left')
        self.referenceWeekDayVar = MyStringVar()
        ttk.Label(localeDateFrame, textvariable=self.referenceWeekDayVar).pack(side='left')
        self.localeDateVar = MyStringVar()
        ttk.Label(localeDateFrame, textvariable=self.localeDateVar).pack(anchor='w')

        # Convert date/day buttons.
        self.datesToDaysButton = ttk.Button(self.narrativeTimeFrame, text=_('Convert dates to days'), command=self.dates_to_days)
        self.datesToDaysButton.pack(side='left', fill='x', expand=True, padx=1, pady=2)
        inputWidgets.append(self.datesToDaysButton)

        self.daysToDatesButton = ttk.Button(self.narrativeTimeFrame, text=_('Convert days to dates'), command=self.days_to_dates)
        self.daysToDatesButton.pack(side='left', fill='x', expand=True, padx=1, pady=2)
        inputWidgets.append(self.daysToDatesButton)

        #--- "Writing progress" frame.
        self.progressFrame = FoldingFrame(self.elementInfoWindow, _('Writing progress'), self._toggle_progress_frame)

        # 'Log writing progress' checkbox.
        self.saveWordCountVar = tk.BooleanVar()
        self._saveWordCountEntry = ttk.Checkbutton(
            self.progressFrame,
            text=_('Log writing progress'),
            variable=self.saveWordCountVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
            )
        self._saveWordCountEntry.pack(anchor='w')
        inputWidgets.append(self._saveWordCountEntry)

        ttk.Separator(self.progressFrame, orient='horizontal').pack(fill='x')

        # 'Words to write' entry.
        self.wordTargetVar = tk.IntVar()
        self._wordTargetEntry = LabelEntry(
            self.progressFrame,
            text=_('Words to write'),
            textvariable=self.wordTargetVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._wordTargetEntry.pack(anchor='w')
        inputWidgets.append(self._wordTargetEntry)

        # 'Starting count' entry.
        self.wordCountStartVar = tk.IntVar()
        self._wordCountStartEntry = LabelEntry(
            self.progressFrame,
            text=_('Starting count'),
            textvariable=self.wordCountStartVar,
            command=self.apply_changes,
            lblWidth=20
            )
        self._wordCountStartEntry.pack(anchor='w')
        inputWidgets.append(self._wordCountStartEntry)

        # 'Set actual wordcount as start' button.
        self._setInitialWcButton = ttk.Button(self.progressFrame, text=_('Set actual wordcount as start'), command=self.set_initial_wc)
        self._setInitialWcButton.pack(pady=2)
        inputWidgets.append(self._setInitialWcButton)

        # 'Words written' display.
        self.wordsWrittenVar = MyStringVar()
        self.wordTargetVar.trace_add('write', self.update_words_written)
        self.wordCountStartVar.trace_add('write', self.update_words_written)
        LabelDisp(self.progressFrame, text=_('Words written'),
                  textvariable=self.wordsWrittenVar, lblWidth=20).pack(anchor='w')

        ttk.Separator(self.progressFrame, orient='horizontal').pack(fill='x')

        self.totalUsedVar = MyStringVar()
        LabelDisp(self.progressFrame, text=_('Used'), textvariable=self.totalUsedVar, lblWidth=20).pack(anchor='w')
        self.totalOutlineVar = MyStringVar()
        LabelDisp(self.progressFrame, text=_('Outline'), textvariable=self.totalOutlineVar, lblWidth=20).pack(anchor='w')
        self.totalDraftVar = MyStringVar()
        LabelDisp(self.progressFrame, text=_('Draft'), textvariable=self.totalDraftVar, lblWidth=20).pack(anchor='w')
        self.total1stEditVar = MyStringVar()
        LabelDisp(self.progressFrame, text=_('1st Edit'), textvariable=self.total1stEditVar, lblWidth=20).pack(anchor='w')
        self.total2ndEditVar = MyStringVar()
        LabelDisp(self.progressFrame, text=_('2nd Edit'), textvariable=self.total2ndEditVar, lblWidth=20).pack(anchor='w')
        self.totalDoneVar = MyStringVar()
        LabelDisp(self.progressFrame, text=_('Done'), textvariable=self.totalDoneVar, lblWidth=20).pack(anchor='w')
        self.totalUnusedVar = MyStringVar()
        LabelDisp(self.progressFrame, text=_('Unused'), textvariable=self.totalUnusedVar, lblWidth=20).pack(anchor='w')
        self.totalWordsVar = MyStringVar()
        LabelDisp(self.progressFrame, text=_('All'), textvariable=self.totalWordsVar, lblWidth=20).pack(anchor='w')

        #--- 'phase' combobox.
        self.phaseVar = MyStringVar()
        self.phaseCombobox = LabelCombo(self.progressFrame, lblWidth=20, text=_('Work phase'), textvariable=self.phaseVar, values=[])
        self.phaseCombobox.pack(anchor='w')
        inputWidgets.append(self.phaseCombobox)
        self.phaseCombobox.bind('<Return>', self.apply_changes)

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
            self._coverFile = None
            self._cover.configure(image=None)
            self._cover.image = None
        super().show()

    def _create_cover_window(self):
        """Create a text box for element notes."""
        self._cover = tk.Label(self.propertiesFrame)
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
            self.languageFrame.hide()
            prefs['show_language_settings'] = False
        else:
            self.languageFrame.show()
            prefs['show_language_settings'] = True
        self.toggle_folding_frame()

    def _toggle_narrative_time_frame(self, event=None):
        """Hide/show the "Narrative time" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs['show_narrative_time']:
            self.narrativeTimeFrame.hide()
            prefs['show_narrative_time'] = False
        else:
            self.narrativeTimeFrame.show()
            prefs['show_narrative_time'] = True
        self.toggle_folding_frame()

    def _toggle_numbering_frame(self, event=None):
        """Hide/show the "Auto numbering" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs['show_auto_numbering']:
            self.numberingFrame.hide()
            prefs['show_auto_numbering'] = False
        else:
            self.numberingFrame.show()
            prefs['show_auto_numbering'] = True
        self.toggle_folding_frame()

    def _toggle_progress_frame(self, event=None):
        """Hide/show the "Writing progress" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs['show_writing_progress']:
            self.progressFrame.hide()
            prefs['show_writing_progress'] = False
        else:
            self.progressFrame.show()
            prefs['show_writing_progress'] = True
        self.toggle_folding_frame()

    def _toggle_renamings_frame(self, event=None):
        """Hide/show the "Renamings" frame.
        
        Callback procedure for the FoldingFrame's button.
        """
        if prefs['show_renamings']:
            self.renamingsFrame.hide()
            prefs['show_renamings'] = False
        else:
            self.renamingsFrame.show()
            prefs['show_renamings'] = True
        self.toggle_folding_frame()


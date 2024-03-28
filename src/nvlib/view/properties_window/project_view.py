"""Provide a tkinter based class for viewing and editing project properties.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
import os
from tkinter import ttk

from nvlib.nv_globals import prefs
from nvlib.view.properties_window.basic_view import BasicView
from nvlib.widgets.folding_frame import FoldingFrame
from nvlib.widgets.label_combo import LabelCombo
from nvlib.widgets.label_disp import LabelDisp
from nvlib.widgets.label_entry import LabelEntry
from nvlib.widgets.my_string_var import MyStringVar
from novxlib.novx_globals import WEEKDAYS
from novxlib.novx_globals import _
import tkinter as tk


class ProjectView(BasicView):
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
            self._elementInfoWindow,
            text=_('Author'),
            textvariable=self._authorName,
            command=self.apply_changes,
            lblWidth=20
            )
        self._authorNameEntry.pack(anchor='w')
        inputWidgets.append(self._authorNameEntry)

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

        #--- "Language settings" frame.
        self._languageFrame = FoldingFrame(self._elementInfoWindow, _('Document language'), self._toggle_language_frame)

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

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
        self._numberingFrame = FoldingFrame(self._elementInfoWindow, _('Auto numbering'), self._toggle_numbering_frame)

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

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
            text=_('Reset chapter number when starting a new part'),
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
        self._renamingsFrame = FoldingFrame(self._elementInfoWindow, _('Renamings'), self._toggle_renamings_frame)

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

        # 'Custom Goal' entry.
        self._customGoal = MyStringVar()
        self._customGoalEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Custom Goal'),
            textvariable=self._customGoal,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customGoalEntry.pack(anchor='w')
        inputWidgets.append(self._customGoalEntry)

        # 'Custom Conflict' entry.
        self._customConflict = MyStringVar()
        self._customConflictEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Custom Conflict'),
            textvariable=self._customConflict,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customConflictEntry.pack(anchor='w')
        inputWidgets.append(self._customConflictEntry)

        # 'Custom Outcome' entry.
        self._customOutcome = MyStringVar()
        self._customOutcomeEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Custom Outcome'),
            textvariable=self._customOutcome,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customOutcomeEntry.pack(anchor='w')
        inputWidgets.append(self._customOutcomeEntry)

        ttk.Separator(self._renamingsFrame, orient='horizontal').pack(fill='x')

        # 'Custom Bio' entry.
        self._customChrBio = MyStringVar()
        self._customChrBioEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Custom chara Bio'),
            textvariable=self._customChrBio,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customChrBioEntry.pack(anchor='w')
        inputWidgets.append(self._customChrBioEntry)

        # 'Custom chara Goals' entry.
        self._customChrGoals = MyStringVar()
        self._customChrGoalsEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Custom chara Goals'),
            textvariable=self._customChrGoals,
            command=self.apply_changes,
            lblWidth=20
            )
        self._customChrGoalsEntry.pack(anchor='w')
        inputWidgets.append(self._customChrGoalsEntry)

        #--- "Narrative time" frame.
        self._narrativeTimeFrame = FoldingFrame(self._elementInfoWindow, _('Narrative time'), self._toggle_narrative_time_frame)

        ttk.Separator(self._elementInfoWindow, orient='horizontal').pack(fill='x')

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
        self._progressFrame = FoldingFrame(self._elementInfoWindow, _('Writing progress'), self._toggle_progress_frame)

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
            self._inputWidgets.append(widget)

        self._prefsShowLinks = 'show_pr_links'

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        super().apply_changes()

        # Author
        authorName = self._authorName.get()
        if authorName:
            authorName = authorName.strip()
        self._element.authorName = authorName

        #--- "Language settings" frame.
        self._element.languageCode = self._languageCode.get()
        self._element.countryCode = self._countryCode.get()

        #--- "Auto numbering" frame.
        self._element.renumberChapters = self._renumberChapters.get()
        self._element.renumberParts = self._renumberParts.get()
        self._element.renumberWithinParts = self._renumberWithinParts.get()
        self._element.romanChapterNumbers = self._romanChapterNumbers.get()
        self._element.romanPartNumbers = self._romanPartNumbers.get()
        self._element.saveWordCount = self._saveWordCount.get()

        #--- "Renamings" frame.
        self._element.chapterHeadingPrefix = self._chapterHeadingPrefix.get()
        self._element.chapterHeadingSuffix = self._chapterHeadingSuffix.get()
        self._element.partHeadingPrefix = self._partHeadingPrefix.get()
        self._element.partHeadingSuffix = self._partHeadingSuffix.get()
        self._element.customGoal = self._customGoal.get()
        self._element.customConflict = self._customConflict.get()
        self._element.customOutcome = self._customOutcome.get()
        self._element.customChrBio = self._customChrBio.get()
        self._element.customChrGoals = self._customChrGoals.get()

        #--- "Narrative time" frame.
        refDateStr = self._referenceDate.get()
        if not refDateStr:
            self._element.referenceDate = None
            self._referenceWeekDay.set('')
            self._localeDate.set('')
        elif refDateStr != self._element.referenceDate:
            try:
                date.fromisoformat(refDateStr)
            except ValueError:
                self._referenceDate.set(self._element.referenceDate)
                self._ui.show_error(f'{_("Wrong date")}: "{refDateStr}"', title=_('Input rejected'))
            else:
                self._element.referenceDate = refDateStr
                if self._element.referenceWeekDay is not None:
                    self._referenceWeekDay.set(WEEKDAYS[self._element.referenceWeekDay])
                else:
                    self._referenceWeekDay.set('')
                    self._localeDate.set('')

        #--- "Writing progress" frame.
        try:
            entry = self._wordTarget.get()
            # entry must be an integer
            if self._element.wordTarget or entry:
                if self._element.wordTarget != entry:
                    self._element.wordTarget = entry
        except:
            # entry is no integer
            pass
        try:
            entry = self._wordCountStart.get()
            # entry must be an integer
            if self._element.wordCountStart or entry:
                if self._element.wordCountStart != entry:
                    self._element.wordCountStart = entry
        except:
            # entry is no integer
            pass

        # Get work phase.
        if not self._phaseCombobox.current():
            entry = None
        else:
            entry = self._phaseCombobox.current()
        self._element.workPhase = entry

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel
        super().set_data(elementId)

        #--- Author entry.
        self._authorName.set(self._element.authorName)

        #--- "Language settings" frame.
        if prefs['show_language_settings']:
            self._languageFrame.show()
        else:
            self._languageFrame.hide()

        # 'Language code' entry.
        self._languageCode.set(self._element.languageCode)

        # 'Country code' entry.
        self._countryCode.set(self._element.countryCode)

        #--- "Auto numbering" frame.
        if prefs['show_auto_numbering']:
            self._numberingFrame.show()
        else:
            self._numberingFrame.hide()

        # 'Auto number chapters' checkbox.
        if self._element.renumberChapters:
            self._renumberChapters.set(True)
        else:
            self._renumberChapters.set(False)
            # applies also to uninitialized values.

        # 'Chapter number prefix' entry.
        self._chapterHeadingPrefix.set(self._element.chapterHeadingPrefix)

        # 'Chapter number suffix' entry.
        self._chapterHeadingSuffix = MyStringVar(value=self._element.chapterHeadingSuffix)

        # 'Use Roman chapter numbers' checkbox.
        if self._element.romanChapterNumbers:
            self._romanChapterNumbers.set(True)
        else:
            self._romanChapterNumbers.set(False)

        # 'Reset chapter number..." checkbox
        if self._element.renumberWithinParts:
            self._renumberWithinParts.set(True)
        else:
            self._renumberWithinParts.set(False)

        # 'Auto number parts' checkbox.
        if self._element.renumberParts:
            self._renumberParts.set(True)
        else:
            self._renumberParts.set(False)

        # 'Part number prefix' entry.
        self._partHeadingPrefix.set(self._element.partHeadingPrefix)

        # 'Part number suffix' entry.
        self._partHeadingSuffix.set(self._element.partHeadingSuffix)

        # 'Use Roman part numbers' checkbox.
        if self._element.romanPartNumbers:
            self._romanPartNumbers.set(True)
        else:
            self._romanPartNumbers.set(False)

        #--- "Renamings" frame.
        if prefs['show_renamings']:
            self._renamingsFrame.show()
        else:
            self._renamingsFrame.hide()

        # 'Custom Goal' entry.
        self._customGoal.set(self._element.customGoal)

        # 'Custom Conflict' entry.
        self._customConflict.set(self._element.customConflict)

        # 'Custom Outcome' entry.
        self._customOutcome.set(self._element.customOutcome)

        # 'Custom Bio' entry.
        self._customChrBio.set(self._element.customChrBio)

        # 'Custom chara Goals' entry.
        self._customChrGoals.set(self._element.customChrGoals)

        #--- "Narrative time" frame
        if prefs['show_narrative_time']:
            self._narrativeTimeFrame.show()
        else:
            self._narrativeTimeFrame.hide()

        if self._element.referenceDate and self._element.referenceWeekDay is not None:
            self._referenceWeekDay.set(
                WEEKDAYS[self._element.referenceWeekDay]
                )
            self._localeDate.set(
                date.fromisoformat(self._element.referenceDate).strftime('%x')
                )
        else:
            self._referenceWeekDay.set('')
            self._localeDate.set('')
        self._referenceDate.set(self._element.referenceDate)

        #--- "Writing progress" frame.
        if prefs['show_writing_progress']:
            self._progressFrame.show()
        else:
            self._progressFrame.hide()

        # 'Save word count' checkbox.
        if self._element.saveWordCount:
            self._saveWordCount.set(True)
        else:
            self._saveWordCount.set(False)

        # 'Words to write' entry.
        if self._element.wordTarget is not None:
            self._wordTarget.set(self._element.wordTarget)
        else:
            self._wordTarget.set(0)

        # 'Starting count' entry.
        if self._element.wordCountStart is not None:
            self._wordCountStart.set(self._element.wordCountStart)
        else:
            self._wordCountStart.set(0)

        # Status counts.
        normalWordsTotal, allWordsTotal = self._mdl.prjFile.count_words()
        self._totalWords.set(allWordsTotal)
        self._totalUsed.set(normalWordsTotal)
        self._totalUnused.set(allWordsTotal - normalWordsTotal)
        statusCounts = self._mdl.get_status_counts()
        self._totalOutline.set(statusCounts[1])
        self._totalDraft.set(statusCounts[2])
        self._total1stEdit.set(statusCounts[3])
        self._total2ndEdit.set(statusCounts[4])
        self._totalDone.set(statusCounts[5])

        # 'Work phase' combobox.
        phases = [_('Undefined'), _('Outline'), _('Draft'), _('1st Edit'), _('2nd Edit'), _('Done')]
        self._phaseCombobox.configure(values=phases)
        try:
            workPhase = int(self._element.workPhase)
        except:
            workPhase = 0
        self._phase.set(value=phases[workPhase])

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

    def _set_initial_wc(self):
        """Set actual wordcount as start.
        
        Callback procedure for the related button.
        """
        self._wordCountStart.set(self._mdl.wordCount)

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

    def _dates_to_days(self):
        """Convert specific section dates to days."""
        buttonText = self._datesToDaysButton['text']
        self._datesToDaysButton['text'] = _('Please wait ...')
        # changing the button text is less time consuming than showing a progress bar
        if self._mdl.novel.referenceDate:
            if self._ui.ask_yes_no(_('Convert all section dates to days relative to the reference date?')):
                self.doNotUpdate = True
                for scId in self._mdl.novel.sections:
                    self._mdl.novel.sections[scId].date_to_day(self._mdl.novel.referenceDate)
                self.doNotUpdate = False
        else:
            self._ui.set_status(f"!{_('The reference date is not set')}.")
        self._datesToDaysButton['text'] = buttonText

    def _days_to_dates(self):
        """Convert section days to specific dates."""
        buttonText = self._daysToDatesButton['text']
        self._daysToDatesButton['text'] = _('Please wait ...')
        # changing the button text is less time consuming than showing a progress bar
        if self._mdl.novel.referenceDate:
            if self._ui.ask_yes_no(_('Convert all section days to dates using the reference date?')):
                self.doNotUpdate = True
                for scId in self._mdl.novel.sections:
                    self._mdl.novel.sections[scId].day_to_date(self._mdl.novel.referenceDate)
                self.doNotUpdate = False
        else:
            self._ui.set_status(f"!{_('The reference date is not set')}.")
        self._daysToDatesButton['text'] = buttonText

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

    def _update_words_written(self, n, m, x):
        """Calculate the percentage of written words.
        
        Callback procedure for traced variables:
        - self._wordCountStart
        - self._wordTarget
        """
        try:
            ww = self._mdl.wordCount - self._wordCountStart.get()
            wt = self._wordTarget.get()
            try:
                wp = f'({round(100*ww/wt)}%)'
            except ZeroDivisionError:
                wp = ''
            self._wordsWritten.set(f'{ww} {wp}')
        except:
            pass


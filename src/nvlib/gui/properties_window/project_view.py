"""Provide a tkinter based class for viewing and editing project properties.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from tkinter import ttk

from nvlib.gui.properties_window.element_view import ElementView
from nvlib.gui.widgets.folding_frame import FoldingFrame
from nvlib.gui.widgets.label_combo import LabelCombo
from nvlib.gui.widgets.label_disp import LabelDisp
from nvlib.gui.widgets.label_entry import LabelEntry
from nvlib.gui.widgets.my_string_var import MyStringVar
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.novx_globals import list_to_string
from nvlib.nv_globals import get_locale_date_str
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class ProjectView(ElementView):
    """Class for viewing and editing project properties."""
    _HELP_PAGE = 'book_view.html'
    _LABEL_WIDTH = 20
    # Width of left-placed labels.

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

        #--- Author entry.
        self._authorNameVar = MyStringVar()
        self._authorNameEntry = LabelEntry(
            self._elementInfoWindow,
            text=_('Author'),
            textvariable=self._authorNameVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._authorNameEntry.pack(anchor='w')
        inputWidgets.append(self._authorNameEntry)

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal',
        ).pack(fill='x')

        #--- "Language settings" frame.
        self._languageFrame = FoldingFrame(
            self._elementInfoWindow,
            _('Document language'),
            self._toggle_language_frame,
        )

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal',
        ).pack(fill='x')

        # Language and country code.

        # Locale  preview.
        self._localePreviewVar = MyStringVar()
        localePreview = ttk.Label(
            self._languageFrame.titleBar,
            textvariable=self._localePreviewVar,
        )
        localePreview.pack(side='left', padx=2)
        localePreview.bind('<Button-1>', self._toggle_language_frame,)

        self._languageCodeVar = MyStringVar()
        self._languageCodeEntry = LabelEntry(
            self._languageFrame,
            text=_('Language code'),
            textvariable=self._languageCodeVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._languageCodeEntry.pack(anchor='w')
        inputWidgets.append(self._languageCodeEntry)

        self._countryCodeVar = MyStringVar()
        self._countryCodeEntry = LabelEntry(
            self._languageFrame,
            text=_('Country code'),
            textvariable=self._countryCodeVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._countryCodeEntry.pack(anchor='w')
        inputWidgets.append(self._countryCodeEntry)

        #--- "Auto numbering" frame.
        self._numberingFrame = FoldingFrame(
            self._elementInfoWindow,
            _('Auto numbering'),
            self._toggle_numbering_frame,
        )

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal',
        ).pack(fill='x')

        # Auto numbering  preview.
        self._numberingPreviewVar = MyStringVar()
        numberingPreview = ttk.Label(
            self._numberingFrame.titleBar,
            textvariable=self._numberingPreviewVar,
        )
        numberingPreview.pack(side='left', padx=2)
        numberingPreview.bind('<Button-1>', self._toggle_numbering_frame)

        # 'Auto number chapters...' checkbox.
        self._renumberChaptersVar = tk.BooleanVar(value=False)
        self._renumberChaptersCheckbox = ttk.Checkbutton(
            self._numberingFrame,
            text=_('Auto number chapters when refreshing the tree'),
            variable=self._renumberChaptersVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._renumberChaptersCheckbox.pack(anchor='w')
        inputWidgets.append(self._renumberChaptersCheckbox)

        # 'Chapter number prefix' entry.
        self._chapterHeadingPrefixVar = MyStringVar()
        self._chapterHeadingPrefixEntry = LabelEntry(
            self._numberingFrame,
            text=_('Chapter number prefix'),
            textvariable=self._chapterHeadingPrefixVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._chapterHeadingPrefixEntry.pack(anchor='w')
        inputWidgets.append(self._chapterHeadingPrefixEntry)

        # 'Chapter number suffix' entry.
        self._chapterHeadingSuffixVar = MyStringVar()
        self._chapterHeadingSuffixEntry = LabelEntry(
            self._numberingFrame,
            text=_('Chapter number suffix'),
            textvariable=self._chapterHeadingSuffixVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._chapterHeadingSuffixEntry.pack(anchor='w')
        inputWidgets.append(self._chapterHeadingSuffixEntry)

        # 'Use Roman chapter numbers' checkbox.
        self.romanChapterNumbersVar = tk.BooleanVar()
        self._romanChapterNumbersCheckbox = ttk.Checkbutton(
            self._numberingFrame,
            text=_('Use Roman chapter numbers'),
            variable=self.romanChapterNumbersVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._romanChapterNumbersCheckbox.pack(anchor='w')
        inputWidgets.append(self._romanChapterNumbersCheckbox)

        # 'Reset chapter number..." checkbox
        self._renumberWithinPartsVar = tk.BooleanVar()
        self._renumberWithinPartsCheckbox = ttk.Checkbutton(
            self._numberingFrame,
            text=_('Restart chapter numbering at part beginning'),
            variable=self._renumberWithinPartsVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._renumberWithinPartsCheckbox.pack(anchor='w')
        inputWidgets.append(self._renumberWithinPartsCheckbox)

        # 'Auto number parts' checkbox.
        self._renumberPartsVar = tk.BooleanVar()
        self._renumberPartsCheckbox = ttk.Checkbutton(
            self._numberingFrame,
            text=_('Auto number parts when refreshing the tree'),
            variable=self._renumberPartsVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._renumberPartsCheckbox.pack(anchor='w')
        inputWidgets.append(self._renumberPartsCheckbox)

        # 'Part number prefix' entry.
        self._partHeadingPrefixVar = MyStringVar()
        self._partHeadingPrefixEntry = LabelEntry(
            self._numberingFrame,
            text=_('Part number prefix'),
            textvariable=self._partHeadingPrefixVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._partHeadingPrefixEntry.pack(anchor='w')
        inputWidgets.append(self._partHeadingPrefixEntry)

        # 'Part number suffix' entry.
        self._partHeadingSuffixVar = MyStringVar()
        self._partHeadingSuffixEntry = LabelEntry(
            self._numberingFrame,
            text=_('Part number suffix'),
            textvariable=self._partHeadingSuffixVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._partHeadingSuffixEntry.pack(anchor='w')
        inputWidgets.append(self._partHeadingSuffixEntry)

        # 'Use Roman part numbers' checkbox.
        self._romanPartNumbersVar = tk.BooleanVar()
        self._romanPartNumbersCheckbox = ttk.Checkbutton(
            self._numberingFrame,
            text=_('Use Roman part numbers'),
            variable=self._romanPartNumbersVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._romanPartNumbersCheckbox.pack(anchor='w')
        inputWidgets.append(self._romanPartNumbersCheckbox)

        #--- "Renamings" frame.
        self._renamingsFrame = FoldingFrame(
            self._elementInfoWindow, _('Renamings'),
            self._toggle_renamings_frame,
        )

        # Renamings  preview.
        self._renamingsPreviewVar = MyStringVar()
        renamingsPreview = ttk.Label(
            self._renamingsFrame.titleBar,
            textvariable=self._renamingsPreviewVar,
        )
        renamingsPreview.pack(side='left', padx=2)
        renamingsPreview.bind('<Button-1>', self._toggle_renamings_frame)

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal',
        ).pack(fill='x')
        ttk.Label(
            self._renamingsFrame,
            text=_('Not a scene'),
        ).pack(anchor='w')

        # Custom 'Plot progress' entry.
        self._customPlotProgressVar = MyStringVar()
        self._customPlotProgressEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Plot progress'),
            textvariable=self._customPlotProgressVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._customPlotProgressEntry.pack(anchor='w')
        inputWidgets.append(self._customPlotProgressEntry)

        # Custom 'Characterization' entry.
        self._customCharacterizationVar = MyStringVar()
        self._customCharacterizationEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Characterization'),
            textvariable=self._customCharacterizationVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._customCharacterizationEntry.pack(anchor='w')
        inputWidgets.append(self._customCharacterizationEntry)

        # Custom 'World building' entry.
        self._customWorldBuildingVar = MyStringVar()
        self._customWorldBuildingEntry = LabelEntry(
            self._renamingsFrame,
            text=_('World building'),
            textvariable=self._customWorldBuildingVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._customWorldBuildingEntry.pack(anchor='w')
        inputWidgets.append(self._customWorldBuildingEntry)

        ttk.Separator(
            self._renamingsFrame,
            orient='horizontal',
        ).pack(fill='x', pady=5)
        ttk.Label(
            self._renamingsFrame,
            text=_('Other scene'),
        ).pack(anchor='w')

        # 'Opening' entry.
        self._customGoalVar = MyStringVar()
        self._customGoalEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Opening'),
            textvariable=self._customGoalVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._customGoalEntry.pack(anchor='w')
        inputWidgets.append(self._customGoalEntry)

        # 'Peak emotional moment' entry.
        self._customConflictVar = MyStringVar()
        self._customConflictEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Peak em. moment'),
            textvariable=self._customConflictVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._customConflictEntry.pack(anchor='w')
        inputWidgets.append(self._customConflictEntry)

        # 'Ending' entry.
        self._customOutcomeVar = MyStringVar()
        self._customOutcomeEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Ending'),
            textvariable=self._customOutcomeVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._customOutcomeEntry.pack(anchor='w')
        inputWidgets.append(self._customOutcomeEntry)

        ttk.Separator(
            self._renamingsFrame,
            orient='horizontal',
        ).pack(fill='x', pady=5)

        ttk.Label(
            self._renamingsFrame,
            text=_('Character'),
        ).pack(anchor='w'),

        # 'Bio' entry.
        self._customChrBioVar = MyStringVar()
        self._customChrBioEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Bio'),
            textvariable=self._customChrBioVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._customChrBioEntry.pack(anchor='w')
        inputWidgets.append(self._customChrBioEntry)

        # 'Goals' entry.
        self._customChrGoalsVar = MyStringVar()
        self._customChrGoalsEntry = LabelEntry(
            self._renamingsFrame,
            text=_('Goals'),
            textvariable=self._customChrGoalsVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._customChrGoalsEntry.pack(anchor='w')
        inputWidgets.append(self._customChrGoalsEntry)

        #--- "Story time" frame.
        self._narrativeTimeFrame = FoldingFrame(
            self._elementInfoWindow,
            _('Story time'),
            self._toggle_narrative_time_frame,
        )

        # Preview reference date.
        self._datePreviewVar = MyStringVar()
        datePreview = ttk.Label(
            self._narrativeTimeFrame.titleBar,
            textvariable=self._datePreviewVar,
        )
        datePreview.pack(side='left', padx=2)
        datePreview.bind('<Button-1>', self._toggle_narrative_time_frame)

        ttk.Separator(
            self._elementInfoWindow,
            orient='horizontal',
        ).pack(fill='x')

        # 'Reference date' entry.
        self._referenceDateVar = MyStringVar()
        self._referenceDateEntry = LabelEntry(
            self._narrativeTimeFrame,
            text=_('Reference date'),
            textvariable=self._referenceDateVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._referenceDateEntry.pack(anchor='w')
        inputWidgets.append(self._referenceDateEntry)

        # Locale reference date display.
        _displayDateFrame = ttk.Frame(self._narrativeTimeFrame)
        _displayDateFrame.pack(fill='x')
        ttk.Label(
            _displayDateFrame,
            width=self._LABEL_WIDTH,
        ).pack(side='left')
        self._displayDateVar = MyStringVar()
        ttk.Label(
            _displayDateFrame,
            textvariable=self._displayDateVar,
        ).pack(anchor='w')

        # Convert date/day buttons.
        self._datesToDaysButton = ttk.Button(
            self._narrativeTimeFrame,
            text=_('Convert dates to days'),
            command=self.dates_to_days,
        )
        self._datesToDaysButton.pack(
            side='left',
            fill='x',
            expand=True,
            padx=1,
            pady=2,
        )
        inputWidgets.append(self._datesToDaysButton)

        self._daysToDatesButton = ttk.Button(
            self._narrativeTimeFrame,
            text=_('Convert days to dates'),
            command=self.days_to_dates,
        )
        self._daysToDatesButton.pack(
            side='left',
            fill='x',
            expand=True,
            padx=1,
            pady=2,
        )
        inputWidgets.append(self._daysToDatesButton)

        #--- "Writing progress" frame.
        self._progressFrame = FoldingFrame(
            self._elementInfoWindow,
            _('Writing progress'),
            self._toggle_progress_frame
        )

        # Progress  preview.
        self._progressPreviewVar = MyStringVar()
        progressPreview = ttk.Label(
            self._progressFrame.titleBar,
            textvariable=self._progressPreviewVar,
        )
        progressPreview.pack(side='left', padx=2)
        progressPreview.bind('<Button-1>', self._toggle_progress_frame)

        # 'Log writing progress' checkbox.
        self._saveWordCountVar = tk.BooleanVar()
        self._saveWordCountEntry = ttk.Checkbutton(
            self._progressFrame,
            text=_('Log writing progress'),
            variable=self._saveWordCountVar,
            onvalue=True,
            offvalue=False,
            command=self.apply_changes,
        )
        self._saveWordCountEntry.pack(anchor='w')
        inputWidgets.append(self._saveWordCountEntry)

        ttk.Separator(
            self._progressFrame,
            orient='horizontal',
        ).pack(fill='x')

        # 'Words to write' entry.
        self._wordTargetVar = MyStringVar()
        self._wordTargetEntry = LabelEntry(
            self._progressFrame,
            text=_('Words to write'),
            textvariable=self._wordTargetVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._wordTargetEntry.pack(anchor='w')
        inputWidgets.append(self._wordTargetEntry)

        # 'Starting count' entry.
        self._wordCountStartVar = MyStringVar()
        self._wordCountStartEntry = LabelEntry(
            self._progressFrame,
            text=_('Starting count'),
            textvariable=self._wordCountStartVar,
            command=self.apply_changes,
            lblWidth=self._LABEL_WIDTH,
        )
        self._wordCountStartEntry.pack(anchor='w')
        inputWidgets.append(self._wordCountStartEntry)

        # 'Set actual wordcount as start' button.
        self._setInitialWcButton = ttk.Button(
            self._progressFrame,
            text=_('Set actual wordcount as start'),
            command=self.set_initial_wc,
        )
        self._setInitialWcButton.pack(pady=2)
        inputWidgets.append(self._setInitialWcButton)

        # 'Words written' display.
        self._wordsWrittenVar = MyStringVar()
        LabelDisp(
            self._progressFrame,
            text=_('Words written'),
            textvariable=self._wordsWrittenVar,
            lblWidth=self._LABEL_WIDTH,
        ).pack(anchor='w')

        ttk.Separator(
            self._progressFrame,
            orient='horizontal',
        ).pack(fill='x')

        self._totalUsedVar = MyStringVar()
        LabelDisp(
            self._progressFrame,
            text=_('Used'),
            textvariable=self._totalUsedVar,
            lblWidth=self._LABEL_WIDTH,
        ).pack(anchor='w')
        self._totalOutlineVar = MyStringVar()
        LabelDisp(
            self._progressFrame,
            text=_('Outline'),
            textvariable=self._totalOutlineVar,
            lblWidth=self._LABEL_WIDTH,
        ).pack(anchor='w')
        self._totalDraftVar = MyStringVar()
        LabelDisp(
            self._progressFrame,
            text=_('Draft'),
            textvariable=self._totalDraftVar,
            lblWidth=self._LABEL_WIDTH,
        ).pack(anchor='w')
        self._total1stEditVar = MyStringVar()
        LabelDisp(
            self._progressFrame,
            text=_('1st Edit'),
            textvariable=self._total1stEditVar,
            lblWidth=self._LABEL_WIDTH,
        ).pack(anchor='w')
        self._total2ndEditVar = MyStringVar()
        LabelDisp(
            self._progressFrame,
            text=_('2nd Edit'),
            textvariable=self._total2ndEditVar,
            lblWidth=self._LABEL_WIDTH,
        ).pack(anchor='w')
        self._totalDoneVar = MyStringVar()
        LabelDisp(
            self._progressFrame,
            text=_('Done'),
            textvariable=self._totalDoneVar,
            lblWidth=self._LABEL_WIDTH,
        ).pack(anchor='w')
        self._totalUnusedVar = MyStringVar()
        LabelDisp(
            self._progressFrame,
            text=_('Unused'),
            textvariable=self._totalUnusedVar,
            lblWidth=self._LABEL_WIDTH,
        ).pack(anchor='w')
        self._totalWordsVar = MyStringVar()
        LabelDisp(
            self._progressFrame,
            text=_('All'),
            textvariable=self._totalWordsVar,
            lblWidth=self._LABEL_WIDTH,
        ).pack(anchor='w')

        #--- 'phase' combobox.
        self._phaseVar = MyStringVar()
        self._phaseCombobox = LabelCombo(
            self._progressFrame,
            lblWidth=self._LABEL_WIDTH,
            text=_('Work phase'),
            textvariable=self._phaseVar,
            values=[],
            )
        self._phaseCombobox.pack(anchor='w')
        inputWidgets.append(self._phaseCombobox)
        self._phaseCombobox.bind('<Return>', self.apply_changes)

        #--- Cover display
        self._coverFile = None

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self.inputWidgets.append(widget)

        self._prefsShowLinks = 'show_pr_links'

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        super().apply_changes()

        # Author
        authorName = self._authorNameVar.get()
        if authorName:
            authorName = authorName.strip()
        self.element.authorName = authorName

        #--- "Language settings" frame.
        self.element.languageCode = self._languageCodeVar.get()
        self.element.countryCode = self._countryCodeVar.get()

        #--- "Auto numbering" frame.
        self.element.renumberChapters = self._renumberChaptersVar.get()
        self.element.renumberParts = self._renumberPartsVar.get()
        self.element.renumberWithinParts = self._renumberWithinPartsVar.get()
        self.element.romanChapterNumbers = self.romanChapterNumbersVar.get()
        self.element.romanPartNumbers = self._romanPartNumbersVar.get()
        self.element.saveWordCount = self._saveWordCountVar.get()

        #--- "Renamings" frame.
        self.element.chapterHeadingPrefix = self._chapterHeadingPrefixVar.get()
        self.element.chapterHeadingSuffix = self._chapterHeadingSuffixVar.get()
        self.element.partHeadingPrefix = self._partHeadingPrefixVar.get()
        self.element.partHeadingSuffix = self._partHeadingSuffixVar.get()
        self.element.customPlotProgress = self._customPlotProgressVar.get()
        self.element.customCharacterization = (
            self._customCharacterizationVar.get()
        )
        self.element.customWorldBuilding = self._customWorldBuildingVar.get()
        self.element.customGoal = self._customGoalVar.get()
        self.element.customConflict = self._customConflictVar.get()
        self.element.customOutcome = self._customOutcomeVar.get()
        self.element.customChrBio = self._customChrBioVar.get()
        self.element.customChrGoals = self._customChrGoalsVar.get()

        #--- "Story time" frame.
        refDateStr = self._referenceDateVar.get()
        if not refDateStr:
            self.element.referenceDate = None
        elif refDateStr != self.element.referenceDate:
            try:
                PyCalendar.verified_date(refDateStr)
            except ValueError:
                self._referenceDateVar.set(self.element.referenceDate)
                self._ui.show_error(
                    message=_('Input rejected'),
                    detail=(
                        f'{_("Wrong date")}: "{refDateStr}"\n'
                        f'{_("Required")}: {PyCalendar.DATE_FORMAT}'
                    )
                )
            else:
                self.element.referenceDate = refDateStr

        #--- "Writing progress" frame.
        wordTargetStr = self._wordTargetVar.get()
        if wordTargetStr is None:
            self.element.wordTarget = None
        else:
            try:
                self.element.wordTarget = int(wordTargetStr)
            except (ValueError, TypeError):
                self._wordTargetVar.set(self.element.wordTarget)

        wordCountStartStr = self._wordCountStartVar.get()
        if wordCountStartStr is None:
            self.element.wordCountStart = 0
            self._wordCountStartVar.set('0')
        else:
            try:
                self.element.wordCountStart = int(wordCountStartStr)
            except (ValueError, TypeError):
                self._wordCountStartVar.set(self.element.wordCountStart)

        # Get work phase.
        if not self._phaseCombobox.current():
            entry = None
        else:
            entry = self._phaseCombobox.current()
        self.element.workPhase = entry

    def configure_display(self):
        """Expand or collapse the property frames."""
        super().configure_display()

        #--- "Language settings" frame.
        if prefs['show_language_settings']:
            self._languageFrame.show()
            self._localePreviewVar.set('')
        else:
            self._languageFrame.hide()
            if self.element.languageCode and self.element.countryCode:
                self._localePreviewVar.set(
                    f'{self.element.languageCode}-{self.element.countryCode}')
            else:
                self._localePreviewVar.set('')

        #--- "Auto numbering" frame.
        if prefs['show_auto_numbering']:
            self._numberingFrame.show()
            self._numberingPreviewVar.set('')
        else:
            self._numberingFrame.hide()
            renumberings = []
            if self.element.renumberChapters:
                renumberings.append(_('Chapters'))
            if self.element.renumberParts:
                renumberings.append(_('Parts'))
            self._numberingPreviewVar.set(
                list_to_string(renumberings, divider=f' {_("and")} ')
                )

        #--- "Renamings" frame.
        if prefs['show_renamings']:
            self._renamingsFrame.show()
            self._renamingsPreviewVar.set('')
        else:
            self._renamingsFrame.hide()
            renamings = []
            if (self.element.customPlotProgress
                or self.element.customCharacterization
                or self.element.customWorldBuilding
            ):
                renamings.append(_('Not a scene'))
            if (self.element.customGoal
                or self.element.customConflict
                or self.element.customOutcome
            ):
                renamings.append(_('Other scene'))
            if (self.element.customChrBio
                or self.element.customChrGoals
            ):
                renamings.append(_('Character'))
            self._renamingsPreviewVar.set(
                list_to_string(renamings, divider='/')
                )

        #--- "Story time" frame
        displayDate = []
        datePreview = []
        if (self.element.referenceDate is not None
            and self.element.referenceWeekDay is not None
        ):
            dispWeekday = PyCalendar.WEEKDAYS[self.element.referenceWeekDay]
            dispDate = get_locale_date_str(self.element.referenceDate)
            displayDate.append(dispWeekday)
            displayDate.append(dispDate)
            datePreview.append(_('Reference date'))
            datePreview.append(dispWeekday)
            datePreview.append(dispDate)

        if prefs['show_narrative_time']:
            self._narrativeTimeFrame.show()
            self._displayDateVar.set(list_to_string(displayDate, divider=' '))
            self._datePreviewVar.set('')
        else:
            self._narrativeTimeFrame.hide()
            self._displayDateVar.set('')
            self._datePreviewVar.set(list_to_string(datePreview, divider=' '))

        #--- "Writing progress" frame.
        wordsWritten = None
        wordPercentage = None

        if (self.element.wordTarget is not None
            and self.element.wordCountStart is not None
        ):
            try:
                wordsWritten = self._mdl.wordCount - self.element.wordCountStart
                wordPercentage = round(
                    100 * wordsWritten / self.element.wordTarget
                )
            except Exception:
                pass

        wordsWrittenDisp = []
        progressPreview = []
        if wordsWritten is not None:
            wordsWrittenDisp.append(str(wordsWritten))
        if wordPercentage is not None:
            wordsWrittenDisp.append(f'({wordPercentage}%)')
            progressPreview.append(f'{wordPercentage}%')

        if prefs['show_writing_progress']:
            self._progressFrame.show()
            self._progressPreviewVar.set('')
            self._wordsWrittenVar.set(
                list_to_string(wordsWrittenDisp, divider=' ')
            )
        else:
            self._progressFrame.hide()
            self._wordsWrittenVar.set('')
            if not self.element.saveWordCount:
                progressPreview.append(_('Logging is off'))
            self._progressPreviewVar.set(
                list_to_string(progressPreview, divider=' - ')
            )

    def dates_to_days(self):
        """Convert specific section dates to days."""
        buttonText = self._datesToDaysButton['text']
        self._datesToDaysButton['text'] = _('Please wait ...')
        # changing the button text is less time consuming
        # than showing a progress bar
        if self._mdl.novel.referenceDate:
            if self._ui.ask_yes_no(
                message=_('Convert all section dates to days relative to the reference date?'),
                detail=(
                    f"{_('Day 0')}: "
                    f"{PyCalendar.WEEKDAYS[self.element.referenceWeekDay]} "
                    f"{get_locale_date_str(self.element.referenceDate)}"
                )
            ):
                self._doNotUpdate = True
                for scId in self._mdl.novel.sections:
                    self._mdl.novel.sections[scId].date_to_day(
                        self._mdl.novel.referenceDate
                    )
                self._doNotUpdate = False
        else:
            self._report_missing_reference_date()
        self._datesToDaysButton['text'] = buttonText

    def days_to_dates(self):
        """Convert section days to specific dates."""
        buttonText = self._daysToDatesButton['text']
        self._daysToDatesButton['text'] = _('Please wait ...')
        # changing the button text is less time consuming
        # than showing a progress bar
        if self._mdl.novel.referenceDate:
            if self._ui.ask_yes_no(
                message=_('Convert all section days to dates using the reference date?'),
                detail=(
                    f"{_('Day 0')}: "
                    f"{PyCalendar.WEEKDAYS[self.element.referenceWeekDay]} "
                    f"{get_locale_date_str(self.element.referenceDate)}"
                )
            ):
                self._doNotUpdate = True
                for scId in self._mdl.novel.sections:
                    self._mdl.novel.sections[scId].day_to_date(
                        self._mdl.novel.referenceDate
                    )
                self._doNotUpdate = False
        else:
            self._report_missing_reference_date()
        self._daysToDatesButton['text'] = buttonText

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel
        super().set_data(elementId)

        #--- Author entry.
        self._authorNameVar.set(self.element.authorName)

        #--- "Language settings" frame.

        self._languageCodeVar.set(self.element.languageCode)
        self._countryCodeVar.set(self.element.countryCode)

        #--- "Auto numbering" frame.

        # "Auto number chapters" checkbox.
        if self.element.renumberChapters:
            self._renumberChaptersVar.set(True)
        else:
            self._renumberChaptersVar.set(False)
            # applies also to uninitialized values.

        # "Chapter number prefix" entry.
        self._chapterHeadingPrefixVar.set(self.element.chapterHeadingPrefix)

        # "Chapter number suffix" entry.
        self._chapterHeadingSuffixVar.set(self.element.chapterHeadingSuffix)

        # "Use Roman chapter numbers" checkbox.
        if self.element.romanChapterNumbers:
            self.romanChapterNumbersVar.set(True)
        else:
            self.romanChapterNumbersVar.set(False)

        # "Reset chapter number..." checkbox
        if self.element.renumberWithinParts:
            self._renumberWithinPartsVar.set(True)
        else:
            self._renumberWithinPartsVar.set(False)

        # "Auto number parts" checkbox.
        if self.element.renumberParts:
            self._renumberPartsVar.set(True)
        else:
            self._renumberPartsVar.set(False)

        # "Part number prefix" entry.
        self._partHeadingPrefixVar.set(self.element.partHeadingPrefix)

        # "Part number suffix" entry.
        self._partHeadingSuffixVar.set(self.element.partHeadingSuffix)

        # "Use Roman part numbers" checkbox.
        if self.element.romanPartNumbers:
            self._romanPartNumbersVar.set(True)
        else:
            self._romanPartNumbersVar.set(False)

        #--- "Renamings" frame.
        self._customPlotProgressVar.set(self.element.customPlotProgress)
        self._customCharacterizationVar.set(
            self.element.customCharacterization
        )
        self._customWorldBuildingVar.set(self.element.customWorldBuilding)
        self._customGoalVar.set(self.element.customGoal)
        self._customConflictVar.set(self.element.customConflict)
        self._customOutcomeVar.set(self.element.customOutcome)
        self._customChrBioVar.set(self.element.customChrBio)
        self._customChrGoalsVar.set(self.element.customChrGoals)

        #--- "Story time" frame
        self._referenceDateVar.set(self.element.referenceDate)

        #--- "Writing progress" frame.

        # "Save word count" checkbox.
        if self.element.saveWordCount:
            self._saveWordCountVar.set(True)
        else:
            self._saveWordCountVar.set(False)

        # "Words to write" entry.
        self._wordTargetVar.set(self.element.wordTarget)

        # "Starting count" entry.
        self._wordCountStartVar.set(self.element.wordCountStart)

        # Status counts.
        normalWordsTotal, allWordsTotal = self._mdl.prjFile.count_words()
        self._totalWordsVar.set(allWordsTotal)
        self._totalUsedVar.set(normalWordsTotal)
        self._totalUnusedVar.set(allWordsTotal - normalWordsTotal)
        statusCounts = self._mdl.get_status_counts()
        self._totalOutlineVar.set(statusCounts[1])
        self._totalDraftVar.set(statusCounts[2])
        self._total1stEditVar.set(statusCounts[3])
        self._total2ndEditVar.set(statusCounts[4])
        self._totalDoneVar.set(statusCounts[5])

        # "Work phase" combobox.
        phases = [
            _('Undefined'),
            _('Outline'),
            _('Draft'),
            _('1st Edit'),
            _('2nd Edit'),
            _('Done'),
        ]
        self._phaseCombobox.configure(values=phases)
        try:
            workPhase = int(self.element.workPhase)
        except:
            workPhase = 0
        self._phaseVar.set(value=phases[workPhase])

    def set_initial_wc(self):
        """Set actual wordcount as start.
        
        Callback procedure for the related button.
        """
        self.element.wordCountStart = self._mdl.wordCount

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

    def _create_button_bar(self):
        self._buttonBar = ttk.Frame(self._propertiesFrame)
        self._buttonBar.pack(fill='x')

        # "Help" button.
        ttk.Button(
            self._buttonBar,
            text=_('Online help'),
            command=self._open_help,
        ).pack(side='left', fill='x', expand=True, padx=1, pady=2)

    def _create_cover_window(self):
        # Create a label for cover image display.
        self._cover = tk.Label(self._propertiesFrame)
        self._cover.pack()

    def _create_frames(self):
        # Template method for creating the frames in the right pane.
        self._create_index_card()
        self._create_element_info_window()
        self._create_links_window()
        self._add_separator()
        self._create_button_bar()
        self._create_cover_window()

    def _toggle_language_frame(self, event=None):
        # Hide/show the "Document language" frame.
        # Callback procedure for the FoldingFrame's button.
        if prefs['show_language_settings']:
            self._languageFrame.hide()
            prefs['show_language_settings'] = False
        else:
            self._languageFrame.show()
            prefs['show_language_settings'] = True
        self._toggle_folding_frame()

    def _toggle_narrative_time_frame(self, event=None):
        # Hide/show the "Story time" frame.
        # Callback procedure for the FoldingFrame's button.
        if prefs['show_narrative_time']:
            self._narrativeTimeFrame.hide()
            prefs['show_narrative_time'] = False
        else:
            self._narrativeTimeFrame.show()
            prefs['show_narrative_time'] = True
        self._toggle_folding_frame()

    def _toggle_numbering_frame(self, event=None):
        # Hide/show the "Auto numbering" frame.
        # Callback procedure for the FoldingFrame's button.
        if prefs['show_auto_numbering']:
            self._numberingFrame.hide()
            prefs['show_auto_numbering'] = False
        else:
            self._numberingFrame.show()
            prefs['show_auto_numbering'] = True
        self._toggle_folding_frame()

    def _toggle_progress_frame(self, event=None):
        # Hide/show the "Writing progress" frame.
        # Callback procedure for the FoldingFrame's button.
        if prefs['show_writing_progress']:
            self._progressFrame.hide()
            prefs['show_writing_progress'] = False
        else:
            self._progressFrame.show()
            prefs['show_writing_progress'] = True
        self._toggle_folding_frame()

    def _toggle_renamings_frame(self, event=None):
        # Hide/show the "Renamings" frame.
        # Callback procedure for the FoldingFrame's button.
        if prefs['show_renamings']:
            self._renamingsFrame.hide()
            prefs['show_renamings'] = False
        else:
            self._renamingsFrame.show()
            prefs['show_renamings'] = True
        self._toggle_folding_frame()


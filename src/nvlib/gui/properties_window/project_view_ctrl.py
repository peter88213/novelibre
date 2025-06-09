"""Provide a mixin class for controlling the project properties view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.properties_window.basic_view_ctrl import BasicViewCtrl
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.novx_globals import list_to_string
from nvlib.nv_globals import datestr
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class ProjectViewCtrl(BasicViewCtrl):
    """Class for viewing and editing project properties."""

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        super().apply_changes()

        # Author
        authorName = self.authorNameVar.get()
        if authorName:
            authorName = authorName.strip()
        self.element.authorName = authorName

        #--- "Language settings" frame.
        self.element.languageCode = self.languageCodeVar.get()
        self.element.countryCode = self.countryCodeVar.get()

        #--- "Auto numbering" frame.
        self.element.renumberChapters = self.renumberChaptersVar.get()
        self.element.renumberParts = self.renumberPartsVar.get()
        self.element.renumberWithinParts = self.renumberWithinPartsVar.get()
        self.element.romanChapterNumbers = self.romanChapterNumbersVar.get()
        self.element.romanPartNumbers = self.romanPartNumbersVar.get()
        self.element.saveWordCount = self.saveWordCountVar.get()

        #--- "Renamings" frame.
        self.element.chapterHeadingPrefix = self.chapterHeadingPrefixVar.get()
        self.element.chapterHeadingSuffix = self.chapterHeadingSuffixVar.get()
        self.element.partHeadingPrefix = self.partHeadingPrefixVar.get()
        self.element.partHeadingSuffix = self.partHeadingSuffixVar.get()
        self.element.customPlotProgress = self.customPlotProgressVar.get()
        self.element.customCharacterization = self.customCharacterizationVar.get()
        self.element.customWorldBuilding = self.customWorldBuildingVar.get()
        self.element.customGoal = self.customGoalVar.get()
        self.element.customConflict = self.customConflictVar.get()
        self.element.customOutcome = self.customOutcomeVar.get()
        self.element.customChrBio = self.customChrBioVar.get()
        self.element.customChrGoals = self.customChrGoalsVar.get()

        #--- "Narrative time" frame.
        refDateStr = self.referenceDateVar.get()
        if not refDateStr:
            self.element.referenceDate = None
        elif refDateStr != self.element.referenceDate:
            try:
                PyCalendar.verified_date(refDateStr)
            except ValueError:
                self.referenceDateVar.set(self.element.referenceDate)
                self._ui.show_error(
                    message=_('Input rejected'),
                    detail=f'{_("Wrong date")}: "{refDateStr}"\n{_("Required")}: {PyCalendar.DATE_FORMAT}'
                    )
            else:
                self.element.referenceDate = refDateStr

        #--- "Writing progress" frame.
        wordTargetStr = self.wordTargetVar.get()
        if wordTargetStr is None:
            self.element.wordTarget = None
        else:
            try:
                self.element.wordTarget = int(wordTargetStr)
            except (ValueError, TypeError):
                self.wordTargetVar.set(self.element.wordTarget)

        wordCountStartStr = self.wordCountStartVar.get()
        if wordCountStartStr is None:
            self.element.wordCountStart = 0
            self.wordCountStartVar.set('0')
        else:
            try:
                self.element.wordCountStart = int(wordCountStartStr)
            except (ValueError, TypeError):
                self.wordCountStartVar.set(self.element.wordCountStart)

        # Get work phase.
        if not self.phaseCombobox.current():
            entry = None
        else:
            entry = self.phaseCombobox.current()
        self.element.workPhase = entry

    def configure_display(self):
        """Expand or collapse the property frames."""
        super().configure_display()

        #--- "Language settings" frame.
        if prefs['show_language_settings']:
            self.languageFrame.show()
            self.localePreviewVar.set('')
        else:
            self.languageFrame.hide()
            if self.element.languageCode and self.element.countryCode:
                self.localePreviewVar.set(
                    f'{self.element.languageCode}-{self.element.countryCode}')
            else:
                self.localePreviewVar.set('')

        #--- "Auto numbering" frame.
        if prefs['show_auto_numbering']:
            self.numberingFrame.show()
            self.numberingPreviewVar.set('')
        else:
            self.numberingFrame.hide()
            renumberings = []
            if self.element.renumberChapters:
                renumberings.append(_('Chapters'))
            if self.element.renumberParts:
                renumberings.append(_('Parts'))
            self.numberingPreviewVar.set(
                list_to_string(renumberings, divider=f' {_("and")} ')
                )

        #--- "Renamings" frame.
        if prefs['show_renamings']:
            self.renamingsFrame.show()
            self.renamingsPreviewVar.set('')
        else:
            self.renamingsFrame.hide()
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
            self.renamingsPreviewVar.set(
                list_to_string(renamings, divider='/')
                )

        #--- "Narrative time" frame
        displayDate = []
        datePreview = []
        if (self.element.referenceDate is not None
            and self.element.referenceWeekDay is not None
        ):
            dispWeekday = PyCalendar.WEEKDAYS[self.element.referenceWeekDay]
            dispDate = datestr(self.element.referenceDate)
            displayDate.append(dispWeekday)
            displayDate.append(dispDate)
            datePreview.append(_('Reference date'))
            datePreview.append(dispWeekday)
            datePreview.append(dispDate)

        if prefs['show_narrative_time']:
            self.narrativeTimeFrame.show()
            self.displayDateVar.set(list_to_string(displayDate, divider=' '))
            self.datePreviewVar.set('')
        else:
            self.narrativeTimeFrame.hide()
            self.displayDateVar.set('')
            self.datePreviewVar.set(list_to_string(datePreview, divider=' '))

        #--- "Writing progress" frame.
        wordsWritten = None
        wordPercentage = None

        if (self.element.wordTarget is not None
            and self.element.wordCountStart is not None
        ):
            try:
                wordsWritten = self._mdl.wordCount - self.element.wordCountStart
                wordPercentage = round(100 * wordsWritten / self.element.wordTarget)
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
            self.progressFrame.show()
            self.progressPreviewVar.set('')
            self.wordsWrittenVar.set(
                list_to_string(wordsWrittenDisp, divider=' ')
            )
        else:
            self.progressFrame.hide()
            self.wordsWrittenVar.set('')
            if not self.element.saveWordCount:
                progressPreview.append(_('Logging is off'))
            self.progressPreviewVar.set(
                list_to_string(progressPreview, divider=' - ')
            )

    def dates_to_days(self):
        """Convert specific section dates to days."""
        buttonText = self.datesToDaysButton['text']
        self.datesToDaysButton['text'] = _('Please wait ...')
        # changing the button text is less time consuming than showing a progress bar
        if self._mdl.novel.referenceDate:
            if self._ui.ask_yes_no(
                message=_('Convert all section dates to days relative to the reference date?'),
                detail=f"{_('Day 0')}: {PyCalendar.WEEKDAYS[self.element.referenceWeekDay]} {datestr(self.element.referenceDate)}"
            ):
                self.doNotUpdate = True
                for scId in self._mdl.novel.sections:
                    self._mdl.novel.sections[scId].date_to_day(self._mdl.novel.referenceDate)
                self.doNotUpdate = False
        else:
            self._report_missing_reference_date()
        self.datesToDaysButton['text'] = buttonText

    def days_to_dates(self):
        """Convert section days to specific dates."""
        buttonText = self.daysToDatesButton['text']
        self.daysToDatesButton['text'] = _('Please wait ...')
        # changing the button text is less time consuming than showing a progress bar
        if self._mdl.novel.referenceDate:
            if self._ui.ask_yes_no(
                message=_('Convert all section days to dates using the reference date?'),
                detail=f"{_('Day 0')}: {PyCalendar.WEEKDAYS[self.element.referenceWeekDay]} {datestr(self.element.referenceDate)}"
            ):
                self.doNotUpdate = True
                for scId in self._mdl.novel.sections:
                    self._mdl.novel.sections[scId].day_to_date(self._mdl.novel.referenceDate)
                self.doNotUpdate = False
        else:
            self._report_missing_reference_date()
        self.daysToDatesButton['text'] = buttonText

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel
        super().set_data(elementId)

        #--- Author entry.
        self.authorNameVar.set(self.element.authorName)

        #--- "Language settings" frame.

        self.languageCodeVar.set(self.element.languageCode)
        self.countryCodeVar.set(self.element.countryCode)

        #--- "Auto numbering" frame.

        # "Auto number chapters" checkbox.
        if self.element.renumberChapters:
            self.renumberChaptersVar.set(True)
        else:
            self.renumberChaptersVar.set(False)
            # applies also to uninitialized values.

        # "Chapter number prefix" entry.
        self.chapterHeadingPrefixVar.set(self.element.chapterHeadingPrefix)

        # "Chapter number suffix" entry.
        self.chapterHeadingSuffixVar.set(self.element.chapterHeadingSuffix)

        # "Use Roman chapter numbers" checkbox.
        if self.element.romanChapterNumbers:
            self.romanChapterNumbersVar.set(True)
        else:
            self.romanChapterNumbersVar.set(False)

        # "Reset chapter number..." checkbox
        if self.element.renumberWithinParts:
            self.renumberWithinPartsVar.set(True)
        else:
            self.renumberWithinPartsVar.set(False)

        # "Auto number parts" checkbox.
        if self.element.renumberParts:
            self.renumberPartsVar.set(True)
        else:
            self.renumberPartsVar.set(False)

        # "Part number prefix" entry.
        self.partHeadingPrefixVar.set(self.element.partHeadingPrefix)

        # "Part number suffix" entry.
        self.partHeadingSuffixVar.set(self.element.partHeadingSuffix)

        # "Use Roman part numbers" checkbox.
        if self.element.romanPartNumbers:
            self.romanPartNumbersVar.set(True)
        else:
            self.romanPartNumbersVar.set(False)

        #--- "Renamings" frame.
        self.customPlotProgressVar.set(self.element.customPlotProgress)
        self.customCharacterizationVar.set(self.element.customCharacterization)
        self.customWorldBuildingVar.set(self.element.customWorldBuilding)
        self.customGoalVar.set(self.element.customGoal)
        self.customConflictVar.set(self.element.customConflict)
        self.customOutcomeVar.set(self.element.customOutcome)
        self.customChrBioVar.set(self.element.customChrBio)
        self.customChrGoalsVar.set(self.element.customChrGoals)

        #--- "Narrative time" frame
        self.referenceDateVar.set(self.element.referenceDate)

        #--- "Writing progress" frame.

        # "Save word count" checkbox.
        if self.element.saveWordCount:
            self.saveWordCountVar.set(True)
        else:
            self.saveWordCountVar.set(False)

        # "Words to write" entry.
        self.wordTargetVar.set(self.element.wordTarget)

        # "Starting count" entry.
        self.wordCountStartVar.set(self.element.wordCountStart)

        # Status counts.
        normalWordsTotal, allWordsTotal = self._mdl.prjFile.count_words()
        self.totalWordsVar.set(allWordsTotal)
        self.totalUsedVar.set(normalWordsTotal)
        self.totalUnusedVar.set(allWordsTotal - normalWordsTotal)
        statusCounts = self._mdl.get_status_counts()
        self.totalOutlineVar.set(statusCounts[1])
        self.totalDraftVar.set(statusCounts[2])
        self.total1stEditVar.set(statusCounts[3])
        self.total2ndEditVar.set(statusCounts[4])
        self.totalDoneVar.set(statusCounts[5])

        # "Work phase" combobox.
        phases = [_('Undefined'), _('Outline'), _('Draft'), _('1st Edit'), _('2nd Edit'), _('Done')]
        self.phaseCombobox.configure(values=phases)
        try:
            workPhase = int(self.element.workPhase)
        except:
            workPhase = 0
        self.phaseVar.set(value=phases[workPhase])

    def set_initial_wc(self):
        """Set actual wordcount as start.
        
        Callback procedure for the related button.
        """
        self.element.wordCountStart = self._mdl.wordCount


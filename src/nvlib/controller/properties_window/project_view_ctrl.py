"""Provide a mixin class for controlling the project properties view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date

from nvlib.controller.properties_window.basic_view_ctrl import BasicViewCtrl
from mvclib.widgets.my_string_var import MyStringVar
from nvlib.novx_globals import WEEKDAYS
from nvlib.novx_globals import _
from nvlib.nv_globals import datestr
from nvlib.nv_globals import prefs


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
        authorName = self._authorName.get()
        if authorName:
            authorName = authorName.strip()
        self.element.authorName = authorName

        #--- "Language settings" frame.
        self.element.languageCode = self._languageCode.get()
        self.element.countryCode = self._countryCode.get()

        #--- "Auto numbering" frame.
        self.element.renumberChapters = self._renumberChapters.get()
        self.element.renumberParts = self._renumberParts.get()
        self.element.renumberWithinParts = self._renumberWithinParts.get()
        self.element.romanChapterNumbers = self._romanChapterNumbers.get()
        self.element.romanPartNumbers = self._romanPartNumbers.get()
        self.element.saveWordCount = self._saveWordCount.get()

        #--- "Renamings" frame.
        self.element.chapterHeadingPrefix = self._chapterHeadingPrefix.get()
        self.element.chapterHeadingSuffix = self._chapterHeadingSuffix.get()
        self.element.partHeadingPrefix = self._partHeadingPrefix.get()
        self.element.partHeadingSuffix = self._partHeadingSuffix.get()
        self.element.customPlotProgress = self._customPlotProgress.get()
        self.element.customCharacterization = self._customCharacterization.get()
        self.element.customWorldBuilding = self._customWorldBuilding.get()
        self.element.customGoal = self._customGoal.get()
        self.element.customConflict = self._customConflict.get()
        self.element.customOutcome = self._customOutcome.get()
        self.element.customChrBio = self._customChrBio.get()
        self.element.customChrGoals = self._customChrGoals.get()

        #--- "Narrative time" frame.
        refDateStr = self._referenceDate.get()
        if not refDateStr:
            self.element.referenceDate = None
            self._referenceWeekDay.set('')
            self._localeDate.set('')
        elif refDateStr != self.element.referenceDate:
            try:
                date.fromisoformat(refDateStr)
            except ValueError:
                self._referenceDate.set(self.element.referenceDate)
                self._ui.show_error(
                    f'{_("Wrong date")}: "{refDateStr}"\n{_("Required")}: {_("YYYY-MM-DD")}',
                    title=_('Input rejected')
                    )
            else:
                self.element.referenceDate = refDateStr
                if self.element.referenceWeekDay is not None:
                    self._referenceWeekDay.set(WEEKDAYS[self.element.referenceWeekDay])
                else:
                    self._referenceWeekDay.set('')
                    self._localeDate.set('')

        #--- "Writing progress" frame.
        try:
            entry = self._wordTarget.get()
            # entry must be an integer
            if self.element.wordTarget or entry:
                if self.element.wordTarget != entry:
                    self.element.wordTarget = entry
        except:
            # entry is no integer
            pass
        try:
            entry = self._wordCountStart.get()
            # entry must be an integer
            if self.element.wordCountStart or entry:
                if self.element.wordCountStart != entry:
                    self.element.wordCountStart = entry
        except:
            # entry is no integer
            pass

        # Get work phase.
        if not self._phaseCombobox.current():
            entry = None
        else:
            entry = self._phaseCombobox.current()
        self.element.workPhase = entry

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        self.element = self._mdl.novel
        super().set_data(elementId)

        #--- Author entry.
        self._authorName.set(self.element.authorName)

        #--- "Language settings" frame.
        if prefs['show_language_settings']:
            self._languageFrame.show()
        else:
            self._languageFrame.hide()

        # 'Language code' entry.
        self._languageCode.set(self.element.languageCode)

        # 'Country code' entry.
        self._countryCode.set(self.element.countryCode)

        #--- "Auto numbering" frame.
        if prefs['show_auto_numbering']:
            self._numberingFrame.show()
        else:
            self._numberingFrame.hide()

        # 'Auto number chapters' checkbox.
        if self.element.renumberChapters:
            self._renumberChapters.set(True)
        else:
            self._renumberChapters.set(False)
            # applies also to uninitialized values.

        # 'Chapter number prefix' entry.
        self._chapterHeadingPrefix.set(self.element.chapterHeadingPrefix)

        # 'Chapter number suffix' entry.
        self._chapterHeadingSuffix = MyStringVar(value=self.element.chapterHeadingSuffix)

        # 'Use Roman chapter numbers' checkbox.
        if self.element.romanChapterNumbers:
            self._romanChapterNumbers.set(True)
        else:
            self._romanChapterNumbers.set(False)

        # 'Reset chapter number..." checkbox
        if self.element.renumberWithinParts:
            self._renumberWithinParts.set(True)
        else:
            self._renumberWithinParts.set(False)

        # 'Auto number parts' checkbox.
        if self.element.renumberParts:
            self._renumberParts.set(True)
        else:
            self._renumberParts.set(False)

        # 'Part number prefix' entry.
        self._partHeadingPrefix.set(self.element.partHeadingPrefix)

        # 'Part number suffix' entry.
        self._partHeadingSuffix.set(self.element.partHeadingSuffix)

        # 'Use Roman part numbers' checkbox.
        if self.element.romanPartNumbers:
            self._romanPartNumbers.set(True)
        else:
            self._romanPartNumbers.set(False)

        #--- "Renamings" frame.
        if prefs['show_renamings']:
            self._renamingsFrame.show()
        else:
            self._renamingsFrame.hide()

        self._customPlotProgress.set(self.element.customPlotProgress)
        self._customCharacterization.set(self.element.customCharacterization)
        self._customWorldBuilding.set(self.element.customWorldBuilding)
        self._customGoal.set(self.element.customGoal)
        self._customConflict.set(self.element.customConflict)
        self._customOutcome.set(self.element.customOutcome)
        self._customChrBio.set(self.element.customChrBio)
        self._customChrGoals.set(self.element.customChrGoals)

        #--- "Narrative time" frame
        if prefs['show_narrative_time']:
            self._narrativeTimeFrame.show()
        else:
            self._narrativeTimeFrame.hide()

        if self.element.referenceDate and self.element.referenceWeekDay is not None:
            self._referenceWeekDay.set(
                WEEKDAYS[self.element.referenceWeekDay]
                )
            self._localeDate.set(
                datestr(self.element.referenceDate)
                )
        else:
            self._referenceWeekDay.set('')
            self._localeDate.set('')
        self._referenceDate.set(self.element.referenceDate)

        #--- "Writing progress" frame.
        if prefs['show_writing_progress']:
            self._progressFrame.show()
        else:
            self._progressFrame.hide()

        # 'Save word count' checkbox.
        if self.element.saveWordCount:
            self._saveWordCount.set(True)
        else:
            self._saveWordCount.set(False)

        # 'Words to write' entry.
        if self.element.wordTarget is not None:
            self._wordTarget.set(self.element.wordTarget)
        else:
            self._wordTarget.set(0)

        # 'Starting count' entry.
        if self.element.wordCountStart is not None:
            self._wordCountStart.set(self.element.wordCountStart)
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
            workPhase = int(self.element.workPhase)
        except:
            workPhase = 0
        self._phase.set(value=phases[workPhase])

    def _set_initial_wc(self):
        """Set actual wordcount as start.
        
        Callback procedure for the related button.
        """
        self._wordCountStart.set(self._mdl.wordCount)

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
            self._show_missing_reference_date_message()
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
            self._show_missing_reference_date_message()
        self._daysToDatesButton['text'] = buttonText

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


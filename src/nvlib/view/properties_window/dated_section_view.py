"""Provide a tkinter based class for viewing and editing section properties with date and time.

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
from mvclib.widgets.label_entry import LabelEntry
from mvclib.widgets.my_string_var import MyStringVar
from novxlib.model.date_time_tools import get_specific_date
from novxlib.novx_globals import WEEKDAYS
from novxlib.novx_globals import _
from nvlib.nv_globals import datestr
from nvlib.nv_globals import get_section_date_str
from nvlib.nv_globals import prefs
from nvlib.view.properties_window.related_section_view import RelatedSectionView


class DatedSectionView(RelatedSectionView):
    """Class for viewing and editing section properties with date and time.

    Adds to the right pane:
    - A folding frame for date/time.
    """
    _DATE_TIME_LBL_X = 15
    # Width of left-placed labels.

    def __init__(self, parent, model, view, controller):
        """Initialize the view once before element data is available.
        
        Extends the superclass constructor.
        """
        super().__init__(parent, model, view, controller)
        inputWidgets = []

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

        for widget in inputWidgets:
            widget.bind('<FocusOut>', self.apply_changes)
            self._inputWidgets.append(widget)

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

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        super().apply_changes()

        #--- Section start.
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

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        self._element = self._mdl.novel.sections[elementId]
        super().set_data(elementId)

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


"""Provide a mixin class for controlling the section properties view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from datetime import datetime

from nvlib.gui.properties_window.basic_view_ctrl import BasicViewCtrl
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
from nvlib.nv_globals import datestr
from nvlib.nv_globals import get_section_date_str
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class SectionViewCtrl(BasicViewCtrl):

    def activate_arc_buttons(self, event=None):
        if self.element.scPlotLines:
            self.plotlineCollection.enable_buttons()
        else:
            self.plotlineCollection.disable_buttons()

    def activate_character_buttons(self, event=None):
        if self.element.characters:
            self.characterCollection.enable_buttons()
        else:
            self.characterCollection.disable_buttons()

    def activate_item_buttons(self, event=None):
        if self.element.items:
            self.itemCollection.enable_buttons()
        else:
            self.itemCollection.disable_buttons()

    def activate_location_buttons(self, event=None):
        if self.element.locations:
            self.locationCollection.enable_buttons()
        else:
            self.locationCollection.disable_buttons()

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        super().apply_changes()

        #--- Section start.

        # 'Tags' entry.
        self.element.tags = string_to_list(self.tagsVar.get())

        # Date and time are checked separately.
        # If an invalid date is entered, the old value is kept.
        # If an invalid time is entered, the old value is kept.
        # If a valid date is entered, the day is cleared, if any.
        # Otherwise, if a valid day is entered, the date is cleared, if any.

        # 'Date' entry.
        dateStr = self.startDateVar.get()
        if not dateStr:
            self.element.date = None
        elif dateStr != self.element.date:
            try:
                dateStr = PyCalendar.verified_date(dateStr)
            except ValueError:
                self.startDateVar.set(self.element.date)
                self._ui.show_error(
                    message=_('Input rejected'),
                    detail=f'{_("Wrong date")}: "{dateStr}"\n{_("Required")}: {PyCalendar.DATE_FORMAT}'
                    )
            else:
                self.element.date = dateStr

        # 'Time' entry.
        timeStr = self.startTimeVar.get()
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
                    self.startTimeVar.set(dispTime)
                    self._ui.show_error(
                        message=_('Input rejected'),
                        detail=f'{_("Wrong time")}: "{timeStr}"\n{_("Required")}: {PyCalendar.TIME_FORMAT}',
                        )
                else:
                    self.element.time = timeStr
                    dispTime = PyCalendar.display_time(self.element.time)
                    self.startTimeVar.set(dispTime)

        # 'Day' entry.
        if self.element.date:
            self.element.day = None
        else:
            self.change_day()

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
        lastsMinutesStr = self.lastsMinutesVar.get()
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
                    self.lastsMinutesVar.set(lastsMinutesStr)
                    newEntry = True

        # 'Duration hours' entry.
        daysLeft = 0
        lastsHoursStr = self.lastsHoursVar.get()
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
                    self.lastsHoursVar.set(lastsHoursStr)
                except ValueError:
                    wrongEntry = True
                else:
                    newEntry = True

        # 'Duration days' entry.
        lastsDaysStr = self.lastsDaysVar.get()
        if daysLeft or lastsDaysStr or self.element.lastsDays:
            if daysLeft or lastsDaysStr != self.element.lastsDays:
                try:
                    if lastsDaysStr:
                        daysLeft += int(lastsDaysStr)
                    if daysLeft > 0:
                        lastsDaysStr = str(daysLeft)
                    else:
                        lastsDaysStr = None
                    self.lastsDaysVar.set(lastsDaysStr)
                except ValueError:
                    wrongEntry = True
                else:
                    newEntry = True

        if wrongEntry:
            self.lastsMinutesVar.set(self.element.lastsMinutes)
            self.lastsHoursVar.set(self.element.lastsHours)
            self.lastsDaysVar.set(self.element.lastsDays)
            self._ui.show_error(
                message=_('Input rejected'),
                detail=f'{_("Wrong entry: number required")}.'
                )
        elif newEntry:
            self.element.lastsMinutes = lastsMinutesStr
            self.element.lastsHours = lastsHoursStr
            self.element.lastsDays = lastsDaysStr

        #--- 'Viewpoint' combobox.
        option = self.characterCombobox.current()
        if option >= 0:
            # Put the selected character at the first position of related characters.
            vpId = self._vpList[option]
            scCharacters = self.element.characters
            if scCharacters:
                    if vpId in scCharacters:
                        scCharacters.remove(vpId)
                    scCharacters.insert(0, vpId)
            else:
                scCharacters = [vpId]
            self.element.characters = scCharacters

        #--- 'Unused' checkbox.
        if self.isUnusedVar.get():
            self._ctrl.set_type_unused()
        else:
            self._ctrl.set_type_normal()
        if self.element.scType > 0:
            self.isUnusedVar.set(True)
            # adjustment for section in an unused chapter

        #--- 'Append to previous section' checkbox.
        self.element.appendToPrev = self.appendToPrevVar.get()

        #--- 'Plot line notes' text box.
        self.save_plot_notes()

        #--- 'Goal/Reaction' window.
        if self.goalWindow.hasChanged:
            self.element.goal = self.goalWindow.get_text()
        #--- 'Conflict/Dilemma' window.
        if self.conflictWindow.hasChanged:
            self.element.conflict = self.conflictWindow.get_text()

        #--- 'Outcome/Choice' window.
        if self.outcomeWindow.hasChanged:
            self.element.outcome = self.outcomeWindow.get_text()

    def auto_set_date(self):
        """Set section start to the end of the previous section."""
        prevScId = self._ui.tv.prev_node(self.elementId)
        if not prevScId:
            self._ui.show_error(
                message=_('Cannot generate date/time'),
                detail=f"{_('There is no previous section')}."
                )
            return

        newDate, newTime, newDay = self._mdl.novel.sections[prevScId].get_end_date_time()
        if newTime is None:
            self._ui.show_error(
                message=_('Cannot generate date/time'),
                detail=f"{_('The previous section has no time set')}."
                )
            return

        # self.doNotUpdate = True
        self.element.date = newDate
        self.element.time = newTime
        self.element.day = newDay
        # self.doNotUpdate = False
        self.startDateVar.set(newDate)
        self.startTimeVar.set(PyCalendar.display_time(newTime))
        self.startDayVar.set(newDay)

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

        try:
            refDateIso = self._mdl.novel.referenceDate
        except:
            refDateIso = date.isoformat(date.today())
        if self._mdl.novel.sections[nextScId].date:
            nextDateIso = self._mdl.novel.sections[nextScId].date
        elif self._mdl.novel.sections[nextScId].day:
            nextDateIso = PyCalendar.specific_date(self._mdl.novel.sections[nextScId].day, refDateIso)
        elif self.element.day:
            nextDateIso = self.element.day
        else:
            nextDateIso = refDateIso
        if self.element.date:
            thisDateIso = self.element.date
        elif self.element.day:
            thisDateIso = PyCalendar.specific_date(self.element.day, refDateIso)
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
        self.element.lastsDays = newDays
        self.element.lastsHours = newHours
        self.element.lastsMinutes = newMinutes
        self.doNotUpdate = False
        self.lastsDaysVar.set(newDays)
        self.lastsHoursVar.set(newHours)
        self.lastsMinutesVar.set(newMinutes)

    def change_day(self, event=None):
        # 'Day' entry. If valid, clear the start date.
        dayStr = self.startDayVar.get()
        if dayStr or self.element.day:
            if dayStr != self.element.day:
                if not dayStr:
                    self.element.day = None
                else:
                    try:
                        int(dayStr)
                    except ValueError:
                        self.startDayVar.set(self.element.day)
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

    def go_to_character(self, event=None):
        """Go to the character selected in the listbox."""
        try:
            selection = self.characterCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.characters[selection])

    def go_to_item(self, event=None):
        """Go to the item selected in the listbox."""
        try:
            selection = self.itemCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.items[selection])

    def go_to_location(self, event=None):
        """Go to the location selected in the listbox."""
        try:
            selection = self.locationCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.locations[selection])

    def go_to_plotline(self, event=None):
        """Go to the plot line selected in the listbox."""
        try:
            selection = self.plotlineCollection.cListbox.curselection()[0]
        except:
            return

        self._ui.tv.go_to_node(self.element.scPlotLines[selection])

    def on_select_plotline(self, selection):
        """Callback routine for section plot line list selection."""
        self.save_plot_notes()
        self.selectedPlotline = self.element.scPlotLines[selection]
        self.plotNotesWindow.config(state='normal')
        if self.element.plotlineNotes:
            self.plotNotesWindow.set_text(self.element.plotlineNotes.get(self.selectedPlotline, ''))
        else:
            self.plotNotesWindow.clear()
        if self._isLocked:
            self.plotNotesWindow.config(state='disabled')
        self.plotNotesWindow.config(bg='white')

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
        """Remove the character selected in the listbox from the section characters."""
        try:
            selection = self.characterCollection.cListbox.curselection()[0]
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
            selection = self.itemCollection.cListbox.curselection()[0]
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
        """Remove the location selected in the listbox from the section locations."""
        try:
            selection = self.locationCollection.cListbox.curselection()[0]
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
        """Remove the plot line selected in the listbox from the section associations."""
        try:
            selection = self.plotlineCollection.cListbox.curselection()[0]
        except:
            return

        plId = self.element.scPlotLines[selection]
        if not self._ui.ask_yes_no(
            message=_('Remove plot line from the list?'),
            detail=f"({self._mdl.novel.plotLines[plId].shortName}) {self._mdl.novel.plotLines[plId].title}"
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
                    # removing the plot line's plot point from the section's list
                    # Note: this doesn't trigger the refreshing method
                    self._mdl.novel.plotPoints[ppId].sectionAssoc = None
                    # un-assigning the section from the plot line's plot point

    def save_plot_notes(self):
        if self.selectedPlotline and self.plotNotesWindow.hasChanged:
            plotlineNotes = self.element.plotlineNotes
            if plotlineNotes is None:
                plotlineNotes = {}
            plotlineNotes[self.selectedPlotline] = self.plotNotesWindow.get_text()
            self.doNotUpdate = True
            self.element.plotlineNotes = plotlineNotes
            self.doNotUpdate = False

    def set_action_scene(self, event=None):
        self.goalLabel.config(text=_('Goal'))
        self.conflictLabel.config(text=_('Conflict'))
        self.outcomeLabel.config(text=_('Outcome'))
        self.element.scene = self.sceneVar.get()

    def set_custom_scene(self, event=None):
        if self.customGoalVar:
            self.goalLabel.config(text=self.customGoalVar)
        else:
            self.goalLabel.config(text=_('Opening'))

        if self.customConflictVar:
            self.conflictLabel.config(text=self.customConflictVar)
        else:
            self.conflictLabel.config(text=_('Peak emotional moment'))

        if self.customOutcomeVar:
            self.outcomeLabel.config(text=self.customOutcomeVar)
        else:
            self.outcomeLabel.config(text=_('Ending'))

        self.element.scene = self.sceneVar.get()

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass method.
        """
        self.element = self._mdl.novel.sections[elementId]
        super().set_data(elementId)

        # 'Tags' entry.
        self.tagsVar.set(list_to_string(self.element.tags))

        #--- Frame for 'Relationships'.
        if prefs['show_relationships']:
            self.relationFrame.show()
        else:
            self.relationFrame.hide()

        # 'Characters' window.
        self.crTitles = self._get_element_titles(self.element.characters, self._mdl.novel.characters)
        self.characterCollection.cList.set(self.crTitles)
        listboxSize = len(self.crTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self.characterCollection.cListbox.config(height=listboxSize)
        if not self.characterCollection.cListbox.curselection() or not self.characterCollection.cListbox.focus_get():
            self.characterCollection.disable_buttons()

        # 'Locations' window.
        self.lcTitles = self._get_element_titles(self.element.locations, self._mdl.novel.locations)
        self.locationCollection.cList.set(self.lcTitles)
        listboxSize = len(self.lcTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self.locationCollection.cListbox.config(height=listboxSize)
        if not self.locationCollection.cListbox.curselection() or not self.locationCollection.cListbox.focus_get():
            self.locationCollection.disable_buttons()

        # 'Items' window.
        self.itTitles = self._get_element_titles(self.element.items, self._mdl.novel.items)
        self.itemCollection.cList.set(self.itTitles)
        listboxSize = len(self.itTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self.itemCollection.cListbox.config(height=listboxSize)
        if not self.itemCollection.cListbox.curselection() or not self.itemCollection.cListbox.focus_get():
            self.itemCollection.disable_buttons()

        #--- Frame for date/time/duration.
        if self.element.date and self.element.weekDay is not None:
            self.weekDayVar.set(PyCalendar.WEEKDAYS[self.element.weekDay])
        elif self.element.day and self._mdl.novel.referenceWeekDay is not None:
            self.weekDayVar.set(PyCalendar.WEEKDAYS[(int(self.element.day) + self._mdl.novel.referenceWeekDay) % 7])
        else:
            self.weekDayVar.set('')
        self.startDateVar.set(self.element.date)
        if self.element.localeDate:
            displayDate = get_section_date_str(self.element)
        elif self.element.day:
            displayDate = f'{_("Day")} {self.element.day}'
        else:
            displayDate = ''
        self.localeDateVar.set(displayDate)

        # Remove the seconds for the display.
        if self.element.time:
            dispTime = PyCalendar.display_time(self.element.time)
        else:
            dispTime = ''
        self.startTimeVar.set(dispTime)

        self.startDayVar.set(self.element.day)
        self.lastsDaysVar.set(self.element.lastsDays)
        self.lastsHoursVar.set(self.element.lastsHours)
        self.lastsMinutesVar.set(self.element.lastsMinutes)

        #--- Frame for date/time.
        if prefs['show_date_time']:
            self.dateTimeFrame.show()
        else:
            self.dateTimeFrame.hide()

        #--- 'Viewpoint' combobox.
        charNames = []
        self._vpList = []
        for crId in self._mdl.novel.tree.get_children(CR_ROOT):
            charNames.append(self._mdl.novel.characters[crId].title)
            self._vpList.append(crId)
        self.characterCombobox.configure(values=charNames)
        if self.element.characters:
            vp = self._mdl.novel.characters[self.element.characters[0]].title
        else:
            vp = ''
        self.viewpointVar.set(value=vp)

        #--- 'Plot lines' listbox.
        self.plotlineTitles = self._get_plotline_titles(self.element.scPlotLines, self._mdl.novel.plotLines)
        self.plotlineCollection.cList.set(self.plotlineTitles)
        listboxSize = len(self.plotlineTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self.plotlineCollection.cListbox.config(height=listboxSize)
        if not self.plotlineCollection.cListbox.curselection() or not self.plotlineCollection.cListbox.focus_get():
            self.plotlineCollection.disable_buttons()

        #--- 'Plot notes' text box.
        self.plotNotesWindow.clear()
        self.plotNotesWindow.config(state='disabled')
        self.plotNotesWindow.config(bg='light gray')
        if self.plotlineTitles:
            self.plotlineCollection.cListbox.select_clear(0, 'end')
            self.plotlineCollection.cListbox.select_set('end')
            self.selectedPlotline = -1
            self.on_select_plotline(-1)
        else:
            self.selectedPlotline = None

        #--- "Plot points" label
        plotPointTitles = []
        for ppId in self.element.scPlotPoints:
            plId = self.element.scPlotPoints[ppId]
            plotPointTitles.append(f'{self._mdl.novel.plotLines[plId].shortName}: {self._mdl.novel.plotPoints[ppId].title}')
        self.plotPointsDisplay.config(text=list_to_string(plotPointTitles))

        #--- 'Unused' checkbox.
        if self.element.scType > 0:
            self.isUnusedVar.set(True)
        else:
            self.isUnusedVar.set(False)

        #--- 'Append to previous section' checkbox.
        self.appendToPrevVar.set(self.element.appendToPrev)

        # Customized Goal/Conflict/Outcome configuration.
        if self._mdl.novel.customPlotProgress:
            self.customPlotProgressVar = self._mdl.novel.customPlotProgress
        else:
            self.customPlotProgressVar = ''

        if self._mdl.novel.customCharacterization:
            self.customCharacterizationVar = self._mdl.novel.customCharacterization
        else:
            self.customCharacterizationVar = ''

        if self._mdl.novel.customWorldBuilding:
            self.customWorldBuildingVar = self._mdl.novel.customWorldBuilding
        else:
            self.customWorldBuildingVar = ''

        if self._mdl.novel.customGoal:
            self.customGoalVar = self._mdl.novel.customGoal
        else:
            self.customGoalVar = ''

        if self._mdl.novel.customConflict:
            self.customConflictVar = self._mdl.novel.customConflict
        else:
            self.customConflictVar = ''

        if self._mdl.novel.customOutcome:
            self.customOutcomeVar = self._mdl.novel.customOutcome
        else:
            self.customOutcomeVar = ''

        #--- Frame for 'Plot'.
        if prefs['show_plot']:
            self.plotFrame.show()
        else:
            self.plotFrame.hide()

        #--- Frame for 'Scene'.
        if prefs['show_scene']:
            self.sceneFrame.show()
        else:
            self.sceneFrame.hide()

        #--- Scene radiobuttons.
        self.sceneVar.set(self.element.scene)

        #--- 'Goal/Reaction' window.
        self.goalWindow.set_text(self.element.goal)

        #--- 'Conflict/Dilemma' window.
        self.conflictWindow.set_text(self.element.conflict)

        #--- 'Outcome/Choice' window.
        self.outcomeWindow.set_text(self.element.outcome)

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
        if self.customPlotProgressVar:
            self.goalLabel.config(text=self.customPlotProgressVar)
        else:
            self.goalLabel.config(text=_('Plot progress'))

        if self.customCharacterizationVar:
            self.conflictLabel.config(text=self.customCharacterizationVar)
        else:
            self.conflictLabel.config(text=_('Characterization'))

        if self.customWorldBuildingVar:
            self.outcomeLabel.config(text=self.customWorldBuildingVar)
        else:
            self.outcomeLabel.config(text=_('World building'))

        self.element.scene = self.sceneVar.get()

    def set_reaction_scene(self, event=None):
        self.goalLabel.config(text=_('Reaction'))
        self.conflictLabel.config(text=_('Dilemma'))
        self.outcomeLabel.config(text=_('Choice'))
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
            except:
                self._report_missing_date()
                return

        charList = []
        for crId in self.element.characters:
            birthDate = self._mdl.novel.characters[crId].birthDate
            deathDate = self._mdl.novel.characters[crId].deathDate
            try:
                years = PyCalendar.age(now, birthDate, deathDate)
                if years < 0:
                    years *= -1
                    suffix = _('years after death')
                else:
                    suffix = _('years old')
                charList.append(f'{self._mdl.novel.characters[crId].title}: {years} {suffix}')
            except:
                charList.append(f'{self._mdl.novel.characters[crId].title}: ({_("no data")})')

        if charList:
            self._ui.show_info(
                message=f'{_("Date")}: {datestr(now)}',
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
            message=f'{_("Date")}: {datestr(now)}',
            detail=f'{self._mdl.nvService.get_moon_phase_str(now)}',
            title=_("Moon phase")
            )

    def toggle_date(self, event=None):
        """Toggle specific/unspecific date."""
        if not self._mdl.novel.referenceDate:
            self._report_missing_reference_date()
            return

        self.doNotUpdate = True
        if self.element.date:
            self.element.date_to_day(self._mdl.novel.referenceDate)
        elif self.element.day:
            self.element.day_to_date(self._mdl.novel.referenceDate)
        else:
            self._report_missing_date()
            return

        self.doNotUpdate = False
        self.set_data(self.elementId)

    def unlock(self):
        """Enable plot line notes only if a plot line is selected."""
        super().unlock()
        if self.selectedPlotline is None:
            self.plotNotesWindow.config(state='disabled')

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

    def _get_element_titles(self, elemIds, elements):
        """Return a list of element titles.
        
        Positional arguments:
            elemIds -- list of element IDs.
            elements -- list of element objects.          
        """
        elemTitles = []
        if elemIds:
            for elemId in elemIds:
                try:
                    elemTitles.append(elements[elemId].title)
                except:
                    pass
        return elemTitles

    def _get_plotline_titles(self, elemIds, elements):
        """Return a list of plot line titles, preceded by the short names.
        
        Positional arguments:
            elemIds -- list of element IDs.
            elements -- list of element objects.          
        """
        elemTitles = []
        if elemIds:
            for elemId in elemIds:
                try:
                    elemTitles.append(f'({elements[elemId].shortName}) {elements[elemId].title}')
                except:
                    pass
        return elemTitles

    def _get_relation_id_list(self, newTitleStr, oldTitleStr, elements):
        """Return a list of valid IDs from a string containing semicolon-separated titles."""
        if newTitleStr or oldTitleStr:
            if oldTitleStr != newTitleStr:
                elemIds = []
                for elemTitle in string_to_list(newTitleStr):
                    for elemId in elements:
                        if elements[elemId].title == elemTitle:
                            elemIds.append(elemId)
                            break
                    else:
                        # No break occurred: there is no element with the specified title
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


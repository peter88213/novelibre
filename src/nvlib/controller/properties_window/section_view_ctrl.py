"""Provide a mixin class for controlling the section properties view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta

from nvlib.controller.properties_window.basic_view_ctrl import BasicViewCtrl
from nvlib.model.data.date_time_tools import get_age
from nvlib.model.data.date_time_tools import get_specific_date
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import WEEKDAYS
from nvlib.novx_globals import _
from nvlib.novx_globals import list_to_string
from nvlib.novx_globals import string_to_list
from nvlib.nv_globals import datestr
from nvlib.nv_globals import get_section_date_str
from nvlib.nv_globals import prefs


class SectionViewCtrl(BasicViewCtrl):

    def apply_changes(self, event=None):
        """Apply changes.
        
        Extends the superclass method.
        """
        if self.element is None:
            return

        super().apply_changes()

        #--- Section start.

        # 'Tags' entry.
        newTags = self.tags.get()
        if self.tagsStr or newTags:
            self.element.tags = string_to_list(newTags)

        # Date and time are checked separately.
        # If an invalid date is entered, the old value is kept.
        # If an invalid time is entered, the old value is kept.
        # If a valid date is entered, the day is cleared, if any.
        # Otherwise, if a valid day is entered, the date is cleared, if any.

        # 'Date' entry.
        dateStr = self._startDate.get()
        if not dateStr:
            self.element.date = None
        elif dateStr != self.element.date:
            try:
                date.fromisoformat(dateStr)
            except ValueError:
                self._startDate.set(self.element.date)
                self._ui.show_error(
                    f'{_("Wrong date")}: "{dateStr}"\n{_("Required")}: {_("YYYY-MM-DD")}',
                    title=_('Input rejected')
                    )
            else:
                self.element.date = dateStr

        # 'Time' entry.
        timeStr = self._startTime.get()
        if not timeStr:
            self.element.time = None
        else:
            if self.element.time:
                dispTime = self.element.time.rsplit(':', 1)[0]
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
                    self.element.time = timeStr
                    dispTime = self.element.time.rsplit(':', 1)[0]
                    self._startTime.set(dispTime)

        # 'Day' entry.
        if self.element.date:
            self.element.day = None
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
                    self._lastsMinutes.set(lastsMinutesStr)
                    newEntry = True

        # 'Duration hours' entry.
        daysLeft = 0
        lastsHoursStr = self._lastsHours.get()
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
                    self._lastsHours.set(lastsHoursStr)
                except ValueError:
                    wrongEntry = True
                else:
                    newEntry = True

        # 'Duration days' entry.
        lastsDaysStr = self._lastsDays.get()
        if daysLeft or lastsDaysStr or self.element.lastsDays:
            if daysLeft or lastsDaysStr != self.element.lastsDays:
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
            self._lastsMinutes.set(self.element.lastsMinutes)
            self._lastsHours.set(self.element.lastsHours)
            self._lastsDays.set(self.element.lastsDays)
            self._ui.show_error(f'{_("Wrong entry: number required")}.', title=_('Input rejected'))
        elif newEntry:
            self.element.lastsMinutes = lastsMinutesStr
            self.element.lastsHours = lastsHoursStr
            self.element.lastsDays = lastsDaysStr

        #--- 'Viewpoint' combobox.
        option = self._characterCombobox.current()
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
        if self._isUnused.get():
            self.element.scType = 1
        else:
            self.element.scType = 0

        #--- 'Append to previous section' checkbox.
        self.element.appendToPrev = self._appendToPrev.get()

        #--- 'Plot line notes' text box.
        self._save_plot_notes()

        #--- 'Goal/Reaction' window.
        if self._goalWindow.hasChanged:
            self.element.goal = self._goalWindow.get_text()
        #--- 'Conflict/Dilemma' window.
        if self._conflictWindow.hasChanged:
            self.element.conflict = self._conflictWindow.get_text()

        #--- 'Outcome/Choice' window.
        if self._outcomeWindow.hasChanged:
            self.element.outcome = self._outcomeWindow.get_text()

    def set_data(self, elementId):
        """Update the widgets with element's data.
        
        Extends the superclass constructor.
        """
        self.element = self._mdl.novel.sections[elementId]
        super().set_data(elementId)

        # 'Tags' entry.
        self.tagsStr = list_to_string(self.element.tags)
        self.tags.set(self.tagsStr)

        #--- Frame for 'Relationships'.
        if prefs['show_relationships']:
            self._relationFrame.show()
        else:
            self._relationFrame.hide()

        # 'Characters' window.
        self._crTitles = self._get_element_titles(self.element.characters, self._mdl.novel.characters)
        self._characterCollection.cList.set(self._crTitles)
        listboxSize = len(self._crTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._characterCollection.cListbox.config(height=listboxSize)
        if not self._characterCollection.cListbox.curselection() or not self._characterCollection.cListbox.focus_get():
            self._characterCollection.disable_buttons()

        # 'Locations' window.
        self._lcTitles = self._get_element_titles(self.element.locations, self._mdl.novel.locations)
        self._locationCollection.cList.set(self._lcTitles)
        listboxSize = len(self._lcTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._locationCollection.cListbox.config(height=listboxSize)
        if not self._locationCollection.cListbox.curselection() or not self._locationCollection.cListbox.focus_get():
            self._locationCollection.disable_buttons()

        # 'Items' window.
        self._itTitles = self._get_element_titles(self.element.items, self._mdl.novel.items)
        self._itemCollection.cList.set(self._itTitles)
        listboxSize = len(self._itTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._itemCollection.cListbox.config(height=listboxSize)
        if not self._itemCollection.cListbox.curselection() or not self._itemCollection.cListbox.focus_get():
            self._itemCollection.disable_buttons()

        #--- Frame for date/time/duration.
        if self.element.date and self.element.weekDay is not None:
            self._weekDay.set(WEEKDAYS[self.element.weekDay])
        elif self.element.day and self._mdl.novel.referenceWeekDay is not None:
            self._weekDay.set(WEEKDAYS[(int(self.element.day) + self._mdl.novel.referenceWeekDay) % 7])
        else:
            self._weekDay.set('')
        self._startDate.set(self.element.date)
        if self.element.localeDate:
            displayDate = get_section_date_str(self.element)
        elif self.element.day:
            displayDate = f'{_("Day")} {self.element.day}'
        else:
            displayDate = ''
        self._localeDate.set(displayDate)

        # Remove the seconds for the display.
        if self.element.time:
            dispTime = self.element.time.rsplit(':', 1)[0]
        else:
            dispTime = ''
        self._startTime.set(dispTime)

        self._startDay.set(self.element.day)
        self._lastsDays.set(self.element.lastsDays)
        self._lastsHours.set(self.element.lastsHours)
        self._lastsMinutes.set(self.element.lastsMinutes)

        #--- Frame for date/time.
        if prefs['show_date_time']:
            self._dateTimeFrame.show()
        else:
            self._dateTimeFrame.hide()

        #--- 'Viewpoint' combobox.
        charNames = []
        self._vpList = []
        for crId in self._mdl.novel.tree.get_children(CR_ROOT):
            charNames.append(self._mdl.novel.characters[crId].title)
            self._vpList.append(crId)
        self._characterCombobox.configure(values=charNames)
        if self.element.characters:
            vp = self._mdl.novel.characters[self.element.characters[0]].title
        else:
            vp = ''
        self._viewpoint.set(value=vp)

        #--- 'Plot lines' listbox.
        self._plotlineTitles = self._get_plotline_titles(self.element.scPlotLines, self._mdl.novel.plotLines)
        self._plotlineCollection.cList.set(self._plotlineTitles)
        listboxSize = len(self._plotlineTitles)
        if listboxSize > self._HEIGHT_LIMIT:
            listboxSize = self._HEIGHT_LIMIT
        self._plotlineCollection.cListbox.config(height=listboxSize)
        if not self._plotlineCollection.cListbox.curselection() or not self._plotlineCollection.cListbox.focus_get():
            self._plotlineCollection.disable_buttons()

        #--- 'Plot notes' text box.
        self._plotNotesWindow.clear()
        self._plotNotesWindow.config(state='disabled')
        self._plotNotesWindow.config(bg='light gray')
        if self._plotlineTitles:
            self._plotlineCollection.cListbox.select_clear(0, 'end')
            self._plotlineCollection.cListbox.select_set('end')
            self._selectedPlotline = -1
            self._on_select_plotline(-1)
        else:
            self._selectedPlotline = None

        #--- "Plot points" label
        plotPointTitles = []
        for ppId in self.element.scPlotPoints:
            plId = self.element.scPlotPoints[ppId]
            plotPointTitles.append(f'{self._mdl.novel.plotLines[plId].shortName}: {self._mdl.novel.plotPoints[ppId].title}')
        self._plotPointsDisplay.config(text=list_to_string(plotPointTitles))

        #--- 'Unused' checkbox.
        if self.element.scType > 0:
            self._isUnused.set(True)
        else:
            self._isUnused.set(False)

        #--- 'Append to previous section' checkbox.
        if self.element.appendToPrev:
            self._appendToPrev.set(True)
        else:
            self._appendToPrev.set(False)

        # Customized Goal/Conflict/Outcome configuration.
        if self._mdl.novel.customPlotProgress:
            self._customPlotProgress = self._mdl.novel.customPlotProgress
        else:
            self._customPlotProgress = ''

        if self._mdl.novel.customCharacterization:
            self._customCharacterization = self._mdl.novel.customCharacterization
        else:
            self._customCharacterization = ''

        if self._mdl.novel.customWorldBuilding:
            self._customWorldBuilding = self._mdl.novel.customWorldBuilding
        else:
            self._customWorldBuilding = ''

        if self._mdl.novel.customGoal:
            self._customGoal = self._mdl.novel.customGoal
        else:
            self._customGoal = ''

        if self._mdl.novel.customConflict:
            self._customConflict = self._mdl.novel.customConflict
        else:
            self._customConflict = ''

        if self._mdl.novel.customOutcome:
            self._customOutcome = self._mdl.novel.customOutcome
        else:
            self._customOutcome = ''

        #--- Frame for 'Plot'.
        if prefs['show_plot']:
            self._plotFrame.show()
        else:
            self._plotFrame.hide()

        #--- Frame for 'Scene'.
        if prefs['show_scene']:
            self._sceneFrame.show()
        else:
            self._sceneFrame.hide()

        #--- Scene radiobuttons.
        self._scene.set(self.element.scene)

        #--- 'Goal/Reaction' window.
        self._goalWindow.set_text(self.element.goal)

        #--- 'Conflict/Dilemma' window.
        self._conflictWindow.set_text(self.element.conflict)

        #--- 'Outcome/Choice' window.
        self._outcomeWindow.set_text(self.element.outcome)

        # Configure the labels.
        if self.element.scene == 3:
            self._set_custom_scene()
        elif self.element.scene == 2:
            self._set_reaction_scene()
        elif self.element.scene == 1:
            self._set_action_scene()
        else:
            self._set_not_applicable()

    def _add_character(self, event=None):
        # Add the selected element to the collection, if applicable.
        crList = self.element.characters
        crId = self._ui.tv.tree.selection()[0]
        if crId.startswith(CHARACTER_PREFIX) and not crId in crList:
            crList.append(crId)
            self.element.characters = crList

    def _add_item(self, event=None):
        # Add the selected element to the collection, if applicable.
        itList = self.element.items
        itId = self._ui.tv.tree.selection()[0]
        if itId.startswith(ITEM_PREFIX)and not itId in itList:
            itList.append(itId)
            self.element.items = itList

    def _add_location(self, event=None):
        # Add the selected element to the collection, if applicable.
        lcList = self.element.locations
        lcId = self._ui.tv.tree.selection()[0]
        if lcId.startswith(LOCATION_PREFIX)and not lcId in lcList:
            lcList.append(lcId)
            self.element.locations = lcList

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

    def _auto_set_date(self):
        """Set section start to the end of the previous section."""
        prevScId = self._ui.tv.prev_node(self.elementId)
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
        self.element.date = newDate
        self.element.time = newTime
        self.element.day = newDay
        # self.doNotUpdate = False
        self._startDate.set(newDate)
        self._startTime.set(newTime.rsplit(':', 1)[0])
        self._startDay.set(newDay)

    def _auto_set_duration(self):
        """Calculate section duration from the start of the next section."""

        def day_to_date(day, refDate):
            deltaDays = timedelta(days=int(day))
            return date.isoformat(refDate + deltaDays)

        nextScId = self._ui.tv.next_node(self.elementId)
        if not nextScId:
            return

        thisTimeIso = self.element.time
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
        elif self.element.day:
            nextDateIso = self.element.day
        else:
            nextDateIso = refDateIso
        if self.element.date:
            thisDateIso = self.element.date
        elif self.element.day:
            thisDateIso = day_to_date(self.element.day, refDate)
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
        self._lastsDays.set(newDays)
        self._lastsHours.set(newHours)
        self._lastsMinutes.set(newMinutes)

    def _clear_duration(self):
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
        if hasData and self._ui.ask_yes_no(_('Clear duration from this section?')):
            self.element.lastsDays = None
            self.element.lastsHours = None
            self.element.lastsMinutes = None

    def _change_day(self, event=None):
        # 'Day' entry. If valid, clear the start date.
            dayStr = self._startDay.get()
            if dayStr or self.element.day:
                if dayStr != self.element.day:
                    if not dayStr:
                        self.element.day = None
                    else:
                        try:
                            int(dayStr)
                        except ValueError:
                            self._startDay.set(self.element.day)
                            self._ui.show_error(
                                f'{_("Wrong entry: number required")}.',
                                title=_('Input rejected')
                                )
                        else:
                            self.element.day = dayStr
                            self.element.date = None

    def _clear_start(self):
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
        if hasData and self._ui.ask_yes_no(_('Clear date/time from this section?')):
            self.element.date = None
            self.element.time = None
            self.element.day = None

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
                        self._ui.show_error(f'{_("Wrong name")}: "{elemTitle}"', title=_('Input rejected'))
                return elemIds

        return None

    def _pick_character(self, event=None):
        """Enter the "add character" selection mode."""
        self._start_picking_mode(command=self._add_character)
        self._ui.tv.see_node(CR_ROOT)

    def _pick_item(self, event=None):
        """Enter the "add item" selection mode."""
        self._start_picking_mode(command=self._add_item)
        self._ui.tv.see_node(IT_ROOT)

    def _pick_location(self, event=None):
        """Enter the "add location" selection mode."""
        self._start_picking_mode(command=self._add_location)
        self._ui.tv.see_node(LC_ROOT)

    def _pick_plotline(self, event=None):
        """Enter the "add plot line" selection mode."""
        self._start_picking_mode(command=self._add_plotline)
        self._ui.tv.see_node(PL_ROOT)

    def _remove_character(self, event=None):
        """Remove the character selected in the listbox from the section characters."""
        try:
            selection = self._characterCollection.cListbox.curselection()[0]
        except:
            return

        crId = self.element.characters[selection]
        title = self._mdl.novel.characters[crId].title
        if self._ui.ask_yes_no(f'{_("Remove character")}: "{title}"?'):
            crList = self.element.characters
            del crList[selection]
            self.element.characters = crList

    def _remove_item(self, event=None):
        """Remove the item selected in the listbox from the section items."""
        try:
            selection = self._itemCollection.cListbox.curselection()[0]
        except:
            return

        itId = self.element.items[selection]
        title = self._mdl.novel.items[itId].title
        if self._ui.ask_yes_no(f'{_("Remove item")}: "{title}"?'):
            itList = self.element.items
            del itList[selection]
            self.element.items = itList

    def _remove_location(self, event=None):
        """Remove the location selected in the listbox from the section locations."""
        try:
            selection = self._locationCollection.cListbox.curselection()[0]
        except:
            return

        lcId = self.element.locations[selection]
        title = self._mdl.novel.locations[lcId].title
        if self._ui.ask_yes_no(f'{_("Remove location")}: "{title}"?'):
            lcList = self.element.locations
            del lcList[selection]
            self.element.locations = lcList

    def _remove_plotline(self, event=None):
        """Remove the plot line selected in the listbox from the section associations."""
        try:
            selection = self._plotlineCollection.cListbox.curselection()[0]
        except:
            return

        plId = self.element.scPlotLines[selection]
        title = self._mdl.novel.plotLines[plId].title
        if not self._ui.ask_yes_no(f'{_("Remove plot line")}: "{title}"?'):
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

    def _save_plot_notes(self):
        if self._selectedPlotline and self._plotNotesWindow.hasChanged:
            plotlineNotes = self.element.plotlineNotes
            if plotlineNotes is None:
                plotlineNotes = {}
            plotlineNotes[self._selectedPlotline] = self._plotNotesWindow.get_text()
            self.doNotUpdate = True
            self.element.plotlineNotes = plotlineNotes
            self.doNotUpdate = False

    def _show_ages(self, event=None):
        """Display the ages of the related characters."""
        if self.element.date is not None:
            now = self.element.date
        else:
            try:
                now = get_specific_date(
                    self.element.day,
                    self._mdl.novel.referenceDate
                    )
            except:
                self._show_missing_date_message()
                return

        charList = []
        for crId in self.element.characters:
            birthDate = self._mdl.novel.characters[crId].birthDate
            deathDate = self._mdl.novel.characters[crId].deathDate
            try:
                years = get_age(now, birthDate, deathDate)
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
                '\n'.join(charList),
                title=f'{_("Date")}: {datestr(now)}'
                )

    def unlock(self):
        """Enable plot line notes only if a plot line is selected."""
        super().unlock()
        if self._selectedPlotline is None:
            self._plotNotesWindow.config(state='disabled')

    def _set_action_scene(self, event=None):
        self._goalLabel.config(text=_('Goal'))
        self._conflictLabel.config(text=_('Conflict'))
        self._outcomeLabel.config(text=_('Outcome'))
        self.element.scene = self._scene.get()

    def _set_custom_scene(self, event=None):
        if self._customGoal:
            self._goalLabel.config(text=self._customGoal)
        else:
            self._goalLabel.config(text=_('Opening'))

        if self._customConflict:
            self._conflictLabel.config(text=self._customConflict)
        else:
            self._conflictLabel.config(text=_('Peak emotional moment'))

        if self._customOutcome:
            self._outcomeLabel.config(text=self._customOutcome)
        else:
            self._outcomeLabel.config(text=_('Ending'))

        self.element.scene = self._scene.get()

    def _set_not_applicable(self, event=None):
        if self._customPlotProgress:
            self._goalLabel.config(text=self._customPlotProgress)
        else:
            self._goalLabel.config(text=_('Plot progress'))

        if self._customCharacterization:
            self._conflictLabel.config(text=self._customCharacterization)
        else:
            self._conflictLabel.config(text=_('Characterization'))

        if self._customWorldBuilding:
            self._outcomeLabel.config(text=self._customWorldBuilding)
        else:
            self._outcomeLabel.config(text=_('World building'))

        self.element.scene = self._scene.get()

    def _set_reaction_scene(self, event=None):
        self._goalLabel.config(text=_('Reaction'))
        self._conflictLabel.config(text=_('Dilemma'))
        self._outcomeLabel.config(text=_('Choice'))
        self.element.scene = self._scene.get()

    def _show_moonphase(self, event=None):
        """Display the moon phase of the section start date."""
        if self.element.date is not None:
            now = self.element.date
        else:
            try:
                now = get_specific_date(
                    self.element.day,
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
        if self.element.date:
            self.element.date_to_day(self._mdl.novel.referenceDate)
        elif self.element.day:
            self.element.day_to_date(self._mdl.novel.referenceDate)
        else:
            self._show_missing_date_message()
            return

        self.doNotUpdate = False
        self.set_data(self.elementId)


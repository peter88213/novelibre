"""Provide a class for ODS plot grid import.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.section import Section
from nvlib.model.ods.duration_parser import DurationParser
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import GRID_SUFFIX, PL_ROOT
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.novx_globals import string_to_list
from nvlib.nv_locale import _
from nvlib.model.data.py_calendar import PyCalendar


class OdsRGrid(OdsReader):
    """ODS section list reader. """
    DESCRIPTION = _('Plot grid')
    SUFFIX = GRID_SUFFIX
    COLUMN_TITLES = [
        'Link',
        'Section',
        'Date',
        'Time',
        'Day',
        'Duration',
        'Title',
        'Description',
        'Viewpoint',
        'Tags',
        'Scene',
        'Goal',
        'Conflict',
        'Outcome',
        'Notes',
    ]
    _idPrefix = SECTION_PREFIX

    def read(self):
        """Parse the ODS file located at filePath, fetching the Section attributes contained.
        
        Extends the superclass method.
        """
        plotLines = self.novel.tree.get_children(PL_ROOT)
        self._columnTitles = self.COLUMN_TITLES[:]
        for plId in plotLines:
            self._columnTitles.append(plId)
        super().read()
        durationParser = DurationParser()
        for scId in self.novel.sections:

            #--- plot line notes
            for plId in plotLines:
                try:
                    odsPlotLineNotes = self._columns[plId][scId]
                except:
                    continue

                plotlineNotes = self.novel.sections[scId].plotlineNotes
                if not plotlineNotes:
                    plotlineNotes = {}
                plotlineNotes[plId] = odsPlotLineNotes.strip()
                self.novel.sections[scId].plotlineNotes = plotlineNotes
                if plotlineNotes[plId] and not plId in self.novel.sections[scId].scPlotLines:
                    scPlotLines = self.novel.sections[scId].scPlotLines
                    scPlotLines.append(plId)
                    self.novel.sections[scId].scPlotLines = scPlotLines
                    plSections = self.novel.plotLines[plId].sections
                    plSections.append(scId)
                    self.novel.plotLines[plId].sections = plSections

            #--- date
            try:
                scDate = self._columns['Date'][scId]
                self.novel.sections[scId].date = PyCalendar.verified_date(scDate)
            except:
                pass

            #--- time
            try:
                scTime = self._columns['Time'][scId]
                self.novel.sections[scId].time = PyCalendar.verified_time(scTime)
            except:
                pass

            #--- day
            try:
                day = self._columns['Day'][scId]
                int(day)
            except:
                pass
            else:
                self.novel.sections[scId].day = day.strip()

            #--- duration
            try:
                durationStr = self._columns['Duration'][scId]
                d, h, m = durationParser.get_duration(durationStr)
            except:
                pass
            else:
                self.novel.sections[scId].lastsDays = str(d)
                self.novel.sections[scId].lastsHours = str(h)
                self.novel.sections[scId].lastsMinutes = str(m)

            #--- title
            try:
                title = self._columns['Title'][scId]
            except:
                pass
            else:
                self.novel.sections[scId].title = title.strip()

            #--- desc
            try:
                desc = self._columns['Description'][scId]
            except:
                pass
            else:
                self.novel.sections[scId].desc = desc.strip()

            #--- viewpoint
            try:
                viewpoint = self._columns['Viewpoint'][scId]
            except:
                pass
            else:
                viewpoint = viewpoint.strip()

                # Get the vp character ID.
                vpId = None
                for crId in self.novel.characters:
                    if self.novel.characters[crId].title == viewpoint:
                        vpId = crId
                        break

                self.novel.sections[scId].viewpoint = vpId

            #--- tags
            try:
                tags = self._columns['Tags'][scId]
            except:
                pass
            else:
                if tags:
                    self.novel.sections[scId].tags = string_to_list(tags, divider=self._DIVIDER)
                elif tags is not None:
                    self.novel.sections[scId].tags = None

            #--- Scene
            try:
                ar = self._columns['Scene'][scId]
            except:
                pass
            else:
                if ar:
                    try:
                        self.novel.sections[scId].scene = Section.SCENE.index(ar)
                    except ValueError:
                        pass

            #--- goal
            try:
                goal = self._columns['Goal'][scId]
            except:
                pass
            else:
                self.novel.sections[scId].goal = goal.strip()

            #--- conflict
            try:
                conflict = self._columns['Conflict'][scId]
            except:
                pass
            else:
                self.novel.sections[scId].conflict = conflict.strip()

            #--- outcome
            try:
                outcome = self._columns['Outcome'][scId]
            except:
                pass
            else:
                self.novel.sections[scId].outcome = outcome.strip()

            #--- notes
            try:
                notes = self._columns['Notes'][scId]
            except:
                pass
            else:
                self.novel.sections[scId].notes = notes.strip()


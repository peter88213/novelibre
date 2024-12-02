"""Provide a class for ODS plot grid import.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date, time

from nvlib.model.data.section import Section
from nvlib.model.ods.ods_reader import OdsReader
from nvlib.novx_globals import GRID_SUFFIX, PL_ROOT
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.novx_globals import string_to_list
from nvlib.nv_locale import _


class OdsRGrid(OdsReader):
    """ODS section list reader. """
    DESCRIPTION = _('Plot grid')
    SUFFIX = GRID_SUFFIX
    _columnTitles = [
        'Link',
        'Section',
        'Date',
        'Time',
        'Day',
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
        for plId in plotLines:
            self._columnTitles.append(plId)
        super().read()
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
                date.fromisoformat(scDate)
            except:
                pass
            else:
                self.novel.sections[scId].date = scDate

            #--- time
            try:
                scTime = self._columns['Time'][scId]
                time.fromisoformat(scTime)
            except:
                pass
            else:
                self.novel.sections[scId].time = scTime

            #--- day
            try:
                day = self._columns['Day'][scId]
                int(day)
            except:
                pass
            else:
                self.novel.sections[scId].day = day.strip()

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

                if vpId is not None:
                    scCharacters = self.novel.sections[scId].characters
                    if scCharacters is None:
                        scCharacters = []

                    # Put the vp character ID at the first position.
                    if vpId in scCharacters:
                        scCharacters.remove(vpId)
                    scCharacters.insert(0, vpId)
                    self.novel.sections[scId].characters = scCharacters

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


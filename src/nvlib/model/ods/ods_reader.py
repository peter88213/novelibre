"""Provide an abstract ODS file reader class.

Other ODS file readers inherit from this class.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod

from nvlib.model.data.py_calendar import PyCalendar
from nvlib.model.file.file_export import FileExport
from nvlib.model.odf.odf_reader import OdfReader
from nvlib.model.ods.duration_parser import DurationParser
from nvlib.model.ods.ods_parser import OdsParser
from nvlib.novx_globals import MAJOR_MARKER
from nvlib.novx_globals import MINOR_MARKER
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import SCENE
from nvlib.novx_globals import string_to_list


class OdsReader(OdfReader, ABC):
    """Abstract OpenDocument spreadsheet document reader."""
    EXTENSION = '.ods'
    # overwrites File.EXTENSION
    _SEPARATOR = ','
    # delimits data fields within a record.
    _columnTitles = []
    _idPrefix = '??'

    _DIVIDER = FileExport._DIVIDER

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.

        Positional arguments:
            filePath: str -- path to the file 
            represented by the File instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self._columnDict = None
        # dict: {column title, {element ID, cell content}}
        self._rows = None
        # list of lists of cell contents
        self.parser = OdsParser()

    @abstractmethod
    def read(self):
        """Parse the file and get the instance variables.
        
        Parse the ODS file located at filePath, fetching the rows.

        Overrides the superclass method.
        """
        self._columnDict = {}
        cellsPerRow = len(self._columnTitles)
        self._rows = self.parser.get_rows(self.filePath, cellsPerRow)
        for title in self._rows[0]:
            self._columnDict[title] = {}
        for row in self._rows:
            if row[0].startswith(self._idPrefix):
                for i, col in enumerate(self._columnDict):
                    self._columnDict[col][row[0]] = row[i]

    def _read_basic_element(self, element, elemId):

        #--- name
        try:
            title = self._columnDict['Name'][elemId]
        except:
            pass
        else:
            element.title = title.rstrip()

        #--- desc
        try:
            desc = self._columnDict['Description'][elemId]
        except:
            pass
        else:
            element.desc = desc.rstrip()

    def _read_basic_element_notes(self, element, elemId):
        self._read_basic_element(element, elemId)

        #--- notes
        try:
            notes = self._columnDict['Notes'][elemId]
        except:
            pass
        else:
            element.notes = notes.rstrip()

    def _read_basic_element_tags(self, element, elemId):
        self._read_basic_element_notes(element, elemId)

        #--- tags
        try:
            tags = self._columnDict['Tags'][elemId]
        except:
            pass
        else:
            if tags:
                element.tags = string_to_list(
                    tags,
                    divider=self._DIVIDER,
                )

    def _read_chapters(self):
        for chId in self.novel.chapters:
            self._read_basic_element_notes(self.novel.chapters[chId], chId)

    def _read_characters(self):
        for crId in self.novel.characters:
            self._read_world_element(self.novel.characters[crId], crId)

            #--- fullName
            try:
                fullName = self._columnDict['Full name'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].fullName = fullName.rstrip()

            #--- bio
            try:
                bio = self._columnDict['Bio'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].bio = bio.rstrip()

            #--- goals
            try:
                goals = self._columnDict['Goals'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].goals = goals.rstrip()

            #--- birthDate
            try:
                birthDate = self._columnDict['Birth date'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].birthDate = birthDate.rstrip()

            #--- deathDate
            try:
                deathDate = self._columnDict['Death date'][crId]
            except:
                pass
            else:
                self.novel.characters[crId].deathDate = deathDate.rstrip()

            #--- importance
            try:
                importance = self._columnDict['Importance'][crId]
            except:
                pass
            else:
                if MAJOR_MARKER in importance:
                    self.novel.characters[crId].isMajor = True
                elif MINOR_MARKER in importance:
                    self.novel.characters[crId].isMajor = False

    def _read_items(self):
        for itId in self.novel.items:
            self._read_world_element(self.novel.items[itId], itId)

    def _read_locations(self):
        for lcId in self.novel.locations:
            self._read_world_element(self.novel.locations[lcId], lcId)

    def _read_plotlines(self):
        for plId in self.novel.plotLines:
            self._read_basic_element_notes(self.novel.plotLines[plId], plId)

    def _read_plot_points(self):
        for ppId in self.novel.plotPoints:
            self._read_basic_element_notes(self.novel.plotPoints[ppId], ppId)

    def _read_project_notes(self):
        for pnId in self.novel.projectNotes:
            self._read_basic_element(self.novel.projectNotes[pnId], pnId)

    def _read_sections(self):
        durationParser = DurationParser()
        for scId in self.novel.sections:
            self._read_basic_element_tags(self.novel.sections[scId], scId)

            #--- plot line notes
            for plId in self.novel.plotLines:
                try:
                    odsPlotLineNotes = self._columnDict[plId][scId]
                except:
                    continue

                plotlineNotes = self.novel.sections[scId].plotlineNotes
                if not plotlineNotes:
                    plotlineNotes = {}
                plotlineNotes[plId] = odsPlotLineNotes.strip()
                self.novel.sections[scId].plotlineNotes = plotlineNotes
                if (
                    plotlineNotes[plId]
                    and not plId in self.novel.sections[scId].scPlotLines
                ):
                    scPlotLines = self.novel.sections[scId].scPlotLines
                    scPlotLines.append(plId)
                    self.novel.sections[scId].scPlotLines = scPlotLines
                    plSections = self.novel.plotLines[plId].sections
                    plSections.append(scId)
                    self.novel.plotLines[plId].sections = plSections

            #--- date
            try:
                scDate = self._columnDict['Date'][scId]
                self.novel.sections[scId].date = PyCalendar.verified_date(
                    scDate)
            except:
                pass

            #--- time
            try:
                scTime = self._columnDict['Time'][scId]
                self.novel.sections[scId].time = PyCalendar.verified_time(
                    scTime)
            except:
                pass

            #--- day
            try:
                day = self._columnDict['Day'][scId]
                int(day)
            except:
                pass
            else:
                self.novel.sections[scId].day = day.strip()

            #--- duration
            try:
                durationStr = self._columnDict['Duration'][scId]
                d, h, m = durationParser.get_duration(durationStr)
            except:
                pass
            else:
                self.novel.sections[scId].lastsDays = str(d)
                self.novel.sections[scId].lastsHours = str(h)
                self.novel.sections[scId].lastsMinutes = str(m)

            #--- viewpoint
            try:
                viewpoint = self._columnDict['Viewpoint'][scId]
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

            #--- Scene
            try:
                ar = self._columnDict['Scene'][scId]
            except:
                pass
            else:
                if ar:
                    try:
                        self.novel.sections[scId].scene = SCENE.index(ar)
                    except ValueError:
                        pass

            #--- goal
            try:
                goal = self._columnDict['Goal'][scId]
            except:
                pass
            else:
                self.novel.sections[scId].goal = goal.strip()

            #--- conflict
            try:
                conflict = self._columnDict['Conflict'][scId]
            except:
                pass
            else:
                self.novel.sections[scId].conflict = conflict.strip()

            #--- outcome
            try:
                outcome = self._columnDict['Outcome'][scId]
            except:
                pass
            else:
                self.novel.sections[scId].outcome = outcome.strip()

    def _read_world_element(self, element, elemId):
        self._read_basic_element_tags(element, elemId)

        #--- aka
        try:
            aka = self._columnDict['Aka'][elemId]
        except:
            pass
        else:
            element.aka = aka.rstrip()


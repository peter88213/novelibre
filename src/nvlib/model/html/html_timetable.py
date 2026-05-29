"""Provide a class for a html time table representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.model.data.section import Section
from nvlib.model.html.html_table import HtmlTable
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import TIMETABLE_SUFFIX
from nvlib.novx_globals import list_to_string
from nvlib.nv_locale import _


class HtmlTimetable(HtmlTable):
    """html time table representation."""
    DESCRIPTION = _('HTML Time table')
    SUFFIX = TIMETABLE_SUFFIX

    def write(self):
        """Create a HTML table.
        
        Overwrites the superclass method.
        """

        # Collect the normal sections with a date/day/time.
        srtSections = self._sort_sections_by_date()
        if not srtSections:
            raise UserWarning(f'{_("No date/time data found")}.')

        htmlText = [self._fileHeader]
        htmlText.extend(self._get_plot_line_styles())

        # Build the HTML table.
        htmlText.append(
            f'<title>{_("Time table")} ({self.novel.title})</title>\n'
            '</head>\n'
            '<body>\n'
            f'<p class=title>{self.novel.title} {_("by")} '
            f'{self.novel.authorName} - {_("Time table")}</p>\n'
            '<table>'
        )

        # Title row.
        htmlText.append('<tr class="heading">')
        htmlText.append(self._new_cell(_('Date')))
        htmlText.append(self._new_cell(_('Time')))
        htmlText.append(self._new_cell(_('Section')))
        htmlText.append(self._new_cell(_('Description')))
        htmlText.append(self._new_cell(_('Duration')))
        htmlText.append(self._new_cell(_('Viewpoint')))
        htmlText.append(self._new_cell(_('Characters')))
        htmlText.append(self._new_cell(_('Locations')))
        htmlText.append(self._new_cell(_('Items')))
        plotLines = self.novel.tree.get_children(PL_ROOT)
        for plId in plotLines:
            htmlText.append(
                self._new_cell(
                    self.novel.plotLines[plId].title,
                    attr=f'class="h{plId}"',
                )
            )
        htmlText.append('</tr>')

        # Section rows.
        currentDateDayStr = ''
        for timestamp, scIds in srtSections:
            for scId in scIds:
                # Section row
                htmlText.append(f'<tr>')
                dateDayStr = (
                    f'{self._get_date_day_str(scId)} '
                    f'{self._get_week_day_str(scId, timestamp)}'
                )
                if dateDayStr != currentDateDayStr:
                    currentDateDayStr = dateDayStr
                else:
                    dateDayStr = ''
                htmlText.append(
                    self._new_cell(
                        dateDayStr
                    )
                )
                htmlText.append(
                    self._new_cell(
                        self._get_time_str(scId)
                    )
                )
                section = self.novel.sections[scId]
                color = section.color or '#ffffff'
                htmlText.append(
                    self._new_cell(
                        section.title,
                        attr=f'style="border-left: 0.5em solid {color}"'
                    )
                )
                htmlText.append(self._new_cell(section.desc))
                htmlText.append(
                    self._new_cell(PyCalendar.get_duration_str(section))
                )
                crId = self.novel.sections[scId].viewpoint
                if crId is not None:
                    vp = self.novel.characters[crId]
                    vpTitle = vp.title
                    color = vp.color or '#ffffff'
                    style = f'style="border-left: 0.5em solid {color}"'
                else:
                    vpTitle = ''
                    style = ''
                htmlText.append(self._new_cell(vpTitle, attr=style))
                htmlText.append(
                    self._new_cell(
                        self._get_relations_str(
                            section.characters,
                            self.novel.characters
                        )
                    )
                )
                htmlText.append(
                    self._new_cell(
                        self._get_relations_str(
                            section.locations,
                            self.novel.locations
                        )
                    )
                )
                htmlText.append(
                    self._new_cell(
                        self._get_relations_str(
                            section.items,
                            self.novel.items
                        )
                    )
                )
                for plId in plotLines:
                    if scId in self.novel.plotLines[plId].sections:
                        plNotes = self.novel.sections[scId].plotlineNotes.get(
                            plId,
                            ''
                        )
                        htmlText.append(
                            self._new_cell(
                                plNotes,
                                attr=f'class="{plId}"',
                            )
                        )
                    else:
                        htmlText.append(self._new_cell(''))
                htmlText.append(f'</tr>')
        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))

    def _get_date_day_str(self, scId):
        # Return a date/day string for the section defined by scId.
        if (
            self.novel.sections[scId].date is not None
            and self.novel.sections[scId].date != Section.NULL_DATE
        ):
            dateDayStr = self.novel.sections[scId].localeDate
        else:
            if self.novel.sections[scId].day is not None:
                dateDayStr = f'{_("Day")} {self.novel.sections[scId].day}'
            else:
                dateDayStr = ''
        return dateDayStr

    def _get_relations_str(self, relations, elements):
        # Return a comma-separated relation titles string.
        elementTitles = []
        for elemId in relations:
            elementTitles.append(elements[elemId].title)
        return list_to_string(elementTitles)

    def _get_time_str(self, scId):
        # Return a time string for the section defined by scId.
        if self.novel.sections[scId].time is not None:
            return PyCalendar.time_disp(self.novel.sections[scId].time)

        else:
            return ''

    def _get_week_day_str(self, scId, timestamp):
        # Return a week day or an empty string.
        if (
            not self.novel.sections[scId].date
            and not self.novel.referenceDate
        ):
            return ''

        return PyCalendar.weekday_str(timestamp)

    def _sort_sections_by_date(self):
        # Return a dictionary with lists of section IDs by timestamp.
        referenceDate = self.novel.referenceDate
        if not referenceDate:
            referenceDate = PyCalendar.min
        scIdsByDate = {}
        for scId in self.novel.sections:
            if self.novel.sections[scId].scType == 0:
                timestamp = PyCalendar.get_timestamp(
                    self.novel.sections[scId],
                    referenceDate,
                )
                if timestamp:
                    if not timestamp in scIdsByDate:
                        scIdsByDate[timestamp] = []
                    scIdsByDate[timestamp].append(scId)

        # Sort sections by timestamp.
        return sorted(scIdsByDate.items())

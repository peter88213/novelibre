"""Provide a class for a html plot grid representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.model.data.section import Section
from nvlib.model.html.html_table import HtmlTable
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import GRID_REPORT_SUFFIX
from nvlib.novx_globals import list_to_string
from nvlib.nv_locale import _


class HtmlGrid(HtmlTable):
    """html plot grid representation."""
    DESCRIPTION = f"HTML {_('Plot grid')}"
    SUFFIX = GRID_REPORT_SUFFIX

    def write(self):
        """Create a HTML table.
        
        Overwrites the superclass method.
        """

        # Collect the sections.
        srtSections = []
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].chType == 0:
                for scId in self.novel.tree.get_children(chId):
                    if self.novel.sections[scId].scType == 0:
                        srtSections.append(scId)

        if not srtSections:
            raise UserWarning(f'{_("No sections found")}.')

        htmlText = [self._fileHeader]
        htmlText.extend(self._get_plot_line_styles())

        # Build the HTML table.
        htmlText.append(
            f'<title>{_("Plot grid")} ({self.novel.title})</title>\n'
            '</head>\n'
            '<body>\n'
            f'<p class=title>{self.novel.title} {_("by")} '
            f'{self.novel.authorName} - {_("Plot grid")}</p>\n'
            '<table>'
        )

        # Title row.
        htmlText.append('<tr class="heading">')
        htmlText.append(self._new_cell(_('Date')))
        htmlText.append(self._new_cell(_('Time')))
        htmlText.append(self._new_cell(_('Duration')))
        htmlText.append(self._new_cell(_('Section')))
        htmlText.append(self._new_cell(_('Description')))
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
        for scId in srtSections:

            # Section row
            section = self.novel.sections[scId]
            htmlText.append(f'<tr>')
            htmlText.append(self._new_cell(self._get_date_day_str(scId)))
            htmlText.append(self._new_cell(self._get_time_str(scId)))
            htmlText.append(
                self._new_cell(PyCalendar.get_duration_str(section))
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


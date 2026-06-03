"""Provide a class for a html plot grid representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_plot_list import HtmlPlotList
from nvlib.model.html.html_table import HtmlTable
from nvlib.novx_globals import GRID_REPORT_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.nv_locale import _


class HtmlGrid(HtmlPlotList):
    """html plot grid representation."""
    DESCRIPTION = f"HTML {_('Plot grid')}"
    SUFFIX = GRID_REPORT_SUFFIX

    _fileHeader = (
        f'{HtmlTable._fileHeader}$Styles'
        f'<title>{_("Plot grid")} ($Title)</title>\n'
        '</head>\n'
        '<body>\n'
        f'<p class=title>$Title {_("by")} $AuthorName - '
        f'{_("Plot grid")}</p>\n'
        '<table>\n'
        '<tr class="heading">\n'
        f'<td>{_("Date")}</td>\n'
        f'<td>{_("Time")}</td>\n'
        f'<td>{_("Duration")}</td>\n'
        f'<td>{_("Title")}</td>\n'
        f'<td>{_("Description")}</td>\n'
        f'<td>{_("Viewpoint")}</td>\n'
        '$PlotlineCells\n'
        f'<td>{_("Tags")}</td>\n'
        f'<td>{_("Scene")}</td>\n'
        f'<td>$NotASceneField1 / {_("Goal")} / {_("Reaction")} / $OtherSceneField1</td>\n'
        f'<td>$NotASceneField2 / {_("Conflict")} / {_("Dilemma")} / $OtherSceneField2</td>\n'
        f'<td>$NotASceneField3 / {_("Outcome")} / {_("Choice")} / $OtherSceneField3</td>\n'
        f'<td>{_("Notes")}</td>\n'
        '</tr>\n'
    )
    _sectionTemplate = _epigraphTemplate = (
        '<tr>\n'
        '<td><p>$ScDate</p></td>\n'
        '<td><p>$Time</p></td>\n'
        '<td><p>$Duration</p></td>\n'
        '<td class="$ID"><p>$Title</p></td>\n'
        '<td>$Desc</td>\n'
        '<td style="border-left: 0.5em solid $VpColor">$Viewpoint</td>\n'
        '$PlotlineCells\n'
        '<td><p>$Tags</p></td>\n'
        '<td><p>$Scene</p></td>\n'
        '<td>$Goal</td>\n'
        '<td>$Conflict</td>\n'
        '<td>$Outcome</td>\n'
        '<td>$Notes</td>\n'
        '</tr>\n'
    )

    def _get_sectionMapping(
            self,
            scId,
            sectionNumber,
            wordsTotal,
            firstInChapter=False,
            isEpigraph=False,
    ):
        """Return a mapping dictionary for a section section.
        
        Positional arguments:
            scId: str -- section ID.
            sectionNumber: int -- section number to be displayed.
            wordsTotal: int -- accumulated wordcount.
        
        Extends the superclass method.
        """
        sectionMapping = super()._get_sectionMapping(
            scId,
            sectionNumber,
            wordsTotal,
            firstInChapter,
            isEpigraph,
        )
        # Viewpoint color
        crId = self.novel.sections[scId].viewpoint
        if crId is not None:
            vpColor = self.novel.characters[crId].color or '#ffffff'
        else:
            vpColor = '#ffffff'
        sectionMapping['VpColor'] = vpColor

        # Plotline cells: one per plot line.
        plotlineCells = []
        for plId in self.novel.tree.get_children(PL_ROOT):
            if scId in self.novel.plotLines[plId].sections:
                attr = f' class="{plId}"'
            else:
                attr = ''
            plotlineNotes = self.novel.sections[scId].plotlineNotes
            if plotlineNotes:
                plotlineNote = plotlineNotes.get(plId, '')
            else:
                plotlineNote = ''
            plotlineCells.append(
                f'<td{attr}>{plotlineNote}</td>\n'
            )
        sectionMapping['PlotlineCells'] = '\n'.join(plotlineCells)

        return sectionMapping


"""Provide a class for html plot list representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_table import HtmlTable
from nvlib.novx_globals import PLOTLIST_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import list_to_string
from nvlib.nv_locale import _


class HtmlPlotList(HtmlTable):
    """html plot list representation."""
    DESCRIPTION = _('HTML Plot table')
    SUFFIX = PLOTLIST_SUFFIX

    _fileHeader = (
        f'{HtmlTable._fileHeader}$Styles'
        f'<title>{_("Plot lines")} ($Title)</title>\n'
        '</head>\n'
        '<body>\n'
        f'<p class=title>$Title {_("by")} $AuthorName - '
        f'{_("Plot lines")}</p>\n'
        '<table>\n'
        '<tr class="heading">\n'
        f'<td>{_("Title")}</td>\n'
        '$PlotlineCells\n'
        '</tr>\n'
    )
    _sectionTemplate = (
        '<tr>\n'
        '<td class="$ID"><p>$Title</p></td>\n'
        '$PlotlineCells\n'
        '</tr>\n'
    )

    def _get_fileHeaderMapping(self):
        """Return a mapping dictionary for the project section.
        
        Extends the superclass method.
        """
        fileHeaderMapping = super()._get_fileHeaderMapping()

        #--- Cells for the plot points: one column per plot line.
        fileHeaderMapping['PlotlineCells'] = '\n'.join([
            f'<td class="h{plId}"><p>{self.novel.plotLines[plId].title}</p></td>\n'
            for plId in self.novel.tree.get_children(PL_ROOT)
        ])
        extraStyles = self._get_extra_styles(self.novel.sections)
        extraStyles.extend(self._get_plot_line_styles())
        fileHeaderMapping['Styles'] = '\n'.join(extraStyles)
        return fileHeaderMapping

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

        # Plotline cells: one per plot line.
        plotlineCells = []
        for plId in self.novel.tree.get_children(PL_ROOT):
            if scId in self.novel.plotLines[plId].sections:
                attr = f' class="{plId}"'
                plotPoints = []
                for ppId in self.novel.tree.get_children(plId):
                    if (
                        scId ==
                        self.novel.plotPoints[ppId].sectionAssoc
                    ):
                        plotPoints.append(
                            self.novel.plotPoints[ppId].title
                        )
                plotPointTitles = list_to_string(
                    plotPoints,
                    divider=self._DIVIDER
                )
            else:
                attr = ''
                plotPointTitles = ''
            plotlineCells.append(
                f'<td{attr}><p>{plotPointTitles}</p></td>\n'
            )
        sectionMapping['PlotlineCells'] = '\n'.join(plotlineCells)
        return sectionMapping


"""Provide a class for html plot list representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import PLOTLIST_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import list_to_string
from nvlib.nv_locale import _


class HtmlPlotList(HtmlReport):
    """html plot list representation."""
    DESCRIPTION = _('HTML Plot table')
    SUFFIX = PLOTLIST_SUFFIX

    def write(self):
        """Create a HTML table.
        
        Raise the "Error" exception in case of error. 
        Extends the superclass method.
        """

        # Collect the plot lines.
        plotLines = self.novel.tree.get_children(PL_ROOT)
        if not plotLines:
            raise UserWarning(f'{_("No plot lines found")}.')

        # Build the HTML table.
        htmlText = [self._fileHeader]
        htmlText.append(
            (
                f'<title>{self.novel.title}</title>\n'
                '</head>\n'
                '<body>\n'
                f'<p class=title>{self.novel.title} - {_("Plot")}</p>\n'
                '<table>'
            )
        )
        plotLineColors = (
            'LightSteelBlue',
            'Gold',
            'Coral',
            'YellowGreen',
            'MediumTurquoise',
            'Plum',
        )

        # Title row.
        htmlText.append('<tr class="heading">')
        htmlText.append(self._new_cell(''))
        for i, plId in enumerate(plotLines):
            colorIndex = i % len(plotLineColors)
            htmlText.append(
                self._new_cell(
                    self.novel.plotLines[plId].title,
                    attr=f'style="background: {plotLineColors[colorIndex]}"'
                )
            )
        htmlText.append('</tr>')

        # Section rows.
        for chId in self.novel.tree.get_children(CH_ROOT):
            for scId in self.novel.tree.get_children(chId):
                # Section row
                if self.novel.sections[scId].scType == 0:
                    htmlText.append(f'<tr>')
                    htmlText.append(
                        self._new_cell(
                            self.novel.sections[scId].title
                        )
                    )
                    for i, plId in enumerate(plotLines):
                        colorIndex = i % len(plotLineColors)
                        if scId in self.novel.plotLines[plId].sections:
                            plotPoints = []
                            for ppId in self.novel.tree.get_children(plId):
                                if (
                                    scId ==
                                    self.novel.plotPoints[ppId].sectionAssoc
                                ):
                                    plotPoints.append(
                                        self.novel.plotPoints[ppId].title
                                    )
                            htmlText.append(
                                self._new_cell(
                                    list_to_string(plotPoints),
                                    attr=(
                                        'style="background: '
                                        f'{plotLineColors[colorIndex]}"'
                                    )
                                )
                            )
                        else:
                            htmlText.append(self._new_cell(''))
                    htmlText.append(f'</tr>')

        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))


"""Provide a class for html plot line board representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_board import HtmlBoard
from nvlib.novx_globals import PLOT_CARD_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.nv_locale import _


class HtmlPlotLineBoard(HtmlBoard):
    """html Plot line board representation."""
    DESCRIPTION = _('HTML Plot line board')
    SUFFIX = PLOT_CARD_SUFFIX

    def write(self):
        """Create a HTML page with a card for each plot line and plot point.
        
        Overwrites the superclass method.
        """

        # Collect the plot lines.
        srtPlotLines = self.novel.tree.get_children(PL_ROOT)
        if not srtPlotLines:
            raise UserWarning(f'{_("No plot lines found")}.')

        htmlText = [self._fileHeader]

        # Plot line card styles.
        htmlText.extend(
            self._get_card_header_styles(
                self.novel.plotLines,
                invert=True,
            )
        )
        htmlText.extend(
            self._get_card_body_styles(
                self.novel.plotLines,
            )
        )

        for plId in srtPlotLines:

            # Plot point card styles per plot line
            # (the default border color is the plot line color).
            plotPoints = {}
            for ppId in self.novel.tree.get_children(plId):
                plotPoints[ppId] = self.novel.plotPoints[ppId]
            htmlText.extend(
                self._get_card_header_styles(
                    plotPoints,
                    defaultBorderColor=self.novel.plotLines[plId].color,
                )
            )
            htmlText.extend(
                self._get_card_body_styles(
                    plotPoints,
                    defaultBorderColor=self.novel.plotLines[plId].color,
                )
            )

        htmlText.append(
            f'<title>{_("Plot line board")} ({self.novel.title})</title>\n'
            '</head>\n'
            '<body>\n'
            f'<p class=title>{self.novel.title} - {_("Plot line board")}</p>\n'
        )

        # Plot line rows.
        for plId in srtPlotLines:
            htmlText.append('<table><tr>')
            htmlText.append(
                self._new_cell(
                    self.novel.plotLines[plId].title,
                    attr=f'class="h{plId}"',
                )
            )
            for ppId in self.novel.tree.get_children(plId):
                htmlText.append(
                    self._new_cell(
                        self.novel.plotPoints[ppId].title,
                        attr=f'class="h{ppId}"',
                    )
                )
            htmlText.append(f'</tr>')
            htmlText.append(f'<tr>')
            htmlText.append(
                self._new_cell(
                    self.novel.plotLines[plId].desc,
                    attr=f'class="{plId}"',
                )
            )
            for ppId in self.novel.tree.get_children(plId):
                htmlText.append(
                    self._new_cell(
                        self.novel.plotPoints[ppId].desc,
                        attr=f'class="{ppId}"',
                    )
                )
            htmlText.append('</tr></table><br />')

        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))


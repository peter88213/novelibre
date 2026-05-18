"""Provide a class for html plot cards representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.hex_color import HexColor
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import PLOT_CARD_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.nv_locale import _


class HtmlPlotCards(HtmlReport):
    """html plot list representation."""
    DESCRIPTION = _('HTML Plot cards')
    SUFFIX = PLOT_CARD_SUFFIX

    _fileHeader = (
        '<html>\n'
        '<head>\n'
        '<meta http-equiv="Content-Type" content="text/html; '
        'charset=utf-8"/>\n\n'
        '<style type="text/css">\n'
        'body {font-family: sans-serif}\n'
        'p.title {font-size: larger; font-weight: bold}\n'
        'td {padding: 10}\n'
        'table, td {border:0px solid transparent; '
        'vertical-align: top}\n'
        'table {border-spacing:1em 0px;} '
        'td {'
        'table-layout:fixed; width:15em; overflow:hidden; '
        'word-wrap:break-word; '
        'min-width:15em; max-widh:15em; '
        '}\n'
        '</style>\n'
    )

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
                defaultColor='#000000',
                invert=True,
            )
        )
        htmlText.extend(
            self._get_card_body_styles(
                self.novel.plotLines,
                defaultColor='#000000',
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
                    defaultColor=self.novel.plotLines[plId].color,
                )
            )
            htmlText.extend(
                self._get_card_body_styles(
                    plotPoints,
                    defaultColor=self.novel.plotLines[plId].color,
                )
            )

        htmlText.append(
            f'<title>{_("Plot cards")} ({self.novel.title})</title>\n'
            '</head>\n'
            '<body>\n'
            f'<p class=title>{self.novel.title} - {_("Plot cards")}</p>\n'
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
            htmlText.append('</tr></table><br>')

        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))

    def _get_card_header_styles(
        self,
        elements,
        defaultColor='#ffffff',
        invert=False,
    ):

        BLACK = '#000000'
        WHITE = '#ffffff'
        htmlText = []
        htmlText.append('<style type="text/css">')
        for elemId in elements:
            elemColor = elements[elemId].color
            fgColor = BLACK
            bgColor = WHITE
            borderColor = defaultColor
            if elemColor is not None:
                borderColor = elemColor
                if invert:
                    bgColor = elemColor
                    if HexColor.is_dark(elemColor):
                        fgColor = WHITE
            htmlText.append(
                f'td.h{elemId} {{'
                'font-weight: bold; '
                f'border-top: 0.2em solid {borderColor}; '
                f'border-right: 0.2em solid {borderColor}; '
                f'border-left: 0.2em solid {borderColor}; '
                f'border-bottom: 0.1em solid #ff0000; '
                f'background: {bgColor}; '
                f'color: {fgColor}'
                '}'
            )
        htmlText.append(
            '</style>\n'
        )
        return htmlText

    def _get_card_body_styles(self, elements, defaultColor='#000000'):

        htmlText = []
        htmlText.append('<style type="text/css">')
        for elemId in elements:
            elemColor = elements[elemId].color
            if elemColor is not None:
                borderColor = elemColor
            else:
                borderColor = defaultColor
            htmlText.append(
                f'td.{elemId} {{'
                f'border-right: 0.2em solid {borderColor}; '
                f'border-left: 0.2em solid {borderColor}; '
                f'border-bottom: 0.2em solid {borderColor}; '
                '}'
            )
        htmlText.append(
            '</style>\n'
        )
        return htmlText


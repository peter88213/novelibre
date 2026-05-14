"""Provide a class for html plot list representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import PLOTLIST_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.nv_locale import _


class HtmlPlotList(HtmlReport):
    """html plot list representation."""
    DESCRIPTION = _('HTML Plot table')
    SUFFIX = PLOTLIST_SUFFIX

    def write(self):
        """Create a HTML table.
        
        Overwrites the superclass method.
        """

        # Collect the plot lines.
        srtPlotLines = self.novel.tree.get_children(PL_ROOT)
        if not srtPlotLines:
            raise UserWarning(f'{_("No plot lines found")}.')

        htmlText = [self._fileHeader]
        htmlText.extend(self._get_plot_line_styles())
        for plId in srtPlotLines:
            plotPoints = {}
            for ppId in self.novel.tree.get_children(plId):
                plotPoints[ppId] = self.novel.plotPoints[ppId]
            htmlText.extend(
                self._get_extra_heading_styles(
                    plotPoints,
                    defaultColor=self.novel.plotLines[plId].color,
                )
            )
            htmlText.extend(
                self._get_extra_styles(
                    plotPoints,
                    defaultColor=self.novel.plotLines[plId].color,
                )
            )

        htmlText.append(
            f'<title>{_("Plot lines")} ({self.novel.title})</title>\n'
            '</head>\n'
            '<body>\n'
            f'<p class=title>{self.novel.title} - {_("Plot lines")}</p>\n'
            '<table>'
        )

        # Plot line rows.
        for plId in srtPlotLines:
            htmlText.append(f'<tr>')
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
            htmlText.append(f'</tr>')

        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))

    def _get_extra_heading_styles(self, elements, defaultColor='#ffffff'):

        htmlText = []
        htmlText.append('<style type="text/css">')
        htmlText.append(
            # 'table {border-spacing:1em;} '
            'td {'
            'table-layout:fixed; width:15em; overflow:hidden; '
            'word-wrap:break-word; '
            'min-width:15em; max-widh:15em; '
            '} '
        )
        for elemId in elements:
            elemColor = elements[elemId].color
            if elemColor is not None:
                borderColor = elemColor
            else:
                borderColor = defaultColor
            htmlText.append(
                f'td.h{elemId} {{'
                'font-weight: bold; '
                f'border-top: 0.2em solid {borderColor}; '
                f'border-right: 0.2em solid {borderColor}; '
                f'border-left: 0.2em solid {borderColor}; '
                f'border-bottom: 0.1em solid #ff0000; '
                '}'
            )
        htmlText.append(
            '</style>\n'
        )
        return htmlText

    def _get_extra_styles(self, elements, defaultColor='#ffffff'):

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


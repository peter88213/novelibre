"""Provide a base class for HTML table representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.hex_color import HexColor
from nvlib.model.html.html_report import HtmlReport


class HtmlTable(HtmlReport):
    """Class for HTML table representation."""

    _extraStyles = (
        '<style type="text/css">\n'
        'tr.heading {'
        'font-size:smaller; font-weight: bold; '
        'background-color:#f0f0f0'
        '}\n'
        'table {border-spacing: 0}\n'
        'table, td {'
        'border: #f0f0f0 solid 1px; '
        '}\n'
        'td.title {font-weight: bold}\n'
        'td.chaptertitle {color: green; font-weight: bold}\n'
        'td.chapter {color: green}\n'
        'td.parttitle {'
        'color: white; '
        'background-color: green; '
        'font-weight: bold; '
        '}\n'
        'td.part {color: white; background-color: green}\n'
        'td.stage {color: red}\n'
        'td.stagetitle {color: red; font-weight: bold}\n'
        '</style>\n'
    )
    _fileHeader = f'{HtmlReport._fileHeader}{_extraStyles}'
    _fileFooter = (
        '</table>\n'
        '</body>\n'
        '</html>\n'
    )

    def _get_extra_styles(self, elements):

        DEFAULT_COLOR = '#dfdfdf'

        htmlText = []
        htmlText.append('<style type="text/css">')
        for elemId in elements:
            elemColor = elements[elemId].color
            if elemColor is not None:
                bgColor = elemColor
            else:
                bgColor = DEFAULT_COLOR
            htmlText.append(
                f'td.{elemId} {{'
                'font-weight: bold; '
                f'border-left: 0.5em solid {bgColor}'
                '}'
            )
        htmlText.append(
            '</style>\n'
        )
        return htmlText

    def _get_plot_line_styles(self):

        # Set up styles that define the plot line colors.
        DEFAULT_PLOTLINE_COLOR = '#dfdfdf'
        DEFAULT_TEXT_COLOR = BLACK = '#000000'
        WHITE = '#ffffff'

        htmlText = []
        htmlText.append('<style type="text/css">')
        for plId in self.novel.plotLines:
            plColor = self.novel.plotLines[plId].color
            if plColor is not None:
                if HexColor.is_dark(plColor):
                    fgColor = WHITE
                else:
                    fgColor = BLACK
                bgColor = plColor
            else:
                fgColor = DEFAULT_TEXT_COLOR
                bgColor = DEFAULT_PLOTLINE_COLOR

            # Plot line column heading cell style.
            htmlText.append(
                f'td.h{plId} {{'
                f'background: {bgColor}; '
                f'color: {fgColor}'
                '}'
            )

            # Plot line node cell style.
            htmlText.append(
                f'td.{plId} {{'
                f'border-left: 0.5em solid {bgColor}; '
                f'background: {DEFAULT_PLOTLINE_COLOR}; '
                f'color: {DEFAULT_TEXT_COLOR}'
                '}'
            )
        htmlText.append(
            '</style>\n'
        )
        return htmlText


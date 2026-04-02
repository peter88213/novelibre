"""Provide a base class for HTML report file representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from html import escape

from nvlib.model.file.file_export import FileExport
from nvlib.model.hex_color import HexColor


class HtmlReport(FileExport):
    """Class for HTML report file representation."""
    DESCRIPTION = 'HTML report'
    EXTENSION = '.html'
    SUFFIX = '_report'

    _fileHeader = (
        '<html>\n'
        '<head>\n'
        '<meta http-equiv="Content-Type" content="text/html; '
        'charset=utf-8"/>\n\n'
        '<style type="text/css">\n'
        'body {font-family: sans-serif}\n'
        'p.title {font-size: larger; font-weight: bold}\n'
        'td {padding: 10}\n'
        'tr.heading {font-size:smaller; font-weight: bold; '
        'background-color:#f0f0f0}\n'
        'table {border-spacing: 0}\n'
        'table, td {border: #f0f0f0 solid 1px; '
        'vertical-align: top}\n'
        'td.title {font-weight: bold}\n'
        'td.chaptertitle {color: green; font-weight: bold}\n'
        'td.chapter {color: green}\n'
        'td.parttitle {color: white; background-color: green; '
        'font-weight: bold}\n'
        'td.part {color: white; background-color: green}\n'
        'td.stage {color: red}\n'
        'td.stagetitle {color: red; font-weight: bold}\n'
        '</style>\n'
    )
    _fileFooter = (
        '</table>\n'
        '</body>\n'
        '</html>\n'
    )

    def _convert_from_novx(self, text, quick=False, **kwargs):
        """Return text, converted from *novelibre* markup to target format.
        
        Positional arguments:
            text -- string to convert.
        
        Optional arguments:
            quick: bool -- if True, apply a conversion mode 
                   for one-liners without formatting.
        
        Overrides the superclass method.
        """
        if not text:
            return ''

        text = escape(text.rstrip())
        if quick:
            return text.replace('\n', ' ')

        newlines = []
        for line in text.split('\n'):
            newlines.append(f'<p>{line}</p>')
        return '\n'.join(newlines)

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

    def _new_cell(self, text, attr=''):
        # Return the markup for a table cell with text and attributes.
        return f'<td {attr}>{self._convert_from_novx(text)}</td>'


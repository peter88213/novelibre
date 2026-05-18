"""Provide a class for html cards representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.hex_color import HexColor
from nvlib.model.html.html_report import HtmlReport


class HtmlCards(HtmlReport):
    """html plot list representation."""

    _fileHeader = (
        '<html>\n'
        '<head>\n'
        '<meta http-equiv="Content-Type" content="text/html; '
        'charset=utf-8"/>\n\n'
        '<style type="text/css">\n'
        'body {font-family: sans-serif; background-color: #dfdfdf}\n'
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

    def _get_card_header_styles(
        self,
        elements,
        defaultBorderColor='#ffffff',
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
            borderColor = elemColor or defaultBorderColor
            if invert:
                bgColor = elemColor or BLACK
                if HexColor.is_dark(bgColor):
                    fgColor = WHITE
                borderColor = bgColor
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

    def _get_card_body_styles(self, elements, defaultBorderColor='#ffffff'):

        htmlText = []
        htmlText.append('<style type="text/css">')
        for elemId in elements:
            elemColor = elements[elemId].color
            if elemColor is not None:
                borderColor = elemColor
            else:
                borderColor = defaultBorderColor
            htmlText.append(
                f'td.{elemId} {{'
                f'border-right: 0.2em solid {borderColor}; '
                f'border-left: 0.2em solid {borderColor}; '
                f'border-bottom: 0.2em solid {borderColor}; '
                'background: #ffffff; '
                '}'
            )
        htmlText.append(
            '</style>\n'
        )
        return htmlText


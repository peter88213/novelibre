"""Provide a base class for HTML report file representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from xml import sax

from nvlib.model.file.file_export import FileExport


class HtmlReport(FileExport):
    """Class for HTML report file representation."""
    DESCRIPTION = 'HTML report'
    EXTENSION = '.html'
    SUFFIX = '_report'

    _fileHeader = (
        '<!DOCTYPE html>\n'
        '<html>\n'
        '<head>\n'
        '<meta http-equiv="Content-Type" content="text/html; '
        'charset=utf-8"/>\n\n'
        '<style type="text/css">\n'
        'body {font-family: sans-serif}\n'
        'p.title {font-size: larger; font-weight: bold}\n'
        'table, td {vertical-align: top}\n'
        'td {'
        'padding: 10;'
        'padding-right: 0.5em; '
        'padding-left: 0.5em; '
        '}\n'
        '</style>\n'
    )

    _fileFooter = (
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

        text = text.rstrip()
        entities = {
            "'": '&apos;',
            '"': '&quot;',
        }
        text = sax.saxutils.escape(text, entities=entities)
        if quick:
            return text.replace('\n', ' ')

        newlines = []
        for line in text.split('\n'):
            newlines.append(f'<p>{line}</p>')
        return '\n'.join(newlines)

    def _new_cell(self, text, attr=''):
        # Return the markup for a table cell with text and attributes.
        return f'<td {attr}>{self._convert_from_novx(text)}</td>'


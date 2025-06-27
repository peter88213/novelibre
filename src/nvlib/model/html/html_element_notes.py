"""Provide a class for html element notes list representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import ELEMENT_NOTES_SUFFIX
from nvlib.nv_locale import _


class HtmlElementNotes(HtmlReport):
    """Class for HTML project notes report file representation."""
    DESCRIPTION = 'HTML element notes report'
    EXTENSION = '.html'
    SUFFIX = ELEMENT_NOTES_SUFFIX

    _fileHeader = (
        f'{HtmlReport._fileHeader}\n'
        f'<title>{_("Notes")} ($Title)</title>\n'
        '</head>\n'
        '<body>\n'
        f'<p class=title>$Title {_("by")} $AuthorName - {_("Notes")}</p>\n'
        '<table>\n'
        '<tr class="heading">\n'
        f'<td class="chtitle">{_("Title")}</td>\n'
        f'<td>{_("Text")}</td>\n'
        '</tr>\n'
    )
    _characterHeadingTemplate = (
        '<tr class="heading">\n'
        f'<td>{_("Characters")}</td>\n'
        '<td />\n'
        '</tr>\n'
    )
    _locationHeadingTemplate = (
        '<tr class="heading">\n'
        f'<td>{_("Locations")}</td>\n'
        '<td />\n'
        '</tr>\n'
    )
    _itemHeadingTemplate = (
        '<tr class="heading">\n'
        f'<td>{_("Items")}</td>\n'
        '<td />\n'
        '</tr>\n'
    )
    _plotLineHeadingTemplate = (
        '<tr class="heading">\n'
        f'<td>{_("Plot lines")}</td>\n'
        '<td />\n'
        '</tr>\n'
    )
    _partTemplate = (
        '<tr>\n'
        '<td class="parttitle">$Title</td>\n'
        '<td class="part">$Notes</td>\n'
        '</tr>\n'
    )
    _chapterTemplate = (
        '<tr>\n'
        '<td class="chaptertitle">$Title</td>\n'
        '<td class="chapter">$Notes</td>\n'
        '</tr>\n'
    )
    __plotLineTemplate = (
        '<tr>\n'
        '<td class="title">$Title</td>\n'
        '<td>$Notes</td>\n'
        '</tr>\n'
    )
    _sectionTemplate = _characterTemplate = _locationTemplate = \
    _itemTemplate = _plotPointTemplate = (
        '<tr>\n'
        '<td>$Title</td>\n'
        '<td>$Notes</td>\n'
        '</tr>\n'
    )
    _stage1Template = (
        '<tr>\n'
        '<td class="stagetitle">$Title</td>\n'
        '<td class="stage">$Notes</td>\n'
        '</tr>\n'
    )
    _stage2Template = (
        '<tr>\n'
        '<td class="stage">$Title</td>\n'
        '<td class="stage">$Notes</td>\n'
        '</tr>\n'
    )

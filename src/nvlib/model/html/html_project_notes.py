"""Provide a class for HTML project notes report file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import PROJECTNOTES_SUFFIX
from nvlib.nv_locale import _


class HtmlProjectNotes(HtmlReport):
    """Class for HTML project notes report file representation."""
    DESCRIPTION = 'HTML project notes report'
    EXTENSION = '.html'
    SUFFIX = PROJECTNOTES_SUFFIX

    _fileHeader = (
        f'{HtmlReport._fileHeader}\n'
        f'<title>{_("Project notes")} ($Title)</title>\n'
        '</head>\n'
        '<body>\n'
        f'<p class=title>$Title {_("by")} $AuthorName - '
        f'{_("Project notes")}</p>\n'
        '<table>\n'
        '<tr class="heading">\n'
        f'<td class="chtitle">{_("Title")}</td>\n'
        f'<td>{_("Text")}</td>\n'
        '</tr>\n'
    )

    _projectNoteTemplate = (
        '<tr>\n'
        '<td class="chtitle">$Title</td>\n'
        '<td>$Desc</td>\n'
        '</tr>\n'
    )

    def write(self):
        if not self.novel.projectNotes:
            raise UserWarning(f'{_("No project notes found")}.')
        super().write()


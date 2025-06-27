"""Provide a class for HTML items report file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import ITEM_REPORT_SUFFIX
from nvlib.novx_globals import Notification
from nvlib.nv_locale import _


class HtmlItems(HtmlReport):
    """Class for HTML items report file representation."""
    DESCRIPTION = 'HTML items report'
    EXTENSION = '.html'
    SUFFIX = ITEM_REPORT_SUFFIX

    _fileHeader = (
        f'{HtmlReport._fileHeader}\n'
        f'<title>{_("Items")} ($Title)</title>\n'
        '</head>\n'
        '<body>\n'
        f'<p class=title>$Title {_("by")} $AuthorName - {_("Items")}</p>\n'
        '<table>\n'
        '<tr class="heading">\n'
        f'<td class="chtitle">{_("Name")}</td>\n'
        f'<td>{_("AKA")}</td>\n'
        f'<td>{_("Tags")}</td>\n'
        f'<td>{_("Description")}</td>\n'
        '</tr>\n'
    )
    _itemTemplate = (
        '<tr>\n'
        '<td class="chtitle">$Title</td>\n'
        '<td>$AKA</td>\n'
        '<td>$Tags</td>\n'
        '<td>$Desc</td>\n'
        '</tr>\n'
    )

    def write(self):
        if not self.novel.items:
            raise Notification(f'{_("No items found")}.')
        super().write()

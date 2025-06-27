"""Provide a class for HTML locations report file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import LOCATION_REPORT_SUFFIX
from nvlib.novx_globals import Notification
from nvlib.nv_locale import _


class HtmlLocations(HtmlReport):
    """Class for HTML locations report file representation."""
    DESCRIPTION = 'HTML locations report'
    EXTENSION = '.html'
    SUFFIX = LOCATION_REPORT_SUFFIX

    _fileHeader = (
        f'{HtmlReport._fileHeader}\n'
        f'<title>{_("Locations")} ($Title)</title>\n'
        '</head>\n'
        '<body>\n'
        f'<p class=title>$Title {_("by")} $AuthorName - '
        f'{_("Locations")}</p>\n'
        '<table>\n'
        '<tr class="heading">\n'
        f'<td class="chtitle">{_("Name")}</td>\n'
        f'<td>{_("AKA")}</td>\n'
        f'<td>{_("Tags")}</td>\n'
        f'<td>{_("Description")}</td>\n'
        '</tr>\n'
    )
    _locationTemplate = (
        '<tr>\n'
        '<td class="chtitle">$Title</td>\n'
        '<td>$AKA</td>\n'
        '<td>$Tags</td>\n'
        '<td>$Desc</td>\n'
        '</tr>\n'
    )

    def write(self):
        if not self.novel.locations:
            raise Notification(f'{_("No locations found")}.')
        super().write()


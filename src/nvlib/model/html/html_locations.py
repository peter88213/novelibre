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

    _fileHeader = f'''{HtmlReport._fileHeader}
<title>{_('Locations')} ($Title)</title>
</head>

<body>
<p class=title>$Title {_('by')} $AuthorName - {_('Locations')}</p>
<table>
<tr class="heading">
<td class="chtitle">{_('Name')}</td>
<td>{_('AKA')}</td>
<td>{_('Tags')}</td>
<td>{_('Description')}</td>
</tr>
'''

    _locationTemplate = '''<tr>
<td class="chtitle">$Title</td>
<td>$AKA</td>
<td>$Tags</td>
<td>$Desc</td>
</tr>
'''

    def write(self):
        if not self.novel.locations:
            raise Notification(f'{_("No locations found")}.')
        super().write()


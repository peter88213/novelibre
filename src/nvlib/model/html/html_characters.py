"""Provide a class for HTML characters report file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.gregorian_calendar import GregorianCalendar as cal
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import CHARACTER_REPORT_SUFFIX
from nvlib.novx_globals import Notification
from nvlib.nv_locale import _


class HtmlCharacters(HtmlReport):
    """Class for HTML characters report file representation."""
    DESCRIPTION = 'HTML charcters report'
    EXTENSION = '.html'
    SUFFIX = CHARACTER_REPORT_SUFFIX

    _fileHeader = f'''{HtmlReport._fileHeader}
<title>{_('Characters')} ($Title)</title>
</head>

<body>
<p class=title>$Title {_('by')} $AuthorName - {_('Characters')}</p>
<table>
<tr class="heading">
<td class="chtitle">{_('Name')}</td>
<td>{_('Full name')}</td>
<td>{_('AKA')}</td>
<td>{_('Tags')}</td>
<td>{_('Description')}</td>
<td>$CustomChrBio</td>
<td>$CustomChrGoals</td>
<td>{_('Birth date')}</td>
<td>{_('Death date')}</td>
<td>{_('Notes')}</td>
</tr>
'''

    _characterTemplate = '''<tr>
<td class="chtitle">$Title</td>
<td>$FullName</td>
<td>$AKA</td>
<td>$Tags</td>
<td>$Desc</td>
<td>$Bio</td>
<td>$Goals</td>
<td>$BirthDate</td>
<td>$DeathDate</td>
<td>$Notes</td>
</tr>
'''

    def write(self):
        if not self.novel.characters:
            raise Notification(f'{_("No characters found")}.')
        super().write()

    def _get_characterMapping(self, crId):
        characterMapping = super()._get_characterMapping(crId)
        if self.localizeDate:
            try:
                characterMapping['BirthDate'] = cal.get_locale_date(characterMapping['BirthDate'])
            except:
                pass
            try:
                characterMapping['DeathDate'] = cal.get_locale_date(characterMapping['DeathDate'])
            except:
                pass
        return characterMapping

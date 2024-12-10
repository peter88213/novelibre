"""Provide a class for HTML characters report file representation.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import CHARACTER_REPORT_SUFFIX
from nvlib.nv_locale import _
from datetime import date


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

    def _get_characterMapping(self, crId):
        characterMapping = super()._get_characterMapping(crId)
        if self.localizeDate:
            try:
                characterMapping['BirthDate'] = date.fromisoformat(characterMapping['BirthDate']).strftime('%x')
            except:
                pass
            try:
                characterMapping['DeathDate'] = date.fromisoformat(characterMapping['DeathDate']).strftime('%x')
            except:
                pass
        return characterMapping

"""Provide a class for HTML characters report file representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import CHARACTER_REPORT_SUFFIX
from nvlib.novx_globals import Notification
from nvlib.nv_locale import _


class HtmlCharacters(HtmlReport):
    """Class for HTML characters report file representation."""
    DESCRIPTION = 'HTML charcters report'
    EXTENSION = '.html'
    SUFFIX = CHARACTER_REPORT_SUFFIX

    _fileHeader = (
        f'{HtmlReport._fileHeader}\n'
        f'<title>{_("Characters")} ($Title)</title>\n'
        '</head>\n'
        '<body>\n'
        f'<p class=title>$Title {_("by")} $AuthorName - '
        f'{_("Characters")}</p>\n'
        '<table>\n'
        '<tr class="heading">\n'
        f'<td class="chtitle">{_("Name")}</td>\n'
        f'<td>{_("Full name")}</td>\n'
        f'<td>{_("AKA")}</td>\n'
        f'<td>{_("Tags")}</td>\n'
        f'<td>{_("Description")}</td>\n'
        f'<td>{_("Bio")}</td>\n'
        '<td>$CharacterExtraField</td>\n'
        f'<td>{_("Birth date")}</td>\n'
        f'<td>{_("Death date")}</td>\n'
        f'<td>{_("Notes")}</td>\n'
        '</tr>\n'
    )
    _characterTemplate = (
        '<tr>\n'
        '<td class="chtitle">$Title</td>\n'
        '<td>$FullName</td>\n'
        '<td>$AKA</td>\n'
        '<td>$Tags</td>\n'
        '<td>$Desc</td>\n'
        '<td>$Bio</td>\n'
        '<td>$Goals</td>\n'
        '<td>$BirthDate</td>\n'
        '<td>$DeathDate</td>\n'
        '<td>$Notes</td>\n'
        '</tr>\n'
    )

    def write(self):
        if not self.novel.characters:
            raise Notification(f'{_("No characters found")}.')
        super().write()

    def _get_characterMapping(self, crId):
        characterMapping = super()._get_characterMapping(crId)
        if self.localizeDate:
            try:
                characterMapping['BirthDate'] = PyCalendar.locale_date(
                    characterMapping['BirthDate']
                )
            except:
                pass
            try:
                characterMapping['DeathDate'] = PyCalendar.locale_date(
                    characterMapping['DeathDate']
                )
            except:
                pass
        return characterMapping

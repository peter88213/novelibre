"""Provide a class for a html time table representation.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from datetime import datetime
from datetime import timedelta

from nvlib.model.data.section import Section
from nvlib.model.html.html_report import HtmlReport
from nvlib.novx_globals import TIMETABLE_SUFFIX
from nvlib.nv_locale import _


class HtmlTimetable(HtmlReport):
    """html time table representation."""
    DESCRIPTION = _('HTML Time table')
    SUFFIX = TIMETABLE_SUFFIX

    def write(self):
        """Create a HTML table.
        
        Raise the "Error" exception in case of error. 
        Overwrites the superclass method.
        """

        htmlText = [self._fileHeader]
        htmlText.append(f'''<title>{self.novel.title}</title>
</head>
<body>
<p class=title>{self.novel.title} - {_("Time table")}</p>
<table>''')

        # Title row.
        htmlText.append('<tr class="heading">')
        htmlText.append(self._new_cell(_('Date')))
        htmlText.append(self._new_cell(_('Time')))
        htmlText.append(self._new_cell(_('Section')))
        htmlText.append(self._new_cell(_('Description')))
        htmlText.append(self._new_cell(_('Duration')))
        htmlText.append('</tr>')

        # Section rows.
        try:
            referenceDate = date.fromisoformat(self.novel.referenceDate)
        except:
            referenceDate = date.min

        scIdsByDate = {}
        for scId in self.novel.sections:
            if self.novel.sections[scId].scType != 0:
                continue

            # Use the timestamp for chronological sorting.
            timestamp = self.get_timestamp(self.novel.sections[scId], referenceDate)
            if not timestamp:
                continue

            if not timestamp in scIdsByDate:
                scIdsByDate[timestamp] = []
            scIdsByDate[timestamp].append(scId)

        # Sort sections by date/time.
        srtSections = sorted(scIdsByDate.items())

        currentDateDayStr = ''
        for timestamp, scIds in srtSections:
            for scId in scIds:
                # Section row
                htmlText.append(f'<tr>')
                dateDayStr = self.get_date_day_str(scId)
                if dateDayStr != currentDateDayStr:
                    currentDateDayStr = dateDayStr
                else:
                    dateDayStr = ''
                htmlText.append(self._new_cell(dateDayStr))
                htmlText.append(self._new_cell(self.get_time_str(scId)))
                htmlText.append(self._new_cell(self.novel.sections[scId].title))
                htmlText.append(self._new_cell(self.novel.sections[scId].desc))
                htmlText.append(self._new_cell(self.get_duration_str(scId)))
                htmlText.append(f'</tr>')
        htmlText.append(self._fileFooter)
        with open(self.filePath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(htmlText))

    def _new_cell(self, text, attr=''):
        """Return the markup for a table cell with text and attributes."""
        return f'<td {attr}>{self._convert_from_novx(text)}</td>'

    def get_timestamp(self, section, referenceDate):
        if not section.time and not section.date and not section.day:
            return

        timeStr = section.time
        if not timeStr:
            timeStr = '00:00'
        if section.date:
            try:
                sectionStart = datetime.fromisoformat(f'{section.date} {timeStr}')
            except:
                return
        else:
            try:
                if section.day:
                    dayInt = int(section.day)
                else:
                    dayInt = 0
                startDate = (referenceDate + timedelta(days=dayInt)).isoformat()
                sectionStart = datetime.fromisoformat(f'{startDate} {timeStr}')
            except:
                return

        return datetime.timestamp(sectionStart)

    def get_date_day_str(self, scId):
        """Return a date/day string for the section defined by scId."""
        if self.novel.sections[scId].date is not None and self.novel.sections[scId].date != Section.NULL_DATE:
            dateDayStr = self.novel.sections[scId].localeDate
        else:
            if self.novel.sections[scId].day is not None:
                dateDayStr = f'{_("Day")} {self.novel.sections[scId].day}'
            else:
                dateDayStr = ''
        return dateDayStr

    def get_time_str(self, scId):
        """Return a time string for the section defined by scId."""
        if self.novel.sections[scId].time is not None:
            h, m, __ = self.novel.sections[scId].time.split(':')
            timeStr = f'{h}:{m}'
        else:
            timeStr = ''
        return timeStr

    def get_duration_str(self, scId):
        """Return a combined duration string for the section defined by scId."""
        if self.novel.sections[scId].lastsDays is not None and self.novel.sections[scId].lastsDays != '0':
            dayStr = f'{self.novel.sections[scId].lastsDays}d '
        else:
            dayStr = ''
        if self.novel.sections[scId].lastsHours is not None and self.novel.sections[scId].lastsHours != '0':
            hourStr = f'{self.novel.sections[scId].lastsHours}h '
        else:
            hourStr = ''
        if self.novel.sections[scId].lastsMinutes is not None and self.novel.sections[scId].lastsMinutes != '0':
            minuteStr = f'{self.novel.sections[scId].lastsMinutes}min'
        else:
            minuteStr = ''
        return f'{dayStr}{hourStr}{minuteStr}'


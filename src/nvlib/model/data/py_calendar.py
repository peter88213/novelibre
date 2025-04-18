"""Provide a class for date/time related calculations.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from calendar import isleap, day_name, month_name
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from nvlib.nv_locale import _


class PyCalendar:
    """Methods for date/time operations using the Python standard library.
    
    - Dates are restricted to the range between 0001-01-01 00:00 and 9999.12.31 23:59.
    - The extended Gregorian calendar is used.
    - ISO date string format: YYYY-MM-DD.
    - ISO time string format: hh:mm:ss, where seconds are not displayed. 
    """
    # Class methods are used instead of static methods, so they can be extended by subclasses.

    min = date.min.isoformat()
    max = date.max.isoformat()
    DATE_FORMAT = _("YYYY-MM-DD")
    TIME_FORMAT = _("hh:mm")
    WEEKDAYS = day_name
    MONTHS = month_name

    @classmethod
    def age(cls, nowIso, birthDateIso, deathDateIso):
        """Return age or time since dead in years (Integer).
        
        Positional arguments:
            nowIso:str -- Reference date/time, formatted acc. to ISO 8601
            birthDateIso:str -- Birth date, formatted acc. to ISO 8601
            deathDateIso:str -- Death date, formatted acc. to ISO 8601
        
        A positive return value indicates the age.
        A negative value indicates the number of years since death.    
        """
        now = datetime.fromisoformat(nowIso)
        if deathDateIso:
            deathDate = datetime.fromisoformat(deathDateIso)
            if now > deathDate:
                years = cls._difference_in_years(deathDate, now)
                return -1 * years

        birthDate = datetime.fromisoformat(birthDateIso)
        years = cls._difference_in_years(birthDate, now)
        return years

    @classmethod
    def get_end_date_time(cls, section):
        """Return a tuple: (endDate, endTime) of a given section."""
        sectionStart = datetime.fromisoformat(f'{section.date} {section.time}')
        sectionEnd = sectionStart + cls._get_duration(section)
        return sectionEnd.isoformat().split('T')

    @classmethod
    def get_end_day_time(cls, section):
        """ Return a tuple: (endDay, endTime) of a given section."""
        if section.day:
            dayInt = int(section.day)
        else:
            dayInt = 0
        virtualStartDate = (date.min + timedelta(days=dayInt)).isoformat()
        virtualSectionStart = datetime.fromisoformat(f'{virtualStartDate} {section.time}')
        virtualSectionEnd = virtualSectionStart + cls._get_duration(section)
        virtualEndDate, endTime = virtualSectionEnd.isoformat().split('T')
        endDay = str((date.fromisoformat(virtualEndDate) - date.min).days)
        return (endDay, endTime)

    @classmethod
    def get_timestamp(cls, section, refIso):
        """Return a timestamp (total seconds since 0001-01-01 00:00)."""
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
                startDate = (date.fromisoformat(refIso) + timedelta(days=dayInt)).isoformat()
                sectionStart = datetime.fromisoformat(f'{startDate} {timeStr}')
            except:
                return

        return int((sectionStart - datetime.min).total_seconds())

    @classmethod
    def h_m_s_str(cls, timeIso):
        """Return a tuple of strings: hours, minutes, seconds."""
        return timeIso.split(':')

    @classmethod
    def locale_date(cls, dateIso):
        """Return a string with the localized date."""
        return date.fromisoformat(dateIso).strftime('%x')

    @classmethod
    def specific_date(cls, dayStr, refIso):
        """Return the ISO-formatted date.
        
        Positional arguments:
            dayStr:str -- Day
            refIso:str -- Reference date/time, formatted acc. to ISO 8601
        """
        # Calculate the section date from day and reference date.
        refDate = date.fromisoformat(refIso)
        return date.isoformat(refDate + timedelta(days=int(dayStr)))

    @classmethod
    def display_time(cls, timeIso):
        """Return a string with the time for display."""
        h, m, __ = cls.verified_time(timeIso).split(':')
        return f'{h}:{m}'

    @classmethod
    def unspecific_date(cls, dateIso, refIso):
        """Return the day as a string.
        
        Positional arguments:
            dateIso:str -- Date/time, formatted acc. to ISO 8601
            refIso:str -- Reference date/time, formatted acc. to ISO 8601
        """
        # Calculate the section day from date and reference date.
        refDate = date.fromisoformat(refIso)
        return str((date.fromisoformat(dateIso) - refDate).days)

    @classmethod
    def verified_date(cls, dateIso):
        """Return a verified iso dateIso or None."""
        if dateIso is not None:
            date.fromisoformat(dateIso)
            # raising an exception if dateIso is not an iso-formatted date
        return dateIso

    @classmethod
    def verified_time(cls, timeIso):
        """Return a verified iso timeIso or None."""
        if  timeIso is not None:
            time.fromisoformat(timeIso)
            # raising an exception if timeIso is not an iso-formatted time
            while timeIso.count(':') < 2:
                timeIso = f'{timeIso}:00'
                # adding minutes or seconds, if missing
        return timeIso

    @classmethod
    def weekday(cls, dateIso):
        """Return the day of the week as an integer."""
        return date.fromisoformat(dateIso).weekday()

    @classmethod
    def weekday_str(cls, timestamp):
        """Return a week day string from a timestamp in seconds."""
        return (datetime.min + timedelta(seconds=timestamp)).strftime('%A')

    @classmethod
    def y_m_d_str(cls, dateIso):
        """Return a tuple of strings: year, month, day."""
        return dateIso.split('-')

    @classmethod
    def _difference_in_years(cls, startDate, endDate):
        """Return the total number of years between startDate and endDate.
        
        Positional arguments: 
            startDate, endDate: datetime.datetime
        
        Algorithm as presented on stack overflow by Lennart Regebro
        https://stackoverflow.com/a/4455470
        """
        diffyears = endDate.year - startDate.year
        difference = endDate - startDate.replace(endDate.year)
        days_in_year = isleap(endDate.year) and 366 or 365
        years = diffyears + (difference.days + difference.seconds / 86400.0) / days_in_year
        return int(years)

    @classmethod
    def _get_duration(cls, section):
        """Return the section's duration in timedelta format."""
        if section.lastsDays:
            lastsDays = int(section.lastsDays)
        else:
            lastsDays = 0
        if section.lastsHours:
            lastsSeconds = int(section.lastsHours) * 3600
        else:
            lastsSeconds = 0
        if section.lastsMinutes:
            lastsSeconds += int(section.lastsMinutes) * 60
        return timedelta(days=lastsDays, seconds=lastsSeconds)


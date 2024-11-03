"""Helper module for date/time related calculations.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from calendar import isleap
from datetime import date
from datetime import datetime
from datetime import timedelta


def difference_in_years(startDate, endDate):
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


def get_age(nowIso, birthDateIso, deathDateIso):
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
            years = difference_in_years(deathDate, now)
            return -1 * years

    birthDate = datetime.fromisoformat(birthDateIso)
    years = difference_in_years(birthDate, now)
    return years


def get_specific_date(dayStr, refIso):
    """Return the ISO-formatted date.
    
    Positional arguments:
        dayStr:str -- Day
        refIso:str -- Reference date/time, formatted acc. to ISO 8601
    """
    # Calculate the section date from day and reference date.
    refDate = date.fromisoformat(refIso)
    return date.isoformat(refDate + timedelta(days=int(dayStr)))


def get_unspecific_date(dateIso, refIso):
    """Return the day as a string.
    
    Positional arguments:
        dateIso:str -- Date/time, formatted acc. to ISO 8601
        refIso:str -- Reference date/time, formatted acc. to ISO 8601
    """
    # Calculate the section day from date and reference date.
    refDate = date.fromisoformat(refIso)
    return str((date.fromisoformat(dateIso) - refDate).days)


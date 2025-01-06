"""Provide functions for moon phase determination.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/aeon2nv
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import math


def get_moon_phase_day(isoDate):
    """Return the phase day for the given ISO-formatted date.
    
    The phase day is 0 to 29, where 0=new moon, 15=full etc.
    Date format is 'YYYY-MM-DD'.
    This is based on a 'do it in your head' algorithm by John Conway. 
    In its current form, it's only valid for the 20th and 21st centuries.
    """
    try:
        y, m, d = isoDate.split('-')
        year = int(y)
        month = int(m)
        day = int(d)
        r = year % 100
        r %= 19
        if r > 9:
            r -= 19
        r = ((r * 11) % 30) + month + day
        if month < 3:
            r += 2
        if year < 2000:
            r -= 4
        else:
            r -= 8.3
        r = math.floor(r + 0.5) % 30
        if r < 0:
            r += 30
    except:
        r = None
    return r


def get_moon_phase_string(isoDate):
    """Return a string containing the moon phase plus a pseudo-graphic display."""
    moonViews = [
        '🌑',
        '🌑',
        '🌒',
        '🌒',
        '🌒',
        '🌒',
        '🌓',
        '🌓',
        '🌓',
        '🌓',
        '🌔',
        '🌔',
        '🌔',
        '🌔',
        '🌕',
        '🌕',
        '🌕',
        '🌖',
        '🌖',
        '🌖',
        '🌖',
        '🌗',
        '🌗',
        '🌗',
        '🌗',
        '🌘',
        '🌘',
        '🌘',
        '🌘',
        '🌑'
    ]
    moonFractions = '00¼¼¼¼½½½½¾¾¾¾111¾¾¾¾½½½½¼¼¼¼0'
    moonPhaseDay = get_moon_phase_day(isoDate)
    if moonPhaseDay is not None:
        display = f'{moonPhaseDay} {moonViews[moonPhaseDay]} {moonFractions[moonPhaseDay]}'
    else:
        display = ''
    return display


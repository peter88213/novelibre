"""Provide a class for parsing duration strings.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import re


class DurationParser:

    def __init__(self):
        self.hPattern = re.compile(r'(\d+) *h')
        self.dPattern = re.compile(r'(\d+) *d')
        self.mPattern = re.compile(r'(\d+) *min')

    def get_duration(self, durationStr):
        hours = 0
        try:
            minutes = int(self.mPattern.search(durationStr).group(1))
            hours, minutes = divmod(minutes, 60)
        except AttributeError:
            minutes = 0
        days = 0
        try:
            hours += int(self.hPattern.search(durationStr).group(1))
            days, hours = divmod(hours, 24)
        except AttributeError:
            pass
        try:
            days += int(self.dPattern.search(durationStr).group(1))
        except AttributeError:
            pass
        return days, hours, minutes


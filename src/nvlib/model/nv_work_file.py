"""Provide a class for the noveltree project file.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import date
from datetime import datetime
import os

from novxlib.novx_globals import CH_ROOT
from novxlib.novx.novx_file import NovxFile
from novxlib.novx_globals import _


class NvWorkFile(NovxFile):
    """noveltree project file representation.
    
    This is to be an adapter to the .novx project format.
    
    Public instance variables:
        timestamp: float -- Time of last file modification (number of seconds since the epoch).
    
    Public properties:
        fileDate: str -- ISO-formatted file date/time (YYYY-MM-DD hh:mm:ss).

    Extends the superclass.
    """
    DESCRIPTION = _('noveltree project')
    _LOCKFILE_PREFIX = '.LOCK.'
    _LOCKFILE_SUFFIX = '#'

    def __init__(self, filePath, **kwargs):
        """Initialize instance variables.
        
        Positional arguments:
            filePath: str -- path to the project file.
            
        Optional arguments:
            kwargs -- keyword arguments (not used here).            
        
        Extends the superclass constructor.
        """
        super().__init__(filePath)
        self.timestamp = None

    @property
    def fileDate(self):
        if self.timestamp is not None:
            return datetime.fromtimestamp(self.timestamp).replace(microsecond=0).isoformat(sep=' ')
        else:
            return _('Never')

    def adjust_section_types(self):
        """Make sure the "trash bin" is at the end.
        
        Extends the superclass method.
        """
        super().adjust_section_types()
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].isTrash and self.novel.tree.next(chId):
                self.novel.tree.move(chId, CH_ROOT, 'end')
                break

    def has_changed_on_disk(self):
        """Return True if the yw project file has changed since last opened."""
        try:
            if self.timestamp != os.path.getmtime(self.filePath):
                return True
            else:
                return False

        except:
            # this is for newly created projects
            return False

    def has_lockfile(self):
        """Return True if a project lockfile exists."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        return os.path.isfile(lockfilePath)

    def lock(self):
        """Create a project lockfile."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        if not os.path.isfile(lockfilePath):
            with open(lockfilePath, 'w') as f:
                f.write('')

    def read(self):
        """Read file, get custom data, word count log, and timestamp.
        
        Extends the superclass method.
        """
        super().read()

        #--- Read the file timestamp.
        try:
            self.timestamp = os.path.getmtime(self.filePath)
        except:
            self.timestamp = None

        #--- Keep the actual wordcount, if not logged.
        # Thus the words written with another word processor can be logged on writing.
        if self.wcLog:
            actualCountInt, actualTotalCountInt = self.count_words()
            actualCount = str(actualCountInt)
            actualTotalCount = str(actualTotalCountInt)
            latestDate = list(self.wcLog)[-1]
            latestCount = self.wcLog[latestDate][0]
            latestTotalCount = self.wcLog[latestDate][1]
            if actualCount != latestCount or actualTotalCount != latestTotalCount:
                try:
                    fileDate = date.fromtimestamp(self.timestamp).isoformat()
                except:
                    fileDate = date.today().isoformat()
                self.wcLogUpdate[fileDate] = [actualCount, actualTotalCount]

        #--- If no reasonable looking locale is set, set the system locale.
        self.novel.check_locale()

    def unlock(self):
        """Delete the project lockfile, if any."""
        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        try:
            os.remove(lockfilePath)
        except:
            pass

    def write(self):
        """Update the timestamp.
        
        Extends the superclass method.
        """
        super().write()
        self.timestamp = os.path.getmtime(self.filePath)

    def _split_file_path(self):
        head, tail = os.path.split(self.filePath)
        if head:
            head = f'{head}/'
        else:
            head = './'
        return head, tail


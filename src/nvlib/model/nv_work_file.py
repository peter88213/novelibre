"""Provide a class for the novelibre project file.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os

from nvlib.model.novx.novx_file import NovxFile
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import _


class NvWorkFile(NovxFile):
    """novelibre project file representation.
    
    Public properties:
        fileDate: str -- Localized file date/time.

    Extends the superclass.
    """
    DESCRIPTION = _('novelibre project')
    _LOCKFILE_PREFIX = '.LOCK.'
    _LOCKFILE_SUFFIX = '#'

    @property
    def fileDate(self):
        if self.timestamp is None:
            return _('Never')
        else:
            return datetime.fromtimestamp(self.timestamp).strftime('%c')

    def adjust_section_types(self):
        """Make sure the "trash bin" is at the end.
        
        Extends the superclass method.
        """
        super().adjust_section_types()
        for chId in self.novel.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].isTrash and self.novel.tree.next(chId):
                self.novel.tree.move(chId, CH_ROOT, 'end')
                return

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
        if not self.filePath:
            return

        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        return os.path.isfile(lockfilePath)

    def lock(self):
        """Create a project lockfile."""
        if not self.filePath:
            return

        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        if not os.path.isfile(lockfilePath):
            with open(lockfilePath, 'w') as f:
                f.write('')

    def read(self):
        """Read file and make sure a locale is set.
        
        Extends the superclass method.
        """
        super().read()
        self.novel.check_locale()
        # using the system locale if no reasonable looking locale is set

    def unlock(self):
        """Delete the project lockfile, if any."""
        if not self.filePath:
            return

        head, tail = self._split_file_path()
        lockfilePath = f'{head}{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
        # This cannot be done by the constructor,because filePath might change
        try:
            os.remove(lockfilePath)
        except:
            pass

    def _split_file_path(self):
        head, tail = os.path.split(self.filePath)
        if head:
            head = f'{head}/'
        else:
            head = './'
        return head, tail


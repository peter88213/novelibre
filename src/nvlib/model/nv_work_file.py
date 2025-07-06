"""Provide a class for the novelibre project file.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os

from nvlib.model.novx.novx_file import NovxFile
from nvlib.novx_globals import CH_ROOT
from nvlib.nv_locale import _


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
            if (self.novel.chapters[chId].isTrash
                and self.novel.tree.next(chId)
            ):
                self.novel.tree.move(chId, CH_ROOT, 'end')
                return

    def get_lockfile_path(self):
        """Assemble and return a path for the project's lock file."""
        # This cannot be done by the constructor,
        # because filePath might change
        try:
            head, tail = self._split_file_path()

        except:
            return None

        else:
            return (
                f'{head}'
                f'{self._LOCKFILE_PREFIX}{tail}{self._LOCKFILE_SUFFIX}'
            )

    def has_changed_on_disk(self):
        """Return True if the project file has changed since last opened."""
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
        # This cannot be done by the constructor,
        # because filePath might change
        if not self.filePath:
            return None

        return os.path.isfile(self.get_lockfile_path())

    def lock(self):
        """Create a project lockfile."""
        # This cannot be done by the constructor,
        # because filePath might change
        if not self.filePath:
            return

        lockfilePath = self.get_lockfile_path()
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
        # This cannot be done by the constructor,
        # because filePath might change
        if not self.filePath:
            return

        try:
            os.remove(self.get_lockfile_path())
        except:
            pass

    def _split_file_path(self):
        head, tail = os.path.split(self.filePath)
        if head:
            head = f'{head}/'
        else:
            head = './'
        return head, tail


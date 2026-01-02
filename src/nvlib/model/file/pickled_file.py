"""Provide a class for binary file representation.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import pickle

from nvlib.model.file.file import File
from nvlib.nv_locale import _


class PickledFile(File):

    DESCRIPTION = _('novelibre project binary')
    EXTENSION = '.pickle'

    def read(self):
        with open(self.filePath, 'rb') as f:
            self.novel, self.wcLog = pickle.load(f)

    def write(self):
        with open(self.filePath, 'wb') as f:
            pickle.dump((self.novel, self.wcLog), f)


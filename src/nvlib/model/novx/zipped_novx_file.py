"""Provide a class for zipped novx file import.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.novx.novx_file import NovxFile
from nvlib.model.novx.zipped_novx_opener import ZippedNovxOpener


class ZippedNovxFile(NovxFile):

    DESCRIPTION = _('Zipped novelibre project')
    EXTENSION = '.zip'

    fileOpener = ZippedNovxOpener

    def write(self):
        raise NotImplementedError

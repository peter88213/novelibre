"""Regression test for novelibre file processing.

Test the conversion of the metadata text.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

import unittest

from nvlib.model.ods.ods_r_metadata_text import OdsRMetadataText
from nvlib.model.ods.ods_w_metadata_text import OdsWMetadataText
from testlib.import_export_test import ImportExportTest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = OdsRMetadataText
    _exportClass = OdsWMetadataText

    # The test methods must be defined here to identify the source of failure.

    def test_novx_to_exp(self):
        super().test_novx_to_exp()

    def test_imp_to_novx(self):
        super().test_imp_to_novx()

    def test_data(self):
        super().test_data()


def main():
    unittest.main()


if __name__ == '__main__':
    main()

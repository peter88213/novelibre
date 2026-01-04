"""Regression test for novelibre file processing.

Test the conversion of the manuscript with unused text.

For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import unittest

from nvlib.model.odt.odt_r_full import OdtRFull
from nvlib.model.odt.odt_w_full import OdtWFull
from testlib.import_export_test import ImportExportTest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = OdtRFull
    _exportClass = OdtWFull

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

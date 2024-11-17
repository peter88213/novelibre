"""Regression test for novelibre file processing.

Test the conversion of the manuscript.

For further information see https://github.com/peter88213/novelibre
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from nvlib.model.odt.odt_r_manuscript import OdtRManuscript
from nvlib.model.odt.odt_w_manuscript import OdtWManuscript
from testlib.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = OdtRManuscript
    _exportClass = OdtWManuscript

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

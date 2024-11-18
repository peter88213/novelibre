"""Regression test for novelibre file processing.

Test the import of an outline.

For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_r_outline import OdtROutline
from testlib.import_test import ImportTest
import unittest


class NrmOpr(ImportTest, unittest.TestCase):
    _dataPath = '../test/data/_outline/'
    _importClass = OdtROutline

    # The test methods must be defined here to identify the source of failure.

    def test_imp_to_novx(self):
        super().test_imp_to_novx()


def main():
    unittest.main()


if __name__ == '__main__':
    main()

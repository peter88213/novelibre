"""Regression test for novelibre file processing.

Test the odt brief synopsis.

For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.model.odt.odt_w_brief_synopsis import OdtWBriefSynopsis
from testlib.export_test import ExportTest
import unittest


class NrmOpr(ExportTest, unittest.TestCase):
    _exportClass = OdtWBriefSynopsis

    # The test methods must be defined here to identify the source of failure.

    def test_novx_to_exp(self):
        super().test_novx_to_exp()


def main():
    unittest.main()


if __name__ == '__main__':
    main()

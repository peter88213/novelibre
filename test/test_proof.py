"""Regression test for novelibre file processing.

Test the conversion of the proofread-manuscript.

For further information see https://github.com/peter88213/novelibre
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from nvlib.model.odt.odt_r_proof import OdtRProof
from nvlib.model.odt.odt_w_proof import OdtWProof
from testlib.import_export_test import ImportExportTest
import unittest


class NrmOpr(ImportExportTest, unittest.TestCase):
    _importClass = OdtRProof
    _exportClass = OdtWProof

    # The test methods must be defined here to identify the source of failure.

    def test_novx_to_exp(self):
        super().test_novx_to_exp()

    def test_imp_to_novx(self):
        super().test_imp_to_novx()

    def test_data(self):
        super().test_data()


class ImportFromWord(ImportExportTest, unittest.TestCase):
    """Convert an ODT proofread document saved by MS Word."""
    _importClass = OdtRProof
    _exportClass = OdtWProof

    def _init_paths(self):
        """Initialize the test data and execution paths."""
        super()._init_paths()
        self._prfImpFile = f'{self._dataPath}word{self._importClass.EXTENSION}'
        self._prfNovxFile = f'{self._dataPath}word.novx'

    # The test methods must be defined here to identify the source of failure.

    def test_imp_to_novx(self):
        super().test_imp_to_novx()

    def _remove_all_tempfiles(self):
        super()._remove_all_tempfiles()

    def test_data(self):
        pass


class ImportFromGoogledocs(ImportExportTest, unittest.TestCase):
    """Convert an ODT proofread document saved by MS Word."""
    _importClass = OdtRProof
    _exportClass = OdtWProof

    def _init_paths(self):
        """Initialize the test data and execution paths."""
        super()._init_paths()
        self._prfImpFile = f'{self._dataPath}googledocs{self._importClass.EXTENSION}'
        self._prfNovxFile = f'{self._dataPath}googledocs.novx'

    # The test methods must be defined here to identify the source of failure.

    def test_imp_to_novx(self):
        super().test_imp_to_novx()

    def _remove_all_tempfiles(self):
        super()._remove_all_tempfiles()

    def test_data(self):
        pass


def main():
    unittest.main()


if __name__ == '__main__':
    main()

"""Provide an abstract test case class for novelibre import and export.

Import/export standard test routines used for Regression test.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from shutil import copyfile

from nvlib.model.converter.novx_converter import NovxConverter
from testlib.export_test import ExportTest
from testlib.helper import read_file

UPDATE = False


class ImportExportTest(ExportTest):
    """Test case: Import and export yWriter project.
    
    Subclasses must also inherit from unittest.TestCase
    """
    _importClass = None

    def test_data(self):
        """Verify test data integrity. 

        Initial test data must differ from the "proofed" test data.
        """
        self.assertNotEqual(read_file(self._refNovxFile), read_file(self._prfNovxFile))

    def test_imp_to_novx(self):
        """Test ODF import to novelibre, using the YwCnvUi converter class. 
        
        - Overwrite the initial yWriter project file.
        - Compare the generated yWriter project file with the reference file.
        - Compare the yWriter backup with the initial project file.
        """
        copyfile(self._prfImpFile, self._testImpFile)
        converter = NovxConverter()
        converter.run(self._testImpFile)
        if UPDATE:
            copyfile(self._testNovxFile, self._prfNovxFile)
        self.assertEqual(read_file(self._testNovxFile), read_file(self._prfNovxFile))
        self.assertEqual(read_file(self._ywBakFile), read_file(self._refNovxFile))

    def _init_paths(self):
        """Initialize the test data and execution paths."""
        super()._init_paths()
        self._testImpFile = f'{self._execPath}yw7 Sample Project{self._importClass.SUFFIX}{self._importClass.EXTENSION}'
        self._refImpFile = f'{self._dataPath}normal{self._importClass.EXTENSION}'
        self._prfImpFile = f'{self._dataPath}proofed{self._importClass.EXTENSION}'

    def _remove_all_tempfiles(self):
        """Clean up the test execution directory."""
        super()._remove_all_tempfiles()
        try:
            os.remove(self._testImpFile)
        except:
            pass


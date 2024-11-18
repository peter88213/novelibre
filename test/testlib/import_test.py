"""Provide an abstract test case class for novelibre import.

Import standard test routines used for Regression test.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from shutil import copyfile

from nvlib.model.converter.novx_converter import NovxConverter
from nvlib.novx_globals import _
from nvlib.novx_globals import norm_path
from testlib.helper import read_file

UPDATE = False


class ImportTest:
    """Test case: Import yWriter project.
    
    Subclasses must also inherit from unittest.TestCase
    """
    _importClass = None

    def setUp(self):
        """Set up the test environment.
        
        - Initialize the test data and execution paths.
        - Make sure the directory for text execution exists.
        - Remove files that may remain from previous tests.
        """
        self._init_paths()
        try:
            os.mkdir(self._execPath)
        except:
            pass
        self._remove_all_tempfiles()

    def tearDown(self):
        """Clean up the test execution directory.
        
        This method is called by the unit test framework.
        """
        self._remove_all_tempfiles()

    def test_imp_to_novx(self):
        """Test ODF import to novelibre, using the YwCnvUi converter class. 
        
        Compare the generated yWriter project file with the reference file.
        """
        copyfile(self._refImpFile, self._testImpFile)
        converter = NovxConverter()
        converter.run(self._testImpFile)
        self.assertEqual(converter.ui.infoHowText, f'{_("File written")}: "{norm_path(self._testNovxFile)}".')
        if UPDATE:
            copyfile(self._testNovxFile, self._refNovxFile)
        self.assertEqual(read_file(self._testNovxFile), read_file(self._refNovxFile))

    def _init_paths(self):
        """Initialize the test data and execution paths."""
        if not hasattr(self, '_dataPath'):
            self._dataPath = f'../test/data/{self._importClass.SUFFIX.replace("_tmp","")}/'
        self._execPath = '../test/tmp/'
        self._testNovxFile = f'{self._execPath}yw7 Sample Project.novx'
        self._refNovxFile = f'{self._dataPath}normal.novx'
        self._testImpFile = f'{self._execPath}yw7 Sample Project{self._importClass.SUFFIX}{self._importClass.EXTENSION}'
        self._refImpFile = f'{self._dataPath}normal{self._importClass.EXTENSION}'

    def _remove_all_tempfiles(self):
        """Clean up the test execution directory."""
        try:
            os.remove(self._testImpFile)
        except:
            pass
        try:
            os.remove(self._testNovxFile)
        except:
            pass


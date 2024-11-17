"""Provide an abstract test case class for novelibre export.

Export standard test routines used for Regression test.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
import os
from shutil import copyfile
import zipfile

from nvlib.model.converter.novx_converter import NovxConverter
from nvlib.novx_globals import _
from nvlib.novx_globals import norm_path
from testlib.helper import read_file

UPDATE = False


class ExportTest:
    """Test case: Import and export yWriter project.
    
    Subclasses must also inherit from unittest.TestCase
    """
    _exportClass = None

    def setUp(self):
        """Set up the test environment.
        
        - Initialize the test data and execution paths.
        - Make sure the directory for text execution exists.
        - Remove files that may remain from previous tests.
        - Create a test yWriter project.
        """
        self._init_paths()
        os.makedirs(self._execPath, exist_ok=True)
        self._remove_all_tempfiles()
        copyfile(self._refNovxFile, self._testNovxFile)

    def tearDown(self):
        """Clean up the test execution directory.
        
        This method is called by the unit test framework.
        """
        self._remove_all_tempfiles()

    def test_novx_to_exp(self):
        """Test ODF export from yWriter, using the YwCnvUi converter class. 
        
        Compare the generated content XML file with the reference file.
        """
        converter = NovxConverter()
        kwargs = {'suffix': self._exportClass.SUFFIX}
        converter.run(self._testNovxFile, **kwargs)
        self.assertEqual(converter.ui.infoHowText, f'{_("File written")}: "{ norm_path(self._testExpFile)}".')
        with zipfile.ZipFile(self._testExpFile, 'r') as myzip:
            myzip.extract(self._odfCntntFile, self._execPath)
        if UPDATE:
            copyfile(f'{self._execPath}{self._odfCntntFile}', f'{self._dataPath}{self._odfCntntFile}')
        self.assertEqual(read_file(f'{self._execPath}{self._odfCntntFile}'),
                         read_file(f'{self._dataPath}{self._odfCntntFile}'))

    def _init_paths(self):
        """Initialize the test data and execution paths."""
        if not hasattr(self, '_dataPath'):
            self._dataPath = f'../test/data/{self._exportClass.SUFFIX.replace("_tmp","")}/'
        self._execPath = '../test/tmp/'
        self._testExpFile = f'{self._execPath}yw7 Sample Project{self._exportClass.SUFFIX}{self._exportClass.EXTENSION}'
        self._odfCntntFile = 'content.xml'
        self._testNovxFile = f'{self._execPath}yw7 Sample Project.novx'
        self._ywBakFile = f'{self._testNovxFile}.bak'
        self._refNovxFile = f'{self._dataPath}normal.novx'
        self._prfNovxFile = f'{self._dataPath}proofed.novx'

    def _remove_all_tempfiles(self):
        """Clean up the test execution directory."""
        try:
            os.remove(self._testExpFile)
        except:
            pass
        try:
            os.remove(self._testNovxFile)
        except:
            pass
        try:
            os.remove(self._ywBakFile)
        except:
            pass
        try:
            os.remove(f'{self._execPath}{self._odfCntntFile}')
        except:
            pass


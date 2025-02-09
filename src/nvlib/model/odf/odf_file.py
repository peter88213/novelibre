"""Provide a generic class for OpenDocument xml file export.

All ODS and ODT file representations inherit from this class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os
from shutil import rmtree
from string import Template
import tempfile
import zipfile

from nvlib.model.file.file_export import FileExport
from nvlib.model.odf.check_odf import odf_is_locked
from nvlib.novx_globals import Error
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _


class OdfFile(FileExport):
    """Generic OpenDocument xml file representation."""
    _ODF_COMPONENTS = []
    _MIMETYPE = ''
    _SETTINGS_XML = ''
    _MANIFEST_XML = ''
    _STYLES_XML = ''
    _META_XML = ''

    def __init__(self, filePath, **kwargs):
        """Create a temporary directory for zipfile generation.
        
        Positional arguments:
            filePath: str -- path to the file represented by the Novel instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            

        Extends the superclass constructor,        
        """
        super().__init__(filePath, **kwargs)
        self._tempDir = tempfile.mkdtemp(suffix='.tmp', prefix='odf_')
        self._originalPath = self._filePath

    def __del__(self):
        """Make sure to delete the temporary directory, in case write() has not been called."""
        self._tear_down()

    def is_locked(self):
        """Return True if the file is locked by its application."""
        return odf_is_locked(self.filePath)

    def write_content_xml(self):
        super().write()

    def write(self):
        """Write instance variables to the export file.
        
        Create a template-based output file. 
        Raise the "Error" exception in case of error. 
        Extends the super class method, adding ZIP file operations.
        """

        #--- Create a temporary directory
        # containing the internal structure of an ODS file except "content.xml".
        self._set_up()

        #--- Add "content.xml" to the temporary directory.
        self._originalPath = self._filePath
        self._filePath = f'{self._tempDir}/content.xml'
        self.write_content_xml()
        self._filePath = self._originalPath

        #--- Pack the contents of the temporary directory into the ODF file.
        workdir = os.getcwd()
        backedUp = False
        if os.path.isfile(self.filePath):
            try:
                os.replace(self.filePath, f'{self.filePath}.bak')
            except:
                raise Error(f'{_("Cannot overwrite file")}: "{norm_path(self.filePath)}".')
            else:
                backedUp = True
        try:
            with zipfile.ZipFile(self.filePath, 'w') as odfTarget:
                os.chdir(self._tempDir)
                for file in self._ODF_COMPONENTS:
                    odfTarget.write(file, compress_type=zipfile.ZIP_DEFLATED)
        except:
            os.chdir(workdir)
            if backedUp:
                os.replace(f'{self.filePath}.bak', self.filePath)
            raise Error(f'{_("Cannot create file")}: "{norm_path(self.filePath)}".')

        #--- Remove temporary data.
        os.chdir(workdir)
        self._tear_down()
        return f'{_("File written")}: "{norm_path(self.filePath)}".'

    def _add_novelibre_styles(self, stylesXmlStr):
        """Template method for modifying the ODF styles.xml contents."""
        return stylesXmlStr

    def _set_up(self):
        """Helper method for ZIP file generation.

        Prepare the temporary directory containing the internal structure of an ODF file except 'content.xml'.
        Raise the "Error" exception in case of error. 
        """

        #--- Create and open a temporary directory for the files to zip.
        try:
            self._tear_down()
            os.mkdir(self._tempDir)
            os.mkdir(f'{self._tempDir}/META-INF')
        except:
            raise Error(f'{_("Cannot create directory")}: "{norm_path(self._tempDir)}".')

        #--- Generate mimetype.
        try:
            with open(f'{self._tempDir}/mimetype', 'w', encoding='utf-8') as f:
                f.write(self._MIMETYPE)
        except:
            raise Error(f'{_("Cannot write file")}: "mimetype"')

        #--- Generate settings.xml.
        try:
            with open(f'{self._tempDir}/settings.xml', 'w', encoding='utf-8') as f:
                f.write(self._SETTINGS_XML)
        except:
            raise Error(f'{_("Cannot write file")}: "settings.xml"')

        #--- Generate META-INF\manifest.xml.
        try:
            with open(f'{self._tempDir}/META-INF/manifest.xml', 'w', encoding='utf-8') as f:
                f.write(self._MANIFEST_XML)
        except:
            raise Error(f'{_("Cannot write file")}: "manifest.xml"')

        #--- Generate styles.xml.
        self.novel.check_locale()
        localeMapping = dict(
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,
        )
        template = Template(self._STYLES_XML)
        stylesXmlStr = template.safe_substitute(localeMapping)
        stylesXmlStr = self._add_novelibre_styles(stylesXmlStr)
        try:
            with open(f'{self._tempDir}/styles.xml', 'w', encoding='utf-8') as f:
                f.write(stylesXmlStr)
        except:
            raise Error(f'{_("Cannot write file")}: "styles.xml"')

        #--- Generate meta.xml with actual document metadata.
        metaMapping = dict(
            Author=self.novel.authorName,
            Title=self.novel.title,
            Summary=f'<![CDATA[{self.novel.desc}]]>',
            Datetime=datetime.today().replace(microsecond=0).isoformat(),
        )
        template = Template(self._META_XML)
        stylesXmlStr = template.safe_substitute(metaMapping)
        try:
            with open(f'{self._tempDir}/meta.xml', 'w', encoding='utf-8') as f:
                f.write(stylesXmlStr)
        except:
            raise Error(f'{_("Cannot write file")}: "meta.xml".')

    def _tear_down(self):
        """Delete the temporary directory containing the unpacked ODF directory structure."""
        try:
            rmtree(self._tempDir)
        except:
            pass


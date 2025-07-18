"""Provide a generic class for OpenDocument xml file export.

All ODS and ODT file representations inherit from this class.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
from xml.sax.saxutils import escape
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

    NAMESPACES = dict(
        office='urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        style='urn:oasis:names:tc:opendocument:xmlns:style:1.0',
        text='urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        table='urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        draw='urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
        fo='urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
        xlink='http://www.w3.org/1999/xlink',
        dc='http://purl.org/dc/elements/1.1/',
        meta='urn:oasis:names:tc:opendocument:xmlns:meta:1.0',
        number='urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0',
        svg='urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0',
        chart='urn:oasis:names:tc:opendocument:xmlns:chart:1.0',
        dr3d='urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0',
        math='http://www.w3.org/1998/Math/MathML',
        form='urn:oasis:names:tc:opendocument:xmlns:form:1.0',
        script='urn:oasis:names:tc:opendocument:xmlns:script:1.0',
        ooo='http://openoffice.org/2004/office',
        ooow='http://openoffice.org/2004/writer',
        oooc='http://openoffice.org/2004/calc',
        dom='http://www.w3.org/2001/xml-events',
        rpt='http://openoffice.org/2005/report',
        of='urn:oasis:names:tc:opendocument:xmlns:of:1.2',
        xhtml='http://www.w3.org/1999/xhtml',
        grddl='http://www.w3.org/2003/g/data-view#',
        tableooo='http://openoffice.org/2009/table',
        loext=(
            'urn:org:documentfoundation:names:experimental:'
            'office:xmlns:loext:1.0'
        ),
    )

    def __init__(self, filePath, **kwargs):
        """Create a temporary directory for zipfile generation.
        
        Positional arguments:
            filePath: str -- path to the file 
                             represented by the Novel instance.
            
        Optional arguments:
            kwargs -- keyword arguments to be used by subclasses.            

        Extends the superclass constructor,        
        """
        super().__init__(filePath, **kwargs)
        self._tempDir = tempfile.mkdtemp(suffix='.tmp', prefix='odf_')
        self._originalPath = self._filePath

    def __del__(self):
        # Make sure to delete the temporary directory,
        # in case write() has not been called.
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
        # containing the internal structure of an ODS file
        # except "content.xml".
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
                raise Error(
                    (
                        f'{_("Cannot overwrite file")}: '
                        f'"{norm_path(self.filePath)}".'
                    )
                )
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
            raise Error(
                (
                    f'{_("Cannot create file")}: '
                    f'"{norm_path(self.filePath)}".'
                )
            )

        #--- Remove temporary data.
        os.chdir(workdir)
        self._tear_down()
        return f'{_("File written")}: "{norm_path(self.filePath)}".'

    def _escape(self, text):
        try:
            return escape(text)

        except AttributeError:
            return text

    def _get_styles_xml_str(self):
        """Return the styles.xml data as a string."""
        self.novel.check_locale()
        localeMapping = dict(
            Language=self.novel.languageCode,
            Country=self.novel.countryCode,
        )
        template = Template(self._STYLES_XML)
        stylesXmlStr = template.safe_substitute(localeMapping)
        return stylesXmlStr

    def _set_up(self):
        # Helper method for ZIP file generation.
        # Prepare the temporary directory containing the internal structure
        # of an ODF file except 'content.xml'.
        # Raise the "Error" exception in case of error.

        #--- Create and open a temporary directory for the files to zip.
        try:
            self._tear_down()
            os.mkdir(self._tempDir)
            os.mkdir(f'{self._tempDir}/META-INF')
        except:
            raise Error(
                (
                    f'{_("Cannot create directory")}: '
                    f'"{norm_path(self._tempDir)}".'
                )
            )
        #--- Generate mimetype.
        try:
            with open(
                f'{self._tempDir}/mimetype',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(self._MIMETYPE)
        except:
            raise Error(f'{_("Cannot write file")}: "mimetype"')

        #--- Generate settings.xml.
        try:
            with open(
                f'{self._tempDir}/settings.xml',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(self._SETTINGS_XML)
        except:
            raise Error(f'{_("Cannot write file")}: "settings.xml"')

        #--- Generate META-INF\manifest.xml.
        try:
            with open(
                f'{self._tempDir}/META-INF/manifest.xml',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(self._MANIFEST_XML)
        except:
            raise Error(f'{_("Cannot write file")}: "manifest.xml"')

        #--- Generate styles.xml.
        stylesXmlStr = self._get_styles_xml_str()
        try:
            with open(
                f'{self._tempDir}/styles.xml',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(stylesXmlStr)
        except:
            raise Error(f'{_("Cannot write file")}: "styles.xml"')

        #--- Generate meta.xml with actual document metadata.
        metaMapping = dict(
            Author=self._escape(self.novel.authorName),
            Title=self._escape(self.novel.title),
            Summary=self._escape(self.novel.desc),
            Datetime=datetime.today().replace(microsecond=0).isoformat(),
        )
        template = Template(self._META_XML)
        stylesXmlStr = template.safe_substitute(metaMapping)
        try:
            with open(
                f'{self._tempDir}/meta.xml',
                'w',
                encoding='utf-8'
            ) as f:
                f.write(stylesXmlStr)
        except:
            raise Error(f'{_("Cannot write file")}: "meta.xml".')

    def _tear_down(self):
        # Delete the temporary directory containing the
        # unpacked ODF directory structure.
        try:
            rmtree(self._tempDir)
        except:
            pass


"""Provide a converter class for novelibre universal import and export.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
import os
from tkinter import messagebox

from novxlib.converter.import_source_factory import ImportSourceFactory
from novxlib.converter.import_target_factory import ImportTargetFactory
from novxlib.converter.new_project_factory import NewProjectFactory
from novxlib.novx.novx_file import NovxFile
from novxlib.novx_globals import Error
from novxlib.novx_globals import _
from novxlib.novx_globals import norm_path
from novxlib.ods.ods_r_charlist import OdsRCharList
from novxlib.ods.ods_r_grid import OdsRGrid
from novxlib.ods.ods_r_itemlist import OdsRItemList
from novxlib.ods.ods_r_loclist import OdsRLocList
from novxlib.odt.odt_r_chapterdesc import OdtRChapterDesc
from novxlib.odt.odt_r_characters import OdtRCharacters
from novxlib.odt.odt_r_items import OdtRItems
from novxlib.odt.odt_r_locations import OdtRLocations
from novxlib.odt.odt_r_manuscript import OdtRManuscript
from novxlib.odt.odt_r_partdesc import OdtRPartDesc
from novxlib.odt.odt_r_plotlines import OdtRPlotlines
from novxlib.odt.odt_r_proof import OdtRProof
from novxlib.odt.odt_r_sectiondesc import OdtRSectionDesc
from novxlib.odt.odt_r_stages import OdtRStages
from nvlib.nv_globals import prefs


class NvDocImporter:
    """A converter for universal import.

    Support novelibre projects and most of the File subclasses 
    that are written with OpenOffice/LibreOffice Writer or Calc.
    """
    IMPORT_SOURCE_CLASSES = [
        OdsRCharList,
        OdsRGrid,
        OdsRItemList,
        OdsRLocList,
        OdtRChapterDesc,
        OdtRCharacters,
        OdtRItems,
        OdtRLocations,
        OdtRManuscript,
        OdtRPartDesc,
        OdtRPlotlines,
        OdtRProof,
        OdtRSectionDesc,
        OdtRStages,
        ]
    CREATE_SOURCE_CLASSES = []

    def __init__(self):
        """Set up the Factory strategies."""
        self.importSourceFactory = ImportSourceFactory(self.IMPORT_SOURCE_CLASSES)
        self.newProjectFactory = NewProjectFactory(self.CREATE_SOURCE_CLASSES)
        self.importTargetFactory = ImportTargetFactory([NovxFile])
        self.newFile = None

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.

        Positional arguments: 
            sourcePath: str -- the source file path.
        
        Required keyword arguments: 
            suffix: str -- target file name suffix.

        On success, return a message. Otherwise raise the Error exception.
        """
        self.newFile = None
        if not os.path.isfile(sourcePath):
            raise Error(f'{_("File not found")}: "{norm_path(sourcePath)}".')

        try:
            source, __ = self.importSourceFactory.make_file_objects(sourcePath, **kwargs)
        except Error:

            #--- Import a document without section markers.
            source, target = self.newProjectFactory.make_file_objects(sourcePath, **kwargs)
            if os.path.isfile(target.filePath):
                # do not overwrite an existing novelibre project with a non-tagged document
                raise Error(f'{_("File already exists")}: "{norm_path(target.filePath)}".')

            self._check(source, target)
            source.novel = kwargs['nv_service'].make_novel()
            source.read()
            target.novel = source.novel
            target.write()
            self.newFile = target.filePath
            return f'{_("File written")}: "{norm_path(target.filePath)}".'

        else:

            #--- Import a document with section markers.
            kwargs['suffix'] = source.SUFFIX
            __, target = self.importTargetFactory.make_file_objects(sourcePath, **kwargs)
            self.newFile = None
            self._check(source, target)
            target.novel = kwargs['nv_service'].make_novel()
            target.read()
            source.novel = target.novel
            source.read()
            if source.sectionsSplit and source.is_locked():
                raise Error(f'{_("Please close the document first")}.')

            if os.path.isfile(target.filePath):
                if not messagebox.askyesno(
                    title=source.DESCRIPTION,
                    message=_('Update the project?')
                    ):
                    raise Error(f'{_("Action canceled by user")}.')

            target.novel = source.novel
            target.write()
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
            if source.sectionsSplit:
                os.replace(source.filePath, f'{source.filePath}.bak')
                message = f'{message} - {_("Source document deleted")}.'
            return message

    def _check(self, source, target):
        """Error handling"""
        if source.filePath is None:
            # the source is not correctly initialized
            raise Error(f'{_("File type is not supported")}.')

        if not os.path.isfile(source.filePath):
            # the source document does not exist
            raise Error(f'{_("File not found")}: "{norm_path(source.filePath)}".')

        if source.is_locked():
            # the document might be open in the Office application
            if not prefs['import_mode'] == '2':
                raise Error(f'{_("Please close the document first")}.')


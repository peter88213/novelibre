"""Provide a class for Novel file conversion with file factories.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.model.converter.converter import Converter
from nvlib.model.converter.export_source_factory import ExportSourceFactory
from nvlib.model.converter.export_target_factory import ExportTargetFactory
from nvlib.model.converter.import_source_factory import ImportSourceFactory
from nvlib.model.converter.import_target_factory import ImportTargetFactory
from nvlib.novx_globals import Error
from nvlib.novx_globals import _
from nvlib.novx_globals import norm_path


class ConverterFf(Converter):
    """Class for Novel file conversion using factory methods to create target and source classes.

    Class constants:
        EXPORT_SOURCE_CLASSES -- list of NovxFile subclasses from which can be exported.
        EXPORT_TARGET_CLASSES -- list of FileExport subclasses to which export is possible.
        IMPORT_SOURCE_CLASSES -- list of File subclasses from which can be imported.
        IMPORT_TARGET_CLASSES -- list of NovxFile subclasses to which import is possible.

    All lists are empty and meant to be overridden by subclasses.

    Instance variables:
        exportSourceFactory: ExportSourceFactory.
        exportTargetFactory: ExportTargetFactory.
        importSourceFactory: ImportSourceFactory.
        importTargetFactory: ImportTargetFactory.
        newProjectFactory: FileFactory (to be overridden by subclasses).
    """
    EXPORT_SOURCE_CLASSES = []
    EXPORT_TARGET_CLASSES = []
    IMPORT_SOURCE_CLASSES = []
    IMPORT_TARGET_CLASSES = []

    def __init__(self):
        """Create strategy class instances.
        
        Extends the superclass constructor.
        """
        super().__init__()
        self.exportSourceFactory = ExportSourceFactory(self.EXPORT_SOURCE_CLASSES)
        self.exportTargetFactory = ExportTargetFactory(self.EXPORT_TARGET_CLASSES)
        self.importSourceFactory = ImportSourceFactory(self.IMPORT_SOURCE_CLASSES)
        self.importTargetFactory = ImportTargetFactory(self.IMPORT_TARGET_CLASSES)
        self.newProjectFactory = None

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.

        Positional arguments: 
            sourcePath: str -- the source file path.
        
        Required keyword arguments: 
            suffix: str -- target file name suffix.

        This is a template method that calls superclass methods as primitive operations by case.
        """
        self.newFile = None
        if not os.path.isfile(sourcePath):
            self.ui.set_status(f'!{_("File not found")}: "{norm_path(sourcePath)}".')
            return

        try:
            source, __ = self.exportSourceFactory.new_file_objects(sourcePath, **kwargs)
        except Error:
            # The source file is not a novelibre project.
            try:
                source, __ = self.importSourceFactory.new_file_objects(sourcePath, **kwargs)
            except Error:
                # A new novelibre project might be required.
                try:
                    source, target = self.newProjectFactory.new_file_objects(sourcePath, **kwargs)
                except Error as ex:
                    self.ui.set_status(f'!{str(ex)}')
                else:
                    self.create_novx(source, target)
            else:
                # Try to update an existing novelibre project.
                kwargs['suffix'] = source.SUFFIX
                try:
                    __, target = self.importTargetFactory.new_file_objects(sourcePath, **kwargs)
                except Error as ex:
                    self.ui.set_status(f'!{str(ex)}')
                else:
                    self.import_to_novx(source, target)
        else:
            # The source file is a novelibre project.
            try:
                __, target = self.exportTargetFactory.new_file_objects(sourcePath, **kwargs)
            except Error as ex:
                self.ui.set_status(f'!{str(ex)}')
            else:
                self.export_from_novx(source, target)

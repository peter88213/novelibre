"""Provide a class for Novel file conversion.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.model.converter.export_source_factory import ExportSourceFactory
from nvlib.model.converter.export_target_factory import ExportTargetFactory
from nvlib.model.converter.import_source_factory import ImportSourceFactory
from nvlib.model.converter.import_target_factory import ImportTargetFactory
from nvlib.model.data.novel import Novel
from nvlib.model.data.nv_tree import NvTree
from nvlib.novx_globals import Error
from nvlib.novx_globals import Notification
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _
from nvlib.user_interface.ui import Ui


class Converter:
    """Class for Novel file conversion.
    
    Use factory methods to create target and source classes.

    Class constants:
        EXPORT_SOURCE_CLASSES -- list of NovxFile subclasses 
                                 from which can be exported.
        EXPORT_TARGET_CLASSES -- list of FileExport subclasses 
                                 to which export is possible.
        IMPORT_SOURCE_CLASSES -- list of File subclasses 
                                 from which can be imported.
        IMPORT_TARGET_CLASSES -- list of NovxFile subclasses 
                                 to which import is possible.

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

    NO_SCN_FIELD1_DEFAULT = _('Plot progress')
    NO_SCN_FIELD2_DEFAULT = _('Characterization')
    NO_SCN_FIELD3_DEFAULT = _('World building')
    OTHER_SCN_FIELD1_DEFAULT = _('Opening')
    OTHER_SCN_FIELD2_DEFAULT = _('Peak emotional moment')
    OTHER_SCN_FIELD3_DEFAULT = _('Ending')
    CHR_EXTRA_FIELD_1_DEFAULT = _('Goals')
    CHR_EXTRA_FIELD_2_DEFAULT = _('Role')

    def __init__(self):
        """Create strategy class instances."""
        """Define instance variables."""
        self.ui = Ui('')
        # Per default, 'silent mode' is active.
        self.newFile = None
        # Also indicates successful conversion.
        self.exportSourceFactory = ExportSourceFactory(
            self.EXPORT_SOURCE_CLASSES)
        self.exportTargetFactory = ExportTargetFactory(
            self.EXPORT_TARGET_CLASSES)
        self.importSourceFactory = ImportSourceFactory(
            self.IMPORT_SOURCE_CLASSES)
        self.importTargetFactory = ImportTargetFactory(
            self.IMPORT_TARGET_CLASSES)
        self.newProjectFactory = None

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.

        Positional arguments: 
            sourcePath: str -- the source file path.
        
        Required keyword arguments: 
            suffix: str -- target file name suffix.

        This is a template method that calls superclass methods 
        as primitive operations by case.
        """
        self.newFile = None
        if not os.path.isfile(sourcePath):
            self.ui.set_status(
                (
                    f'!{_("File not found")}: '
                    f'"{norm_path(sourcePath)}".'
                )
            )
            return

        try:
            source, __ = self.exportSourceFactory.new_file_objects(
                sourcePath,
                **kwargs
            )
        except Error:
            # The source file is not a novelibre project.
            try:
                source, __ = self.importSourceFactory.new_file_objects(
                    sourcePath,
                    **kwargs
                )
            except Error:
                # A new novelibre project might be required.
                try:
                    (
                        source,
                        target
                    ) = self.newProjectFactory.new_file_objects(
                        sourcePath,
                        **kwargs
                    )
                except Error as ex:
                    self.ui.set_status(f'!{str(ex)}')
                else:
                    self._create_novx(source, target)
            else:
                # Try to update an existing novelibre project.
                kwargs['suffix'] = source.SUFFIX
                try:
                    (
                        __,
                        target
                    ) = self.importTargetFactory.new_file_objects(
                        sourcePath,
                        **kwargs
                    )
                except Error as ex:
                    self.ui.set_status(f'!{str(ex)}')
                else:
                    self._import_to_novx(source, target)
        else:
            # The source file is a novelibre project.
            try:
                (
                    __,
                    target
                ) = self.exportTargetFactory.new_file_objects(
                    sourcePath,
                    **kwargs
                )
            except Error as ex:
                self.ui.set_status(f'!{str(ex)}')
            else:
                self._export_from_novx(source, target)

    def _check(self, source, target):
        """Error handling:
        
        - Check if source and target are correctly initialized.
        - Ask for permission to overwrite target.
        - Check whether a source or target document is locked 
          by tis application.
        - Raise the "Error" exception in case of error. 
        """
        if source.filePath is None:
            raise Error(f'{_("File type is not supported")}.')

        if not os.path.isfile(source.filePath):
            raise Error(
                (
                    f'{_("File not found")}: '
                    f'"{norm_path(source.filePath)}".'
                )
            )

        if source.is_locked():
            raise Error(f'{_("Please close the document first")}".')

        if target.is_locked():
            raise Error(f'{_("Please close the document first")}.')

        if target.filePath is None:
            raise Error(f'{_("File type is not supported")}.')

        if (
            os.path.isfile(target.filePath)
            and not self._confirm_overwrite(target.filePath)
        ):
            raise Notification(f'{_("Action canceled by user")}.')

    def _confirm_overwrite(self, filePath):
        """Return boolean permission to overwrite the target file.
        
        Positional arguments:
            fileName -- path to the target file.
        
        Overrides the superclass method.
        """
        return self.ui.ask_yes_no(
            message=_('Overwrite existing file?'),
            detail=norm_path(filePath)
            )

    def _create_novx(self, source, target):
        """Create target from source.

        Positional arguments:
            source -- Any Novel subclass instance.
            target -- NovxFile subclass instance.

        Operation:
        1. Send specific information about the conversion to the UI.
        2. Convert source into target.
        3. Pass the status message to the UI.
        4. Save the new file pathname.

        Error handling:
        - Tf target already exists as a file, the conversion is cancelled,
          an error message is sent to the UI.
        - If the conversion fails, newFile is set to None.
        """
        msg = _('Create a novelibre project file from {0}\nNew project: "{1}"')
        self.ui.set_info(
            msg.format(
                source.DESCRIPTION,
                norm_path(target.filePath)
            )
        )
        if os.path.isfile(target.filePath):
            self.ui.set_status(
                (
                    f'!{_("File already exists")}: '
                    f'"{norm_path(target.filePath)}".'
                )
        )
        else:
            statusMsg = ''
            try:
                self._check(source, target)
                source.novel = Novel(
                    tree=NvTree(),
                    noScnField1=self.NO_SCN_FIELD1_DEFAULT,
                    noScnField2=self.NO_SCN_FIELD2_DEFAULT,
                    noScnField3=self.NO_SCN_FIELD3_DEFAULT,
                    otherScnField1=self.OTHER_SCN_FIELD1_DEFAULT,
                    otherScnField2=self.OTHER_SCN_FIELD2_DEFAULT,
                    otherScnField3=self.OTHER_SCN_FIELD3_DEFAULT,
                    chrExtraField1=self.CHR_EXTRA_FIELD_1_DEFAULT,
                    chrExtraField2=self.CHR_EXTRA_FIELD_2_DEFAULT,
                )
                source.novel.check_locale()
                source.read()
                target.novel = source.novel
                target.write()
            except Error as ex:
                statusMsg = f'!{str(ex)}'
                self.newFile = None
            else:
                statusMsg = (
                    f'{_("File written")}: '
                    f'"{norm_path(target.filePath)}".'
                )
                self.newFile = target.filePath
            finally:
                self.ui.set_status(statusMsg)

    def _export_from_novx(self, source, target):
        """Convert from novelibre project to other file format.

        Positional arguments:
            source -- NovxFile subclass instance.
            target -- Any Novel subclass instance.

        Operation:
        1. Send specific information about the conversion to the UI.
        2. Convert source into target.
        3. Pass the status message to the UI.
        4. Save the new file pathname.

        Error handling:
        - If the conversion fails, newFile is set to None.
        """
        self.ui.set_info(
            _('Input: {0} "{1}"\nOutput: {2} "{3}"').format(
                source.DESCRIPTION,
                norm_path(source.filePath),
                target.DESCRIPTION,
                norm_path(target.filePath)
            )
        )
        statusMsg = ''
        try:
            self._check(source, target)
            source.novel = Novel(
                tree=NvTree(),
                noScnField1=self.NO_SCN_FIELD1_DEFAULT,
                noScnField2=self.NO_SCN_FIELD2_DEFAULT,
                noScnField3=self.NO_SCN_FIELD3_DEFAULT,
                otherScnField1=self.OTHER_SCN_FIELD1_DEFAULT,
                otherScnField2=self.OTHER_SCN_FIELD2_DEFAULT,
                otherScnField3=self.OTHER_SCN_FIELD3_DEFAULT,
                chrExtraField1=self.CHR_EXTRA_FIELD_1_DEFAULT,
                chrExtraField2=self.CHR_EXTRA_FIELD_2_DEFAULT,
            )
            source.read()
            target.novel = source.novel
            target.write()
        except Error as ex:
            statusMsg = f'!{str(ex)}'
            self.newFile = None
        else:
            statusMsg = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
        finally:
            self.ui.set_status(statusMsg)

    def _import_to_novx(self, source, target):
        """Convert from any file format to novelibre project.

        Positional arguments:
            source -- Any Novel subclass instance.
            target -- NovxFile subclass instance.

        Operation:
        1. Send specific information about the conversion to the UI.
        2. Convert source into target.
        3. Pass the status message to the UI.
        4. Delete the temporay file, if exists.
        5. Save the new file pathname.
        6. If sections are split during conversion, 
           discard the source document.

        Error handling:
        - If the conversion fails, newFile is set to None.
        """
        self.ui.set_info(
            _('Input: {0} "{1}"\nOutput: {2} "{3}"').format(
                source.DESCRIPTION,
                norm_path(source.filePath),
                target.DESCRIPTION,
                norm_path(target.filePath)
            )
        )
        self.newFile = None
        statusMsg = ''
        try:
            self._check(source, target)
            target.novel = Novel(
                tree=NvTree(),
                noScnField1=self.NO_SCN_FIELD1_DEFAULT,
                noScnField2=self.NO_SCN_FIELD2_DEFAULT,
                noScnField3=self.NO_SCN_FIELD3_DEFAULT,
                otherScnField1=self.OTHER_SCN_FIELD1_DEFAULT,
                otherScnField2=self.OTHER_SCN_FIELD2_DEFAULT,
                otherScnField3=self.OTHER_SCN_FIELD3_DEFAULT,
                chrExtraField1=self.CHR_EXTRA_FIELD_1_DEFAULT,
                chrExtraField2=self.CHR_EXTRA_FIELD_2_DEFAULT,
            )
            target.read()
            source.novel = target.novel
            source.read()
            target.novel = source.novel
            target.write()
        except Exception as ex:
            statusMsg = f'!{str(ex)}'
        else:
            statusMsg = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
            if source.sectionsSplit:
                os.replace(source.filePath, f'{source.filePath}.bak')
                statusMsg = f'{statusMsg} - {_("Source document deleted")}.'
        finally:
            self.ui.set_status(f'{statusMsg}')


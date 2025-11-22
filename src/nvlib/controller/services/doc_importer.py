"""Provide a converter class for novelibre universal import.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvlib.controller.services.service_base import ServiceBase
from nvlib.model.converter.import_source_factory import ImportSourceFactory
from nvlib.model.converter.import_target_factory import ImportTargetFactory
from nvlib.model.converter.new_project_factory import NewProjectFactory
from nvlib.model.converter.novx_conversion import NovxConversion
from nvlib.model.novx.novx_file import NovxFile
from nvlib.novx_globals import Error
from nvlib.novx_globals import norm_path
from nvlib.nv_locale import _


class DocImporter(ServiceBase, NovxConversion):
    """A converter for universal import.

    Support novelibre projects and most of the File subclasses 
    that are written with OpenOffice/LibreOffice Writer or Calc.
    """

    def __init__(self, model, view, controller):
        """Set up the Factory strategies."""
        super().__init__(model, view, controller)
        self.importSourceFactory = ImportSourceFactory(
            self.IMPORT_SOURCE_CLASSES
        )
        self.newProjectFactory = NewProjectFactory(
            self.CREATE_SOURCE_CLASSES
        )
        self.importTargetFactory = ImportTargetFactory(
            [NovxFile]
        )
        self.newFile = None
        self.prefs = self._ctrl.get_preferences()

    def import_document(self, sourcePath, parent=None):
        try:
            message = self._run(sourcePath, parent=parent)
        except UserWarning as ex:
            self._ui.set_status(f'#{str(ex)}')
            return

        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
            return

        if self.newFile:
            self._ctrl.open_project(filePath=self.newFile)
            if (
                os.path.isfile(sourcePath)
                and self.prefs['import_mode'] == '1'
            ):
                os.replace(sourcePath, f'{sourcePath}.bak')
                message = f'{message} - {_("Source document deleted")}.'
            self._ui.set_status(message)

    def _run(self, sourcePath, **kwargs):
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
            source, __ = self.importSourceFactory.new_file_objects(
                sourcePath,
                **kwargs
            )
        except Error:

            #--- Import a document without section markers.
            source, target = self.newProjectFactory.new_file_objects(
                sourcePath,
                **kwargs
            )
            if os.path.isfile(target.filePath):
                # do not overwrite an existing novelibre project
                # with a non-tagged document
                raise Error(
                    (
                        f'{_("File already exists")}: '
                        f'"{norm_path(target.filePath)}".'
                    )
                )

            self._check_source_file(source)
            source.novel = self._mdl.nvService.new_novel()
            source.read()
            target.novel = source.novel
            target.write()
            self.newFile = target.filePath
            return f'{_("File written")}: "{norm_path(target.filePath)}".'

        else:

            #--- Import a document with section markers.
            kwargs['suffix'] = source.SUFFIX
            __, target = self.importTargetFactory.new_file_objects(
                sourcePath,
                **kwargs
            )
            self.newFile = None
            self._check_source_file(source)
            target.novel = self._mdl.nvService.new_novel()
            target.read()
            source.novel = target.novel
            source.read()
            if source.sectionsSplit and source.is_locked():
                raise Error(f'{_("Please close the document first")}.')

            if os.path.isfile(target.filePath):
                if not self._ui.ask_yes_no(
                    message=_('Update the project?'),
                    detail=f"{_('Source document')}: {source.DESCRIPTION}",
                    parent=kwargs.get('parent', None)
                ):
                    raise UserWarning(f'{_("Action canceled by user")}.')

            target.novel = source.novel
            target.write()
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
            if source.sectionsSplit:
                os.replace(source.filePath, f'{source.filePath}.bak')
                message = f'{message} - {_("Source document deleted")}.'
            return message

    def _check_source_file(self, source):
        # Error handling.
        if source.filePath is None:
            # the source is not correctly initialized
            raise Error(f'{_("File type is not supported")}.')

        if not os.path.isfile(source.filePath):
            # the source document does not exist
            raise Error(
                (
                    f'{_("File not found")}: '
                    f'"{norm_path(source.filePath)}".'
                )
            )

        if source.is_locked():
            # the document might be open in the Office application
            if self.prefs['import_mode'] != '2':
                raise Error(f'{_("Please close the document first")}.')


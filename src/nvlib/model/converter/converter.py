"""Provide a base class for Novel file conversion with user interface.

All converters with a user interface inherit from this class. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys

from mvclib.view.ui import Ui
from nvlib.model.data.novel import Novel
from nvlib.model.data.nv_tree import NvTree
from nvlib.model.file.doc_open import open_document
from nvlib.novx_globals import Error
from nvlib.novx_globals import Notification
from nvlib.novx_globals import _
from nvlib.novx_globals import norm_path


class Converter:
    """Base class for Novel file conversion with user interface.

    Instance variables:
        ui -- Ui (can be overridden e.g. by subclasses).
        newFile: str -- path to the target file in case of success.   
    """

    def __init__(self):
        """Define instance variables."""
        self.ui = Ui('')
        # Per default, 'silent mode' is active.
        self.newFile = None
        # Also indicates successful conversion.

    def export_from_novx(self, source, target):
        """Convert from novelibre project to other file format.

        Positional arguments:
            source -- NovxFile subclass instance.
            target -- Any Novel subclass instance.

        Operation:
        1. Send specific information about the conversion to the UI.
        2. Convert source into target.
        3. Pass the message to the UI.
        4. Save the new file pathname.

        Error handling:
        - If the conversion fails, newFile is set to None.
        """
        self.ui.set_info(
            _('Input: {0} "{1}"\nOutput: {2} "{3}"').format(source.DESCRIPTION, norm_path(source.filePath), target.DESCRIPTION, norm_path(target.filePath)))
        message = ''
        try:
            self.check(source, target)
            source.novel = Novel(tree=NvTree())
            source.read()
            target.novel = source.novel
            target.write()
        except Error as ex:
            message = f'!{str(ex)}'
            self.newFile = None
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
        finally:
            self.ui.set_status(message)

    def create_novx(self, source, target):
        """Create target from source.

        Positional arguments:
            source -- Any Novel subclass instance.
            target -- NovxFile subclass instance.

        Operation:
        1. Send specific information about the conversion to the UI.
        2. Convert source into target.
        3. Pass the message to the UI.
        4. Save the new file pathname.

        Error handling:
        - Tf target already exists as a file, the conversion is cancelled,
          an error message is sent to the UI.
        - If the conversion fails, newFile is set to None.
        """
        self.ui.set_info(
            _('Create a novelibre project file from {0}\nNew project: "{1}"').format(source.DESCRIPTION, norm_path(target.filePath)))
        if os.path.isfile(target.filePath):
            self.ui.set_status(f'!{_("File already exists")}: "{norm_path(target.filePath)}".')
        else:
            message = ''
            try:
                self.check(source, target)
                source.novel = Novel(tree=NvTree())
                source.novel.check_locale()
                source.read()
                target.novel = source.novel
                target.write()
            except Error as ex:
                message = f'!{str(ex)}'
                self.newFile = None
            else:
                message = f'{_("File written")}: "{norm_path(target.filePath)}".'
                self.newFile = target.filePath
            finally:
                self.ui.set_status(message)

    def import_to_novx(self, source, target):
        """Convert from any file format to novelibre project.

        Positional arguments:
            source -- Any Novel subclass instance.
            target -- NovxFile subclass instance.

        Operation:
        1. Send specific information about the conversion to the UI.
        2. Convert source into target.
        3. Pass the message to the UI.
        4. Delete the temporay file, if exists.
        5. Save the new file pathname.
        6. If sections are split during conversion, discard the source document.

        Error handling:
        - If the conversion fails, newFile is set to None.
        """
        self.ui.set_info(
            _('Input: {0} "{1}"\nOutput: {2} "{3}"').format(source.DESCRIPTION, norm_path(source.filePath), target.DESCRIPTION, norm_path(target.filePath)))
        self.newFile = None
        message = ''
        try:
            self.check(source, target)
            target.novel = Novel(tree=NvTree())
            target.read()
            source.novel = target.novel
            source.read()
            target.novel = source.novel
            target.write()
        except Error as ex:
            message = f'!{str(ex)}'
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
            if source.sectionsSplit:
                os.replace(source.filePath, f'{source.filePath}.bak')
                message = f'{message} - {_("Source document deleted")}.'
        finally:
            self.ui.set_status(f'{message}')

    def _confirm_overwrite(self, filePath):
        """Return boolean permission to overwrite the target file.
        
        Positional arguments:
            fileName -- path to the target file.
        
        Overrides the superclass method.
        """
        return self.ui.ask_yes_no(_('Overwrite existing file "{}"?').format(norm_path(filePath)))

    def _open_newFile(self):
        """Open the converted file for editing and exit the converter script."""
        open_document(self.newFile)
        sys.exit(0)

    def check(self, source, target):
        """Error handling:
        
        - Check if source and target are correctly initialized.
        - Ask for permission to overwrite target.
        - Check whether a source or target document is locked by tis application.
        - Raise the "Error" exception in case of error. 
        """
        if source.filePath is None:
            raise Error(f'{_("File type is not supported")}.')

        if not os.path.isfile(source.filePath):
            raise Error(f'{_("File not found")}: "{norm_path(source.filePath)}".')

        if source.is_locked():
            raise Error(f'{_("Please close the document first")}".')

        if target.is_locked():
            raise Error(f'{_("Please close the document first")}.')

        if target.filePath is None:
            raise Error(f'{_("File type is not supported")}.')

        if os.path.isfile(target.filePath) and not self._confirm_overwrite(target.filePath):
            raise Notification(f'{_("Action canceled by user")}.')


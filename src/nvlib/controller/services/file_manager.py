"""Provide a service class for novelibre file and directory handling.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from shutil import copy2
from tkinter import filedialog
import zipfile

from nvlib.controller.services.service_base import ServiceBase
from nvlib.model.exporter.nv_doc_exporter import NvDocExporter
from nvlib.model.exporter.nv_html_reporter import NvHtmlReporter
from nvlib.model.file.doc_open import open_document
from nvlib.model.html.html_report import HtmlReport
from nvlib.model.nv_work_file import NvWorkFile
from nvlib.model.odf.check_odf import odf_is_locked
from nvlib.model.odt.odt_writer import OdtWriter
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import Error
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.novx_globals import Notification
from nvlib.novx_globals import norm_path
from nvlib.nv_globals import HOME_DIR
from nvlib.nv_globals import INSTALL_DIR
from nvlib.nv_globals import USER_STYLES_DIR
from nvlib.nv_globals import USER_STYLES_XML
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class FileManager(ServiceBase):

    def __init__(self, model, view, controller):
        super().__init__(model, view, controller)
        self.exporter = NvDocExporter(self._ui)
        self.reporter = NvHtmlReporter()
        self.prefs = self._ctrl.get_preferences()

    def create_project(self):
        """Create a novelibre project instance.
        
        Return True on success, otherwise return None.
        """
        self._ui.restore_status()
        if self._mdl.prjFile is not None:
            if self._ctrl.on_close() is None:
                # user aborts
                return

        self._mdl.create_project(self._ui.tv.tree)
        self._ctrl.refresh_tree()
        self._ui.show_path(_('Unnamed'))
        # setting the path bar
        self._ctrl.enable_menu()
        self._ctrl.update_status()
        # setting the status bar
        self._ui.tv.update_tree()
        # making the root element titles visible
        self._ui.tv.refresh()
        # enabling selecting
        self._ui.tv.go_to_node(CH_ROOT)
        self.save_project()
        return True

    def copy_css(self):
        """Copy the provided css style sheet into the project directory."""
        self._ui.restore_status()
        try:
            projectDir = os.path.dirname(self._mdl.prjFile.filePath)
            copy2(f'{INSTALL_DIR}/css/novx.css', projectDir)
            message = _('Style sheet copied into the project folder.')
        except Exception as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(message)

    def copy_to_backup(self, filePath):
        """Copy the file specified by filePath to the backup directory.
        
        The backup file name gets a suffix in order not to be 
        worked on by accident.
        If no valid backup directory is specified, do nothing.
        If the backup fails, show a notification on the status bar.
        """
        if not self.prefs['enable_backup']:
            return

        backupDir = self.prefs['backup_dir']
        if not backupDir:
            self._ui.set_status(
                (
                    f'#{_("Backup directory not set")}. '
                    f'{_("Please check the setting")}.'
                )
            )
            return

        if not os.path.isdir(backupDir):
            self._ui.set_status(
                (
                    f'#{_("Backup directory not found")}: '
                    f'"{norm_path(backupDir)}". '
                    f'{_("Please check the setting")}.'
                )
            )
            return

        try:
            basename = os.path.basename(filePath)
            copy2(
                filePath,
                f'{backupDir}/{basename}{self.prefs["backup_suffix"]}'
            )
        except Exception as ex:
            self._ui.set_status(f"#{_('Backup failed')}: {str(ex)}")

    def discard_manuscript(self):
        """Rename the current editable manuscript. 
        
        This might be useful to avoid confusion in certain cases.
        """
        self._ui.restore_status()
        fileName, __ = os.path.splitext(self._mdl.prjFile.filePath)
        manuscriptPath = f'{fileName}{MANUSCRIPT_SUFFIX}.odt'
        if not os.path.isfile(manuscriptPath):
            self._ui.set_status(f"#{_('Manuscript not found')}.")
            return

        if odf_is_locked(manuscriptPath):
            self._ui.set_status(
                f"!{_('Please close the manuscript first')}."
            )
        elif self._ui.ask_yes_no(
            message=_('Discard manuscript?'),
            detail=self._mdl.novel.title
            ):
            os.replace(
                manuscriptPath,
                f'{fileName}{MANUSCRIPT_SUFFIX}.odt.bak'
            )
            self._ui.set_status(f"{_('Manuscript discarded')}.")

    def export_document(self, suffix, **kwargs):
        """Export a document.
        
        Required arguments:
            suffix -- str: Document type suffix.
        """
        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        if self._mdl.prjFile.filePath is None:
            if not self.save_project():
                return

        if self._mdl.isModified:
            if self._ui.ask_yes_no(
                message=_('Save changes?')
            ):
                self.save_project()
            else:
                # Do not export a document from an unsaved project.
                self._ui.set_status(f'#{_("Action canceled by user")}.')
                return

        try:
            self._ui.set_status(
                self.exporter.run(
                    self._mdl.prjFile,
                    suffix,
                    **kwargs
                )
            )
        except Notification as ex:
            self._ui.set_status(f'#{str(ex)}')
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
        else:
            if kwargs.get('lock', True) and self.prefs['lock_on_export']:
                self._ctrl.lock()

    def import_odf(
            self, sourcePath=None,
            defaultExtension='.odt',
            parent=None,
        ):
        """Update or create the project from an ODF document.
        
        Optional arguments:
            sourcePath: str -- Path specifying the source document. 
                               If None, a file picker is used.
            defaultExtension: str -- Extension to be preset in the file picker.
        """
        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        if sourcePath is None:
            if self.prefs['last_open']:
                startDir = os.path.dirname(self.prefs['last_open'])
            else:
                startDir = '.'
            sourcePath = filedialog.askopenfilename(
                filetypes=[
                    (_('ODF Text document'), '.odt'),
                    (_('ODF Spreadsheet document'), '.ods'),
                ],
                defaultextension=defaultExtension,
                initialdir=startDir,
            )
            if not sourcePath:
                return

        if self._mdl.isModified:
            doSave = self._ui.ask_yes_no_cancel(_('Save changes?'))
            if doSave is None:
                return

            elif doSave:
                if not self.save_project():
                    self._ui.show_error(
                        message=_('Cannot save the project')
                    )
                    return

        self._ctrl.docImporter.import_document(sourcePath, parent=parent)
        if self._mdl.prjFile:
            self.copy_to_backup(self._mdl.prjFile.filePath)

    def open_installationFolder(self):
        """Open the installation folder with the OS file manager."""
        self._ui.restore_status()
        try:
            open_document(INSTALL_DIR)
        except Exception as ex:
            self._ui.set_status(f'!{str(ex)}')

    def open_project(self, filePath='', doNotSave=False):
        """Create a novelibre project instance and read the file.
        
        Optional arguments:
            filePath: str -- The new project's file name.
            doNotSave: Boolean -- If True, close the current project 
                                  without saving.
        
        If no file name is given, a file picker is opened.
        Display project title, description and status.
        Return True on success, otherwise return False.
        """
        self._ui.restore_status()
        filePath = self.select_project(filePath)
        if not filePath:
            return False

        if self._mdl.prjFile is not None:
            if self._ctrl.on_close(doNotSave=doNotSave) is None:
                # user aborts
                return False

        if prefs['warn_before_reopening']:
            pidfile = f'{filePath}.pid'
            if os.path.isfile(pidfile):
                message = (
                    f"{_('This project may be already open in novelibre')}:"
                    '\n'
                    f'"{norm_path(filePath)}"'
                )
                if not self._ui.ask_ok_cancel(
                    message=message,
                    detail=_('Open anyway?'),
                ):
                    return False

            with open(pidfile, 'w') as f:
                f.write(str(os.getpid()))

        self.prefs['last_open'] = filePath
        try:
            self._mdl.open_project(filePath)
        except Error as ex:
            self._ctrl.on_close(doNotSave=doNotSave)
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ui.show_path(f'{norm_path(self._mdl.prjFile.filePath)}')
        self._ctrl.enable_menu()
        self._ctrl.refresh_tree()
        self._ui.show_path(_('{0} (last saved on {1})').format(
            norm_path(self._mdl.prjFile.filePath),
            self._mdl.prjFile.fileDate)
        )
        self._ctrl.update_status()
        self._ui.contentsView.view_text()
        if self._mdl.prjFile.has_lockfile():
            self._ctrl.lock()
        self._ui.tv.show_branch(CH_ROOT)
        self._ctrl.on_open()
        return True

    def open_project_folder(self):
        """Open the project folder with the OS file manager."""
        self._ui.restore_status()
        if not self._mdl:
            return 'break'

        if not self._mdl.prjFile:
            return 'break'

        if self._mdl.prjFile.filePath is None:
            if not self._ui.ask_ok_cancel(
                message=_('Please save now'),
                detail=_('Project path unknown'),
            ):
                return 'break'

            if not self.save_project():
                return 'break'

        try:
            open_document(os.path.dirname(self._mdl.prjFile.filePath))
        except Exception as ex:
            self._ui.set_status(f'!{str(ex)}')
        return 'break'

    def reload_project(self):
        """Discard changes and reload the project."""
        self._ui.restore_status()
        if self._mdl.prjFile is None:
            return

        if self._mdl.isModified and not self._ui.ask_yes_no(
            message=_('Discard changes and reload the project?')
        ):
            return

        if (
            self._mdl.prjFile.has_changed_on_disk()
            and not self._ui.ask_yes_no(
                message=_('File has changed on disk. Reload anyway?')
            )
        ):
            return

        # this is to avoid saving when closing the project
        if self.open_project(
            filePath=self._mdl.prjFile.filePath,
            doNotSave=True,
        ):
            # includes closing
            self._ui.set_status(_('Project successfully restored from disk.'))
        return

    def restore_backup(self):
        """Discard changes and restore the latest backup file."""
        self._ui.restore_status()
        if self._mdl.prjFile is None:
            return

        latestBackup = f'{self._mdl.prjFile.filePath}.bak'
        if not os.path.isfile(latestBackup):
            self._ui.set_status(f'!{_("No backup available")}')
            return

        if self._mdl.isModified:
            if not self._ui.ask_yes_no(
                message=_('Discard changes and load the ".bak" file?')
            ):
                return

        elif not self._ui.ask_yes_no(
            message=_('Overwrite the last saved project file with the ".bak" file?')
        ):
            return

        try:
            os.replace(latestBackup, self._mdl.prjFile.filePath)
        except Exception as ex:
            self._ui.set_status(str(ex))
        else:
            if self.open_project(
                filePath=self._mdl.prjFile.filePath,
                doNotSave=True,
            ):
                # Includes closing
                self._ui.set_status(_('Latest backup successfully restored.'))
        return

    def restore_default_styles(self, *args):
        """Remove the user's styles.xml file from the installation."""
        self._ui.restore_status()
        try:
            os.remove(USER_STYLES_XML)
        except:
            self._ui.set_status(f'#{_("Default styles are already set")}.')
        else:
            self._ui.set_status(f'{_("Default styles are restored")}.')

    def save_as(self):
        """Rename the project file and save it to disk.
        
        Return True on success, otherwise return False.
        """
        self._ui.restore_status()
        if self._mdl.prjFile is None:
            return False

        if self.prefs['last_open']:
            initDir = os.path.dirname(self.prefs['last_open'])
        else:
            initDir = HOME_DIR
        fileTypes = [(NvWorkFile.DESCRIPTION, NvWorkFile.EXTENSION)]
        fileName = filedialog.asksaveasfilename(
            filetypes=fileTypes,
            defaultextension=fileTypes[0][1],
            initialdir=initDir,
        )
        if not fileName:
            return False

        self._ui.propertiesView.apply_changes()
        try:
            self._mdl.save_project(fileName)
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
            return False

        else:
            self._ctrl.unlock()
            self._ui.show_path(
                (
                    f'{norm_path(self._mdl.prjFile.filePath)} '
                    f'({_("last saved on")} {self._mdl.prjFile.fileDate})'
                )
            )
            self._ui.restore_status()
            self.prefs['last_open'] = self._mdl.prjFile.filePath
            self.copy_to_backup(self._mdl.prjFile.filePath)
            self._ctrl.on_open()
            return True

    def save_project(self):
        """Save the novelibre project to disk.
        
        Return True on success, otherwise return False.
        """
        self._ui.restore_status()
        if self._mdl.prjFile is None:
            return False

        if self._ctrl.check_lock():
            self._ui.set_status(
                f'!{_("Cannot save: The project is locked")}.'
            )
            return False

        if self._mdl.prjFile.filePath is None:
            return self.save_as()

        if (
            self._mdl.prjFile.has_changed_on_disk()
            and not self._ui.ask_yes_no(
                message=_('File has changed on disk. Save anyway?')
            )
        ):
            return False

        self._ui.propertiesView.apply_changes()
        try:
            self._mdl.save_project()
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ui.show_path(
            (
                f'{norm_path(self._mdl.prjFile.filePath)} '
                f'({_("last saved on")} {self._mdl.prjFile.fileDate})'
            )
        )
        self._ui.restore_status()
        self.prefs['last_open'] = self._mdl.prjFile.filePath
        self.copy_to_backup(self._mdl.prjFile.filePath)
        self._ctrl.on_open()
        return True

    def select_project(self, fileName):
        """Return a project file path.

        Positional arguments:
            fileName: str -- project file path.
            
        Priority:
        1. use file name argument
        2. open file select dialog

        On error, return an empty string.
        """
        self._ui.restore_status()
        initDir = os.path.dirname(self.prefs.get('last_open', ''))
        if not initDir:
            initDir = HOME_DIR
        if not fileName or not os.path.isfile(fileName):
            fileTypes = [(NvWorkFile.DESCRIPTION, NvWorkFile.EXTENSION)]
            fileName = filedialog.askopenfilename(
                filetypes=fileTypes,
                defaultextension=fileTypes[0][1],
                initialdir=initDir,
            )
        if not fileName:
            return ''

        return fileName

    def set_user_styles(self, *args):
        """Set user styles for ODT document export.
        
        1. Extract styles.xml from an user-selected OTT or ODT document.
        2. Remove novelibre-specific styles, if any.
        3. Add styles.xml to the installation.
        """
        self._ui.restore_status()
        os.makedirs(USER_STYLES_DIR, exist_ok=True)
        fileTypes = [
            (f'{_("ODF Text Document Template")} (*.ott)', '.ott'),
            (f'{_("ODF Text Document")} (*.odt)', '.odt') ,
        ]
        docTemplate = filedialog.askopenfilename(
            filetypes=fileTypes,
            defaultextension=fileTypes[0][1],
            )
        if not docTemplate:
            return

        templateName = os.path.basename(docTemplate)
        try:
            with zipfile.ZipFile(docTemplate) as myzip:
                with myzip.open('styles.xml') as myfile:
                    stylesXmlStr = myfile.read().decode('utf-8')
            stylesXmlStr = OdtWriter.remove_novelibre_styles(stylesXmlStr)
            with open(USER_STYLES_XML, 'w', encoding='utf-8') as f:
                f.write(stylesXmlStr)
        except:
            self._ui.set_status(
                (
                    f'!{_("Invalid document template")}: '
                    f'"{templateName}".'
                )
            )
        else:
            self._ui.set_status(
                (
                    f'{_("Document template is set")}: '
                    f'"{templateName}".'
                )
            )

    def show_report(self, suffix):
        """Create HTML report for the web browser.
        
        Positional arguments:
            suffix: str -- the HTML file name suffix, 
                           indicating the report type.        
        """
        self._ui.restore_status()
        if self._mdl.prjFile.filePath is None:
            return False

        self._ui.propertiesView.apply_changes()
        HtmlReport.localizeDate = self.prefs['localize_date']
        try:
            self.reporter.run(
                self._mdl.prjFile,
                suffix,
                tempdir=self._ctrl.tempDir,
            )
        except Notification as ex:
            self._ui.set_status(f'#{str(ex)}')
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')


"""Provide a service class for novelibre file and directory handling.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
import sys
from shutil import copy2
from tkinter import filedialog
import zipapp

from mvclib.controller.service_base import ServiceBase
from nvlib.model.exporter.nv_doc_exporter import NvDocExporter
from nvlib.model.exporter.nv_html_reporter import NvHtmlReporter
from nvlib.model.html.html_report import HtmlReport
from nvlib.model.nv_work_file import NvWorkFile
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import Error
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.novx_globals import Notification
from nvlib.novx_globals import norm_path
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _


class FileManager(ServiceBase):

    def __init__(self, model, view, controller):
        super().__init__(model, view, controller)
        self.exporter = NvDocExporter(self._ui)
        self.reporter = NvHtmlReporter()

    def create_project(self):
        """Create a novelibre project instance."""
        if self._mdl.prjFile is not None:
            self._ctrl.on_close()
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

    def copy_to_backup(self, filePath):
        """Create a self-extracting backup file."""
        prefs = self._ctrl.get_preferences()
        backupDir = prefs['backup_dir']
        if os.path.isdir(backupDir):
            try:
                __, tail = os.path.split(filePath)
                copy2(filePath, f'{backupDir}/{tail}.copy')
            except Exception as ex:
                self._ui.set_status(f"!{_('Backup error')}: {str(ex)}")

    def discard_manuscript(self):
        """Rename the current editable manuscript. 
        
        This might be useful to avoid confusion in certain cases.
        """
        fileName, __ = os.path.splitext(self._mdl.prjFile.filePath)
        manuscriptPath = f'{fileName}{MANUSCRIPT_SUFFIX}.odt'
        if os.path.isfile(manuscriptPath):
            prjPath, manuscriptName = os.path.split(manuscriptPath)
            if os.path.isfile(f'{prjPath}/.~lock.{manuscriptName}#'):
                self._ui.set_status(f"!{_('Please close the manuscript first')}.")
            elif self._ui.ask_yes_no(f"{_('Discard manuscript')}?", self._mdl.novel.title):
                os.replace(manuscriptPath, f'{fileName}{MANUSCRIPT_SUFFIX}.odt.bak')
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
            if self._ui.ask_yes_no(_('Save changes?')):
                self.save_project()
            else:
                # Do not export a document from an unsaved project.
                self._ui.set_status(f'#{_("Action canceled by user")}.')
                return

        try:
            self._ui.set_status(self.exporter.run(self._mdl.prjFile, suffix, **kwargs))
        except Notification as ex:
            self._ui.set_status(f'#{str(ex)}')
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
        else:
            if kwargs.get('lock', True) and prefs['lock_on_export']:
                self._ctrl.lock()

    def import_odf(self, sourcePath=None, defaultExtension='.odt'):
        """Update or create the project from an ODF document.
        
        Optional arguments:
            sourcePath: str -- Path specifying the source document. If None, a file picker is used.
            defaultExtension: str -- Extension to be preset in the file picker.
        """
        if sourcePath is None:
            if prefs['last_open']:
                startDir, __ = os.path.split(prefs['last_open'])
            else:
                startDir = '.'
            sourcePath = filedialog.askopenfilename(
                filetypes=[(_('ODF Text document'), '.odt'), (_('ODF Spreadsheet document'), '.ods')],
                defaultextension=defaultExtension,
                initialdir=startDir,
                )
            if not sourcePath:
                return

        if self._mdl.prjFile is not None:
            self._ctrl.update_status()
            self._ctrl.refresh_tree()
            self._ctrl.unlock()
            if self._mdl.isModified:
                if self._ui.ask_yes_no(_('Save changes?')):
                    self.save_project()
        self._ctrl.docImporter.import_document(sourcePath)

    def open_installationFolder(self):
        """Open the installation folder with the OS file manager."""
        installDir = os.path.dirname(sys.argv[0])
        try:
            os.startfile(norm_path(installDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(installDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(installDir))
                    # Mac
                except:
                    pass

    def open_project(self, filePath='', doNotSave=False):
        """Create a novelibre project instance and read the file.
        
        Optional arguments:
            filePath: str -- The new project's file name.
            doNotSave: Boolean -- If True, close the current project without saving.
        
        If no file name is given, a file picker is opened.
        Display project title, description and status.
        Return True on success, otherwise return False.
        """
        self._ui.restore_status()
        filePath = self.select_project(filePath)
        if not filePath:
            return False

        prefs['last_open'] = filePath

        if self._mdl.prjFile is not None:
            self._ctrl.on_close(doNotSave=doNotSave)
        try:
            self._mdl.open_project(filePath)
        except Error as ex:
            self._ctrl.on_close(doNotSave=doNotSave)
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ui.show_path(f'{norm_path(self._mdl.prjFile.filePath)}')
        self._ctrl.enable_menu()
        self._ctrl.refresh_tree()
        self._ui.show_path(_('{0} (last saved on {1})').format(norm_path(self._mdl.prjFile.filePath), self._mdl.prjFile.fileDate))
        self._ctrl.update_status()
        self._ui.contentsView.view_text()
        if self._mdl.prjFile.has_lockfile():
            self._ctrl.lock()
        self._ui.tv.show_branch(CH_ROOT)
        return True

    def open_project_folder(self):
        """Open the project folder with the OS file manager."""
        if not self._mdl:
            return 'break'

        if not self._mdl.prjFile:
            return 'break'

        if self._mdl.prjFile.filePath is None:
            if not self._ui.ask_ok_cancel(_('Please save now'), title=_('Project path unknown')):
                return 'break'

            if not self.save_project():
                return 'break'

        projectDir, __ = os.path.split(self._mdl.prjFile.filePath)
        try:
            os.startfile(norm_path(projectDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(projectDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(projectDir))
                    # Mac
                except:
                    pass

    def save_as(self):
        """Rename the project file and save it to disk.
        
        Return True on success, otherwise return False.
        """
        if self._mdl.prjFile is None:
            return False

        if prefs['last_open']:
            startDir, __ = os.path.split(prefs['last_open'])
        else:
            startDir = str(Path.home()).replace('\\', '/')
        fileTypes = [(NvWorkFile.DESCRIPTION, NvWorkFile.EXTENSION)]
        fileName = filedialog.asksaveasfilename(
            filetypes=fileTypes,
            defaultextension=fileTypes[0][1],
            initialdir=startDir,
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
            self._ui.show_path(f'{norm_path(self._mdl.prjFile.filePath)} ({_("last saved on")} {self._mdl.prjFile.fileDate})')
            self._ui.restore_status()
            prefs['last_open'] = self._mdl.prjFile.filePath
            self.copy_to_backup(self._mdl.prjFile.filePath)
            return True

    def save_project(self):
        """Save the novelibre project to disk.
        
        Return True on success, otherwise return False.
        """
        if self._mdl.prjFile is None:
            return False

        if self._ctrl.check_lock():
            self._ui.set_status(f'!{_("Cannot save: The project is locked")}.')
            return False

        if self._mdl.prjFile.filePath is None:
            return self.save_as()

        if self._mdl.prjFile.has_changed_on_disk() and not self._ui.ask_yes_no(_('File has changed on disk. Save anyway?')):
            return False

        self._ui.propertiesView.apply_changes()
        try:
            self._mdl.save_project()
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ui.show_path(f'{norm_path(self._mdl.prjFile.filePath)} ({_("last saved on")} {self._mdl.prjFile.fileDate})')
        self._ui.restore_status()
        prefs['last_open'] = self._mdl.prjFile.filePath
        self.copy_to_backup(self._mdl.prjFile.filePath)
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
        initDir = os.path.dirname(prefs.get('last_open', ''))
        if not initDir:
            initDir = str(Path.home()).replace('\\', '/')
        if not fileName or not os.path.isfile(fileName):
            fileTypes = [(NvWorkFile.DESCRIPTION, NvWorkFile.EXTENSION)]
            fileName = filedialog.askopenfilename(
                filetypes=fileTypes,
                defaultextension=fileTypes[0][1],
                initialdir=initDir
                )
        if not fileName:
            return ''

        return fileName

    def show_report(self, suffix):
        """Create HTML report for the web browser.
        
        Positional arguments:
            suffix: str -- the HTML file name suffix, indicating the report type.        
        """
        if self._mdl.prjFile.filePath is None:
            return False

        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        HtmlReport.localizeDate = prefs['localize_date']
        try:
            self.reporter.run(self._mdl.prjFile, suffix, tempdir=self._ctrl.tempDir)
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')


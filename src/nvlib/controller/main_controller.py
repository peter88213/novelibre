"""Provide a main controller class for novelibre.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
from tkinter import filedialog

from mvclib.controller.controller_base import ControllerBase
from nvlib.controller.commands import Commands
from nvlib.controller.importer.nv_data_importer import NvDataImporter
from nvlib.controller.importer.nv_doc_importer import NvDocImporter
from nvlib.controller.link_processor import LinkProcessor
from nvlib.controller.plugin.plugin_collection import PluginCollection
from nvlib.gui.main_view import MainView
from nvlib.model.exporter.nv_doc_exporter import NvDocExporter
from nvlib.model.exporter.nv_html_reporter import NvHtmlReporter
from nvlib.model.nv_model import NvModel
from nvlib.model.nv_work_file import NvWorkFile
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import Error
from nvlib.novx_globals import Notification
from nvlib.novx_globals import _
from nvlib.nv_globals import prefs

PLUGIN_PATH = f'{sys.path[0]}/plugin'


class MainController(ControllerBase, Commands):
    """Controller for the novelibre application."""

    _MAX_NR_NEW_SECTIONS = 20
    # maximum number of sections to add in bulk
    _INI_NR_NEW_SECTIONS = 1
    # initial value when asking for the number of sections to add

    def __init__(self, title, tempDir):
        """Initialize the model, set up the application's user interface, and load plugins.
    
        Positional arguments:
            title: str -- Application title to be displayed at the window frame.
            tempDir: str -- Path of the temporary directory, used for e.g. packing zipfiles.          
        
        Extends the superclass constructor.
        """
        super().__init__(title)
        self.tempDir = tempDir

        #--- Create the model
        self._mdl = NvModel()
        self._mdl.add_observer(self)

        self.launchers = {}
        # launchers for opening linked non-standard filetypes.

        self.linkProcessor = LinkProcessor(self._mdl)
        # strategy for processing links

        self._fileTypes = [(NvWorkFile.DESCRIPTION, NvWorkFile.EXTENSION)]
        self.importFiletypes = [(_('ODF Text document'), '.odt'), (_('ODF Spreadsheet document'), '.ods')]

        #--- Build the GUI.
        self._ui = MainView(self._mdl, self, title)
        self.register_client(self._ui)

        # Link the model to the view.
        # Strictly speaking, this breaks the MVC pattern, since the
        # model depends on a data structure defined by the GUI framework.
        self._mdl.tree = self._ui.tv.tree

        #--- Load the plugins.
        self.plugins = PluginCollection(self._mdl, self._ui, self)
        # Dict-like Container for registered plugin objects.

        self.plugins.load_plugins(PLUGIN_PATH)
        self.register_client(self.plugins)
        self.disable_menu()

        self._ui.tv.reset_view()

    def check_lock(self):
        """If the project is locked, unlock it on demand.

        Return True, if the project remains locked, otherwise return False.
        """
        if self.isLocked:
            if self._ui.ask_yes_no(_('The project is locked.\nUnlock?'), title=_('Can not do')):
                self.unlock()
                return False
            else:
                return True
        else:
            return False

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

        exporter = NvDocExporter(self._ui)
        try:
            self._ui.set_status(exporter.run(self._mdl.prjFile, suffix, **kwargs))
        except Notification as ex:
            self._ui.set_status(f'#{str(ex)}')
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
        else:
            if kwargs.get('lock', True) and prefs['lock_on_export']:
                self.lock()

    def get_preferences(self):
        """Return the global preferences dictionary."""
        return prefs

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
                filetypes=self.importFiletypes,
                defaultextension=defaultExtension,
                initialdir=startDir,
                )
            if not sourcePath:
                return

        if self._mdl.prjFile is not None:
            self.update_status()
            self.refresh_tree()
            self.unlock()
            if self._mdl.isModified:
                if self._ui.ask_yes_no(_('Save changes?')):
                    self.save_project()
        importer = NvDocImporter(self._mdl, self._ui, self)
        importer.import_document(sourcePath)

    def import_elements(self, prefix):
        """Import elements from an XML data file.
        
        Positional arguments:
            prefix: str -- Prefix specifying the element type to be imported.
        """
        self._ui.restore_status()
        fileTypes = [(_('XML data file'), '.xml')]
        filePath = filedialog.askopenfilename(filetypes=fileTypes)
        if filePath:
            NvDataImporter(self._mdl, self._ui, self, filePath, prefix)

    def lock(self, event=None):
        """Lock the project.
        
        Return True on success, otherwise return False.
        Extends the superclass method.
        """
        if self._mdl.isModified and not self._internalLockFlag:
            if self._ui.ask_yes_no(_('Save and lock?')):
                self.save_project()
            else:
                return False

        if self._mdl.prjFile.filePath is not None:
            super().lock()
            self._mdl.prjFile.lock()
            # make it persistent
            return True
        else:
            return False

    def on_close(self, doNotSave=False):
        """Close the current project.
        
        - Save changes
        - clear all views
        - reset flags
        - trigger plugins.
        """
        self.update_status()
        self._ui.propertiesView.apply_changes()
        if self._mdl.isModified and not doNotSave:
            doSave = self._ui.ask_yes_no_cancel(_('Save changes?'))
            if doSave is None:
                return None

            elif doSave:
                if not self.save_project():
                    self._ui.show_error(_('Cannot save the project'), _('Critical Error'))
                    return False

        # Close the sub-controllers.
        super().on_close()

        # Close the model.
        self._mdl.close_project()

        # Unlock the controller and sub-controllers.
        self._internalLockFlag = False
        super().unlock()
        # calling the public unlock() method here would clear the lockfile

        self._ui.root.title(self._ui.title)
        self.update_status('')
        self._ui.show_path('')
        self.disable_menu()
        return True

    def on_quit(self, event=None):
        """Save changes and keyword arguments before exiting the program.
        
        Extends the superclass method.
        """
        try:
            if self._mdl.prjFile is not None:
                if not self.close_project():
                    return 'break'

            super().on_quit()
        except Exception as ex:
            self._ui.show_error(str(ex), title='ERROR: Unhandled exception on exit')
            self._ui.root.quit()
        return 'break'

    def refresh(self):
        """Callback function to report model element modifications."""
        self.update_status()

    def select_project(self, fileName):
        """Return a project file path.

        Positional arguments:
            fileName: str -- project file path.
            
        Optional arguments:
            fileTypes -- list of tuples for file selection (display text, extension).

        Priority:
        1. use file name argument
        2. open file select dialog

        On error, return an empty string.
        """
        initDir = os.path.dirname(prefs.get('last_open', ''))
        if not initDir:
            initDir = './'
        if not fileName or not os.path.isfile(fileName):
            fileName = filedialog.askopenfilename(
                filetypes=self._fileTypes,
                defaultextension=NvWorkFile.EXTENSION,
                initialdir=initDir
                )
        if not fileName:
            return ''

        return fileName

    def set_character_status(self, isMajor, elemIds=None):
        """Set character status to Major.
        
        Optional arguments:
            isMajor: bool -- If True, make the characters major. Otherwise, make them minor.
            elemIds: list of character IDs to process.
        """
        if self.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._ui.tv.open_children(CR_ROOT)
        self._mdl.set_character_status(isMajor, elemIds)

    def set_completion_status(self, newStatus, elemIds=None):
        """Set section completion status (Outline/Draft..).
        
        Positional arguments:
            newStatus: int -- New section status to be set.        
            elemIds: list of IDs to process.            
        """
        if self.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._ui.tv.open_children(elemIds[0])
        self._mdl.set_completion_status(newStatus, elemIds)

    def set_level(self, newLevel, elemIds=None):
        """Set chapter or stage level.
        
        Positional arguments:
            newLevel: int -- New level to be set.
            elemIds: list of IDs to process.
        """
        if self.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._mdl.set_level(newLevel, elemIds)

    def set_type(self, newType, elemIds=None):
        """Set section or chapter type Normal).
        
        Positional arguments:
            newType: int -- New type to be set.
            elemIds: list of IDs to process.
        """
        if self.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._ui.tv.open_children(elemIds[0])
        self._mdl.set_type(newType, elemIds)

    def show_report(self, suffix):
        """Create HTML report for the web browser.
        
        Positional arguments:
            suffix: str -- the HTML file name suffix, indicating the report type.        
        """
        if self._mdl.prjFile.filePath is None:
            return False

        self._ui.restore_status()
        self._ui.propertiesView.apply_changes()
        reporter = NvHtmlReporter()
        try:
            reporter.run(self._mdl.prjFile, suffix, tempdir=self.tempDir)
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')

    def unlock(self, event=None):
        """Unlock the project.
        
        If the project file was modified from the outside while it was 
        locked in the application, reload it after confirmation.
        Extends the superclass method.
        """
        super().unlock()
        self._mdl.prjFile.unlock()
        # make it persistent
        if self._mdl.prjFile.has_changed_on_disk():
            if self._ui.ask_yes_no(_('File has changed on disk. Reload?')):
                self.open_project(filePath=self._mdl.prjFile.filePath)
        return 'break'

    def update_status(self, statusText=None):
        """Display project statistics at the status bar.
        
        Optional arguments:
            statusText: str -- Message to be displayed instead of the statistics.
        """
        if self._mdl.novel is not None and not statusText:
            wordCount, sectionCount, chapterCount, partCount = self._mdl.get_counts()
            statusText = _('{0} parts, {1} chapters, {2} sections, {3} words').format(partCount, chapterCount, sectionCount, wordCount)
            self.wordCount = wordCount
        self._ui.update_status(statusText)

    def view_new_element(self, newNode):
        """View the element with ID newNode.
        
        - Open the properties window for the new element.
        - Show and select it in the tree view.
        - Prepare the current element's title entry for manual input.
        The order is mandatory for smooth operation.
        """
        if newNode:
            self._ui.tv.go_to_node(newNode)
            self._ui.propertiesView.show_properties(newNode)
            self._ui.propertiesView.focus_title()
        else:
            self._ui.set_status(f'!{_("Cannot create the element at this position")}.')


"""Provide a main controller class for novelibre.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys

from mvclib.controller.controller_base import ControllerBase
from nvlib.controller.commands import Commands
from nvlib.controller.plugin.plugin_collection import PluginCollection
from nvlib.controller.services.data_importer import DataImporter
from nvlib.controller.services.doc_importer import DocImporter
from nvlib.controller.services.element_manager import ElementManager
from nvlib.controller.services.file_manager import FileManager
from nvlib.controller.services.file_splitter import FileSplitter
from nvlib.controller.services.link_processor import LinkProcessor
from nvlib.gui.main_view import MainView
from nvlib.model.nv_model import NvModel
from nvlib.novx_globals import _
from nvlib.nv_globals import prefs

PLUGIN_PATH = f'{sys.path[0]}/plugin'


class MainController(ControllerBase, Commands):
    """Controller for the novelibre application."""

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

        #--- Build the GUI.
        self._ui = MainView(self._mdl, self, title)
        self.register_client(self._ui)

        # Link the model to the view.
        # Strictly speaking, this breaks the MVC pattern, since the
        # model depends on a data structure defined by the GUI framework.
        self._mdl.tree = self._ui.tv.tree

        #--- Initialize services.
        # Services are strategy classes used to implement the application's main features.
        # Basically, they can be exchanged by plugins.
        self.importFiletypes = [(_('ODF Text document'), '.odt'), (_('ODF Spreadsheet document'), '.ods')]

        self.launchers = {}
        # launchers for opening linked non-standard filetypes.
        # key: extension, value: path to application

        self.linkProcessor = LinkProcessor(self._mdl, self._ui, self)
        self.dataImporter = DataImporter(self._mdl, self._ui, self)
        self.docImporter = DocImporter(self._mdl, self._ui, self)
        self.fileSplitter = FileSplitter(self._mdl, self._ui, self)
        self.fileManager = FileManager(self._mdl, self._ui, self)
        self.elementManager = ElementManager(self._mdl, self._ui, self)

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

    def get_preferences(self):
        """Return the global preferences dictionary."""
        return prefs

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
                if not self.fileManager.save_project():
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
                if not self.on_close():
                    return 'break'

            super().on_quit()
        except Exception as ex:
            self._ui.show_error(str(ex), title='ERROR: Unhandled exception on exit')
            self._ui.root.quit()
        return 'break'

    def refresh(self):
        """Callback function to report model element modifications."""
        self.update_status()

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


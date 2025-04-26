"""Provide a main controller class for novelibre.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import sys

from nvlib.controller.commands import Commands
from nvlib.controller.plugin.plugin_collection import PluginCollection
from nvlib.controller.services.clipboard_manager import ClipboardManager
from nvlib.controller.services.data_importer import DataImporter
from nvlib.controller.services.doc_importer import DocImporter
from nvlib.controller.services.element_manager import ElementManager
from nvlib.controller.services.file_manager import FileManager
from nvlib.controller.services.file_splitter import FileSplitter
from nvlib.controller.services.link_processor import LinkProcessor
from nvlib.controller.sub_controller import SubController
from nvlib.gui.main_view import MainView
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.platform.platform_settings import MOUSE
from nvlib.gui.platform.platform_settings import PLATFORM
from nvlib.model.nv_model import NvModel
from nvlib.nv_globals import launchers
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _

PLUGIN_PATH = f'{sys.path[0]}/plugin'


class MainController(SubController, Commands):
    """Controller for the novelibre application."""

    def __init__(self, title, tempDir):
        """Initialize the model, set up the application's user interface, and load plugins.
    
        Positional arguments:
            title: str -- Application title to be displayed at the window frame.
            tempDir: str -- Path of the temporary directory, used for e.g. packing zipfiles.          
        
        Extends the superclass constructor.
        """
        super().__init__()
        self._internalLockFlag = False
        self._clients = []
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

        self.dataImporter = DataImporter(self._mdl, self._ui, self)
        self.docImporter = DocImporter(self._mdl, self._ui, self)
        self.fileSplitter = FileSplitter(self._mdl, self._ui, self)
        self.fileManager = FileManager(self._mdl, self._ui, self)
        self.elementManager = ElementManager(self._mdl, self._ui, self)
        self.linkProcessor = LinkProcessor(self._mdl, self._ui, self)
        self.clipboardManager = ClipboardManager(self._mdl, self._ui, self)

        #--- Load the plugins.
        self.plugins = PluginCollection(self._mdl, self._ui, self)
        # Dict-like Container for registered plugin objects.

        self.plugins.load_plugins(PLUGIN_PATH)
        self.register_client(self.plugins)

        #--- tk root event bindings.
        self._bind_events()

        self.disable_menu()
        self._ui.tv.reset_view()

    @property
    def isLocked(self):
        # Boolean -- True if the project is locked.
        return self._internalLockFlag

    def check_lock(self):
        """If the project is locked, unlock it on demand.

        Return True, if the project remains locked, otherwise return False.
        """
        if self.isLocked:
            if self._ui.ask_yes_no(
                message=_('Unlock?'),
                detail=f"{_('The project is locked')}."
                ):
                self.unlock()
                return False
            else:
                return True
        else:
            return False

    def disable_menu(self):
        """Disable UI widgets, e.g. when no project is open."""
        for client in self._clients:
            client.disable_menu()

    def enable_menu(self):
        """Enable UI widgets, e.g. when a project is opened."""
        for client in self._clients:
            client.enable_menu()

    def get_launchers(self):
        """Return the global launchers dictionary."""
        return launchers

    def get_preferences(self):
        """Return the global preferences dictionary."""
        return prefs

    def get_view(self):
        """Return a reference to the application's main view object."""
        return self._ui

    def lock(self, event=None):
        """Lock the project.
        
        Return True on success, otherwise return False.
        """
        if self._mdl.isModified and not self._internalLockFlag:
            if self._ui.ask_yes_no(
                message=_('Save and lock?'),
                detail=f"{_('There are unsaved changes')}."
                ):
                self.save_project()
            else:
                return False

        if self._mdl.prjFile.filePath is None:
            return False

        self._internalLockFlag = True
        for client in self._clients:
            client.lock()
        self._mdl.prjFile.lock()
        # make it persistent
        return True

    def on_close(self, doNotSave=False):
        """Close the current project.

        Optional arguments:
            doNotSave: Boolean -- If True, close the current project without saving.
        
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
                    self._ui.show_error(
                        message=_('Cannot save the project')
                        )
                    return False

        # Close the sub-controllers.
        for client in self._clients:
            client.on_close()

        # Close the model.
        self._mdl.close_project()

        # Unlock the controller and sub-controllers.
        self._internalLockFlag = False
        super().unlock()
        # calling the public unlock() method here would clear the lockfile

        self.update_status('')
        self.disable_menu()
        return True

    def on_open(self):
        """Actions to be performed after a project is opened."""
        for client in self._clients:
            client.on_open()

    def on_quit(self, event=None):
        """Save changes and keyword arguments before exiting the program.
        
        Extends the superclass method.
        """
        try:
            if self._mdl.prjFile is not None:
                if not self.on_close():
                    return 'break'

            for client in self._clients:
                client.on_quit()
        except Exception as ex:
            self._ui.show_error(
                message=_('Unhandled exception on exit'),
                detail=str(ex)
                )
            self._ui.root.quit()
        return 'break'

    def register_client(self, client):
        """Add a sub controller instance to the list."""
        if not client in self._clients:
            self._clients.append(client)

    def refresh(self):
        """Callback function to report model element modifications."""
        self.update_status()

    def unlock(self, event=None):
        """Unlock the project.
        
        If the project file was modified from the outside while it was 
        locked in the application, reload it after confirmation.
        """
        self._internalLockFlag = False
        for client in self._clients:
            client.unlock()
        self._mdl.prjFile.unlock()
        # making it persistent
        if self._mdl.prjFile.has_changed_on_disk():
            if self._ui.ask_yes_no(
                message=_('File has changed on disk. Reload?')
                ):
                self.open_project(filePath=self._mdl.prjFile.filePath)
        return 'break'

    def unregister_client(self, client):
        """Remove a sub controller instance from the list."""
        if client in self._clients:
            self._clients.remove(client)

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

    def _bind_events(self):
        event_callbacks = {
            KEYS.RESTORE_STATUS[0]: self._ui.restore_status,
            KEYS.OPEN_PROJECT[0]: self.open_project,
            KEYS.LOCK_PROJECT[0]: self.lock,
            KEYS.UNLOCK_PROJECT[0]: self.unlock,
            KEYS.RELOAD_PROJECT[0]: self.reload_project,
            KEYS.RESTORE_BACKUP[0]: self.restore_backup,
            KEYS.FOLDER[0]: self.open_project_folder,
            KEYS.REFRESH_TREE[0]: self.refresh_tree,
            KEYS.SAVE_PROJECT[0]: self.save_project,
            KEYS.SAVE_AS[0]: self.save_as,
            KEYS.CHAPTER_LEVEL[0]: self._ui.tv.show_chapter_level,
            KEYS.TOGGLE_VIEWER[0]: self._ui.toggle_contents_view,
            KEYS.TOGGLE_PROPERTIES[0]: self._ui.toggle_properties_view,
            KEYS.DETACH_PROPERTIES[0]: self._ui.toggle_properties_window,
            KEYS.ADD_ELEMENT[0]: self.add_new_element,
            KEYS.ADD_CHILD[0]: self.add_new_child,
            KEYS.ADD_PARENT[0]: self.add_new_parent,
            KEYS.OPEN_HELP[0]: self.open_help,
        }
        if PLATFORM == 'win':
            event_callbacks.update({
                MOUSE.BACK_CLICK: self._ui.tv.go_back,
                MOUSE.FORWARD_CLICK: self._ui.tv.go_forward,
            })
        else:
            event_callbacks.update({
                KEYS.QUIT_PROGRAM[0]: self.on_quit,
            })
        for sequence, callback in event_callbacks.items():
            self._ui.root.bind(sequence, callback)


"""Provide a plugin registry class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import glob
import importlib
import os
import sys

from nvlib.nv_globals import prefs
from nvlib.plugin.rejected_plugin import RejectedPlugin
from novxlib.novx_globals import _


class PluginCollection(dict):
    """A plugin registry class.
    
    Represents a dictionary with 
        key: str -- The module name.
        value: object -- The module's Plugin() instance.
    
    Public instance variables:
        majorVersion: int -- The application's major version number.
        minorVersion: int -- The application's minor version number.    
    """

    def __init__(self, model, view, controller):
        """Set up the API references and the version number.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.
            
        Extends the superclass constructor.
        """
        super().__init__()
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        # Get the major and minor version numbers for API compatibility check.
        # The version number is inserted on building the script.
        versionStr = '@release'
        # This is a placehoder for the build script.

        try:
            majorStr, minorStr, patchStr = versionStr.split('.')
            self.majorVersion = int(majorStr)
            self.minorVersion = int(minorStr)
            self.patchlevel = int(patchStr)
        except ValueError:
            # Set defaults for testing.
            self.majorVersion = 3
            self.minorVersion = 8
            self.patchlevel = 0

    def delete_file(self, moduleName):
        """Remove a module from the file system.
        
        Positional arguments:
            moduleName -- str: Module name as used as registry key.
        
        Note: the plugin remains active until restart.
        Return True on success, otherwise return False. 
        """
        if moduleName in self:
            try:
                if self[moduleName].filePath:
                    if self._ui.ask_yes_no(f'{_("Delete file")} "{self[moduleName].filePath}"?'):
                        os.remove(self[moduleName].filePath)
                        self[moduleName].filePath = ''
                        return True

            except Exception as ex:
                print(str(ex))
        return False

    def load_file(self, filePath):
        """Load and register a single plugin.

        Positional arguments:
            filePath -- str: The module's location in the file system. 

        Return True on success, otherwise return False. 
        """
        try:
            moduleName = os.path.split(filePath)[1][:-3]

            # Import the module.
            module = importlib.import_module(moduleName)

            # Check API compatibility.
            pluginObject = module.Plugin()
            try:
                apiVerStr = pluginObject.API_VERSION
                isCompatible = True
            except AttributeError:
                # might be a 1.x API plugin
                apiVerStr = pluginObject.NOVELTREE_API
                isCompatible = False
            majorStr, minorStr = apiVerStr.split('.')
            apiMajorVersion = int(majorStr)
            apiMinorVersion = int(minorStr)
            if apiMajorVersion != self.majorVersion:
                isCompatible = False
            if apiMinorVersion > self.minorVersion:
                isCompatible = False
            if isCompatible:
                # Install the plugin by calling its constructor substitute.
                pluginObject.install(self._mdl, self._ui, self._ctrl, prefs)

            # Change flags to indicate the installation.
            # Plugin classes that don't inherit from PluginBase may be monkey-patched.
            pluginObject.isActive = isCompatible
            pluginObject.isRejected = False

            # Register the module.
            self[moduleName] = pluginObject

            # Locate the module.
            module.Plugin.filePath = filePath
            return True

        except Exception as ex:
            self[moduleName] = RejectedPlugin(filePath, str(ex))
            return False

    def load_plugins(self, pluginPath):
        """Load and register the plugins.
        
        Import modules from the "plugin" subdirectory 
        and instantiate their 'Plugin' classes.
        The objects are stored in the self._plugins collection.
        Return True on success, otherwise return False. 
        """
        if not os.path.isdir(pluginPath):
            print('Plugin directory not found.')
            return False

        # Set Key bindings to be used by all plugins.
        self._ui.tv.tree.bind('<Double-1>', self.open_node)
        self._ui.tv.tree.bind('<Return>', self.open_node)

        # Load all plugins in the Plugin path.
        sys.path.append(pluginPath)
        for file in glob.iglob(f'{pluginPath}/nv_*.py'):
            self.load_file(file)

        return True

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        for moduleName in self:
            if self[moduleName].isActive:
                try:
                    self[moduleName].disable_menu()
                except:
                    pass

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        for moduleName in self:
            if self[moduleName].isActive:
                try:
                    self[moduleName].enable_menu()
                except:
                    pass

    def lock(self):
        """Prevent the plugins from changing the model."""
        for moduleName in self:
            if self[moduleName].isActive:
                try:
                    self[moduleName].lock()
                except:
                    pass

    def unlock(self):
        """Allow the plugins changing the model."""
        for moduleName in self:
            if self[moduleName].isActive:
                try:
                    self[moduleName].unlock()
                except:
                    pass

    def on_quit(self):
        """Perform actions before the application is closed."""
        for moduleName in self:
            if self[moduleName].isActive:
                try:
                    self[moduleName].on_quit()
                except:
                    pass

    def on_close(self):
        """Perform actions before a project is closed."""
        for moduleName in self:
            if self[moduleName].isActive:
                try:
                    self[moduleName].on_close()
                except:
                    pass

    def open_node(self, event=None):
        """Actions on double-clicking on a node or pressing the Return key."""
        for moduleName in self:
            if self[moduleName].isActive:
                try:
                    self[moduleName].open_node()
                except:
                    pass


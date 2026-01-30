"""Provide a plugin registry class.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import glob
import importlib
import os
import sys

from nvlib.controller.plugin.rejected_plugin import RejectedPlugin
from nvlib.controller.sub_controller import SubController


class PluginCollection(dict, SubController):
    """A collection of plugins.
        
    Represents a dictionary with 
        key: str -- The plugin's module name.
        value: object -- The imported module's Plugin instance.
    
    Passes down the following commands to the plugins:
        - close
        - quit
        - enable/disable menu
        - lock  
    
    Public instance variables:
        majorVersion: int -- The application's major version number.
        minorVersion: int -- The application's minor version number.    
    """

    def __init__(self, model, view, controller):
        """Set up the API references and the version number.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.
            
        Extends the superclass constructor.
        """
        dict.__init__(self)
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
            self.majorVersion = 5
            self.minorVersion = 51
            self.patchlevel = 0

    def uninstall_plugin(self, pluginName):
        """Call the plugin's uninstall method and delete its module file.
        
        Positional arguments:
            pluginName -- str: Plugin name as used as registry key.
        
        Note: the plugin remains active until restart.
        Return True on success, otherwise return False. 
        """
        if pluginName in self:
            try:
                if self[pluginName].filePath:
                    try:
                        self[pluginName].uninstall()
                    except AttributeError:
                        # the plugin doesn't have an uninstaller method
                        pass
                    os.remove(self[pluginName].filePath)
                    self[pluginName].filePath = ''
                    return True

            except Exception as ex:
                print(str(ex))
        return False

    def disable_menu(self):
        """Disable menu entries when the plugin has not been activated."""
        for pluginName in self:
            if self[pluginName].isActive:
                try:
                    self[pluginName].disable_menu()
                except:
                    pass

    def enable_menu(self):
        """Enable menu entries when a project has been activated."""
        for pluginName in self:
            if self[pluginName].isActive:
                try:
                    self[pluginName].enable_menu()
                except:
                    pass

    def load_file(self, filePath):
        """Load and register a single plugin.

        Positional arguments:
            filePath -- str: The plugin's location in the file system. 

        Return True on success, otherwise return False. 
        """
        try:
            pluginName, __ = os.path.splitext(os.path.basename(filePath))

            # Import the plugin.
            pluginModule = importlib.import_module(pluginName)

            # Check API compatibility.
            pluginObject = pluginModule.Plugin()
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
                pluginObject.install(self._mdl, self._ui, self._ctrl)

            # Change flags to indicate the installation.
            # Plugin classes that don't inherit from PluginBase
            # may be monkey-patched.
            pluginObject.isActive = isCompatible
            pluginObject.isRejected = False

            # Register the plugin.
            self[pluginName] = pluginObject

            # Locate the plugin.
            pluginObject.filePath = filePath
            return True

        except Exception as ex:
            self[pluginName] = RejectedPlugin(filePath, str(ex))
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

        # Load all plugins in the Plugin path.
        sys.path.append(pluginPath)
        for file in glob.iglob(f'{pluginPath}/nv_*.py'):
            self.load_file(file)

        return True

    def lock(self):
        """Prevent the plugins from changing the model."""
        for pluginName in self:
            if self[pluginName].isActive:
                try:
                    self[pluginName].lock()
                except:
                    pass

    def on_close(self):
        """Perform actions before a project is closed."""
        for pluginName in self:
            if self[pluginName].isActive:
                try:
                    self[pluginName].on_close()
                except:
                    pass

    def on_open(self):
        """Actions to be performed after a project is opened."""
        for pluginName in self:
            if self[pluginName].isActive:
                try:
                    self[pluginName].on_open()
                except:
                    pass

    def on_quit(self):
        """Perform actions before the application is closed."""
        for pluginName in self:
            if self[pluginName].isActive:
                try:
                    self[pluginName].on_quit()
                except:
                    pass

    def unlock(self):
        """Allow the plugins changing the model."""
        for pluginName in self:
            if self[pluginName].isActive:
                try:
                    self[pluginName].unlock()
                except:
                    pass


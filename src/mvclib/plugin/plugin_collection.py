"""Provide a plugin collection class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/mvclib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""


class PluginCollection(list):
    """A list of PluginBase instances.
      
    Passes down the following commands to the plugins:
        - close
        - quit
        - enable/disable menu    
        - lock  
    """

    PLUGINS = []
    # to be overwritten by subclasses

    def __init__(self, model, view, controller):
        """Instantiate the plugin objects and put them on the list.

        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.
            
        Extends the superclass constructor.
        """
        super().__init__()
        for plugin in self.PLUGINS:
            self.append(plugin(model, view, controller))

    def disable_menu(self):
        """Disable UI widgets when no project is open."""
        for plugin in self:
            plugin.disable_menu()

    def enable_menu(self):
        """Enable UI widgets when a project is open."""
        for plugin in self:
            plugin.enable_menu()

    def lock(self):
        """Prevent the plugins from changing the model."""
        for plugin in self:
            plugin.lock()

    def on_close(self):
        """Perform actions before a project is closed."""
        for plugin in self:
            plugin.on_close()

    def on_quit(self):
        """Perform actions before the application is closed."""
        for plugin in self:
            plugin.on_quit()


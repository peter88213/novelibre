"""Provide a view base class for a MVC framework.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from tkinter import ttk

from nvlib.gui.footers.status_bar import StatusBar
from nvlib.gui.observer import Observer
from nvlib.gui.user_interface.ui_facade import UiFacade
import tkinter as tk


class ViewBase(UiFacade, Observer):
    """Base class for a view with a main menu, a main window, and a status bar."""

    def __init__(self, model, controller, title):
        super().__init__(title)

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", controller.on_quit)
        self.root.title(title)
        self.title = title

        model.add_observer(self)

        #---  Add en empty main menu to the root window.
        self.mainMenu = tk.Menu(self.root)
        self.root.config(menu=self.mainMenu)

        #--- Create the main window within the root window.
        self.mainWindow = ttk.Frame()
        self.mainWindow.pack(expand=True, fill='both')

        #--- Create the status bar below the main window.
        self._create_status_bar()

        #--- Initialize GUI theme.
        self.guiStyle = ttk.Style()

    def on_quit(self):
        """Gracefully close the user interface."""
        self.root.quit()

    def restore_status(self, event=None):
        """Overwrite error message with the status before."""
        self.statusBar.restore_status()

    def set_status(self, message, colors=None):
        """Display a message on the status bar.
        
        Positional arguments:
            message -- message to be displayed. 
            
        Optional arguments:
            colors: tuple -- (background color, foreground color).

        Default status bar color is red if the message starts with "!", 
        yellow, if the message starts with "#", otherwise green.
        
        Overrides the superclass method.
        """
        if message is not None:
            self.infoHowText = self.statusBar.show_message(message, colors)
            # inherited message buffer

    def start(self):
        """Start the Tk main loop.
        
        Note: This can not be done in the constructor method.
        """
        self.root.mainloop()

    def update_status(self, statusText=''):
        """Update the project status information on the status bar.
        
        Optional arguments:
            statusText: str -- Text to be displayed on the status bar.
        """
        self.statusBar.update_status(statusText)

    def _create_status_bar(self):
        self.statusBar = StatusBar(self.root, text='', anchor='w', padx=5, pady=2)
        self.statusBar.pack(expand=False, fill='both')


"""Provide a view base class for a MVC framework.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import abstractmethod

from mvclib.view.ui_facade import UiFacade
import tkinter as tk
from mvclib.view.observer import Observer


class ViewBase(UiFacade, Observer):

    @abstractmethod
    def __init__(self, model, controller, title):
        UiFacade.__init__(self, title)

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", controller.on_quit)
        self.root.title(title)
        self.title = title
        model.add_observer(self)

    def on_quit(self):
        """Gracefully close the user interface."""
        self.root.quit()

    def start(self):
        """Start the Tk main loop.
        
        Note: This can not be done in the constructor method.
        """
        self.root.mainloop()


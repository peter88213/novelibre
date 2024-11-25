"""Provide a user interface facade with dialogs.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import messagebox

from mvclib.view.ui import Ui


class UiFacade(Ui):

    def __init__(self, title):
        Ui.__init__(self, title)

    def ask_ok_cancel(self, text, title=None):
        """Query ok or cancel with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askokcancel(title, text)

    def ask_yes_no(self, text, title=None):
        """Query yes or no with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askyesno(title, text)

    def ask_yes_no_cancel(self, text, title=None):
        """Query yes or no or cancel with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askyesnocancel(title, text)

    def show_error(self, message, title=None):
        """Display an error message box.
        
        Positional arguments:
            message -- error message to be displayed.
            
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showerror(title, message)

    def show_info(self, message, title=None):
        """Display an informational message box.
        
        Positional arguments:
            message -- informational message to be displayed.
            
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showinfo(title, message)

    def show_warning(self, message, title=None):
        """Display a warning message box.
        
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showwarning(title, message)


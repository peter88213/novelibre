"""Provide a user interface facade with dialogs.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import messagebox

from nvlib.alternative_ui.ui import Ui


class UiFacade(Ui):

    def __init__(self, title):
        Ui.__init__(self, title)

    def ask_ok_cancel(self, message='', detail='', title=None, **options):
        """Query ok or cancel with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askokcancel(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )

    def ask_yes_no(self, message='', detail='', title=None, **options):
        """Query yes or no with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askyesno(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )

    def ask_yes_no_cancel(self, message='', detail='', title=None, **options):
        """Query yes or no or cancel with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askyesnocancel(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )

    def show_error(self, message='', detail='', title=None, **options):
        """Display an error message box.
        
        Positional arguments:
            message -- error message to be displayed.
            
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showerror(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )

    def show_info(self, message='', detail='', title=None, **options):
        """Display an informational message box.
        
        Positional arguments:
            message -- informational message to be displayed.
            
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showinfo(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )

    def show_warning(self, message='', detail='', title=None, **options):
        """Display a warning message box.
        
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showwarning(
            title=title, 
            message=message, 
            detail=detail, 
            **options
        )


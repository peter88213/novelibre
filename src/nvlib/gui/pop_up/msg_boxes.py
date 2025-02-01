"""Provide a mixin class with message box dialogs.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import messagebox

from nvlib.gui.widgets.nv_simpledialog import SimpleDialog
from nvlib.nv_locale import _


class MsgBoxes:

    def ask_delete_all_skip_cancel(self, text, default=0, title=None):
        """Query delete, all, skip, or cancel with a pop-up box. 
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        
        Return:
        - 0 for overwrite,
        - 1 for open existing, 
        - 2 for cancel. 
        """
        return SimpleDialog(
                    None,
                    text=text,
                    buttons=[_('Delete'), _('All'), _('Skip'), _('Cancel')],
                    default=0,
                    cancel=3,
                    title=title
                    ).go()

    def ask_ok_cancel(self, text, title=None, **options):
        """Query ok or cancel with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askokcancel(title, text, **options)

    def ask_overwrite_open_cancel(self, text, default=0, title=None):
        """Query overwrite, open existing, or cancel with a pop-up box. 
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        
        Return:
        - 0 for overwrite,
        - 1 for open existing, 
        - 2 for cancel. 
        """
        return SimpleDialog(
            None,
            text=text,
            buttons=[_('Overwrite'), _('Open existing'), _('Cancel')],
            default=default,
            cancel=2,
            title=title
            ).go()

    def ask_yes_no(self, text, title=None, **options):
        """Query yes or no with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askyesno(title, text, **options)

    def ask_yes_no_cancel(self, text, title=None, **options):
        """Query yes or no or cancel with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askyesnocancel(title, text, **options)

    def show_error(self, message, title=None, **options):
        """Display an error message box.
        
        Positional arguments:
            message -- error message to be displayed.
            
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showerror(title, message, **options)

    def show_info(self, message, title=None, **options):
        """Display an informational message box.
        
        Positional arguments:
            message -- informational message to be displayed.
            
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showinfo(title, message, **options)

    def show_warning(self, message, title=None, **options):
        """Display a warning message box.
        
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showwarning(title, message, **options)


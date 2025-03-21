"""Provide a mixin class with message box dialogs.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import messagebox

from nvlib.gui.widgets.nv_simpledialog import SimpleDialog
from nvlib.nv_locale import _


class MsgBoxes:

    def ask_delete_all_skip_cancel(self, text, default=0, title='novelibre'):
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
                    default=default,
                    cancel=3,
                    title=title
                    ).go()

    def ask_ok_cancel(self, message='', detail='', title='novelibre', **options):
        """Query ok or cancel with a pop-up box.
        
        Optional arguments:
            message -- question to be asked in the pop-up box. 
            detail -- additional text to be displayed.
            title -- title to be displayed on the window frame.            
        """
        return messagebox.askokcancel(
            message=message,
            detail=detail,
            title=title,
            **options
            )

    def ask_overwrite_open_cancel(self, text, default=0, title='novelibre'):
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

    def ask_yes_no(self, message='', detail='', title='novelibre', **options):
        """Query yes or no with a pop-up box.
        
        Optional arguments:
            message -- question to be asked in the pop-up box. 
            detail -- additional text to be displayed.
            title -- title to be displayed on the window frame.            
        """
        return messagebox.askyesno(
            message=message,
            detail=detail,
            title=title,
            **options
            )

    def ask_yes_no_cancel(self, message='', detail='', title='novelibre', **options):
        """Query yes or no or cancel with a pop-up box.
        
        Optional arguments:
            message -- question to be asked in the pop-up box. 
            detail -- additional text to be displayed.
            title -- title to be displayed on the window frame.            
        """
        return messagebox.askyesnocancel(
            message=message,
            detail=detail,
            title=title,
            **options
            )

    def show_error(self, message='', detail='', title='novelibre', **options):
        """Display an error message box.
        
        Optional arguments:
            message -- error message to be displayed.
            detail -- additional text to be displayed.
            title -- title to be displayed on the window frame.
        """
        messagebox.showerror(
            message=message,
            detail=detail,
            title=title,
            **options
            )

    def show_info(self, message='', detail='', title='novelibre', **options):
        """Display an informational message box.
        
        Optional arguments:
            message -- informational message to be displayed.
            detail -- additional text to be displayed.            
            title -- title to be displayed on the window frame.
        """
        messagebox.showinfo(
            message=message,
            detail=detail,
            title=title,
            **options
            )

    def show_warning(self, message='', detail='', title='novelibre', **options):
        """Display a warning message box.
        
        Optional arguments:
            message -- warning message to be displayed.
            detail -- additional text to be displayed.
            title -- title to be displayed on the window frame.
        """
        messagebox.showwarning(
            message=message,
            detail=detail,
            title=title,
            **options
            )


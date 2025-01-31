"""Helper module to set a custom icon at the tk windows.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
import tkinter as tk


def set_icon(widget, icon='logo', path=None, default=True):
    """Set the window icon. 
    
    Assign the "path"/"icon".png image to the "widget" window.
    
    Positional arguments:
        widget: tk object -- The tk application window.
        
    Optional arguments:
        icon: str -- The icon filename without extension.
        path: str -- The directory containing the icons.
        default: bool -- If True, assign the icon to all subsequently opened toplevel windows.
        
    If no path is specified, a subdirectory "icons" of the script location is used.     
    The "png" filetype is required as icon. 
    
    Return False, if an error occurs, otherwise return True.
    """
    if path is None:
        path = os.path.dirname(sys.argv[0])
        if not path:
            path = '.'
        path = f'{path}/icons'
    try:
        pic = tk.PhotoImage(file=f'{path}/{icon}.png')
        widget.iconphoto(default, pic)
    except:
        return False

    return True


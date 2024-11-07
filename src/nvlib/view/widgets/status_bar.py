"""Provide a class for the novelibre status bar.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.view.observer import Observer
from nvlib.nv_globals import prefs
import tkinter as tk


class StatusBar(Observer, tk.Label):

    COLOR_NORMAL_BG = 'light gray'
    COLOR_NORMAL_FG = 'black'

    def __init__(self, master, **kw):
        tk.Label.__init__(self, master, **kw)
        self._statusText = ''
        # text buffer; the status bar can be overwritten temporarily with messages

    def restore_status(self, event=None):
        """Overwrite error message with the status before."""
        self.show_status(self._statusText)

    def set_status(self, message, colors=None):
        """Display a message on the status bar.
        
        Positional arguments:
            message -- message to be displayed. 
            
        Optional arguments:
            colors: tuple -- (background color, foreground color).

        Default status bar color is red if the message starts with "!", 
        yellow, if the message starts with "#", otherwise green.
        """
        if message is None:
            return ''

        try:
            self.config(bg=colors[0])
            self.config(fg=colors[1])
        except:
            if message.startswith('!'):
                # error
                self.config(bg=prefs['color_status_error_bg'])
                self.config(fg=prefs['color_status_error_fg'])
                message = message.lstrip('!').strip()
            elif message.startswith('#'):
                # notification/warning
                self.config(bg=prefs['color_status_notification_bg'])
                self.config(fg=prefs['color_status_notification_fg'])
                message = message.lstrip('#').strip()
            else:
                # success
                self.config(bg=prefs['color_status_success_bg'])
                self.config(fg=prefs['color_status_success_fg'])
        self.config(text=message)
        return message

    def show_status(self, statusText=''):
        """Display a statusText on the status bar.
        
        Optional arguments:
            statusText: str -- Text to be displayed on the status bar.
        """
        self._statusText = statusText
        self.config(bg=self.COLOR_NORMAL_BG)
        self.config(fg=self.COLOR_NORMAL_FG)
        self.config(text=statusText)

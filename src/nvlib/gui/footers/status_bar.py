"""Provide a class for a status bar.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import tkinter as tk


class StatusBar(tk.Label):

    COLOR_NORMAL_BG = 'light gray'
    COLOR_NORMAL_FG = 'black'
    COLOR_SUCCESS_BG = 'green'
    COLOR_SUCCESS_FG = 'white'
    COLOR_ERROR_BG = 'red'
    COLOR_ERROR_FG = 'white'
    COLOR_NOTIFICATION_BG = 'yellow'
    COLOR_NOTIFICATION_FG = 'black'

    def __init__(self, master, **kw):
        tk.Label.__init__(self, master, **kw)
        self._statusText = ''
        # text buffer; the regular status information can be overwritten temporarily with messages

    def restore_status(self, event=None):
        """Overwrite error message with the status before."""
        self.update_status(self._statusText)

    def show_message(self, message, colors=None):
        """Overwrite the status text temporarily with a message to be returned.
        
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
                self.config(bg=self.COLOR_ERROR_BG)
                self.config(fg=self.COLOR_ERROR_FG)
                message = message.lstrip('!').strip()
            elif message.startswith('#'):
                # notification/warning
                self.config(bg=self.COLOR_NOTIFICATION_BG)
                self.config(fg=self.COLOR_NOTIFICATION_FG)
                message = message.lstrip('#').strip()
            else:
                # success
                self.config(bg=self.COLOR_SUCCESS_BG)
                self.config(fg=self.COLOR_SUCCESS_FG)
        self.config(text=message)
        return message

    def update_status(self, statusText=''):
        """Update the regular status text on the status bar.
        
        Optional arguments:
            statusText: str -- Text to be displayed on the status bar.
        """
        self._statusText = statusText
        self.config(bg=self.COLOR_NORMAL_BG)
        self.config(fg=self.COLOR_NORMAL_FG)
        self.config(text=statusText)

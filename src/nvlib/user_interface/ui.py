"""Provide a base class for user interface facades.

All UI facades inherit from this class. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class Ui:
    """Base class for UI facades, implementing a 'silent mode'.
    
    Public instance variables:
        infoWhatText -- buffer for general messages.
        infoHowText -- buffer for error/success messages.
    """

    def __init__(self, title):
        """Initialize text buffers for messaging.
        
        Positional arguments:
            title -- application title.
        """
        self.infoWhatText = ''
        self.infoHowText = ''
        # message buffers

    def ask_yes_no(self, text):
        """Return True or False.
        
        Positional arguments:
            text -- question to be asked. 
            
        This is a stub used for "silent mode".
        The application may use a subclass for confirmation requests.    
        """
        return True

    def set_info(self, message):
        """Show what the converter is going to do.
        
        Positional arguments:
            message -- message to be buffered. 
        """
        self.infoWhatText = message

    def set_status(self, message):
        """Set a buffered message for display in any status area.
        
        Positional arguments:
            message -- message to be buffered.
            
        Replace error/notification markers, if any.
        """
        if message.startswith('!'):
            message = f'Error: {message.split("!", maxsplit=1)[1].strip()}'
        elif message.startswith('#'):
            message = f'Notification: {message.split("#", maxsplit=1)[1].strip()}'
        self.infoHowText = message

    def show_warning(self, message):
        """Stub for displaying a warning message.

        Positional arguments:
            message -- message to be displayed. 
        """
        pass

    def start(self):
        """Launch the GUI, if any.
        
        To be overridden by subclasses requiring
        special action to launch the user interaction.
        """
        pass


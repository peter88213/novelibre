"""Provide a mixin class for controlling the toolbar.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""

from mvclib.controller.sub_controller import SubController


class ToolbarCtrl(SubController):

    def disable_menu(self):
        """Disable toolbar buttons when no project is open.        
        
        Overrides the superclass method.
        """
        self.addChildButton.config(state='disabled')
        self.addElementButton.config(state='disabled')
        self.addParentButton.config(state='disabled')
        self.goBackButton.config(state='disabled')
        self.goForwardButton.config(state='disabled')
        self.lockButton.config(state='disabled')
        self.manuscriptButton.config(state='disabled')
        self.deleteElementButton.config(state='disabled')
        self.saveButton.config(state='disabled')
        self.updateButton.config(state='disabled')
        self.viewBookButton.config(state='disabled')
        self.viewCharactersButton.config(state='disabled')
        self.viewItemsButton.config(state='disabled')
        self.viewLocationsButton.config(state='disabled')
        self.viewPlotLinesButton.config(state='disabled')
        self.viewProjectnotesButton.config(state='disabled')

    def enable_menu(self):
        """Enable toolbar buttons when a project is open.        
        
        Overrides the superclass method.
        """
        self.addChildButton.config(state='normal')
        self.addElementButton.config(state='normal')
        self.addParentButton.config(state='normal')
        self.goBackButton.config(state='normal')
        self.goForwardButton.config(state='normal')
        self.lockButton.config(state='normal')
        self.manuscriptButton.config(state='normal')
        self.deleteElementButton.config(state='normal')
        self.saveButton.config(state='normal')
        self.updateButton.config(state='normal')
        self.viewBookButton.config(state='normal')
        self.viewCharactersButton.config(state='normal')
        self.viewItemsButton.config(state='normal')
        self.viewLocationsButton.config(state='normal')
        self.viewPlotLinesButton.config(state='normal')
        self.viewProjectnotesButton.config(state='normal')

    def lock(self):
        """Make the "locked" state take effect.
        
        Overrides the superclass method.
        """
        self.manuscriptButton.config(state='disabled')
        self.addElementButton.config(state='disabled')
        self.addChildButton.config(state='disabled')
        self.addParentButton.config(state='disabled')
        self.deleteElementButton.config(state='disabled')

    def unlock(self):
        """Make the "unlocked" state take effect.
        
        Overrides the superclass method.
        """
        self.manuscriptButton.config(state='normal')
        self.addElementButton.config(state='normal')
        self.addChildButton.config(state='normal')
        self.addParentButton.config(state='normal')
        self.deleteElementButton.config(state='normal')


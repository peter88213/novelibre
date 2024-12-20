"""Provide a mixin class for controlling the main view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController
from nvlib.nv_locale import _


class MainViewCtrl(SubController):

    def about(self):
        self.show_info(__doc__)

    def disable_menu(self):
        """Disable menu entries when no project is open.        
        
        Overrides the superclass method.
        """
        self.fileMenu.entryconfig(_('Close'), state='disabled')
        self.mainMenu.entryconfig(_('Part'), state='disabled')
        self.mainMenu.entryconfig(_('Chapter'), state='disabled')
        self.mainMenu.entryconfig(_('Section'), state='disabled')
        self.mainMenu.entryconfig(_('Characters'), state='disabled')
        self.mainMenu.entryconfig(_('Locations'), state='disabled')
        self.mainMenu.entryconfig(_('Items'), state='disabled')
        self.mainMenu.entryconfig(_('Plot'), state='disabled')
        self.mainMenu.entryconfig(_('Project notes'), state='disabled')
        self.mainMenu.entryconfig(_('Export'), state='disabled')
        self.mainMenu.entryconfig(_('Import'), state='disabled')
        self.fileMenu.entryconfig(_('Reload'), state='disabled')
        self.fileMenu.entryconfig(_('Restore backup'), state='disabled')
        self.fileMenu.entryconfig(_('Refresh Tree'), state='disabled')
        self.fileMenu.entryconfig(_('Lock'), state='disabled')
        self.fileMenu.entryconfig(_('Unlock'), state='disabled')
        self.fileMenu.entryconfig(_('Open Project folder'), state='disabled')
        self.fileMenu.entryconfig(_('Copy style sheet'), state='disabled')
        self.fileMenu.entryconfig(_('Save'), state='disabled')
        self.fileMenu.entryconfig(_('Save as...'), state='disabled')
        self.fileMenu.entryconfig(_('Discard manuscript'), state='disabled')
        self.viewMenu.entryconfig(_('Chapter level'), state='disabled')
        self.viewMenu.entryconfig(_('Expand selected'), state='disabled')
        self.viewMenu.entryconfig(_('Collapse selected'), state='disabled')
        self.viewMenu.entryconfig(_('Expand all'), state='disabled')
        self.viewMenu.entryconfig(_('Collapse all'), state='disabled')
        self.viewMenu.entryconfig(_('Show Book'), state='disabled')
        self.viewMenu.entryconfig(_('Show Characters'), state='disabled')
        self.viewMenu.entryconfig(_('Show Locations'), state='disabled')
        self.viewMenu.entryconfig(_('Show Items'), state='disabled')
        self.viewMenu.entryconfig(_('Show Plot lines'), state='disabled')
        self.viewMenu.entryconfig(_('Show Project notes'), state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self.fileMenu.entryconfig(_('Close'), state='normal')
        self.mainMenu.entryconfig(_('Part'), state='normal')
        self.mainMenu.entryconfig(_('Chapter'), state='normal')
        self.mainMenu.entryconfig(_('Section'), state='normal')
        self.mainMenu.entryconfig(_('Characters'), state='normal')
        self.mainMenu.entryconfig(_('Locations'), state='normal')
        self.mainMenu.entryconfig(_('Items'), state='normal')
        self.mainMenu.entryconfig(_('Plot'), state='normal')
        self.mainMenu.entryconfig(_('Project notes'), state='normal')
        self.mainMenu.entryconfig(_('Export'), state='normal')
        self.mainMenu.entryconfig(_('Import'), state='normal')
        self.fileMenu.entryconfig(_('Reload'), state='normal')
        self.fileMenu.entryconfig(_('Restore backup'), state='normal')
        self.fileMenu.entryconfig(_('Refresh Tree'), state='normal')
        self.fileMenu.entryconfig(_('Lock'), state='normal')
        self.fileMenu.entryconfig(_('Open Project folder'), state='normal')
        self.fileMenu.entryconfig(_('Copy style sheet'), state='normal')
        self.fileMenu.entryconfig(_('Save'), state='normal')
        self.fileMenu.entryconfig(_('Save as...'), state='normal')
        self.fileMenu.entryconfig(_('Discard manuscript'), state='normal')
        self.viewMenu.entryconfig(_('Chapter level'), state='normal')
        self.viewMenu.entryconfig(_('Expand selected'), state='normal')
        self.viewMenu.entryconfig(_('Collapse selected'), state='normal')
        self.viewMenu.entryconfig(_('Expand all'), state='normal')
        self.viewMenu.entryconfig(_('Collapse all'), state='normal')
        self.viewMenu.entryconfig(_('Show Book'), state='normal')
        self.viewMenu.entryconfig(_('Show Characters'), state='normal')
        self.viewMenu.entryconfig(_('Show Locations'), state='normal')
        self.viewMenu.entryconfig(_('Show Items'), state='normal')
        self.viewMenu.entryconfig(_('Show Plot lines'), state='normal')
        self.viewMenu.entryconfig(_('Show Project notes'), state='normal')

    def lock(self):
        """Make the "locked" state take effect.
        
        Overrides the superclass method.
        """
        self.pathBar.set_locked()
        self.fileMenu.entryconfig(_('Save'), state='disabled')
        self.fileMenu.entryconfig(_('Lock'), state='disabled')
        self.fileMenu.entryconfig(_('Unlock'), state='normal')
        self.mainMenu.entryconfig(_('Part'), state='disabled')
        self.mainMenu.entryconfig(_('Chapter'), state='disabled')
        self.mainMenu.entryconfig(_('Section'), state='disabled')
        self.mainMenu.entryconfig(_('Characters'), state='disabled')
        self.mainMenu.entryconfig(_('Locations'), state='disabled')
        self.mainMenu.entryconfig(_('Items'), state='disabled')
        self.mainMenu.entryconfig(_('Plot'), state='disabled')
        self.mainMenu.entryconfig(_('Project notes'), state='disabled')
        self.mainMenu.entryconfig(_('Export'), state='disabled')

    def set_title(self):
        """Set the main window title. 
        
        'Document title by author - application'
        """
        if self._mdl.novel is None:
            return

        if self._mdl.novel.title:
            titleView = self._mdl.novel.title
        else:
            titleView = _('Untitled project')
        if self._mdl.novel.authorName:
            authorView = self._mdl.novel.authorName
        else:
            authorView = _('Unknown author')
        self.root.title(f'{titleView} {_("by")} {authorView} - {self.title}')

    def unlock(self):
        """Make the "unlocked" state take effect.
        
        Overrides the superclass method.
        """
        self.pathBar.set_normal()
        self.fileMenu.entryconfig(_('Save'), state='normal')
        self.fileMenu.entryconfig(_('Lock'), state='normal')
        self.fileMenu.entryconfig(_('Unlock'), state='disabled')
        self.mainMenu.entryconfig(_('Part'), state='normal')
        self.mainMenu.entryconfig(_('Chapter'), state='normal')
        self.mainMenu.entryconfig(_('Section'), state='normal')
        self.mainMenu.entryconfig(_('Characters'), state='normal')
        self.mainMenu.entryconfig(_('Locations'), state='normal')
        self.mainMenu.entryconfig(_('Items'), state='normal')
        self.mainMenu.entryconfig(_('Plot'), state='normal')
        self.mainMenu.entryconfig(_('Project notes'), state='normal')
        self.mainMenu.entryconfig(_('Export'), state='normal')


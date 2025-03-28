"""Provide a mixin class for controlling the main view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.sub_controller import SubController
from nvlib.nv_locale import _


class MainViewCtrl(SubController):

    def about(self):
        """Display a legal notice window.
        
        Important: after building the program, __doc__ will be the novelibre docstring.
        """
        self.show_info(
            message=f'novelibre {self._ctrl.plugins.majorVersion}',
            detail=__doc__,
            title=_('About novelibre')
            )

    def initialize_controller(self, model, view, controller):
        SubController.initialize_controller(self, model, view, controller)
        self._fileMenuNormalOpen = [
            _('Close'),
            _('Copy style sheet'),
            _('Discard manuscript'),
            _('Lock'),
            _('Open Project folder'),
            _('Refresh Tree'),
            _('Reload'),
            _('Restore backup'),
            _('Save as...'),
            _('Save'),
            _('Unlock'),
        ]
        self._mainMenuNormalOpen = [
            _('Chapter'),
            _('Characters'),
            _('Export'),
            _('Import'),
            _('Items'),
            _('Locations'),
            _('Part'),
            _('Plot'),
            _('Project notes'),
            _('Section'),
        ]
        self._viewMenuNormalOpen = [
            _('Chapter level'),
            _('Collapse all'),
            _('Collapse selected'),
            _('Expand all'),
            _('Expand selected'),
            _('Show Book'),
            _('Show Characters'),
            _('Show Items'),
            _('Show Locations'),
            _('Show Plot lines'),
            _('Show Project notes'),
        ]
        self._fileMenuNormalUnlocked = [
            _('Save'),
        ]
        self._mainMenuNormalUnlocked = [
            _('Chapter'),
            _('Characters'),
            _('Export'),
            _('Items'),
            _('Locations'),
            _('Part'),
            _('Plot'),
            _('Project notes'),
            _('Section'),
        ]

    def disable_menu(self):
        """Disable menu entries when no project is open.        
        
        Overrides the superclass method.
        """
        for entry in self._fileMenuNormalOpen:
            self.fileMenu.entryconfig(entry, state='disabled')
        for entry in self._mainMenuNormalOpen:
            self.mainMenu.entryconfig(entry, state='disabled')
        for entry in self._viewMenuNormalOpen:
            self.viewMenu.entryconfig(entry, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        for entry in self._fileMenuNormalOpen:
            self.fileMenu.entryconfig(entry, state='normal')
        for entry in self._mainMenuNormalOpen:
            self.mainMenu.entryconfig(entry, state='normal')
        for entry in self._viewMenuNormalOpen:
            self.viewMenu.entryconfig(entry, state='normal')

    def lock(self):
        """Make the "locked" state take effect.
        
        Overrides the superclass method.
        """
        self.pathBar.set_locked()
        self.fileMenu.entryconfig(_('Unlock'), state='normal')
        self.fileMenu.entryconfig(_('Lock'), state='disabled')
        for entry in self._fileMenuNormalUnlocked:
            self.fileMenu.entryconfig(entry, state='disabled')
        for entry in self._mainMenuNormalUnlocked:
            self.mainMenu.entryconfig(entry, state='disabled')

    def on_close(self):
        """Actions to be performed when a project is closed.
        
        Overrides the superclass method.
        """
        self.root.title(self.title)
        self.show_path('')
        self.pathBar.set_normal()

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
        self.fileMenu.entryconfig(_('Unlock'), state='disabled')
        self.fileMenu.entryconfig(_('Lock'), state='normal')
        for entry in self._fileMenuNormalUnlocked:
            self.fileMenu.entryconfig(entry, state='normal')
        for entry in self._mainMenuNormalUnlocked:
            self.mainMenu.entryconfig(entry, state='normal')


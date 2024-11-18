"""Provide a mixin class for controlling the main view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController
from nvlib.novx_globals import _
from nvlib.nv_globals import open_help
from nvlib.view.pop_up.export_options_window import ExportOptionsWindow
from nvlib.view.pop_up.plugin_manager import PluginManager
from nvlib.view.pop_up.prj_updater import PrjUpdater
from nvlib.view.pop_up.view_options_window import ViewOptionsWindow
from nvlib.view.widgets.nv_simpledialog import askinteger


class NvMainViewCtrl(SubController):

    _MAX_NR_NEW_SECTIONS = 20
    # maximum number of sections to add in bulk
    _INI_NR_NEW_SECTIONS = 1
    # initial value when asking for the number of sections to add

    def add_multiple_sections(self):
        """Ask how many sections are to be added, then call the controller."""
        n = askinteger(
            title=_('New'),
            prompt=_('How many sections to add?'),
            initialvalue=self._INI_NR_NEW_SECTIONS,
            minvalue=0,
            maxvalue=self._MAX_NR_NEW_SECTIONS
            )
        if n is not None:
            for __ in range(n):
                self._ctrl.add_section()

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
        """Make the "locked" state visible.
        
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

    def open_export_options(self, event=None):
        """Open a toplevel window to edit the export options."""
        ExportOptionsWindow(self._mdl, self, self._ctrl)
        return 'break'

    def open_help(self, event=None):
        open_help('')

    def open_plugin_manager(self, event=None):
        """Open a toplevel window to manage the plugins."""
        PluginManager(self._mdl, self, self._ctrl)
        return 'break'

    def open_project_updater(self, event=None):
        """Update the project from a previously exported document.
        
        Using a toplevel window with a pick list of refresh sources.
        """
        PrjUpdater(self._mdl, self, self._ctrl)
        return 'break'

    def open_view_options(self, event=None):
        """Open a toplevel window to edit the view options."""
        ViewOptionsWindow(self._mdl, self, self._ctrl)
        return 'break'

    def unlock(self):
        """Make the "unlocked" state visible.
        
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


"""Provide a tkinter based GUI for novelibre.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.controller.sub_controller import SubController
from nvlib.gui.contents_window.contents_viewer import ContentsViewer
from nvlib.gui.footers.path_bar import PathBar
from nvlib.gui.footers.status_bar import StatusBar
from nvlib.gui.icons import Icons
from nvlib.gui.observer import Observer
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.platform.platform_settings import MOUSE
from nvlib.gui.platform.platform_settings import PLATFORM
from nvlib.gui.pop_up.msg_boxes import MsgBoxes
from nvlib.gui.properties_window.properties_viewer import PropertiesViewer
from nvlib.gui.set_icon_tk import set_icon
from nvlib.gui.toolbar.toolbar import Toolbar
from nvlib.gui.tree_window.tree_viewer import TreeViewer
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class MainView(Observer, MsgBoxes, SubController):
    """View for the novelibre application."""
    _MIN_WINDOW_WIDTH = 400
    _MIN_WINDOW_HEIGHT = 200
    # minimum size's main window

    def __init__(self, model, controller, title):
        self._mdl = model
        self._ctrl = controller

        #--- Create the tk root window and set the size.
        self.root = tk.Tk()
        self.root.minsize(self._MIN_WINDOW_WIDTH, self._MIN_WINDOW_HEIGHT)
        self.root.protocol("WM_DELETE_WINDOW", self._ctrl.on_quit)
        self.root.title(title)
        self.title = title

        self._mdl.add_observer(self)

        #---  Add en empty main menu to the root window.
        self.mainMenu = tk.Menu(self.root)
        self.root.config(menu=self.mainMenu)

        #--- Create the main window within the root window.
        self.mainWindow = ttk.Frame()
        self.mainWindow.pack(expand=True, fill='both')

        #--- Create the status bar below the main window.
        self._create_status_bar()

        #--- Initialize GUI theme.
        self.guiStyle = ttk.Style()
        if prefs.get('root_geometry', None):
            self.root.geometry(prefs['root_geometry'])

        #--- Create the path bar below the status bar.
        self._create_path_bar()

        #--- Initalize icons.
        set_icon(self.root, icon='nLogo32')
        self.icons = Icons()

        #--- Build the GUI frames.

        #--- Create an application window with three frames.
        self.appWindow = ttk.Frame(self.mainWindow)
        self.appWindow.pack(expand=True, fill='both')

        #--- left frame (intended for the tree).
        self.leftFrame = ttk.Frame(self.appWindow)
        self.leftFrame.pack(side='left', expand=True, fill='both')

        #--- Create a novel tree window in the left frame.
        self.tv = TreeViewer(
            self.leftFrame,
            self._mdl,
            self,
            self._ctrl,
        )
        self._mdl.add_observer(self.tv)
        self._ctrl.register_client(self.tv)
        self.tv.pack(expand=True, fill='both')
        self._selection = None

        #--- Middle frame (intended for the content viewer).
        self.middleFrame = ttk.Frame(
            self.appWindow,
            width=prefs['middle_frame_width'],
        )
        self.middleFrame.pack_propagate(0)

        #--- Create a text viewer in the middle frame.
        self.contentsView = ContentsViewer(
            self.middleFrame,
            self._mdl,
            self._ctrl,
        )
        self._mdl.add_observer(self.contentsView)
        self._ctrl.register_client(self.contentsView)
        if prefs['show_contents']:
            self.middleFrame.pack(side='left', expand=False, fill='both')

        #--- Right frame for for the element properties view.
        self.rightFrame = ttk.Frame(
            self.appWindow,
            width=prefs['right_frame_width'],
        )
        self.rightFrame.pack_propagate(0)
        if prefs['show_properties']:
            self.rightFrame.pack(expand=True, fill='both')

        #--- Create an element properties view in the right frame.
        self.propertiesView = PropertiesViewer(
            self.rightFrame,
            self._mdl,
            self,
            self._ctrl,
        )
        self.propertiesView.pack(expand=True, fill='both')
        self._propWinDetached = False
        if prefs['detach_prop_win']:
            self._detach_properties_frame()
        self._mdl.add_observer(self.propertiesView)
        self._ctrl.register_client(self.propertiesView)

        #--- Add commands and submenus to the main menu.
        self._create_menu()

        #--- Add a toolbar.
        self.toolbar = Toolbar(self, self._ctrl)
        self._ctrl.register_client(self.toolbar)

    @property
    def selectedNode(self):
        return self._selection[0]

    @property
    def selectedNodes(self):
        return self._selection

    def disable_menu(self):
        """Disable menu entries when no project is open.        
        
        Overrides the SubController method.
        """
        for entry in self._fileMenuDisableOnClose:
            self.fileMenu.entryconfig(entry, state='disabled')
        for entry in self._mainMenuDisableOnClose:
            self.mainMenu.entryconfig(entry, state='disabled')
        for entry in self._viewMenuDisableOnClose:
            self.viewMenu.entryconfig(entry, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the SubController method.
        """
        for entry in self._fileMenuDisableOnClose:
            self.fileMenu.entryconfig(entry, state='normal')
        for entry in self._mainMenuDisableOnClose:
            self.mainMenu.entryconfig(entry, state='normal')
        for entry in self._viewMenuDisableOnClose:
            self.viewMenu.entryconfig(entry, state='normal')

    def lock(self):
        """Make the "locked" state take effect.
        
        Overrides the SubController method.
        """
        self.pathBar.set_locked()
        self.fileMenu.entryconfig(_('Unlock'), state='normal')
        self.fileMenu.entryconfig(_('Lock'), state='disabled')
        for entry in self._mainMenuDisableOnLock:
            self.mainMenu.entryconfig(entry, state='disabled')
        for entry in self._fileMenuDisableOnLock:
            self.fileMenu.entryconfig(entry, state='disabled')
        for entry in self._sectionMenuDisableOnLock:
            self.sectionMenu.entryconfig(entry, state='disabled')
        for entry in self._characterMenuDisableOnLock:
            self.characterMenu.entryconfig(entry, state='disabled')
        for entry in self._locationMenuDisableOnLock:
            self.locationMenu.entryconfig(entry, state='disabled')
        for entry in self._itemMenuDisableOnLock:
            self.itemMenu.entryconfig(entry, state='disabled')
        for entry in self._plotMenuDisableOnLock:
            self.plotMenu.entryconfig(entry, state='disabled')
        for entry in self._prjNoteMenuDisableOnLock:
            self.prjNoteMenu.entryconfig(entry, state='disabled')
        for entry in self._exportMenuDisableOnLock:
            self.exportMenu.entryconfig(entry, state='disabled')

    def on_change_selection(self, nodeId):
        """Event handler for element selection.
        
        Show the properties/contents of the selected element.
        """
        self._selection = self.tv.tree.selection()
        self.propertiesView.show_properties(nodeId)
        self.contentsView.see(nodeId)
        self.root.event_generate('<<selection_changed>>', when='tail')
        # this event can be used by plugins

    def on_close(self):
        """Actions to be performed when a project is closed.
        
        Overrides the SubController method.
        """
        self.root.title(self.title)
        self.show_path('')
        self.pathBar.set_normal()

    def on_quit(self):
        """Gracefully close the user interface.
        
        Overrides the SubController method.
        """

        # Save contents window "show markup" state.
        prefs['show_markup'] = self.contentsView.showMarkup.get()

        # Save windows size and position.
        if self._propWinDetached:
            prefs['prop_win_geometry'] = self._propertiesWindow.winfo_geometry()
        prefs['root_geometry'] = self.root.winfo_geometry()
        self.root.quit()

    def refresh(self):
        """Implements the Observer method."""
        self.set_title()

    def restore_status(self, event=None):
        """Overwrite error message with the status before."""
        self.statusBar.restore_status()

    def set_status(self, message, colors=None):
        """Display a message on the status bar.
        
        Positional arguments:
            message -- message to be displayed. 
            
        Optional arguments:
            colors: tuple -- (background color, foreground color).

        Default status bar color is red if the message starts with "!", 
        yellow, if the message starts with "#", otherwise green.
        
        """
        if message is not None:
            self.infoHowText = self.statusBar.show_message(message, colors)
            # inherited message buffer

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

    def show_path(self, message):
        """Put the message on the path bar."""
        self.pathBar.config(text=message)

    def start(self):
        """Start the Tk main loop.
        
        Note: This can not be done in the constructor method.
        """
        self.root.mainloop()

    def toggle_contents_view(self, event=None):
        """Show/hide the contents viewer text box."""
        if self.middleFrame.winfo_manager():
            self.middleFrame.pack_forget()
            prefs['show_contents'] = False
        else:
            self.middleFrame.pack(
                after=self.leftFrame,
                side='left',
                expand=False,
                fill='both',
            )
            prefs['show_contents'] = True
        return 'break'

    def toggle_properties_view(self, event=None):
        """Show/hide the element properties frame."""
        if self.rightFrame.winfo_manager():
            self.propertiesView.apply_changes()
            self.rightFrame.pack_forget()
            prefs['show_properties'] = False
        elif not self._propWinDetached:
            self.rightFrame.pack(side='left', expand=False, fill='both')
            prefs['show_properties'] = True
        return 'break'

    def toggle_properties_window(self, event=None):
        """Detach/dock the element properties frame."""
        if self._propWinDetached:
            self._dock_properties_frame()
        else:
            self._detach_properties_frame()
        self.root.event_generate('<<RebuildPropertiesView>>')
        # this is for plugins that modify the properties view
        return 'break'

    def unlock(self):
        """Make the "unlocked" state take effect.
        
        Overrides the SubController method.
        """
        self.pathBar.set_normal()
        self.fileMenu.entryconfig(_('Unlock'), state='disabled')
        self.fileMenu.entryconfig(_('Lock'), state='normal')
        for entry in self._mainMenuDisableOnLock:
            self.mainMenu.entryconfig(entry, state='normal')
        for entry in self._fileMenuDisableOnLock:
            self.fileMenu.entryconfig(entry, state='normal')
        for entry in self._sectionMenuDisableOnLock:
            self.sectionMenu.entryconfig(entry, state='normal')
        for entry in self._characterMenuDisableOnLock:
            self.characterMenu.entryconfig(entry, state='normal')
        for entry in self._locationMenuDisableOnLock:
            self.locationMenu.entryconfig(entry, state='normal')
        for entry in self._itemMenuDisableOnLock:
            self.itemMenu.entryconfig(entry, state='normal')
        for entry in self._plotMenuDisableOnLock:
            self.plotMenu.entryconfig(entry, state='normal')
        for entry in self._prjNoteMenuDisableOnLock:
            self.prjNoteMenu.entryconfig(entry, state='normal')
        for entry in self._exportMenuDisableOnLock:
            self.exportMenu.entryconfig(entry, state='normal')

    def update_status(self, statusText=''):
        """Update the project status information on the status bar.
        
        Optional arguments:
            statusText: str -- Text to be displayed on the status bar.
        """
        self.statusBar.update_status(statusText)

    def _about(self):
        # Display a legal notice window.
        # After building the program, __doc__ will be the novelibre docstring.
        self.show_info(
            message=f'novelibre {self._ctrl.plugins.majorVersion}',
            detail=__doc__,
            title=_('About novelibre'),
        )

    def _create_menu(self):

        # "New" submenu
        self.newMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.newMenu.add_command(
            label=_('Empty project'),
            command=self._ctrl.create_project,
        )
        self.newMenu.add_command(
            label=_('Create from ODT...'),
            command=self._ctrl.import_odf,
        )

        # Files
        self.fileMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('File'),
            menu=self.fileMenu,
        )
        self.fileMenu.add_cascade(
            label=_('New'), menu=self.newMenu)
        self.fileMenu.add_command(
            label=_('Open...'),
            accelerator=KEYS.OPEN_PROJECT[1],
            command=self._ctrl.open_project,
        )
        self.fileMenu.add_command(
            label=_('Reload'),
            accelerator=KEYS.RELOAD_PROJECT[1],
            command=self._ctrl.reload_project,
        )
        self.fileMenu.add_command(
            label=_('Restore backup'),
            accelerator=KEYS.RESTORE_BACKUP[1],
            command=self._ctrl.restore_backup,
        )
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
            label=_('Refresh Tree'),
            accelerator=KEYS.REFRESH_TREE[1],
            command=self._ctrl.refresh_tree,
        )
        self.fileMenu.add_command(
            label=_('Lock'),
            accelerator=KEYS.LOCK_PROJECT[1],
            command=self._ctrl.lock,
        )
        self.fileMenu.add_command(
            label=_('Unlock'),
            accelerator=KEYS.UNLOCK_PROJECT[1],
            command=self._ctrl.unlock,
        )
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
            label=_('Open Project folder'),
            accelerator=KEYS.FOLDER[1],
            command=self._ctrl.open_project_folder,
        )
        self.fileMenu.add_command(
            label=_('Copy style sheet'),
            command=self._ctrl.copy_css,
        )
        self.fileMenu.add_command(
            label=_('Discard manuscript'),
            command=self._ctrl.discard_manuscript,
        )
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
            label=_('Save'),
            accelerator=KEYS.SAVE_PROJECT[1],
            command=self._ctrl.save_project,
        )
        self.fileMenu.add_command(
            label=_('Save as...'),
            accelerator=KEYS.SAVE_AS[1],
            command=self._ctrl.save_as,
        )
        self.fileMenu.add_command(
            label=_('Close'),
            command=self._ctrl.close_project,
        )
        if PLATFORM == 'win':
            self.fileMenu.add_command(
                label=_('Exit'),
                accelerator=KEYS.QUIT_PROGRAM[1],
                command=self._ctrl.on_quit,
            )
        else:
            self.fileMenu.add_command(
                label=_('Quit'),
                accelerator=KEYS.QUIT_PROGRAM[1],
                command=self._ctrl.on_quit,
            )

        self._fileMenuDisableOnClose = [
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
        self._fileMenuDisableOnLock = [
            _('Reload'),
            _('Refresh Tree'),
            _('Save'),
        ]

        # View
        self.viewMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('View'), menu=self.viewMenu)
        self.viewMenu.add_command(
            label=_('Chapter level'),
            accelerator=KEYS.CHAPTER_LEVEL[1],
            command=self.tv.show_chapter_level,
        )
        self.viewMenu.add_command(
            label=_('Expand selected'),
            command=self.tv.expand_selected,
        )
        self.viewMenu.add_command(
            label=_('Collapse selected'),
            command=self.tv.collapse_selected,
        )
        self.viewMenu.add_command(
            label=_('Expand all'),
            command=self.tv.expand_all,
        )
        self.viewMenu.add_command(
            label=_('Collapse all'),
            command=self.tv.collapse_all,
        )
        self.viewMenu.add_separator()
        self.viewMenu.add_command(
            label=_('Show Book'),
            command=self.tv.show_book,
        )
        self.viewMenu.add_command(
            label=_('Show Characters'),
            command=self.tv.show_characters,
        )
        self.viewMenu.add_command(
            label=_('Show Locations'),
            command=self.tv.show_locations,
        )
        self.viewMenu.add_command(
            label=_('Show Items'),
            command=self.tv.show_items,
        )
        self.viewMenu.add_command(
            label=_('Show Plot lines'),
            command=self.tv.show_plot_lines,
        )
        self.viewMenu.add_command(
            label=_('Show Project notes'),
            command=self.tv.show_project_notes,
        )
        self.viewMenu.add_separator()
        self.viewMenu.add_command(
            label=_('Toggle Text viewer'),
            accelerator=KEYS.TOGGLE_VIEWER[1],
            command=self.toggle_contents_view,
        )
        self.viewMenu.add_command(
            label=_('Toggle Properties'),
            accelerator=KEYS.TOGGLE_PROPERTIES[1],
            command=self.toggle_properties_view,
        )
        self.viewMenu.add_command(
            label=_('Detach/Dock Properties'),
            accelerator=KEYS.DETACH_PROPERTIES[1],
            command=self.toggle_properties_window,
        )
        self.viewMenu.add_separator()
        self.viewMenu.add_command(
            label=_('Options'),
            command=self._ctrl.open_view_options,
        )

        self._viewMenuDisableOnClose = [
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

        # Part
        self.partMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Part'),
            menu=self.partMenu,
        )
        self.partMenu.add_command(
            label=_('Add'),
            command=self._ctrl.add_new_part,
        )
        self.partMenu.add_separator()
        self.partMenu.add_command(
            label=_('Export part descriptions for editing'),
            command=self._ctrl.export_part_desc,
        )
        self.partMenu.add_command(
            label=_('Export part list (spreadsheet)'),
            command=self._ctrl.export_part_list,
        )

        # Chapter
        self.chapterMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Chapter'),
            menu=self.chapterMenu,
        )
        self.chapterMenu.add_command(
            label=_('Add'),
            command=self._ctrl.add_new_chapter,
        )
        self.chapterMenu.add_separator()
        self.chapterMenu.add_cascade(
            label=_('Set Type'),
            menu=self.tv.selectTypeMenu,
        )
        self.chapterMenu.add_cascade(
            label=_('Change Level'),
            menu=self.tv.selectLevelMenu,
        )
        self.chapterMenu.add_separator()
        self.chapterMenu.add_command(
            label=_('Move selected chapters to new project'),
            command=self._ctrl.split_file,
        )
        self.chapterMenu.add_separator()
        self.chapterMenu.add_command(
            label=_('Export chapter descriptions for editing'),
            command=self._ctrl.export_chapter_desc,
        )
        self.chapterMenu.add_command(
            label=_('Export chapter list (spreadsheet)'),
            command=self._ctrl.export_chapter_list,
        )

        # Section
        self.sectionMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Section'),
            menu=self.sectionMenu,
        )
        self.sectionMenu.add_command(
            label=_('Add'),
            command=self._ctrl.add_new_section,
        )
        self.sectionMenu.add_command(
            label=_('Add multiple sections'),
            command=self._ctrl.add_multiple_new_sections,
        )
        self.sectionMenu.add_separator()
        self.sectionMenu.add_cascade(
            label=_('Set Type'),
            menu=self.tv.selectTypeMenu,
        )
        self.sectionMenu.add_cascade(
            label=_('Set Status'),
            menu=self.tv.scStatusMenu,
        )
        self.sectionMenu.add_command(
            label=_('Set Viewpoint...'),
            command=self._ctrl.set_viewpoint,
        )
        self.sectionMenu.add_separator()
        self.sectionMenu.add_command(
            label=_('Export section descriptions for editing'),
            command=self._ctrl.export_section_desc,
        )
        self.sectionMenu.add_separator()
        self.sectionMenu.add_command(
            label=_('Section list (export only)'),
            command=self._ctrl.export_section_list,
        )
        self.sectionMenu.add_command(
            label=_('Show Time table'),
            command=self._ctrl.show_timetable,
        )

        self._sectionMenuDisableOnLock = [
            _('Add'),
            _('Add multiple sections'),
            _('Set Type'),
            _('Set Status'),
            _('Set Viewpoint...'),
            _('Export section descriptions for editing'),
        ]
        # Character
        self.characterMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Characters'),
            menu=self.characterMenu,
        )
        self.characterMenu.add_command(
            label=_('Add'),
            command=self._ctrl.add_new_character,
        )
        self.characterMenu.add_separator()
        self.characterMenu.add_cascade(
            label=_('Set Status'),
            menu=self.tv.crStatusMenu,
        )
        self.characterMenu.add_separator()
        self.characterMenu.add_command(
            label=_('Import'),
            command=self._ctrl.import_character_data,
        )
        self.characterMenu.add_separator()
        self.characterMenu.add_command(
            label=_('Export character descriptions for editing'),
            command=self._ctrl.export_character_desc,
        )
        self.characterMenu.add_command(
            label=_('Export character list (spreadsheet)'),
            command=self._ctrl.export_character_list,
        )
        self.characterMenu.add_separator()
        self.characterMenu.add_command(
            label=_('Show list'),
            command=self._ctrl.show_character_list,
        )

        self._characterMenuDisableOnLock = [
            _('Add'),
            _('Set Status'),
            _('Import'),
            _('Export character descriptions for editing'),
            _('Export character list (spreadsheet)'),
        ]

        # Location
        self.locationMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Locations'),
            menu=self.locationMenu,
        )
        self.locationMenu.add_command(
            label=_('Add'),
            command=self._ctrl.add_new_location,
        )
        self.locationMenu.add_separator()
        self.locationMenu.add_command(
            label=_('Import'),
            command=self._ctrl.import_location_data,
        )
        self.locationMenu.add_separator()
        self.locationMenu.add_command(
            label=_('Export location descriptions for editing'),
            command=self._ctrl.export_location_desc,
        )
        self.locationMenu.add_command(
            label=_('Export location list (spreadsheet)'),
            command=self._ctrl.export_location_list,
        )
        self.locationMenu.add_separator()
        self.locationMenu.add_command(
            label=_('Show list'),
            command=self._ctrl.show_location_list,
        )

        self._locationMenuDisableOnLock = [
            _('Add'),
            _('Import'),
            _('Export location descriptions for editing'),
            _('Export location list (spreadsheet)'),
        ]

        # "Item" menu.
        self.itemMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Items'),
            menu=self.itemMenu,
        )
        self.itemMenu.add_command(
            label=_('Add'),
            command=self._ctrl.add_new_item,
        )
        self.itemMenu.add_separator()
        self.itemMenu.add_command(
            label=_('Import'),
            command=self._ctrl.import_item_data,
        )
        self.itemMenu.add_separator()
        self.itemMenu.add_command(
            label=_('Export item descriptions for editing'),
            command=self._ctrl.export_item_desc,
        )
        self.itemMenu.add_command(
            label=_('Export item list (spreadsheet)'),
            command=self._ctrl.export_item_list,
        )
        self.itemMenu.add_separator()
        self.itemMenu.add_command(
            label=_('Show list'),
            command=self._ctrl.show_item_list,
        )

        self._itemMenuDisableOnLock = [
            _('Add'),
            _('Import'),
            _('Export item descriptions for editing'),
            _('Export item list (spreadsheet)'),
        ]

        # "Plot" menu.
        self.plotMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Plot'), menu=self.plotMenu)
        self.plotMenu.add_command(
            label=_('Add Plot line'),
            command=self._ctrl.add_new_plot_line,
        )
        self.plotMenu.add_command(
            label=_('Add Plot point'),
            command=self._ctrl.add_new_plot_point,
        )
        self.plotMenu.add_separator()
        self.plotMenu.add_command(
            label=_('Insert Stage'),
            command=self._ctrl.add_new_stage,
        )
        self.plotMenu.add_cascade(
            label=_('Change Level'),
            menu=self.tv.selectLevelMenu,
        )
        self.plotMenu.add_separator()
        self.plotMenu.add_command(
            label=_('Import plot lines'),
            command=self._ctrl.import_plot_lines,
        )
        self.plotMenu.add_separator()
        self.plotMenu.add_command(
            label=_('Export plot grid for editing'),
            command=self._ctrl.export_plot_grid,
        )
        self.plotMenu.add_command(
            label=_('Export story structure description for editing'),
            command=self._ctrl.export_story_structure_desc,
        )
        self.plotMenu.add_command(
            label=_('Export plot line descriptions for editing'),
            command=self._ctrl.export_plot_lines_desc,
        )
        self.plotMenu.add_separator()
        self.plotMenu.add_command(
            label=_('Plot list (export only)'),
            command=self._ctrl.export_plot_list,
        )
        self.plotMenu.add_command(
            label=_('Show Plot list'),
            command=self._ctrl.show_plot_list,
        )

        self._plotMenuDisableOnLock = [
            _('Add Plot line'),
            _('Add Plot point'),
            _('Insert Stage'),
            _('Change Level'),
            _('Import plot lines'),
            _('Export plot grid for editing'),
            _('Export story structure description for editing'),
            _('Export plot line descriptions for editing'),
        ]

        # Project notes
        self.prjNoteMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Project notes'),
            menu=self.prjNoteMenu,
        )
        self.prjNoteMenu.add_command(
            label=_('Add'),
            command=self._ctrl.add_new_project_note,
        )
        self.prjNoteMenu.add_separator()
        self.prjNoteMenu.add_command(
            label=_('Show list'),
            command=self._ctrl.show_projectnotes_list,
        )

        self._prjNoteMenuDisableOnLock = [
            _('Add'),
        ]

        # "Import" menu.
        self.mainMenu.add_command(
            label=_('Import'), command=self._ctrl.open_project_updater)

        # "Export" menu.
        self.exportMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Export'),
            menu=self.exportMenu,
        )
        self.exportMenu.add_command(
            label=_('Manuscript for editing'),
            command=self._ctrl.export_manuscript,
        )
        self.exportMenu.add_command(
            label=_('Manuscript for third-party word processing'),
            command=self._ctrl.export_proofing_manuscript,
        )
        self.exportMenu.add_separator()
        self.exportMenu.add_command(
            label=_('Final manuscript document (export only)'),
            command=self._ctrl.export_final_document,
        )
        self.exportMenu.add_command(
            label=_('Brief synopsis (export only)'),
            command=self._ctrl.export_brief_synopsis,
        )
        self.exportMenu.add_command(
            label=_('Cross references (export only)'),
            command=self._ctrl.export_cross_references,
        )
        self.exportMenu.add_separator()
        self.exportMenu.add_command(
            label=_('XML data files'),
            command=self._ctrl.export_xml_data_files,
        )
        self.exportMenu.add_separator()
        self.exportMenu.add_command(
            label=_('Options'),
            command=self._ctrl.open_export_options,
        )

        self._exportMenuDisableOnLock = [
            _('Manuscript for editing'),
            _('Manuscript for third-party word processing'),
            _('Final manuscript document (export only)'),
            _('Brief synopsis (export only)'),
            _('Cross references (export only)'),
            _('XML data files'),
        ]

        # "Tools" menu.
        self.toolsMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Tools'), menu=self.toolsMenu)
        self.toolsMenu.add_command(
            label=_('Backup options'),
            command=self._ctrl.open_backup_options,
        )
        self.toolsMenu.add_separator()
        self.toolsMenu.add_command(
            label=_('Open installation folder'),
            command=self._ctrl.open_installationFolder,
        )
        self.toolsMenu.add_separator()
        self.toolsMenu.add_command(
            label=_('Plugin Manager'),
            command=self._ctrl.open_plugin_manager,
        )
        self.toolsMenu.add_separator()
        self.toolsMenu.add_command(
            label=_('Show notes'),
            command=self._ctrl.show_notes_list,
        )
        self.toolsMenu.add_separator()

        # "Help" menu.
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(
            label=_('Help'),
            menu=self.helpMenu,
        )
        self.helpMenu.add_command(
            label=_('Online help'),
            accelerator=KEYS.OPEN_HELP[1],
            command=self._ctrl.open_help,
        )
        self.helpMenu.add_command(
            label=_('About novelibre'),
            command=self._about,
        )
        self.helpMenu.add_command(
            label=f"novelibre {_('Home page')}",
            command=self._ctrl.open_homepage,
        )
        self.helpMenu.add_separator()

        # Group main menu entries for enabling/disabling.
        self._mainMenuDisableOnClose = [
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
        self._mainMenuDisableOnLock = [
            _('Chapter'),
            _('Import'),
            _('Part'),
        ]

    def _create_path_bar(self):
        self.pathBar = PathBar(
            self.root,
            self._mdl,
            text='',
            anchor='w',
            padx=5,
            pady=3,
        )
        self.pathBar.pack(expand=False, fill='both')
        self._mdl.add_observer(self.pathBar)

        self.pathBar.COLOR_NORMAL_BG = self.mainMenu.cget('background')
        self.pathBar.COLOR_NORMAL_FG = self.mainMenu.cget('foreground')
        self.pathBar.COLOR_MODIFIED_BG = prefs['color_modified_bg']
        self.pathBar.COLOR_MODIFIED_FG = prefs['color_modified_fg']
        self.pathBar.COLOR_LOCKED_BG = prefs['color_locked_bg']
        self.pathBar.COLOR_LOCKED_FG = prefs['color_locked_fg']

    def _create_status_bar(self):
        self.statusBar = StatusBar(
            self.root,
            text='',
            anchor='w',
            padx=5,
            pady=2,
        )
        self.statusBar.pack(expand=False, fill='both')
        self.statusBar.bind(MOUSE.LEFT_CLICK, self.statusBar.restore_status)
        self.statusBar.COLOR_NORMAL_BG = self.mainMenu.cget('background')
        self.statusBar.COLOR_NORMAL_FG = self.mainMenu.cget('foreground')
        self.statusBar.COLOR_SUCCESS_BG = prefs['color_status_success_bg']
        self.statusBar.COLOR_SUCCESS_FG = prefs['color_status_success_fg']
        self.statusBar.COLOR_ERROR_BG = prefs['color_status_error_bg']
        self.statusBar.COLOR_ERROR_FG = prefs['color_status_error_fg']
        self.statusBar.COLOR_NOTIFICATION_BG = prefs['color_status_notification_bg']
        self.statusBar.COLOR_NOTIFICATION_FG = prefs['color_status_notification_fg']

    def _detach_properties_frame(self, event=None):
        # View the properties in its own window.
        self.propertiesView.apply_changes()
        if self._propWinDetached:
            return

        if self.rightFrame.winfo_manager():
            self.rightFrame.pack_forget()
        self._propertiesWindow = tk.Toplevel()
        self._propertiesWindow.geometry(prefs['prop_win_geometry'])
        set_icon(self._propertiesWindow, icon='pLogo32', default=False)

        # "Re-parent" the Properties viewer.
        self.propertiesView.pack_forget()
        self._mdl.delete_observer(self.propertiesView)
        self._ctrl.unregister_client(self.propertiesView)
        self.propertiesView = PropertiesViewer(
            self._propertiesWindow, self._mdl, self, self._ctrl)
        self._mdl.add_observer(self.propertiesView)
        self._ctrl.register_client(self.propertiesView)
        self.propertiesView.pack(expand=True, fill='both')

        self._propertiesWindow.bind(
            KEYS.DETACH_PROPERTIES[0], self._dock_properties_frame)
        self._propertiesWindow.protocol(
            "WM_DELETE_WINDOW", self._dock_properties_frame)
        prefs['detach_prop_win'] = True
        self._propWinDetached = True
        try:
            self.propertiesView.show_properties(self.tv.tree.selection()[0])
        except IndexError:
            pass
        return 'break'

    def _dock_properties_frame(self, event=None):
        # Dock the properties window at the right pane, if detached.
        self.propertiesView.apply_changes()
        if not self._propWinDetached:
            return

        if not self.rightFrame.winfo_manager():
            self.rightFrame.pack(side='left', expand=False, fill='both')

        prefs['prop_win_geometry'] = self._propertiesWindow.winfo_geometry()

        # "Re-parent" the Properties viewer.
        self._propertiesWindow.destroy()
        self._mdl.delete_observer(self.propertiesView)
        self._ctrl.unregister_client(self.propertiesView)
        self.propertiesView = PropertiesViewer(
            self.rightFrame,
            self._mdl,
            self,
            self._ctrl,
        )
        self._mdl.add_observer(self.propertiesView)
        self._ctrl.register_client(self.propertiesView)
        self.propertiesView.pack(expand=True, fill='both')
        self.root.lift()

        prefs['show_properties'] = True
        prefs['detach_prop_win'] = False
        self._propWinDetached = False
        try:
            self.propertiesView.show_properties(self.tv.tree.selection()[0])
        except IndexError:
            pass
        return 'break'


"""Provide a tkinter based GUI for novelibre.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.view.path_bar import PathBar
from mvclib.view.set_icon_tk import set_icon
from mvclib.view.view_base import ViewBase
from nvlib.controller.main_view.main_view_ctrl import MainViewCtrl
from nvlib.novx_globals import BRF_SYNOPSIS_SUFFIX
from nvlib.novx_globals import CHAPTERS_SUFFIX
from nvlib.novx_globals import CHARACTERS_SUFFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CHARACTER_REPORT_SUFFIX
from nvlib.novx_globals import CHARLIST_SUFFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import DATA_SUFFIX
from nvlib.novx_globals import ITEMLIST_SUFFIX
from nvlib.novx_globals import ITEMS_SUFFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import ITEM_REPORT_SUFFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATIONS_SUFFIX
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import LOCATION_REPORT_SUFFIX
from nvlib.novx_globals import LOCLIST_SUFFIX
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.novx_globals import PARTS_SUFFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import PN_ROOT
from nvlib.novx_globals import PROOF_SUFFIX
from nvlib.novx_globals import SECTIONLIST_SUFFIX
from nvlib.novx_globals import SECTIONS_SUFFIX
from nvlib.novx_globals import XREF_SUFFIX
from nvlib.novx_globals import _
from nvlib.nv_globals import prefs
from nvlib.view.contents_window.contents_viewer import ContentsViewer
from nvlib.view.icons import Icons
from nvlib.view.platform.platform_settings import KEYS
from nvlib.view.platform.platform_settings import MOUSE
from nvlib.view.platform.platform_settings import PLATFORM
from nvlib.view.properties_window.properties_viewer import PropertiesViewer
from nvlib.view.toolbar.toolbar import Toolbar
from nvlib.view.tree_window.tree_viewer import TreeViewer
import tkinter as tk


class MainView(ViewBase, MainViewCtrl):
    """View for the novelibre application."""
    _MIN_WINDOW_WIDTH = 400
    _MIN_WINDOW_HEIGHT = 200
    # minimum size of the application's main window

    def __init__(self, model, controller, title):
        """Extends the superclass constructor."""
        super().__init__(model, controller, title)
        self.initialize_controller(model, self, controller)

        #--- Create the tk root window and set the size.
        if prefs.get('root_geometry', None):
            self.root.geometry(prefs['root_geometry'])
        set_icon(self.root, icon='nLogo32')
        self.root.minsize(self._MIN_WINDOW_WIDTH, self._MIN_WINDOW_HEIGHT)

        #--- Create the path bar below the status bar.
        self._create_path_bar()

        #--- Initalize icons.
        self.icons = Icons()

        #--- Build the GUI frames.

        #--- Create an application window with three frames.
        self.appWindow = ttk.Frame(self.mainWindow)
        self.appWindow.pack(expand=True, fill='both')

        #--- left frame (intended for the tree).
        self.leftFrame = ttk.Frame(self.appWindow)
        self.leftFrame.pack(side='left', expand=True, fill='both')

        #--- Create a novel tree window in the left frame.
        self.tv = TreeViewer(self.leftFrame, self._mdl, self, self._ctrl)
        self._mdl.add_observer(self.tv)
        self._ctrl.register_client(self.tv)
        self.tv.pack(expand=True, fill='both')
        self._selection = None

        #--- Middle frame (intended for the content viewer).
        self.middleFrame = ttk.Frame(self.appWindow, width=prefs['middle_frame_width'])
        self.middleFrame.pack_propagate(0)

        #--- Create a text viewer in the middle frame.
        self.contentsView = ContentsViewer(self.middleFrame, self._mdl, self, self._ctrl)
        self._mdl.add_observer(self.contentsView)
        self._ctrl.register_client(self.contentsView)
        if prefs['show_contents']:
            self.middleFrame.pack(side='left', expand=False, fill='both')

        #--- Right frame for for the element properties view.
        self.rightFrame = ttk.Frame(self.appWindow, width=prefs['right_frame_width'])
        self.rightFrame.pack_propagate(0)
        if prefs['show_properties']:
            self.rightFrame.pack(expand=True, fill='both')

        #--- Create an element properties view in the right frame.
        self.propertiesView = PropertiesViewer(self.rightFrame, self._mdl, self, self._ctrl)
        self.propertiesView.pack(expand=True, fill='both')
        self._propWinDetached = False
        if prefs['detach_prop_win']:
            self.detach_properties_frame()
        self._mdl.add_observer(self.propertiesView)
        self._ctrl.register_client(self.propertiesView)

        #--- Add commands and submenus to the main menu.
        self._create_menu()

        #--- Add a toolbar.
        self.toolbar = Toolbar(self.mainWindow, self._mdl, self, self._ctrl)
        self._ctrl.register_client(self.toolbar)

        #--- tk root event bindings.
        self._bind_events()

    @property
    def selectedNode(self):
        return self._selection[0]

    @property
    def selectedNodes(self):
        return self._selection

    def detach_properties_frame(self, event=None):
        """View the properties in its own window."""
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
        self.propertiesView = PropertiesViewer(self._propertiesWindow, self._mdl, self, self._ctrl)
        self._mdl.add_observer(self.propertiesView)
        self._ctrl.register_client(self.propertiesView)
        self.propertiesView.pack(expand=True, fill='both')

        self._propertiesWindow.protocol("WM_DELETE_WINDOW", self.dock_properties_frame)
        prefs['detach_prop_win'] = True
        self._propWinDetached = True
        try:
            self.propertiesView.show_properties(self.tv.tree.selection()[0])
        except IndexError:
            pass
        return 'break'

    def dock_properties_frame(self, event=None):
        """Dock the properties window at the right pane, if detached."""
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
        self.propertiesView = PropertiesViewer(self.rightFrame, self._mdl, self, self._ctrl)
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

    def on_change_selection(self, nodeId):
        """Event handler for element selection.
        
        Show the properties/contents of the selected element.
        """
        self._selection = self.tv.tree.selection()
        self.propertiesView.show_properties(nodeId)
        self.contentsView.see(nodeId)

    def on_quit(self):
        """Gracefully close the user interface.
        
        Extends the superclass method.
        """

        # Save contents window "show markup" state.
        prefs['show_markup'] = self.contentsView.showMarkup.get()

        # Save windows size and position.
        if self._propWinDetached:
            prefs['prop_win_geometry'] = self._propertiesWindow.winfo_geometry()
        prefs['root_geometry'] = self.root.winfo_geometry()
        super().on_quit()

    def refresh(self):
        """Update view components and path bar.
        
        Overrides the superclass method.
        """
        self.set_title()

    def show_path(self, message):
        """Put text on the path bar."""
        self.pathBar.config(text=message)

    def toggle_contents_view(self, event=None):
        """Show/hide the contents viewer text box."""
        if self.middleFrame.winfo_manager():
            self.middleFrame.pack_forget()
            prefs['show_contents'] = False
        else:
            self.middleFrame.pack(after=self.leftFrame, side='left', expand=False, fill='both')
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
            self.dock_properties_frame()
        else:
            self.detach_properties_frame()
        return 'break'

    def _bind_events(self):
        self.root.bind(KEYS.RESTORE_STATUS[0], self.restore_status)
        self.root.bind(KEYS.OPEN_PROJECT[0], self._ctrl.open_project)

        self.root.bind(KEYS.LOCK_PROJECT[0], self._ctrl.lock)
        self.root.bind(KEYS.UNLOCK_PROJECT[0], self._ctrl.unlock)
        self.root.bind(KEYS.RELOAD_PROJECT[0], self._ctrl.reload_project)
        self.root.bind(KEYS.RESTORE_BACKUP[0], self._ctrl.restore_backup)
        self.root.bind(KEYS.FOLDER[0], self._ctrl.open_project_folder)
        self.root.bind(KEYS.REFRESH_TREE[0], self._ctrl.refresh_tree)
        self.root.bind(KEYS.SAVE_PROJECT[0], self._ctrl.save_project)
        self.root.bind(KEYS.SAVE_AS[0], self._ctrl.save_as)
        self.root.bind(KEYS.CHAPTER_LEVEL[0], self.tv.show_chapter_level)
        self.root.bind(KEYS.TOGGLE_VIEWER[0], self.toggle_contents_view)
        self.root.bind(KEYS.TOGGLE_PROPERTIES[0], self.toggle_properties_view)
        self.root.bind(KEYS.DETACH_PROPERTIES[0], self.toggle_properties_window)
        self.root.bind(KEYS.ADD_ELEMENT[0], self._ctrl.add_element)
        self.root.bind(KEYS.ADD_CHILD[0], self._ctrl.add_child)
        self.root.bind(KEYS.ADD_PARENT[0], self._ctrl.add_parent)
        if PLATFORM == 'win':
            self.root.bind(MOUSE.BACK_CLICK, self.tv.go_back)
            self.root.bind(MOUSE.FORWARD_CLICK, self.tv.go_forward)
        else:
            self.root.bind(KEYS.QUIT_PROGRAM[0], self._ctrl.on_quit)
        self.root.bind(KEYS.OPEN_HELP[0], self._ctrl.open_help)

    def _create_menu(self):
        """Add commands and submenus to the main menu."""

        # "New" submenu
        self.newMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.newMenu.add_command(label=_('Empty project'), command=self._ctrl.new_project)
        self.newMenu.add_command(label=_('Create from ODT...'), command=self._ctrl.import_odf)

        # Files
        self.fileMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('File'), menu=self.fileMenu)
        self.fileMenu.add_cascade(label=_('New'), menu=self.newMenu)
        self.fileMenu.add_command(label=_('Open...'), accelerator=KEYS.OPEN_PROJECT[1], command=self._ctrl.open_project)
        self.fileMenu.add_command(label=_('Reload'), accelerator=KEYS.RELOAD_PROJECT[1], command=self._ctrl.reload_project)
        self.fileMenu.add_command(label=_('Restore backup'), accelerator=KEYS.RESTORE_BACKUP[1], command=self._ctrl.restore_backup)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=_('Refresh Tree'), accelerator=KEYS.REFRESH_TREE[1], command=self._ctrl.refresh_tree)
        self.fileMenu.add_command(label=_('Lock'), accelerator=KEYS.LOCK_PROJECT[1], command=self._ctrl.lock)
        self.fileMenu.add_command(label=_('Unlock'), accelerator=KEYS.UNLOCK_PROJECT[1], command=self._ctrl.unlock)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=_('Open Project folder'), accelerator=KEYS.FOLDER[1], command=self._ctrl.open_project_folder)
        self.fileMenu.add_command(label=_('Copy style sheet'), command=self._ctrl.copy_css)
        self.fileMenu.add_command(label=_('Discard manuscript'), command=self._ctrl.discard_manuscript)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label=_('Save'), accelerator=KEYS.SAVE_PROJECT[1], command=self._ctrl.save_project)
        self.fileMenu.add_command(label=_('Save as...'), accelerator=KEYS.SAVE_AS[1], command=self._ctrl.save_as)
        self.fileMenu.add_command(label=_('Close'), command=self._ctrl.close_project)
        if PLATFORM == 'win':
            self.fileMenu.add_command(label=_('Exit'), accelerator=KEYS.QUIT_PROGRAM[1], command=self._ctrl.on_quit)
        else:
            self.fileMenu.add_command(label=_('Quit'), accelerator=KEYS.QUIT_PROGRAM[1], command=self._ctrl.on_quit)

        # View
        self.viewMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('View'), menu=self.viewMenu)
        self.viewMenu.add_command(label=_('Chapter level'), accelerator=KEYS.CHAPTER_LEVEL[1], command=self.tv.show_chapter_level)
        self.viewMenu.add_command(label=_('Expand selected'), command=lambda: self.tv.open_children(self.tv.tree.selection()[0]))
        self.viewMenu.add_command(label=_('Collapse selected'), command=lambda: self.tv.close_children(self.tv.tree.selection()[0]))
        self.viewMenu.add_command(label=_('Expand all'), command=lambda: self.tv.open_children(''))
        self.viewMenu.add_command(label=_('Collapse all'), command=lambda: self.tv.close_children(''))
        self.viewMenu.add_separator()
        self.viewMenu.add_command(label=_('Show Book'), command=lambda: self.tv.show_branch(CH_ROOT))
        self.viewMenu.add_command(label=_('Show Characters'), command=lambda: self.tv.show_branch(CR_ROOT))
        self.viewMenu.add_command(label=_('Show Locations'), command=lambda: self.tv.show_branch(LC_ROOT))
        self.viewMenu.add_command(label=_('Show Items'), command=lambda: self.tv.show_branch(IT_ROOT))
        self.viewMenu.add_command(label=_('Show Plot lines'), command=lambda: self.tv.show_branch(PL_ROOT))
        self.viewMenu.add_command(label=_('Show Project notes'), command=lambda: self.tv.show_branch(PN_ROOT))
        self.viewMenu.add_separator()
        self.viewMenu.add_command(label=_('Toggle Text viewer'), accelerator=KEYS.TOGGLE_VIEWER[1], command=self.toggle_contents_view)
        self.viewMenu.add_command(label=_('Toggle Properties'), accelerator=KEYS.TOGGLE_PROPERTIES[1], command=self.toggle_properties_view)
        self.viewMenu.add_command(label=_('Detach/Dock Properties'), accelerator=KEYS.DETACH_PROPERTIES[1], command=self.toggle_properties_window)
        self.viewMenu.add_separator()
        self.viewMenu.add_command(label=_('Options'), command=self._ctrl.open_view_options)

        # Part
        self.partMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Part'), menu=self.partMenu)
        self.partMenu.add_command(label=_('Add'), command=self._ctrl.add_part)
        self.partMenu.add_separator()
        self.partMenu.add_command(label=_('Export part descriptions for editing'), command=lambda: self._ctrl.export_document(PARTS_SUFFIX))

        # Chapter
        self.chapterMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Chapter'), menu=self.chapterMenu)
        self.chapterMenu.add_command(label=_('Add'), command=self._ctrl.add_chapter)
        self.chapterMenu.add_separator()
        self.chapterMenu.add_cascade(label=_('Set Type'), menu=self.tv.selectTypeMenu)
        self.chapterMenu.add_cascade(label=_('Change Level'), menu=self.tv.selectLevelMenu)
        self.chapterMenu.add_separator()
        self.chapterMenu.add_command(label=_('Export chapter descriptions for editing'), command=lambda: self._ctrl.export_document(CHAPTERS_SUFFIX))

        # Section
        self.sectionMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Section'), menu=self.sectionMenu)
        self.sectionMenu.add_command(label=_('Add'), command=self._ctrl.add_section)
        self.sectionMenu.add_command(label=_('Add multiple sections'), command=self._ctrl.add_multiple_sections)
        self.sectionMenu.add_separator()
        self.sectionMenu.add_cascade(label=_('Set Type'), menu=self.tv.selectTypeMenu)
        self.sectionMenu.add_cascade(label=_('Set Status'), menu=self.tv.scStatusMenu)
        self.sectionMenu.add_separator()
        self.sectionMenu.add_command(label=_('Export section descriptions for editing'), command=lambda: self._ctrl.export_document(SECTIONS_SUFFIX))
        self.sectionMenu.add_command(label=_('Section list (export only)'), command=lambda: self._ctrl.export_document(SECTIONLIST_SUFFIX))

        # Character
        self.characterMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Characters'), menu=self.characterMenu)
        self.characterMenu.add_command(label=_('Add'), command=self._ctrl.add_character)
        self.characterMenu.add_separator()
        self.characterMenu.add_cascade(label=_('Set Status'), menu=self.tv.crStatusMenu)
        self.characterMenu.add_separator()
        self.characterMenu.add_command(label=_('Import'), command=lambda: self._ctrl.import_elements(CHARACTER_PREFIX))
        self.characterMenu.add_separator()
        self.characterMenu.add_command(label=_('Export character descriptions for editing'), command=lambda: self._ctrl.export_document(CHARACTERS_SUFFIX))
        self.characterMenu.add_command(label=_('Export character list (spreadsheet)'), command=lambda: self._ctrl.export_document(CHARLIST_SUFFIX))
        self.characterMenu.add_command(label=_('Show list'), command=lambda: self._ctrl.show_report(CHARACTER_REPORT_SUFFIX))

        # Location
        self.locationMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Locations'), menu=self.locationMenu)
        self.locationMenu.add_command(label=_('Add'), command=self._ctrl.add_location)
        self.locationMenu.add_separator()
        self.locationMenu.add_command(label=_('Import'), command=lambda: self._ctrl.import_elements(LOCATION_PREFIX))
        self.locationMenu.add_separator()
        self.locationMenu.add_command(label=_('Export location descriptions for editing'), command=lambda: self._ctrl.export_document(LOCATIONS_SUFFIX))
        self.locationMenu.add_command(label=_('Export location list (spreadsheet)'), command=lambda: self._ctrl.export_document(LOCLIST_SUFFIX))
        self.locationMenu.add_command(label=_('Show list'), command=lambda: self._ctrl.show_report(LOCATION_REPORT_SUFFIX))

        # "Item" menu.
        self.itemMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Items'), menu=self.itemMenu)
        self.itemMenu.add_command(label=_('Add'), command=self._ctrl.add_item)
        self.itemMenu.add_separator()
        self.itemMenu.add_command(label=_('Import'), command=lambda: self._ctrl.import_elements(ITEM_PREFIX))
        self.itemMenu.add_separator()
        self.itemMenu.add_command(label=_('Export item descriptions for editing'), command=lambda: self._ctrl.export_document(ITEMS_SUFFIX))
        self.itemMenu.add_command(label=_('Export item list (spreadsheet)'), command=lambda: self._ctrl.export_document(ITEMLIST_SUFFIX))
        self.itemMenu.add_command(label=_('Show list'), command=lambda: self._ctrl.show_report(ITEM_REPORT_SUFFIX))

        # "Plot" menu.
        self.plotMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Plot'), menu=self.plotMenu)
        self.plotMenu.add_command(label=_('Add Plot line'), command=self._ctrl.add_plot_line)
        self.plotMenu.add_command(label=_('Add Plot point'), command=self._ctrl.add_plot_point)
        self.plotMenu.add_separator()
        self.plotMenu.add_command(label=_('Insert Stage'), command=self._ctrl.add_stage)
        self.plotMenu.add_cascade(label=_('Change Level'), menu=self.tv.selectLevelMenu)
        self.plotMenu.add_separator()
        self.plotMenu.add_command(label=_('Import plot lines'), command=self._ctrl.import_plot_lines)
        self.plotMenu.add_separator()
        self.plotMenu.add_command(label=_('Export plot grid for editing'), command=self._ctrl.export_plot_grid)
        self.plotMenu.add_command(label=_('Export story structure description for editing'), command=self._ctrl.export_story_structure_desc)
        self.plotMenu.add_command(label=_('Export plot line descriptions for editing'), command=self._ctrl.export_plot_lines_desc)
        self.plotMenu.add_separator()
        self.plotMenu.add_command(label=_('Export plot list (spreadsheet)'), command=self._ctrl.export_plot_list)
        self.plotMenu.add_command(label=_('Show Plot list'), command=self._ctrl.show_plot_list)

        # Project notes
        self.prjNoteMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Project notes'), menu=self.prjNoteMenu)
        self.prjNoteMenu.add_command(label=_('Add'), command=self._ctrl.add_project_note)
        self.prjNoteMenu.add_separator()
        self.prjNoteMenu.add_command(label=_('Show list'), command=lambda: self._ctrl.show_report('_projectnote_report'))

        # "Export" menu.
        self.exportMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Export'), menu=self.exportMenu)
        self.exportMenu.add_command(label=_('Manuscript for editing'), command=lambda:self._ctrl.export_document(MANUSCRIPT_SUFFIX))
        self.exportMenu.add_command(label=_('Manuscript for third-party word processing'), command=lambda: self._ctrl.export_document(PROOF_SUFFIX))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Manuscript for printing (export only)'), command=lambda: self._ctrl.export_document('', lock=False))
        self.exportMenu.add_command(label=_('Brief synopsis (export only)'), command=lambda: self._ctrl.export_document(BRF_SYNOPSIS_SUFFIX, lock=False))
        self.exportMenu.add_command(label=_('Cross references (export only)'), command=lambda: self._ctrl.export_document(XREF_SUFFIX, lock=False))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('XML data files'), command=lambda: self._ctrl.export_document(DATA_SUFFIX, lock=False, show=False))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Options'), command=self._ctrl.open_export_options)

        # "Update" menu.
        self.mainMenu.add_command(label=_('Import'), command=self._ctrl.open_project_updater)

        # "Tools" menu.
        self.toolsMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Tools'), menu=self.toolsMenu)
        self.toolsMenu.add_command(label=_('Plugin Manager'), command=self._ctrl.open_plugin_manager)
        self.toolsMenu.add_command(label=_('Open installation folder'), command=self._ctrl.open_installationFolder)
        self.toolsMenu.add_separator()

        # "Help" menu.
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), accelerator=KEYS.OPEN_HELP[1], command=self._ctrl.open_help)
        self.helpMenu.add_command(label=f"novelibre {_('Home page')}", command=self._ctrl.open_homepage)

    def _create_path_bar(self):
        """Extends the superclass method."""
        self.pathBar = PathBar(self.root, self._mdl, text='', anchor='w', padx=5, pady=3)
        self.pathBar.pack(expand=False, fill='both')
        self._mdl.add_observer(self.pathBar)

        self.pathBar.COLOR_NORMAL_BG = self.mainMenu.cget('background')
        self.pathBar.COLOR_NORMAL_FG = self.mainMenu.cget('foreground')
        self.pathBar.COLOR_MODIFIED_BG = prefs['color_modified_bg']
        self.pathBar.COLOR_MODIFIED_FG = prefs['color_modified_fg']
        self.pathBar.COLOR_LOCKED_BG = prefs['color_locked_bg']
        self.pathBar.COLOR_LOCKED_FG = prefs['color_locked_fg']

    def _create_status_bar(self):
        """Extends the superclass method."""
        super()._create_status_bar()
        self.statusBar.bind(MOUSE.LEFT_CLICK, self.statusBar.restore_status)
        self.statusBar.COLOR_NORMAL_BG = self.mainMenu.cget('background')
        self.statusBar.COLOR_NORMAL_FG = self.mainMenu.cget('foreground')
        self.statusBar.COLOR_SUCCESS_BG = prefs['color_status_success_bg']
        self.statusBar.COLOR_SUCCESS_FG = prefs['color_status_success_fg']
        self.statusBar.COLOR_ERROR_BG = prefs['color_status_error_bg']
        self.statusBar.COLOR_ERROR_FG = prefs['color_status_error_fg']
        self.statusBar.COLOR_NOTIFICATION_BG = prefs['color_status_notification_bg']
        self.statusBar.COLOR_NOTIFICATION_FG = prefs['color_status_notification_fg']

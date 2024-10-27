"""Provide a tkinter based GUI for novelibre.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import messagebox
from tkinter import ttk
import webbrowser

from novxlib.novx_globals import BRF_SYNOPSIS_SUFFIX
from novxlib.novx_globals import CHAPTERS_SUFFIX
from novxlib.novx_globals import CHARACTERS_SUFFIX
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import CHARACTER_REPORT_SUFFIX
from novxlib.novx_globals import CHARLIST_SUFFIX
from novxlib.novx_globals import CH_ROOT
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import DATA_SUFFIX
from novxlib.novx_globals import GRID_SUFFIX
from novxlib.novx_globals import ITEMLIST_SUFFIX
from novxlib.novx_globals import ITEMS_SUFFIX
from novxlib.novx_globals import ITEM_PREFIX
from novxlib.novx_globals import ITEM_REPORT_SUFFIX
from novxlib.novx_globals import IT_ROOT
from novxlib.novx_globals import LC_ROOT
from novxlib.novx_globals import LOCATIONS_SUFFIX
from novxlib.novx_globals import LOCATION_PREFIX
from novxlib.novx_globals import LOCATION_REPORT_SUFFIX
from novxlib.novx_globals import LOCLIST_SUFFIX
from novxlib.novx_globals import MANUSCRIPT_SUFFIX
from novxlib.novx_globals import PARTS_SUFFIX
from novxlib.novx_globals import PLOTLINES_SUFFIX
from novxlib.novx_globals import PLOTLIST_SUFFIX
from novxlib.novx_globals import PL_ROOT
from novxlib.novx_globals import PN_ROOT
from novxlib.novx_globals import PROOF_SUFFIX
from novxlib.novx_globals import SECTIONLIST_SUFFIX
from novxlib.novx_globals import SECTIONS_SUFFIX
from novxlib.novx_globals import STAGES_SUFFIX
from novxlib.novx_globals import XREF_SUFFIX
from novxlib.novx_globals import _
from novxlib.ui.set_icon_tk import set_icon
from nvlib.nv_globals import HOME_URL
from nvlib.nv_globals import open_help
from nvlib.nv_globals import prefs
from nvlib.view.contents_window.contents_viewer import ContentsViewer
from nvlib.view.icons import Icons
from nvlib.view.platform.platform_settings import KEYS
from nvlib.view.platform.platform_settings import MOUSE
from nvlib.view.platform.platform_settings import PLATFORM
from nvlib.view.pop_up.export_options_window import ExportOptionsWindow
from nvlib.view.pop_up.prj_updater import PrjUpdater
from nvlib.view.pop_up.view_options_window import ViewOptionsWindow
from nvlib.view.properties_window.properties_viewer import PropertiesViewer
from nvlib.view.toolbar.toolbar import Toolbar
from nvlib.view.tree_window.tree_viewer import TreeViewer
from nvlib.widgets.nv_simpledialog import askinteger
import tkinter as tk
from nvlib.view.pop_up.plugin_manager import PluginManager


class NvView:
    """View for the novelibre application."""
    _MIN_WINDOW_WIDTH = 400
    _MIN_WINDOW_HEIGHT = 200
    # minimum size of the application's main window

    _MAX_NR_NEW_SECTIONS = 20
    # maximum number of sections to add in bulk
    _INI_NR_NEW_SECTIONS = 1
    # initial value when asking for the number of sections to add

    def __init__(self, model, controller, title):
        """Set up the application's user interface."""
        self._mdl = model
        self._ctrl = controller
        self._mdl.register_client(self)
        self._viewComponents = []
        # list of composed view objects

        #--- Create the tk root window and set the size.
        self.title = title
        self._statusText = ''
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self._ctrl.on_quit)
        self.root.title(title)
        if prefs.get('root_geometry', None):
            self.root.geometry(prefs['root_geometry'])
        set_icon(self.root, icon='nLogo32')
        self.root.minsize(self._MIN_WINDOW_WIDTH, self._MIN_WINDOW_HEIGHT)

        #---  Add en empty main menu to the root window.
        self.mainMenu = tk.Menu(self.root)
        self.root.config(menu=self.mainMenu)

        #--- Create the main window.
        self.mainWindow = tk.Frame()
        self.mainWindow.pack(expand=True, fill='both')

        #--- Create the status bar.
        self.statusBar = tk.Label(self.root, text='', anchor='w', padx=5, pady=2)
        self.statusBar.pack(expand=False, fill='both')
        self.statusBar.bind(MOUSE.LEFT_CLICK, self.restore_status)
        self.infoWhatText = ''
        self.infoHowText = ''

        #--- Create the path bar.
        self.pathBar = tk.Label(self.root, text='', anchor='w', padx=5, pady=3)
        self.pathBar.pack(expand=False, fill='both')

        #--- Initialize GUI theme.
        self.guiStyle = ttk.Style()

        #--- Initalize icons.
        self.icons = Icons()

        #--- Build the GUI frames.

        # Create an application window with three frames.
        self.appWindow = ttk.Frame(self.mainWindow)
        self.appWindow.pack(expand=True, fill='both')

        #--- left frame (intended for the tree).
        self.leftFrame = ttk.Frame(self.appWindow)
        self.leftFrame.pack(side='left', expand=True, fill='both')

        #--- Create a novel tree window in the left frame.
        self.tv = TreeViewer(self.leftFrame, self._mdl, self, self._ctrl, prefs)
        self.register_view(self.tv)
        self.tv.pack(expand=True, fill='both')

        #--- Middle frame (intended for the content viewer).
        self.middleFrame = ttk.Frame(self.appWindow, width=prefs['middle_frame_width'])
        self.middleFrame.pack_propagate(0)

        #--- Create a text viewer in the middle frame.
        self.contentsView = ContentsViewer(self.middleFrame, self._mdl, self, self._ctrl)
        self.register_view(self.contentsView)
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
        self.register_view(self.propertiesView)

        #--- Add commands and submenus to the main menu.
        self._build_menu()

        #--- Add a toolbar.
        self.toolbar = Toolbar(self.mainWindow, self._mdl, self, self._ctrl)
        self.register_view(self.toolbar)

        #--- tk root event bindings.
        self._bind_events()

    def ask_yes_no(self, text, title=None):
        """Query yes or no with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askyesno(title, text)

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
        self.unregister_view(self.propertiesView)
        self.propertiesView = PropertiesViewer(self._propertiesWindow, self._mdl, self, self._ctrl)
        self.register_view(self.propertiesView)
        self.propertiesView.pack(expand=True, fill='both')

        self._propertiesWindow.protocol("WM_DELETE_WINDOW", self.dock_properties_frame)
        prefs['detach_prop_win'] = True
        self._propWinDetached = True
        try:
            self.propertiesView.show_properties(self.tv.tree.selection()[0])
        except IndexError:
            pass
        return 'break'

    def disable_menu(self):
        """Disable menu entries when no project is open."""
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
        for viewComponent in self._viewComponents:
            viewComponent.disable_menu()

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
        self.unregister_view(self.propertiesView)
        self.propertiesView = PropertiesViewer(self.rightFrame, self._mdl, self, self._ctrl)
        self.register_view(self.propertiesView)
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

    def enable_menu(self):
        """Enable menu entries when a project is open."""
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
        for viewComponent in self._viewComponents:
            viewComponent.enable_menu()

    def lock(self):
        """Make the "locked" state visible."""
        self.pathBar.config(bg=prefs['color_locked_bg'])
        self.pathBar.config(fg=prefs['color_locked_fg'])
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
        for viewComponent in self._viewComponents:
            viewComponent.lock()

    def on_change_selection(self, nodeId):
        """Event handler for element selection.
        
        Show the properties of the selected element.
        """
        self.propertiesView.show_properties(nodeId)
        self.contentsView.see(nodeId)

    def on_quit(self):
        """Gracefully close the user interface."""

        # Save contents window "show markup" state.
        prefs['show_markup'] = self.contentsView.showMarkup.get()

        # Save windows size and position.
        if self._propWinDetached:
            prefs['prop_win_geometry'] = self._propertiesWindow.winfo_geometry()
        self.tv.on_quit()
        prefs['root_geometry'] = self.root.winfo_geometry()
        self.root.quit()

    def refresh(self):
        """Set the path bar colors and refresh the composed objects."""
        if self._mdl.isModified:
            self.pathBar.config(bg=prefs['color_modified_bg'])
            self.pathBar.config(fg=prefs['color_modified_fg'])
        else:
            self.pathBar.config(bg=self.root.cget('background'))
            self.pathBar.config(fg='black')
        for viewComponent in self._viewComponents:
            viewComponent.refresh()
        self.set_title()

    def register_view(self, viewComponent):
        """Add a view object to the composite list."""
        if not viewComponent in self._viewComponents:
            self._viewComponents.append(viewComponent)

    def restore_status(self, event=None):
        """Overwrite error message with the status before."""
        self.show_status(self._statusText)

    def set_info(self, message):
        """This is a stub, just for compatibility with several converters."""
        pass

    def set_status(self, message, colors=None):
        """SDisplay a message at the status bar.
        
        Positional arguments:
            message -- message to be displayed. 
            
        Optional arguments:
            colors: tuple -- (background color, foreground color).

        Default status bar color is red if the message starts with "!", 
        yellow, if the message starts with "#", otherwise green.
        """
        if message is not None:
            try:
                self.statusBar.config(bg=colors[0])
                self.statusBar.config(fg=colors[1])
                self.infoHowText = message
            except:
                if message.startswith('!'):
                    # error
                    self.statusBar.config(bg=prefs['color_status_error_bg'])
                    self.statusBar.config(fg=prefs['color_status_error_fg'])
                    self.infoHowText = message.lstrip('!').strip()
                elif message.startswith('#'):
                    # notification/warning
                    self.statusBar.config(bg=prefs['color_status_notification_bg'])
                    self.statusBar.config(fg=prefs['color_status_notification_fg'])
                    self.infoHowText = message.lstrip('#').strip()
                else:
                    # success
                    self.statusBar.config(bg=prefs['color_status_success_bg'])
                    self.statusBar.config(fg=prefs['color_status_success_fg'])
                    self.infoHowText = message
            self.statusBar.config(text=self.infoHowText)

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

    def show_error(self, message, title=None):
        """Display an error message box.
        
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showerror(title, message)

    def show_info(self, message, title=None):
        """Display an informational message box.
        
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showinfo(title, message)

    def show_warning(self, message, title=None):
        """Display a warning message box.
        
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showwarning(title, message)

    def show_path(self, message):
        """Put text on the path bar."""
        self.pathBar.config(text=message)

    def show_status(self, message=''):
        """Display project statistics at the status bar.
        
        Optional arguments:
            message: str -- Message to be displayed instead of the statistics.
        """
        self._statusText = message
        self.statusBar.config(bg=self.root.cget('background'))
        self.statusBar.config(fg='black')
        self.statusBar.config(text=message)

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

    def unlock(self):
        """Make the "unlocked" state visible."""
        self.pathBar.config(bg=self.root.cget('background'))
        self.pathBar.config(fg='black')
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
        for viewComponent in self._viewComponents:
            viewComponent.unlock()

    def unregister_view(self, viewComponent):
        """Revove a view object from the composite list."""
        try:
            self._viewComponents.remove(viewComponent)
        except:
            pass

    def _add_multiple_sections(self):
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

    def _bind_events(self):
        self.root.bind(KEYS.RESTORE_STATUS[0], self.restore_status)
        self.root.bind(KEYS.OPEN_PROJECT[0], self._ctrl.open_project)

        self.root.bind(KEYS.LOCK_PROJECT[0], self._ctrl.lock)
        self.root.bind(KEYS.UNLOCK_PROJECT[0], self._ctrl.unlock)
        self.root.bind(KEYS.RELOAD_PROJECT[0], self._ctrl.reload_project)
        self.root.bind(KEYS.RESTORE_BACKUP[0], self._ctrl.restore_backup)
        self.root.bind(KEYS.FOLDER[0], self._ctrl.open_project_folder)
        self.root.bind(KEYS.REFRESH_TREE[0], self._ctrl.refresh_views)
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
        self.root.bind(KEYS.OPEN_HELP[0], self._open_help)

    def _build_menu(self):
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
        self.fileMenu.add_command(label=_('Refresh Tree'), accelerator=KEYS.REFRESH_TREE[1], command=self._ctrl.refresh_views)
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
        self.viewMenu.add_command(label=_('Options'), command=self._open_view_options)

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
        self.sectionMenu.add_command(label=_('Add multiple sections'), command=self._add_multiple_sections)
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
        self.characterMenu.add_command(label=_('Import'), command=lambda: self._ctrl.import_world_elements(CHARACTER_PREFIX))
        self.characterMenu.add_separator()
        self.characterMenu.add_command(label=_('Export character descriptions for editing'), command=lambda: self._ctrl.export_document(CHARACTERS_SUFFIX))
        self.characterMenu.add_command(label=_('Export character list (spreadsheet)'), command=lambda: self._ctrl.export_document(CHARLIST_SUFFIX))
        self.characterMenu.add_command(label=_('Show list'), command=lambda: self._ctrl.show_report(CHARACTER_REPORT_SUFFIX))

        # Location
        self.locationMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Locations'), menu=self.locationMenu)
        self.locationMenu.add_command(label=_('Add'), command=self._ctrl.add_location)
        self.locationMenu.add_separator()
        self.locationMenu.add_command(label=_('Import'), command=lambda: self._ctrl.import_world_elements(LOCATION_PREFIX))
        self.locationMenu.add_separator()
        self.locationMenu.add_command(label=_('Export location descriptions for editing'), command=lambda: self._ctrl.export_document(LOCATIONS_SUFFIX))
        self.locationMenu.add_command(label=_('Export location list (spreadsheet)'), command=lambda: self._ctrl.export_document(LOCLIST_SUFFIX))
        self.locationMenu.add_command(label=_('Show list'), command=lambda: self._ctrl.show_report(LOCATION_REPORT_SUFFIX))

        # "Item" menu.
        self.itemMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Items'), menu=self.itemMenu)
        self.itemMenu.add_command(label=_('Add'), command=self._ctrl.add_item)
        self.itemMenu.add_separator()
        self.itemMenu.add_command(label=_('Import'), command=lambda: self._ctrl.import_world_elements(ITEM_PREFIX))
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
        self.plotMenu.add_command(label=_('Export plot grid for editing'), command=lambda:self._ctrl.export_document(GRID_SUFFIX))
        self.plotMenu.add_command(label=_('Export story structure description for editing'), command=lambda:self._ctrl.export_document(STAGES_SUFFIX))
        self.plotMenu.add_command(label=_('Export plot line descriptions for editing'), command=lambda: self._ctrl.export_document(PLOTLINES_SUFFIX, lock=False))
        self.plotMenu.add_separator()
        self.plotMenu.add_command(label=_('Export plot list (spreadsheet)'), command=lambda: self._ctrl.export_document(PLOTLIST_SUFFIX, lock=False))
        self.plotMenu.add_command(label=_('Show Plot list'), command=lambda: self._ctrl.show_report(PLOTLIST_SUFFIX))

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
        self.exportMenu.add_command(label=_('Characters/locations/items data files'), command=lambda: self._ctrl.export_document(DATA_SUFFIX, lock=False, show=False))
        self.exportMenu.add_separator()
        self.exportMenu.add_command(label=_('Options'), command=self._open_export_options)

        # "Update" menu.
        self.mainMenu.add_command(label=_('Import'), command=self._open_project_updater)

        # "Tools" menu.
        self.toolsMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Tools'), menu=self.toolsMenu)
        self.toolsMenu.add_command(label=_('Plugin Manager'), command=self._open_plugin_manager)
        self.toolsMenu.add_command(label=_('Open installation folder'), command=self._ctrl.open_installationFolder)
        self.toolsMenu.add_separator()

        # "Help" menu.
        self.helpMenu = tk.Menu(self.mainMenu, tearoff=0)
        self.mainMenu.add_cascade(label=_('Help'), menu=self.helpMenu)
        self.helpMenu.add_command(label=_('Online help'), accelerator=KEYS.OPEN_HELP[1], command=self._open_help)
        self.helpMenu.add_command(label=f"novelibre {_('Home page')}", command=lambda: webbrowser.open(HOME_URL))

    def _open_export_options(self, event=None):
        """Open a toplevel window to edit the export options."""
        ExportOptionsWindow(self._mdl, self, self._ctrl)
        return 'break'

    def _open_help(self, event=None):
        open_help('')

    def _open_plugin_manager(self, event=None):
        """Open a toplevel window to manage the plugins."""
        PluginManager(self._mdl, self, self._ctrl)
        return 'break'

    def _open_project_updater(self, event=None):
        """Update the project from a previously exported document.
        
        Using a toplevel window with a pick list of refresh sources.
        """
        PrjUpdater(self._mdl, self, self._ctrl)
        return 'break'

    def _open_view_options(self, event=None):
        """Open a toplevel window to edit the view options."""
        ViewOptionsWindow(self._mdl, self, self._ctrl)
        return 'break'


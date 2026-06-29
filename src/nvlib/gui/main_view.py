"""Provide a tkinter based GUI for novelibre.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.controller.sub_controller import SubController
from nvlib.gui.contents_window.contents_viewer import ContentsViewer
from nvlib.gui.footers.path_bar import PathBar
from nvlib.gui.footers.status_bar import StatusBar
from nvlib.gui.icons import Icons
from nvlib.gui.menus.main_menu import MainMenu
from nvlib.gui.observer import Observer
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.platform.platform_settings import MOUSE
from nvlib.gui.pop_up.msg_boxes import MsgBoxes
from nvlib.gui.properties_window.properties_viewer import PropertiesViewer
from nvlib.gui.set_icon_tk import set_icon
from nvlib.gui.toolbar.toolbar import Toolbar
from nvlib.gui.tree_window.tree_viewer import TreeViewer
from nvlib.gui.widgets.tk_color_chooser import TkColorChooser
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk


class MainView(Observer, MsgBoxes, SubController, MainMenu):
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

        colorProbe = tk.Label(self.root)
        self.colorFg = colorProbe.cget('fg')
        self.colorBg = colorProbe.cget('bg')
        del colorProbe
        self.colorChooser = TkColorChooser()

        self._mdl.add_observer(self)

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
        set_icon(self.root, icon='novelibre')
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
        )

        self._mdl.add_observer(self.tv)
        self._ctrl.register_client(self.tv)
        self.tv.pack(expand=True, fill='both')

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

        #--- Create the menu structure.
        self.create_menus()

        #--- Add a toolbar.
        self.toolbar = Toolbar(self, self._ctrl)
        self._ctrl.register_client(self.toolbar)

    @property
    def selectedNode(self):
        return self.tv.tree.selection()[0]

    @property
    def selectedNodes(self):
        return self.tv.tree.selection()

    def lock(self):
        self.restore_status()
        self.pathBar.set_locked()
        self.fileMenu.entryconfig(_('Unlock'), state='normal')
        self.fileMenu.entryconfig(_('Lock'), state='disabled')

    def on_change_selection(self, nodeId):
        """Event handler for element selection.
        
        Show the properties/contents of the selected element.
        """
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
            prefs['prop_win_geometry'
                  ] = self._propertiesWindow.winfo_geometry()
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
        self.restore_status()
        self.pathBar.set_normal()
        self.fileMenu.entryconfig(_('Unlock'), state='disabled')
        self.fileMenu.entryconfig(_('Lock'), state='normal')

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

        self.pathBar.COLOR_NORMAL_BG = self.colorBg
        self.pathBar.COLOR_NORMAL_FG = self.colorFg
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

        self.statusBar.COLOR_NORMAL_BG = self.colorBg
        self.statusBar.COLOR_NORMAL_FG = self.colorFg
        self.statusBar.COLOR_SUCCESS_BG = prefs['color_status_success_bg']
        self.statusBar.COLOR_SUCCESS_FG = prefs['color_status_success_fg']
        self.statusBar.COLOR_ERROR_BG = prefs['color_status_error_bg']
        self.statusBar.COLOR_ERROR_FG = prefs['color_status_error_fg']
        self.statusBar.COLOR_NOTIFICATION_BG = (
            prefs['color_status_notification_bg']
        )
        self.statusBar.COLOR_NOTIFICATION_FG = (
            prefs['color_status_notification_fg']
        )

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

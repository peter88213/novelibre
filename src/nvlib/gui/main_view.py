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
from nvlib.gui.menus.nv_context_menu import NvContextMenu
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.gui.menus.tree_context_menu import TreeContextMenu
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
        colorProbe = tk.Label(self.root)
        self.colorFg = colorProbe.cget('fg')
        self.colorBg = colorProbe.cget('bg')
        del colorProbe

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

        #--- Create the menu structure.
        self._create_menus()

        #--- Add a toolbar.
        self.toolbar = Toolbar(self, self._ctrl)
        self._ctrl.register_client(self.toolbar)

    @property
    def selectedNode(self):
        return self._selection[0]

    @property
    def selectedNodes(self):
        return self._selection

    def lock(self):
        self.restore_status()
        self.pathBar.set_locked()
        self.fileMenu.entryconfig(_('Unlock'), state='normal')
        self.fileMenu.entryconfig(_('Lock'), state='disabled')

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

    def add_add_command(self, menu):
        label = _('Add')
        menu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_element,
        )
        menu.disableOnLock.append(label)

    def add_clipboard_commands(self, menu):
        label = _('Cut')
        menu.add_command(
            label=label,
            accelerator=KEYS.CUT[1],
            image=self.icons.cutIcon,
            compound='left',
            command=self._ctrl.cut_element,
        )
        menu.disableOnLock.append(label)

        label = _('Copy')
        menu.add_command(
            label=label,
            accelerator=KEYS.COPY[1],
            image=self.icons.copyIcon,
            compound='left',
            command=self._ctrl.copy_element,
        )
        label = _('Paste')
        menu.add_command(
            label=label,
            accelerator=KEYS.PASTE[1],
            image=self.icons.pasteIcon,
            compound='left',
            command=self._ctrl.paste_element,
        )
        menu.disableOnLock.append(label)

    def add_add_section_command(self, menu):
        label = _('Add Section')
        menu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_section,
        )
        menu.disableOnLock.append(label)

    def add_delete_command(self, menu):
        label = _('Delete')
        menu.add_command(
            label=label,
            accelerator=KEYS.DELETE[1],
            image=self.icons.removeIcon,
            compound='left',
            command=self._ctrl.delete_elements,
        )
        menu.disableOnLock.append(label)

    def add_change_level_cascade(self, menu):
        label = _('Change Level')
        menu.add_cascade(
            label=label,
            menu=self.selectLevelMenu,
        )
        menu.disableOnLock.append(label)

    def add_chapter_part_commands(self, menu):
        label = _('Add Chapter')
        menu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_chapter
        )
        menu.disableOnLock.append(label)

        label = _('Add Part')
        menu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_part,
        )
        menu.disableOnLock.append(label)

    def add_highlight_related_command(self, menu):
        label = _('Highlight related sections')
        menu.add_command(
            label=label,
            image=self.icons.highlightIcon,
            compound='left',
            command=self.tv.highlight_related_sections,
        )

    def add_insert_stage_command(self, menu):
        label = _('Insert Stage')
        menu.add_command(
            label=label,
            command=self._ctrl.add_new_stage,
        )
        menu.disableOnLock.append(label)

    def add_set_cr_status_cascade(self, menu):
        label = _('Set Status')
        menu.add_cascade(
            label=label,
            menu=self.selectCharacterStatusMenu,
        )
        menu.disableOnLock.append(label)

    def add_set_status_cascade(self, menu):
        label = _('Set Status')
        menu.add_cascade(
            label=label,
            menu=self.selectSectionStatusMenu,
        )
        menu.disableOnLock.append(label)

    def add_set_type_cascade(self, menu):
        label = _('Set Type')
        menu.add_cascade(
            label=label,
            menu=self.selectTypeMenu,
        )
        menu.disableOnLock.append(label)

    def add_set_viewpoint_command(self, menu):
        label = _('Set Viewpoint...')
        menu.add_command(
            label=label,
            command=self._ctrl.set_viewpoint,
        )
        menu.disableOnLock.append(label)

    def add_view_commands(self, menu):
        label = _('Chapter level')
        menu.add_command(
            label=label,
            command=self.tv.show_chapter_level,
        )
        menu.disableOnClose.append(label)

        label = _('Expand all')
        menu.add_command(
            label=label,
            command=self.tv.expand_all,
        )
        menu.disableOnClose.append(label)

        label = _('Collapse all')
        menu.add_command(
            label=label,
            command=self.tv.collapse_all,
        )
        menu.disableOnClose.append(label)

    def _create_menus(self):

        #--- Selection submenus.

        self.selectTypeMenu = NvMenu()

        label = _('Normal')
        self.selectTypeMenu.add_command(
            label=label,
            command=self._ctrl.set_type_normal,
        )

        label = _('Unused')
        self.selectTypeMenu.add_command(
            label=label,
            command=self._ctrl.set_type_unused,
        )

        self.selectLevelMenu = NvMenu()

        label = _('1st Level')
        self.selectLevelMenu.add_command(
            label=label,
            command=self._ctrl.set_level_1,
        )

        label = _('2nd Level')
        self.selectLevelMenu.add_command(
            label=label,
            command=self._ctrl.set_level_2,
        )

        self.selectSectionStatusMenu = NvMenu()

        label = _('Outline')
        self.selectSectionStatusMenu.add_command(
            label=label,
            command=self._ctrl.set_scn_status_outline,
        )

        label = _('Draft')
        self.selectSectionStatusMenu.add_command(
            label=label,
            command=self._ctrl.set_scn_status_draft,
        )

        label = _('1st Edit')
        self.selectSectionStatusMenu.add_command(
            label=label,
            command=self._ctrl.set_scn_status_1st_edit,
        )

        label = _('2nd Edit')
        self.selectSectionStatusMenu.add_command(
            label=label,
            command=self._ctrl.set_scn_status_2nd_edit,
        )

        label = _('Done')
        self.selectSectionStatusMenu.add_command(
            label=label,
            command=self._ctrl.set_scn_status_done,
        )

        self.selectCharacterStatusMenu = NvMenu()

        label = _('Major Character')
        self.selectCharacterStatusMenu.add_command(
            label=label,
            command=self._ctrl.set_chr_status_major,
        )

        label = _('Minor Character')
        self.selectCharacterStatusMenu.add_command(
            label=label,
            command=self._ctrl.set_chr_status_minor,
        )

        #--- Main submenus.

        # "File" > "New".
        self.newMenu = NvMenu()

        label = _('Empty project')
        self.newMenu.add_command(
            label=label,
            command=self._ctrl.create_project,
        )

        label = _('Create from ODT...')
        self.newMenu.add_command(
            label=label,
            command=self._ctrl.import_odf,
        )

        # "File"
        self.fileMenu = NvMenu()

        label = _('New')
        self.fileMenu.add_cascade(
            label=label,
            menu=self.newMenu
        )

        label = _('Open...')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.OPEN_PROJECT[1],
            command=self._ctrl.open_project,
        )

        label = _('Reload')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.RELOAD_PROJECT[1],
            command=self._ctrl.reload_project,
        )
        self.fileMenu.disableOnClose.append(label)
        self.fileMenu.disableOnLock.append(label)

        label = _('Restore backup')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.RESTORE_BACKUP[1],
            command=self._ctrl.restore_backup,
        )
        self.fileMenu.disableOnClose.append(label)
        self.fileMenu.disableOnLock.append(label)

        self.fileMenu.add_separator()

        label = _('Refresh Tree')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.REFRESH_TREE[1],
            command=self._ctrl.refresh_tree,
        )
        self.fileMenu.disableOnClose.append(label)
        self.fileMenu.disableOnLock.append(label)

        label = _('Lock')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.LOCK_PROJECT[1],
            image=self.icons.lockIcon,
            compound='left',
            command=self._ctrl.lock,
        )
        self.fileMenu.disableOnClose.append(label)

        label = _('Unlock')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.UNLOCK_PROJECT[1],
            command=self._ctrl.unlock,
        )
        self.fileMenu.disableOnClose.append(label)

        self.fileMenu.add_separator()

        label = _('Open Project folder')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.FOLDER[1],
            command=self._ctrl.open_project_folder,
        )
        self.fileMenu.disableOnClose.append(label)

        label = _('Copy style sheet')
        self.fileMenu.add_command(
            label=label,
            command=self._ctrl.copy_css,
        )
        self.fileMenu.disableOnClose.append(label)

        label = _('Discard manuscript')
        self.fileMenu.add_command(
            label=label,
            command=self._ctrl.discard_manuscript,
        )
        self.fileMenu.disableOnClose.append(label)
        self.fileMenu.disableOnLock.append(label)

        self.fileMenu.add_separator()

        label = _('Save')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.SAVE_PROJECT[1],
            image=self.icons.saveIcon,
            compound='left',
            command=self._ctrl.save_project,
        )
        self.fileMenu.disableOnClose.append(label)
        self.fileMenu.disableOnLock.append(label)

        label = _('Save as...')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.SAVE_AS[1],
            command=self._ctrl.save_as,
        )
        self.fileMenu.disableOnClose.append(label)

        label = _('Close')
        self.fileMenu.add_command(
            label=label,
            command=self._ctrl.close_project,
        )
        self.fileMenu.disableOnClose.append(label)

        if PLATFORM == 'win':
            label = _('Exit'),
        else:
            label = _('Quit'),
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.QUIT_PROGRAM[1],
            command=self._ctrl.on_quit,
        )

        self._ctrl.register_client(self.fileMenu)

        # "View".
        self.viewMenu = NvMenu()

        label = _('Highlight tagged elements')
        self.viewMenu.add_command(
            label=label,
            image=self.icons.tagsIcon,
            compound='left',
            command=self.tv.select_tag_and_highlight_elements,
        )
        self.viewMenu.disableOnClose.append(label)

        label = _('Reset Highlighting')
        self.viewMenu.add_command(
            label=label,
            image=self.icons.resetHighlightIcon,
            compound='left',
            command=self.tv.reset_highlighting,
        )

        self.viewMenu.add_separator()

        label = _('Show Book')
        self.viewMenu.add_command(
            label=label,
            image=self.icons.viewBookIcon,
            compound='left',
            command=self.tv.show_book,
        )
        self.viewMenu.disableOnClose.append(label)

        label = _('Show Characters')
        self.viewMenu.add_command(
            label=label,
            image=self.icons.viewCharactersIcon,
            compound='left',
            command=self.tv.show_characters,
        )
        self.viewMenu.disableOnClose.append(label)

        label = _('Show Locations')
        self.viewMenu.add_command(
            label=label,
            image=self.icons.viewLocationsIcon,
            compound='left',
            command=self.tv.show_locations,
        )
        self.viewMenu.disableOnClose.append(label)

        label = _('Show Items')
        self.viewMenu.add_command(
            label=label,
            image=self.icons.viewItemsIcon,
            compound='left',
            command=self.tv.show_items,
        )
        self.viewMenu.disableOnClose.append(label)

        label = _('Show Plot lines')
        self.viewMenu.add_command(
            label=label,
            image=self.icons.viewPlotLinesIcon,
            compound='left',
            command=self.tv.show_plot_lines,
        )
        self.viewMenu.disableOnClose.append(label)

        label = _('Show Project notes')
        self.viewMenu.add_command(
            label=label,
            image=self.icons.viewProjectnotesIcon,
            compound='left',
            command=self.tv.show_project_notes,
        )
        self.viewMenu.disableOnClose.append(label)

        self.viewMenu.add_separator()

        self.add_view_commands(self.viewMenu)

        label = _('Expand selected')
        self.viewMenu.add_command(
            label=label,
            command=self.tv.expand_selected,
        )
        self.viewMenu.disableOnClose.append(label)

        label = _('Collapse selected')
        self.viewMenu.add_command(
            label=label,
            command=self.tv.collapse_selected,
        )
        self.viewMenu.disableOnClose.append(label)

        self.viewMenu.add_separator()

        label = _('Toggle Text viewer')
        self.viewMenu.add_command(
            label=label,
            accelerator=KEYS.TOGGLE_VIEWER[1],
            image=self.icons.viewerIcon,
            compound='left',
            command=self.toggle_contents_view,
        )

        label = _('Toggle Properties')
        self.viewMenu.add_command(
            label=label,
            accelerator=KEYS.TOGGLE_PROPERTIES[1],
            image=self.icons.propertiesIcon,
            compound='left',
            command=self.toggle_properties_view,
        )

        label = _('Detach/Dock Properties')
        self.viewMenu.add_command(
            label=label,
            accelerator=KEYS.DETACH_PROPERTIES[1],
            command=self.toggle_properties_window,
        )

        self.viewMenu.add_separator()

        label = _('Options')
        self.viewMenu.add_command(
            label=label,
            command=self._ctrl.open_view_options,
        )

        self._ctrl.register_client(self.viewMenu)

        # "Part".
        self.partMenu = NvMenu()

        label = _('Add')
        self.partMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_part,
        )
        self.partMenu.disableOnLock.append(label)

        self.partMenu.add_separator()

        label = _('Export part descriptions for editing')
        self.partMenu.add_command(
            label=label,
            command=self._ctrl.export_part_desc,
        )
        self.partMenu.disableOnLock.append(label)

        label = _('Export part table')
        self.partMenu.add_command(
            label=label,
            command=self._ctrl.export_part_list,
        )
        self.partMenu.disableOnLock.append(label)

        self._ctrl.register_client(self.partMenu)

        # "Chapter".
        self.chapterMenu = NvMenu()

        label = _('Add')
        self.chapterMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_chapter,
        )
        self.chapterMenu.disableOnLock.append(label)

        label = _('Add multiple chapters...')
        self.chapterMenu.add_command(
            label=label,
            command=self._ctrl.add_multiple_new_chapters,
        )
        self.chapterMenu.disableOnLock.append(label)

        self.chapterMenu.add_separator()

        self.add_set_type_cascade(self.chapterMenu)
        self.add_change_level_cascade(self.chapterMenu)

        self.chapterMenu.add_separator()

        label = _('Move selected chapters to new project')
        self.chapterMenu.add_command(
            label=label,
            command=self._ctrl.split_file,
        )
        self.chapterMenu.disableOnLock.append(label)

        self.chapterMenu.add_separator()

        label = _('Export chapter descriptions for editing')
        self.chapterMenu.add_command(
            label=label,
            command=self._ctrl.export_chapter_desc,
        )
        self.chapterMenu.disableOnLock.append(label)

        label = _('Export chapter table')
        self.chapterMenu.add_command(
            label=label,
            command=self._ctrl.export_chapter_list,
        )
        self.chapterMenu.disableOnLock.append(label)

        self._ctrl.register_client(self.chapterMenu)

        # "Section".
        self.sectionMenu = NvMenu()

        label = _('Add')
        self.sectionMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_section,
        )
        self.sectionMenu.disableOnLock.append(label)

        label = _('Add multiple sections...')
        self.sectionMenu.add_command(
            label=label,
            command=self._ctrl.add_multiple_new_sections,
        )
        self.sectionMenu.disableOnLock.append(label)

        self.sectionMenu.add_separator()

        self.add_set_type_cascade(self.sectionMenu)
        self.add_set_status_cascade(self.sectionMenu)
        self.add_set_viewpoint_command(self.sectionMenu)

        self.sectionMenu.add_separator()

        label = _('Export section descriptions for editing')
        self.sectionMenu.add_command(
            label=label,
            command=self._ctrl.export_section_desc,
        )
        self.sectionMenu.disableOnLock.append(label)

        self.sectionMenu.add_separator()

        label = _('Section table (export only)')
        self.sectionMenu.add_command(
            label=label,
            command=self._ctrl.export_section_list,
        )

        label = _('Show Time table')
        self.sectionMenu.add_command(
            label=label,
            command=self._ctrl.show_timetable,
        )

        self._ctrl.register_client(self.sectionMenu)

        # "Characters"
        self.characterMenu = NvMenu()

        label = _('Add')
        self.characterMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_character,
        )
        self.characterMenu.disableOnLock.append(label)

        self.characterMenu.add_separator()

        self.add_set_cr_status_cascade(self.characterMenu)

        self.characterMenu.add_separator()

        label = _('Import')
        self.characterMenu.add_command(
            label=label,
            command=self._ctrl.import_character_data,
        )
        self.characterMenu.disableOnLock.append(label)

        self.characterMenu.add_separator()

        label = _('Export character descriptions for editing')
        self.characterMenu.add_command(
            label=label,
            command=self._ctrl.export_character_desc,
        )
        self.characterMenu.disableOnLock.append(label)

        label = _('Export character table')
        self.characterMenu.add_command(
            label=label,
            command=self._ctrl.export_character_list,
        )
        self.characterMenu.disableOnLock.append(label)

        self.characterMenu.add_separator()

        label = _('Show table in Browser')
        self.characterMenu.add_command(
            label=label,
            command=self._ctrl.show_character_list,
        )

        self._ctrl.register_client(self.characterMenu)

        # "Locations".
        self.locationMenu = NvMenu()

        label = _('Add')
        self.locationMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_location,
        )
        self.locationMenu.disableOnLock.append(label)

        self.locationMenu.add_separator()

        label = _('Import')
        self.locationMenu.add_command(
            label=label,
            command=self._ctrl.import_location_data,
        )
        self.locationMenu.disableOnLock.append(label)

        self.locationMenu.add_separator()

        label = _('Export location descriptions for editing')
        self.locationMenu.add_command(
            label=label,
            command=self._ctrl.export_location_desc,
        )
        self.locationMenu.disableOnLock.append(label)

        label = _('Export location table')
        self.locationMenu.add_command(
            label=label,
            command=self._ctrl.export_location_list,
        )
        self.locationMenu.disableOnLock.append(label)

        self.locationMenu.add_separator()

        label = _('Show table in Browser')
        self.locationMenu.add_command(
            label=label,
            command=self._ctrl.show_location_list,
        )

        self._ctrl.register_client(self.locationMenu)

        # "Items".
        self.itemMenu = NvMenu()

        label = _('Add')
        self.itemMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_item,
        )
        self.itemMenu.disableOnLock.append(label)

        self.itemMenu.add_separator()

        label = _('Import')
        self.itemMenu.add_command(
            label=label,
            command=self._ctrl.import_item_data,
        )
        self.itemMenu.disableOnLock.append(label)

        self.itemMenu.add_separator()

        label = _('Export item descriptions for editing')
        self.itemMenu.add_command(
            label=label,
            command=self._ctrl.export_item_desc,
        )
        self.itemMenu.disableOnLock.append(label)

        label = _('Export item table')
        self.itemMenu.add_command(
            label=label,
            command=self._ctrl.export_item_list,
        )
        self.itemMenu.disableOnLock.append(label)

        self.itemMenu.add_separator()

        label = _('Show table in Browser')
        self.itemMenu.add_command(
            label=label,
            command=self._ctrl.show_item_list,
        )

        self._ctrl.register_client(self.itemMenu)

        # "Plot".
        self.plotMenu = NvMenu()

        label = _('Add Plot line')
        self.plotMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_plot_line,
        )
        self.plotMenu.disableOnLock.append(label)

        label = _('Add Plot point')
        self.plotMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_plot_point,
        )
        self.plotMenu.disableOnLock.append(label)

        self.plotMenu.add_separator()

        self.add_insert_stage_command(self.plotMenu)
        self.add_change_level_cascade(self.plotMenu)

        self.plotMenu.add_separator()

        label = _('Import plot lines')
        self.plotMenu.add_command(
            label=label,
            command=self._ctrl.import_plot_lines,
        )
        self.plotMenu.disableOnLock.append(label)

        self.plotMenu.add_separator()

        label = _('Export plot grid for editing')
        self.plotMenu.add_command(
            label=label,
            command=self._ctrl.export_plot_grid,
        )
        self.plotMenu.disableOnLock.append(label)

        label = _('Export story structure description for editing')
        self.plotMenu.add_command(
            label=label,
            command=self._ctrl.export_story_structure_desc,
        )
        self.plotMenu.disableOnLock.append(label)

        label = _('Export plot line descriptions for editing')
        self.plotMenu.add_command(
            label=label,
            command=self._ctrl.export_plot_lines_desc,
        )
        self.plotMenu.disableOnLock.append(label)

        self.plotMenu.add_separator()

        label = _('Plot table (export only)')
        self.plotMenu.add_command(
            label=label,
            command=self._ctrl.export_plot_list,
        )

        label = _('Show Plot table in browser')
        self.plotMenu.add_command(
            label=label,
            command=self._ctrl.show_plot_list,
        )

        self._ctrl.register_client(self.plotMenu)

        # "Project notes"
        self.prjNoteMenu = NvMenu()

        label = _('Add')
        self.prjNoteMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_project_note,
        )
        self.prjNoteMenu.disableOnLock.append(label)

        self.prjNoteMenu.add_separator()

        label = _('Show table in Browser')
        self.prjNoteMenu.add_command(
            label=label,
            command=self._ctrl.show_projectnotes_list,
        )

        self._ctrl.register_client(self.prjNoteMenu)

        # "Export"
        self.exportMenu = NvMenu()

        label = _('Manuscript for editing')
        self.exportMenu.add_command(
            label=label,
            image=self.icons.manuscriptIcon,
            compound='left',
            command=self._ctrl.export_manuscript,
        )
        self.exportMenu.disableOnLock.append(label)
        self.exportMenu.disableOnClose.append(label)

        label = _('Manuscript for third-party word processing')
        self.exportMenu.add_command(
            label=label,
            command=self._ctrl.export_proofing_manuscript,
        )
        self.exportMenu.disableOnLock.append(label)
        self.exportMenu.disableOnClose.append(label)

        self.exportMenu.add_separator()

        label = _('Final manuscript document (export only)')
        self.exportMenu.add_command(
            label=label,
            command=self._ctrl.export_final_document,
        )
        self.exportMenu.disableOnClose.append(label)

        label = _('Brief synopsis (export only)')
        self.exportMenu.add_command(
            label=label,
            command=self._ctrl.export_brief_synopsis,
        )
        self.exportMenu.disableOnClose.append(label)

        label = _('Cross references (export only)')
        self.exportMenu.add_command(
            label=label,
            command=self._ctrl.export_cross_references,
        )
        self.exportMenu.disableOnClose.append(label)

        self.exportMenu.add_separator()

        label = _('XML data files')
        self.exportMenu.add_command(
            label=label,
            command=self._ctrl.export_xml_data_files,
        )
        self.exportMenu.disableOnClose.append(label)

        self.exportMenu.add_separator()

        label = _('Options')
        self.exportMenu.add_command(
            label=label,
            command=self._ctrl.open_export_options,
        )

        self._ctrl.register_client(self.exportMenu)

        # "Tools".
        self.toolsMenu = NvMenu()

        label = _('Backup options')
        self.toolsMenu.add_command(
            label=label,
            command=self._ctrl.open_backup_options,
        )

        self.toolsMenu.add_separator()

        label = _('Open installation folder')
        self.toolsMenu.add_command(
            label=label,
            command=self._ctrl.open_installationFolder,
        )

        self.toolsMenu.add_separator()

        label = _('Plugin Manager')
        self.toolsMenu.add_command(
            label=label,
            command=self._ctrl.open_plugin_manager,
        )

        self.toolsMenu.add_separator()

        label = _('Show notes')
        self.toolsMenu.add_command(
            label=label,
            command=self._ctrl.show_notes_list,
        )
        self.toolsMenu.disableOnClose.append(label)

        self.toolsMenu.add_separator()

        self._ctrl.register_client(self.toolsMenu)

        # "Help".
        self.helpMenu = NvMenu()

        label = _('Online help')
        self.helpMenu.add_command(
            label=label,
            accelerator=KEYS.OPEN_HELP[1],
            command=self._ctrl.open_help,
        )

        label = _('About novelibre')
        self.helpMenu.add_command(
            label=label,
            command=self._about,
        )

        label = f"novelibre {_('Home page')}"
        self.helpMenu.add_command(
            label=label,
            command=self._ctrl.open_homepage,
        )

        label = _('News about novelibre')
        self.helpMenu.add_command(
            label=label,
            command=self._ctrl.open_news,
        )

        self.helpMenu.add_separator()

        self._ctrl.register_client(self.helpMenu)

        #--- Main menu.
        self.mainMenu = NvMenu()

        label = _('File')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.fileMenu,
        )

        label = _('View')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.viewMenu
        )

        label = _('Part')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.partMenu,
        )
        self.mainMenu.disableOnClose.append(label)

        label = _('Chapter')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.chapterMenu,
        )
        self.mainMenu.disableOnClose.append(label)

        label = _('Section')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.sectionMenu,
        )
        self.mainMenu.disableOnClose.append(label)

        label = _('Characters')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.characterMenu,
        )
        self.mainMenu.disableOnClose.append(label)

        label = _('Locations')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.locationMenu,
        )
        self.mainMenu.disableOnClose.append(label)

        label = _('Items')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.itemMenu,
        )
        self.mainMenu.disableOnClose.append(label)

        label = _('Plot')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.plotMenu
        )
        self.mainMenu.disableOnClose.append(label)

        label = _('Project notes')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.prjNoteMenu,
        )
        self.mainMenu.disableOnClose.append(label)

        label = _('Import')
        self.mainMenu.add_command(
            label=label,
            command=self._ctrl.open_project_updater
        )
        self.mainMenu.disableOnLock.append(label)
        self.mainMenu.disableOnClose.append(label)

        label = _('Export')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.exportMenu,
        )

        label = _('Tools')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.toolsMenu
        )

        label = _('Help')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.helpMenu,
        )

        self._ctrl.register_client(self.mainMenu)
        self.root.config(menu=self.mainMenu)

        #--- Tree context menus.

        #--- Book context menu.
        self.bookContextMenu = NvContextMenu()

        self.add_chapter_part_commands(self.bookContextMenu)

        self.bookContextMenu.add_separator()

        self.add_set_status_cascade(self.bookContextMenu)
        self.add_set_viewpoint_command(self.bookContextMenu)

        self.bookContextMenu.add_separator()

        self.add_view_commands(self.bookContextMenu)

        self._ctrl.register_client(self.bookContextMenu)

        #--- Chapter context menu.
        self.chapterContextMenu = NvContextMenu()

        self.add_add_section_command(self.chapterContextMenu)
        self.add_chapter_part_commands(self.chapterContextMenu)
        self.add_insert_stage_command(self.chapterContextMenu)

        self.chapterContextMenu.add_separator()

        self.add_delete_command(self.chapterContextMenu)

        self.chapterContextMenu.add_separator()

        self.add_clipboard_commands(self.chapterContextMenu)

        self.chapterContextMenu.add_separator()

        self.add_change_level_cascade(self.chapterContextMenu)
        self.add_set_type_cascade(self.chapterContextMenu)
        self.add_set_status_cascade(self.chapterContextMenu)
        self.add_set_viewpoint_command(self.chapterContextMenu)

        self.chapterContextMenu.add_separator()

        label = _('Export this chapter')
        self.chapterContextMenu.add_cascade(
            label=label,
            command=self._ctrl.export_filtered_manuscript,
        )
        self.chapterContextMenu.disableOnLock.append(label)

        self.chapterContextMenu.add_separator()

        self.add_view_commands(self.chapterContextMenu)

        self._ctrl.register_client(self.chapterContextMenu)

        #--- Character context menu.
        self.characterContextMenu = NvContextMenu()

        self.add_add_command(self.characterContextMenu)

        self.characterContextMenu.add_separator()

        self.add_delete_command(self.characterContextMenu)

        self.characterContextMenu.add_separator()

        self.add_clipboard_commands(self.characterContextMenu)

        self.characterContextMenu.add_separator()

        self.add_set_cr_status_cascade(self.characterContextMenu)

        self.characterContextMenu.add_separator()

        label = _('Export manuscript filtered by viewpoint')
        self.characterContextMenu.add_command(
            label=label,
            image=self.icons.manuscriptIcon,
            compound='left',
            command=self._ctrl.export_filtered_manuscript,
        )
        self.characterContextMenu.disableOnLock.append(label)

        label = _('Export synopsis filtered by viewpoint')
        self.characterContextMenu.add_command(
            label=label,
            image=self.icons.manuscriptIcon,
            compound='left',
            command=self._ctrl.export_filtered_synopsis,
        )
        self.characterContextMenu.disableOnLock.append(label)

        self.characterContextMenu.add_separator()

        self.add_view_commands(self.characterContextMenu)

        self.characterContextMenu.add_separator()

        label = _('Highlight sections with this viewpoint')
        self.characterContextMenu.add_command(
            label=label,
            image=self.icons.highlightIcon,
            compound='left',
            command=self.tv.highlight_viewpoint_sections,
        )

        self.add_highlight_related_command(self.characterContextMenu)

        self._ctrl.register_client(self.characterContextMenu)

        #--- Characters root context menu.
        self.crRootContextMenu = NvContextMenu()

        self.add_add_command(self.crRootContextMenu)

        self.crRootContextMenu.add_separator()

        self.add_set_cr_status_cascade(self.crRootContextMenu)

        self.crRootContextMenu.add_separator()

        self.add_view_commands(self.crRootContextMenu)

        self._ctrl.register_client(self.crRootContextMenu)

        #--- Location/item/plot line/project note context menu.
        self.elementContextMenu = NvContextMenu()

        self.add_add_command(self.elementContextMenu)

        self.elementContextMenu.add_separator()

        self.add_delete_command(self.elementContextMenu)

        self.elementContextMenu.add_separator()

        self.add_clipboard_commands(self.elementContextMenu)

        self.elementContextMenu.add_separator()

        self.add_view_commands(self.elementContextMenu)

        self.elementContextMenu.add_separator()

        self.add_highlight_related_command(self.elementContextMenu)

        self._ctrl.register_client(self.elementContextMenu)

        #--- Plot line context menu.
        self.plotLineContextMenu = NvContextMenu()

        label = _('Add Plot line')
        self.plotLineContextMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_plot_line,
        )
        self.plotLineContextMenu.disableOnLock.append(label)

        label = _('Add Plot point')
        self.plotLineContextMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_plot_point,
        )
        self.plotLineContextMenu.disableOnLock.append(label)

        self.plotLineContextMenu.add_separator()

        self.add_delete_command(self.plotLineContextMenu)

        self.plotLineContextMenu.add_separator()

        self.add_clipboard_commands(self.plotLineContextMenu)

        self.plotLineContextMenu.add_separator()

        label = _('Change sections to Unused')
        self.plotLineContextMenu.add_command(
            label=label,
            command=self._ctrl.exclude_plot_line,
        )
        self.plotLineContextMenu.disableOnLock.append(label)

        label = _('Change sections to Normal')
        self.plotLineContextMenu.add_command(
            label=label,
            command=self._ctrl.include_plot_line
        )
        self.plotLineContextMenu.disableOnLock.append(label)

        self.plotLineContextMenu.add_separator()

        label = _('Export manuscript filtered by plot line')
        self.plotLineContextMenu.add_command(
            label=label,
            command=self._ctrl.export_filtered_manuscript,
        )
        self.plotLineContextMenu.disableOnLock.append(label)

        label = _('Export synopsis filtered by plot line')
        self.plotLineContextMenu.add_command(
            label=label,
            command=self._ctrl.export_filtered_synopsis,
        )
        self.plotLineContextMenu.disableOnLock.append(label)

        self.plotLineContextMenu.add_separator()

        self.add_view_commands(self.plotLineContextMenu)

        self.plotLineContextMenu.add_separator()

        self.add_highlight_related_command(self.plotLineContextMenu)

        self._ctrl.register_client(self.plotLineContextMenu)

        #--- Locations/items/plot lines/project notes root menu.
        self.rootContextMenu = NvContextMenu()

        self.add_add_command(self.rootContextMenu)

        self.rootContextMenu.add_separator()

        self.add_view_commands(self.rootContextMenu)

        self._ctrl.register_client(self.rootContextMenu)

        #--- Section context menu.
        self.sectionContextMenu = NvContextMenu()

        self.add_add_section_command(self.sectionContextMenu)
        self.add_insert_stage_command(self.sectionContextMenu)

        self.sectionContextMenu.add_separator()

        self.add_delete_command(self.sectionContextMenu)

        self.sectionContextMenu.add_separator()

        self.add_clipboard_commands(self.sectionContextMenu)

        self.sectionContextMenu.add_separator()

        self.add_set_type_cascade(self.sectionContextMenu)
        self.add_set_status_cascade(self.sectionContextMenu)
        self.add_set_viewpoint_command(self.sectionContextMenu)

        self.sectionContextMenu.add_separator()

        label = _('Join with previous')
        self.sectionContextMenu.add_command(
            label=label,
            command=self._ctrl.join_sections,
        )
        self.sectionContextMenu.disableOnLock.append(label)

        self.sectionContextMenu.add_separator()

        self.add_view_commands(self.sectionContextMenu)

        self._ctrl.register_client(self.sectionContextMenu)

        #--- Stage context menu.
        self.stageContextMenu = NvContextMenu()

        self.add_add_section_command(self.stageContextMenu)
        self.add_insert_stage_command(self.stageContextMenu)

        self.stageContextMenu.add_separator()

        self.add_delete_command(self.stageContextMenu)

        self.stageContextMenu.add_separator()

        self.add_clipboard_commands(self.stageContextMenu)

        self.stageContextMenu.add_separator()

        self.add_change_level_cascade(self.stageContextMenu)

        self.stageContextMenu.add_separator()

        self.add_view_commands(self.stageContextMenu)

        self._ctrl.register_client(self.stageContextMenu)

        #--- Trash bin context menu.
        self.trashContextMenu = NvContextMenu()

        self.add_delete_command(self.trashContextMenu)

        self._ctrl.register_client(self.trashContextMenu)

        self.contextMenu = TreeContextMenu(self._mdl, self)

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

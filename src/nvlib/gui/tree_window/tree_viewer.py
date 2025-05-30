"""Provide a tkinter based novelibre tree view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.observer import Observer
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.platform.platform_settings import MOUSE
from nvlib.gui.tree_window.history_list import HistoryList
from nvlib.gui.tree_window.tree_viewer_ctrl import TreeViewerCtrl
from nvlib.gui.widgets.context_menu import ContextMenu
from nvlib.model.nv_treeview import NvTreeview
from nvlib.novx_globals import string_to_list
from nvlib.nv_globals import prefs
from nvlib.nv_locale import _
import tkinter as tk
import tkinter.font as tkFont


class TreeViewer(ttk.Frame, Observer, TreeViewerCtrl):
    """Widget for novelibre tree view."""
    COLORING_MODES = [_('None'), _('Status'), _('Work phase')]
    # List[str] -- Section row coloring modes.

    _COLUMNS = dict(
        wc=(_('Words'), 'wc_width'),
        vp=(_('Viewpoint'), 'vp_width'),
        st=(_('Status'), 'status_width'),
        nt=(_('N'), 'nt_width'),
        dt=(_('Date'), 'date_width'),
        tm=(_('Time'), 'time_width'),
        dr=(_('Duration'), 'duration_width'),
        tg=(_('Tags'), 'tags_width'),
        po=(_('Position'), 'ps_width'),
        ac=(_('Plot lines'), 'arcs_width'),
        sc=(_('Scene'), 'scene_width'),
        tp=(_('Plot points'), 'points_width'),
        )
    # Key: column ID
    # Value: (column title, column width)

    def __init__(self, parent, model, view, controller, **kw):
        """Put a tkinter tree in the specified parent widget.
        
        Positional arguments:
            parent -- parent widget for displaying the tree view.
            view -- GUI class reference.        
        """
        super().__init__(parent, **kw)
        self.initialize_controller(model, view, controller)

        self.skipUpdate = False
        self._branch_status = {}
        # open/close

        # Create a novel tree.
        self.tree = NvTreeview(self)
        scrollX = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        scrollY = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(xscrollcommand=scrollX.set)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollX.pack(side='bottom', fill='x')
        scrollY.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)

        #--- Add columns to the tree.
        self.configure_columns()

        #--- configure tree row display.
        fontSize = tkFont.nametofont('TkDefaultFont').actual()['size']
        self.tree.tag_configure('root', font=('', fontSize, 'bold'))
        self.tree.tag_configure('chapter', foreground=prefs['color_chapter'])
        self.tree.tag_configure('arc', font=('', fontSize, 'bold'), foreground=prefs['color_arc'])
        self.tree.tag_configure('plot_point', foreground=prefs['color_arc'])
        self.tree.tag_configure('unused', foreground=prefs['color_unused'])
        self.tree.tag_configure('stage1', font=('', fontSize, 'bold'), foreground=prefs['color_stage'])
        self.tree.tag_configure('stage2', foreground=prefs['color_stage'])
        self.tree.tag_configure('part', font=('', fontSize, 'bold'))
        self.tree.tag_configure('major', foreground=prefs['color_major'])
        self.tree.tag_configure('minor', foreground=prefs['color_minor'])
        self.tree.tag_configure('status1', foreground=prefs['color_outline'])
        self.tree.tag_configure('status2', foreground=prefs['color_draft'])
        self.tree.tag_configure('status3', foreground=prefs['color_1st_edit'])
        self.tree.tag_configure('status4', foreground=prefs['color_2nd_edit'])
        self.tree.tag_configure('status5', foreground=prefs['color_done'])
        self.tree.tag_configure('On_schedule', foreground=prefs['color_on_schedule'])
        self.tree.tag_configure('Behind_schedule', foreground=prefs['color_behind_schedule'])
        self.tree.tag_configure('Before_schedule', foreground=prefs['color_before_schedule'])

        #--- Browsing history.
        self._history = HistoryList()

        # -- Section coloring mode.
        try:
            self.coloringMode = int(prefs['coloring_mode'])
        except:
            self.coloringMode = 0
        if self.coloringMode > len(self.COLORING_MODES):
            self.coloringMode = 0

        #--- Create public submenus and local context menus.
        self._create_menus()

        #--- Bind events.
        self._bind_events()

    def close_children(self, parent):
        """Recursively close children nodes.
        
        Positional arguments:
            parent: str -- Root node of the branch to close.
        """
        self.tree.item(parent, open=False)
        self.update_node_values(parent, collect=True)
        for child in self.tree.get_children(parent):
            self.close_children(child)

    def configure_columns(self):
        """Determine the order of the columnns.
        
        Read from the ui keyword arguments:
            column_order: str -- ordered column IDs, semicolon-separated.
        
        Write instance variables:
            _colPos: dict -- key=ID, value=index.
            columns -- list of tuples (ID, title, width).
        """
        # Column position by column ID.
        self._colPos = {}
        self.columns = []
        titles = []
        srtColumns = string_to_list(prefs['column_order'])

        # Check data integrity.
        for coId in self._COLUMNS:
            if not coId in srtColumns:
                srtColumns.append(coId)
        i = 0
        for coId in srtColumns:
            try:
                title, width = self._COLUMNS[coId]
            except:
                continue

            self._colPos[coId] = i
            i += 1
            self.columns.append((coId, title, width))
            titles.append(title)
        self.tree.configure(columns=tuple(titles))
        for column in self.columns:
            self.tree.heading(column[1], text=column[1], anchor='w')
            self.tree.column(column[1], width=int(prefs[column[2]]), minwidth=3, stretch=False)
        self.tree.column('#0', width=int(prefs['title_width']), stretch=False)

    def go_back(self, event=None):
        """Select a node back in the tree browsing history."""
        self._browse_tree(self._history.go_back())
        return('break')

    def go_forward(self, event=None):
        """Select a node forward in the tree browsing history."""
        self._browse_tree(self._history.go_forward())
        return('break')

    def go_to_node(self, node):
        """Select and view a node.
        
        Positional arguments:
            node: str -- Tree element to select and show.
        """
        try:
            self.tree.focus_set()
            self.tree.selection_set(node)
            self.see_node(node)
            self.tree.focus(node)
            self._ui.on_change_selection(node)
        except:
            pass

    def on_quit(self):
        """Write the applicaton's keyword arguments."""
        prefs['title_width'] = self.tree.column('#0', 'width')
        for i, column in enumerate(self.columns):
            prefs[column[2]] = self.tree.column(i, 'width')

        # Save section coloring mode.
        prefs['coloring_mode'] = self.coloringMode

    def open_children(self, parent):
        """Recursively show children nodes.
        
        Positional arguments:
            parent: str -- Root node of the branch to open.
        """
        self.tree.item(parent, open=True)
        self.update_node_values(parent, collect=False)
        for child in self.tree.get_children(parent):
            self.open_children(child)

    def refresh(self, event=None):
        """Update the tree display to view changes.
        
        Iterate the tree and re-configure the columns.
        """
        if self.skipUpdate:
            self.skipUpdate = False
            return

        if self._mdl.prjFile is None:
            return

        self.update_tree()
        self.tree.configure(selectmode='extended')

    def reset_view(self):
        """Clear the displayed tree, and reset the browsing history."""
        self._history.reset()
        for rootElement in self.tree.get_children(''):
            self.tree.item(rootElement, text='')
            # Make the root element "invisible".
        self.tree.configure({'selectmode': 'none'})
        self._mdl.reset_tree()

    def save_branch_status(self):
        self._branch_status.clear()
        for category in self.tree.get_children(''):
            self._branch_status[category] = self.tree.item(category, option='open')
            for branch in self.tree.get_children(category):
                self._branch_status[branch] = self.tree.item(branch, option='open')

    def see_node(self, node):
        """View a node.
        
        If the parent is being expanded for this, 
        remove collected values from the parent's row.
        
        Positional arguments:
            node: str -- Tree element to view.
        """
        try:
            self.tree.see(node)
            parent = self.tree.parent(node)
            self.update_node_values(parent, collect=False)
        except:
            pass

    def show_branch(self, node):
        """Go to node and open children.
        
        Positional arguments:
            node: str -- Root element of the branch to open.
        """
        self.go_to_node(node)
        self.open_children(node)
        return 'break'
        # this stops event propagation and allows for re-mapping e.g. the F10 key
        # (see: https://stackoverflow.com/questions/22907200/remap-default-keybinding-in-tkinter)

    def restore_branch_status(self):
        for branch in self._branch_status:
            try:
                self.tree.item(branch, open=self._branch_status[branch])
            except:
                pass

    def _bind_events(self):
        self.tree.bind('<<TreeviewSelect>>', self._on_select_node)
        self.tree.bind('<<TreeviewOpen>>', self._on_open_branch)
        self.tree.bind('<<TreeviewClose>>', self._on_close_branch)
        self.tree.bind(KEYS.DELETE[0], self._ctrl.delete_elements)
        self.tree.bind(MOUSE.RIGHT_CLICK, self.open_context_menu)
        self.tree.bind(MOUSE.MOVE_NODE, self._on_move_node)
        self.tree.bind(KEYS.CUT[0], self._ctrl.cut_element)
        self.tree.bind(KEYS.COPY[0], self._ctrl.copy_element)
        self.tree.bind(KEYS.PASTE[0], self._ctrl.paste_element)
        self.tree.bind(KEYS.PREVIOUS[0], self.load_prev)
        self.tree.bind(KEYS.NEXT[0], self.load_next)
        self.tree.bind(KEYS.FORWARD[0], self.go_forward)
        self.tree.bind(KEYS.BACK[0], self.go_back)

    def _browse_tree(self, node):
        """Select and show node. 
        
        Positional arguments:
            node: str -- History list element pointed to.
        
        - Do not add the move to the history list.
        - If node doesn't exist, reset the history.
        """
        if node and self.tree.exists(node):
            if self.tree.selection()[0] != node:
                self._history.lock()
                # make sure not to extend the history list
                self.go_to_node(node)
        else:
            self._history.reset()
            self._history.append_node(self.tree.selection()[0])

    def _create_menus(self):
        """Create public submenus and local context menus."""

        #--- Create public submenus.

        #--- Create a section type submenu.
        self.selectTypeMenu = tk.Menu(self.tree, tearoff=0)
        self.selectTypeMenu.add_command(label=_('Normal'), command=self._ctrl.set_type_normal)
        self.selectTypeMenu.add_command(label=_('Unused'), command=self._ctrl.set_type_unused)

        #--- Create a chapter/stage level submenu.
        self.selectLevelMenu = tk.Menu(self.tree, tearoff=0)
        self.selectLevelMenu.add_command(label=_('1st Level'), command=self._ctrl.set_level_1)
        self.selectLevelMenu.add_command(label=_('2nd Level'), command=self._ctrl.set_level_2)

        #--- Create a section status submenu.
        self.scStatusMenu = tk.Menu(self.tree, tearoff=0)
        self.scStatusMenu.add_command(label=_('Outline'), command=self._ctrl.set_scn_status_outline)
        self.scStatusMenu.add_command(label=_('Draft'), command=self._ctrl.set_scn_status_draft)
        self.scStatusMenu.add_command(label=_('1st Edit'), command=self._ctrl.set_scn_status_1st_edit)
        self.scStatusMenu.add_command(label=_('2nd Edit'), command=self._ctrl.set_scn_status_2nd_edit)
        self.scStatusMenu.add_command(label=_('Done'), command=self._ctrl.set_scn_status_done)

        #--- Create a character status submenu.
        self.crStatusMenu = tk.Menu(self.tree, tearoff=0)
        self.crStatusMenu.add_command(label=_('Major Character'), command=self._ctrl.set_chr_status_major)
        self.crStatusMenu.add_command(label=_('Minor Character'), command=self._ctrl.set_chr_status_minor)

        #--- Create local context menus.

        #--- Create a narrative context menu.
        self.nvCtxtMenu = ContextMenu(self.tree, tearoff=0)
        self.nvCtxtMenu.add_command(label=_('Add Section'), command=self._ctrl.add_new_section)
        self.nvCtxtMenu.add_command(label=_('Add Chapter'), command=self._ctrl.add_new_chapter)
        self.nvCtxtMenu.add_command(label=_('Add Part'), command=self._ctrl.add_new_part)
        self.nvCtxtMenu.add_command(label=_('Insert Stage'), command=self._ctrl.add_new_stage)
        self.nvCtxtMenu.add_cascade(label=_('Change Level'), menu=self.selectLevelMenu)
        self.nvCtxtMenu.add_cascade(label=_('Export this chapter'), command=self.export_manuscript)
        self.nvCtxtMenu.add_separator()
        self.nvCtxtMenu.add_command(label=_('Delete'), accelerator=KEYS.DELETE[1], command=self._ctrl.delete_elements)
        self.nvCtxtMenu.add_separator()
        self.nvCtxtMenu.add_cascade(label=_('Set Type'), menu=self.selectTypeMenu)
        self.nvCtxtMenu.add_cascade(label=_('Set Status'), menu=self.scStatusMenu)
        self.nvCtxtMenu.add_separator()
        self.nvCtxtMenu.add_command(label=_('Join with previous'), command=self._ctrl.join_sections)
        self.nvCtxtMenu.add_separator()
        self.nvCtxtMenu.add_command(label=_('Chapter level'), command=self.show_chapter_level)
        self.nvCtxtMenu.add_command(label=_('Expand'), command=self.expand_selected)
        self.nvCtxtMenu.add_command(label=_('Collapse'), command=self.collapse_selected)
        self.nvCtxtMenu.add_command(label=_('Expand all'), command=self.expand_all)
        self.nvCtxtMenu.add_command(label=_('Collapse all'), command=self.collapse_all)

        #--- Create a world element context menu.
        self.wrCtxtMenu = ContextMenu(self.tree, tearoff=0)
        self.wrCtxtMenu.add_command(label=_('Add'), command=self._ctrl.add_new_element)
        self.wrCtxtMenu.add_separator()
        self.wrCtxtMenu.add_command(label=_('Export manuscript filtered by viewpoint'), command=self.export_manuscript)
        self.wrCtxtMenu.add_command(label=_('Export synopsis filtered by viewpoint'), command=self.export_synopsis)
        self.wrCtxtMenu.add_separator()
        self.wrCtxtMenu.add_command(label=_('Delete'), accelerator=KEYS.DELETE[1], command=self._ctrl.delete_elements)
        self.wrCtxtMenu.add_separator()
        self.wrCtxtMenu.add_cascade(label=_('Set Status'), menu=self.crStatusMenu)

        #--- Create a plot line context menu.
        self.plCtxtMenu = ContextMenu(self.tree, tearoff=0)
        self.plCtxtMenu.add_command(label=_('Add Plot line'), command=self._ctrl.add_new_plot_line)
        self.plCtxtMenu.add_command(label=_('Add Plot point'), command=self._ctrl.add_new_plot_point)
        self.plCtxtMenu.add_separator()
        self.plCtxtMenu.add_command(label=_('Export manuscript filtered by plot line'), command=self.export_manuscript)
        self.plCtxtMenu.add_command(label=_('Export synopsis filtered by plot line'), command=self.export_synopsis)
        self.plCtxtMenu.add_separator()
        self.plCtxtMenu.add_command(label=_('Change sections to Unused'), command=self._ctrl.exclude_plot_line)
        self.plCtxtMenu.add_command(label=_('Change sections to Normal'), command=self._ctrl.include_plot_line)
        self.plCtxtMenu.add_separator()
        self.plCtxtMenu.add_command(label=_('Delete'), accelerator=KEYS.DELETE[1], command=self._ctrl.delete_elements)

        #--- Create a project note context menu.
        self.pnCtxtMenu = ContextMenu(self.tree, tearoff=0)
        self.pnCtxtMenu.add_command(label=_('Add Project note'), command=self._ctrl.add_new_project_note)
        self.pnCtxtMenu.add_separator()
        self.pnCtxtMenu.add_command(label=_('Delete'), accelerator=KEYS.DELETE[1], command=self._ctrl.delete_elements)

    def _on_close_branch(self, event):
        """Event handler for manually collapsing a branch."""
        self.update_node_values(self.tree.selection()[0], collect=True)

    def _on_move_node(self, event):
        """Event handler for manually moving a node."""
        self._ctrl.move_node(
            self.tree.selection()[0],
            self.tree.identify_row(event.y)
            )

    def _on_open_branch(self, event):
        """Event handler for manually expanding a branch."""
        self.update_node_values(self.tree.selection()[0], collect=False)

    def _on_select_node(self, event):
        """Event handler for node selection.
        
        - Add the node ID to the browsing history.
        - Call the controller.
        """
        try:
            nodeId = self.tree.selection()[0]
        except IndexError:
            return

        self._history.append_node(nodeId)
        self._ui.on_change_selection(nodeId)


"""Provide a tkinter based novelibre tree view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from apptk.view.view_component_base import ViewComponentBase
from apptk.widgets.context_menu import ContextMenu
from novxlib.novx_globals import CHAPTER_PREFIX
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import CH_ROOT
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import ITEM_PREFIX
from novxlib.novx_globals import IT_ROOT
from novxlib.novx_globals import LC_ROOT
from novxlib.novx_globals import LOCATION_PREFIX
from novxlib.novx_globals import MANUSCRIPT_SUFFIX
from novxlib.novx_globals import PLOT_LINE_PREFIX
from novxlib.novx_globals import PLOT_POINT_PREFIX
from novxlib.novx_globals import PL_ROOT
from novxlib.novx_globals import PN_ROOT
from novxlib.novx_globals import PRJ_NOTE_PREFIX
from novxlib.novx_globals import ROOT_PREFIX
from novxlib.novx_globals import SECTIONS_SUFFIX
from novxlib.novx_globals import SECTION_PREFIX
from novxlib.novx_globals import _
from novxlib.novx_globals import list_to_string
from novxlib.novx_globals import string_to_list
from nvlib.model.nv_treeview import NvTreeview
from nvlib.nv_globals import get_section_date_str
from nvlib.nv_globals import prefs
from nvlib.nv_globals import to_string
from nvlib.view.platform.platform_settings import KEYS
from nvlib.view.platform.platform_settings import MOUSE
from nvlib.view.tree_window.history_list import HistoryList
import tkinter as tk
import tkinter.font as tkFont


class TreeViewer(ViewComponentBase, ttk.Frame):
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

    _ROOT_TITLES = {
        CH_ROOT: _('Book'),
        CR_ROOT: _('Characters'),
        LC_ROOT: _('Locations'),
        IT_ROOT: _('Items'),
        PL_ROOT: _('Plot lines'),
        PN_ROOT: _('Project notes'),
        }

    _SCENE = [
        '-',
        _('A'),
        _('R'),
        'x',
        ]

    _NOTE_INDICATOR = _('N')

    def __init__(self, parent, model, view, controller, **kw):
        """Put a tkinter tree in the specified parent widget.
        
        Positional arguments:
            parent -- parent widget for displaying the tree view.
            view -- GUI class reference.        
        """
        ViewComponentBase.__init__(self, model, view, controller)
        ttk.Frame.__init__(self, parent, **kw)
        self._wordsTotal = None
        self.skipUpdate = False

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
        self._build_menus()

        #--- Bind events.
        self._bind_events()

    def close_children(self, parent):
        """Recursively close children nodes.
        
        Positional arguments:
            parent: str -- Root node of the branch to close.
        """
        self.tree.item(parent, open=False)
        self._update_node_values(parent, collect=True)
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

    def go_forward(self, event=None):
        """Select a node forward in the tree browsing history."""
        self._browse_tree(self._history.go_forward())

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
            self._update_node_values(parent, collect=False)
        except:
            pass

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
        except:
            pass

    def next_node(self, thisNode):
        """Return the next node ID  of the same element type as thisNode.
        
        Positional arguments: 
            thisNode: str -- node ID
        """

        def search_tree(parent, result, flag):
            """Search the tree for the node ID after thisNode."""
            for child in self.tree.get_children(parent):
                if result:
                    break
                if child.startswith(prefix):
                    if prefix == CHAPTER_PREFIX:
                        if self._mdl.novel.chapters[child].chLevel != self._mdl.novel.chapters[thisNode].chLevel:
                            continue

                    elif prefix == SECTION_PREFIX:
                        if self._mdl.novel.sections[thisNode].scType > 1:
                            if self._mdl.novel.sections[child].scType != self._mdl.novel.sections[thisNode].scType:
                                continue

                        elif self._mdl.novel.sections[thisNode].scType < 2:
                            if self._mdl.novel.sections[child].scType > 1:
                                continue

                    if flag:
                        result = child
                        break

                    elif child == thisNode:
                        flag = True
                else:
                    result, flag = search_tree(child, result, flag)
            return result, flag

        prefix = thisNode[:2]
        root = self.tree.parent(thisNode)
        while not root.startswith(ROOT_PREFIX):
            root = self.tree.parent(root)
        nextNode, __ = search_tree(root, None, False)
        return nextNode

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
        self._update_node_values(parent, collect=False)
        for child in self.tree.get_children(parent):
            self.open_children(child)

    def prev_node(self, thisNode):
        """Return the previous node ID of the same element type as thisNode.

        Positional arguments: 
            thisNode: str -- node ID
        """

        def search_tree(parent, result, prevNode):
            """Search the tree for the node ID before thisNode."""
            for child in self.tree.get_children(parent):
                if result:
                    break

                if child.startswith(prefix):
                    if prefix == CHAPTER_PREFIX:
                        if self._mdl.novel.chapters[child].chLevel != self._mdl.novel.chapters[thisNode].chLevel:
                            continue

                    elif prefix == SECTION_PREFIX:
                        if self._mdl.novel.sections[thisNode].scType > 1:
                            if self._mdl.novel.sections[child].scType != self._mdl.novel.sections[thisNode].scType:
                                continue

                        elif self._mdl.novel.sections[thisNode].scType < 2:
                            if self._mdl.novel.sections[child].scType > 1:
                                continue

                    if child == thisNode:
                        result = prevNode
                        break
                    else:
                        prevNode = child
                else:
                    result, prevNode = search_tree(child, result, prevNode)
            return result, prevNode

        prefix = thisNode[:2]
        root = self.tree.parent(thisNode)
        while not root.startswith(ROOT_PREFIX):
            root = self.tree.parent(root)
        prevNode, __ = search_tree(root, None, None)
        return prevNode

    def reset_view(self):
        """Clear the displayed tree, and reset the browsing history."""
        self._history.reset()
        for rootElement in self.tree.get_children(''):
            self.tree.item(rootElement, text='')
            # Make the root element "invisible".
        self.tree.configure({'selectmode': 'none'})
        self._ctrl.reset_tree()

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

    def show_chapter_level(self, event=None):
        """Open all Book/part nodes and close all chapter nodes in the tree viewer."""

        def show_chapters(parent):
            if parent.startswith(CHAPTER_PREFIX):
                self.tree.item(parent, open=False)
                self._update_node_values(parent, collect=True)
            else:
                self.tree.item(parent, open=True)
                for child in self.tree.get_children(parent):
                    show_chapters(child)

        show_chapters(CH_ROOT)
        return 'break'

    def refresh(self, event=None):
        """Update the tree display to view changes.
        
        Iterate the tree and re-configure the columns.
        """

        def update_branch(node, scnPos=0):
            """Recursive tree walker.
            
            Positional arguments: 
                node: str -- Node ID to start from.
            Optional arguments:
                scnPos: int -- Word count so far.
            
            Return the incremented word count.
            """
            for elemId in self.tree.get_children(node):
                if elemId.startswith(SECTION_PREFIX):
                    title, nodeValues, nodeTags = self._get_section_row_data(elemId, position=scnPos)
                    if self._mdl.novel.sections[elemId].scType == 0:
                        scnPos += self._mdl.novel.sections[elemId].wordCount
                elif elemId.startswith(CHARACTER_PREFIX):
                    title, nodeValues, nodeTags = self._get_character_row_data(elemId)
                elif elemId.startswith(LOCATION_PREFIX):
                    title, nodeValues, nodeTags = self._get_location_row_data(elemId)
                elif elemId.startswith(ITEM_PREFIX):
                    title, nodeValues, nodeTags = self._get_item_row_data(elemId)
                elif elemId.startswith(CHAPTER_PREFIX):
                    chpPos = scnPos
                    # save chapter start position, because the positions of the
                    # chapters sections will now be added to scnPos.
                    scnPos = update_branch(elemId, scnPos)
                    isCollapsed = not self.tree.item(elemId, 'open')
                    title, nodeValues, nodeTags = self._get_chapter_row_data(elemId, position=chpPos, collect=isCollapsed)
                elif elemId.startswith(PLOT_LINE_PREFIX):
                    update_branch(elemId, scnPos)
                    isCollapsed = not self.tree.item(elemId, 'open')
                    title, nodeValues, nodeTags = self._get_plot_line_row_data(elemId, collect=isCollapsed)
                elif elemId.startswith(PLOT_POINT_PREFIX):
                    title, nodeValues, nodeTags = self._get_plot_point_row_data(elemId)
                elif elemId.startswith(PRJ_NOTE_PREFIX):
                    title, nodeValues, nodeTags = self._get_prj_note_row_data(elemId)
                else:
                    title = self._ROOT_TITLES[elemId]
                    nodeValues = []
                    nodeTags = 'root'
                    update_branch(elemId, scnPos)
                self.tree.item(elemId, text=title, values=nodeValues, tags=nodeTags)
            return scnPos

        if self.skipUpdate:
            self.skipUpdate = False
        elif self._mdl.prjFile is not None:
            self._wordsTotal = self._mdl.get_counts()[0]
            update_branch('')
            self.tree.configure(selectmode='extended')

    def _bind_events(self):
        self.tree.bind('<<TreeviewSelect>>', self._on_select_node)
        self.tree.bind('<<TreeviewOpen>>', self._on_open_branch)
        self.tree.bind('<<TreeviewClose>>', self._on_close_branch)
        self.tree.bind(KEYS.DELETE[0], self._ctrl.delete_elements)
        self.tree.bind(MOUSE.RIGHT_CLICK, self._on_open_context_menu)
        self.tree.bind(MOUSE.MOVE_NODE, self._on_move_node)

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

    def _build_menus(self):
        """Create public submenus and local context menus."""

        #--- Create public submenus.

        #--- Create a section type submenu.
        self.selectTypeMenu = tk.Menu(self.tree, tearoff=0)
        self.selectTypeMenu.add_command(label=_('Normal'), command=lambda:self._ctrl.set_type(0))
        self.selectTypeMenu.add_command(label=_('Unused'), command=lambda:self._ctrl.set_type(1))

        #--- Create a chapter/stage level submenu.
        self.selectLevelMenu = tk.Menu(self.tree, tearoff=0)
        self.selectLevelMenu.add_command(label=_('1st Level'), command=lambda:self._ctrl.set_level(1))
        self.selectLevelMenu.add_command(label=_('2nd Level'), command=lambda:self._ctrl.set_level(2))

        #--- Create a section status submenu.
        self.scStatusMenu = tk.Menu(self.tree, tearoff=0)
        self.scStatusMenu.add_command(label=_('Outline'), command=lambda:self._ctrl.set_completion_status(1))
        self.scStatusMenu.add_command(label=_('Draft'), command=lambda:self._ctrl.set_completion_status(2))
        self.scStatusMenu.add_command(label=_('1st Edit'), command=lambda:self._ctrl.set_completion_status(3))
        self.scStatusMenu.add_command(label=_('2nd Edit'), command=lambda:self._ctrl.set_completion_status(4))
        self.scStatusMenu.add_command(label=_('Done'), command=lambda:self._ctrl.set_completion_status(5))

        #--- Create a character status submenu.
        self.crStatusMenu = tk.Menu(self.tree, tearoff=0)
        self.crStatusMenu.add_command(label=_('Major Character'), command=lambda:self._ctrl.set_character_status(True))
        self.crStatusMenu.add_command(label=_('Minor Character'), command=lambda:self._ctrl.set_character_status(False))

        #--- Create local context menus.

        #--- Create a narrative context menu.
        self._nvCtxtMenu = ContextMenu(self.tree, tearoff=0)
        self._nvCtxtMenu.add_command(label=_('Add Section'), command=self._ctrl.add_section)
        self._nvCtxtMenu.add_command(label=_('Add Chapter'), command=self._ctrl.add_chapter)
        self._nvCtxtMenu.add_command(label=_('Add Part'), command=self._ctrl.add_part)
        self._nvCtxtMenu.add_command(label=_('Insert Stage'), command=self._ctrl.add_stage)
        self._nvCtxtMenu.add_cascade(label=_('Change Level'), menu=self.selectLevelMenu)
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_command(label=_('Delete'), accelerator=KEYS.DELETE[1], command=self._ctrl.delete_elements)
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_cascade(label=_('Set Type'), menu=self.selectTypeMenu)
        self._nvCtxtMenu.add_cascade(label=_('Set Status'), menu=self.scStatusMenu)
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_command(label=_('Join with previous'), command=self._ctrl.join_sections)
        self._nvCtxtMenu.add_separator()
        self._nvCtxtMenu.add_command(label=_('Chapter level'), command=self.show_chapter_level)
        self._nvCtxtMenu.add_command(label=_('Expand'), command=lambda: self.open_children(self.tree.selection()[0]))
        self._nvCtxtMenu.add_command(label=_('Collapse'), command=lambda: self.close_children(self.tree.selection()[0]))
        self._nvCtxtMenu.add_command(label=_('Expand all'), command=lambda: self.open_children(''))
        self._nvCtxtMenu.add_command(label=_('Collapse all'), command=lambda: self.close_children(''))

        #--- Create a world element context menu.
        self._wrCtxtMenu = ContextMenu(self.tree, tearoff=0)
        self._wrCtxtMenu.add_command(label=_('Add'), command=self._ctrl.add_element)
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_command(label=_('Export manuscript filtered by viewpoint'), command=self._export_manuscript)
        self._wrCtxtMenu.add_command(label=_('Export synopsis filtered by viewpoint'), command=self._export_synopsis)
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_command(label=_('Delete'), accelerator=KEYS.DELETE[1], command=self._ctrl.delete_elements)
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_cascade(label=_('Set Status'), menu=self.crStatusMenu)

        #--- Create a plot line context menu.
        self._plCtxtMenu = ContextMenu(self.tree, tearoff=0)
        self._plCtxtMenu.add_command(label=_('Add Plot line'), command=self._ctrl.add_plot_line)
        self._plCtxtMenu.add_command(label=_('Add Plot point'), command=self._ctrl.add_plot_point)
        self._plCtxtMenu.add_separator()
        self._plCtxtMenu.add_command(label=_('Export manuscript filtered by plot line'), command=self._export_manuscript)
        self._plCtxtMenu.add_command(label=_('Export synopsis filtered by plot line'), command=self._export_synopsis)
        self._plCtxtMenu.add_separator()
        self._plCtxtMenu.add_command(label=_('Delete'), accelerator=KEYS.DELETE[1], command=self._ctrl.delete_elements)

        #--- Create a project note context menu.
        self._pnCtxtMenu = ContextMenu(self.tree, tearoff=0)
        self._pnCtxtMenu.add_command(label=_('Add Project note'), command=self._ctrl.add_project_note)
        self._pnCtxtMenu.add_separator()
        self._pnCtxtMenu.add_command(label=_('Delete'), accelerator=KEYS.DELETE[1], command=self._ctrl.delete_elements)

    def _collect_ch_note_indicators(self, chId):
        """Return a string that indicates section notes within the chapter.
        
        Positional arguments:
            chId: str -- Chapter ID            
        """
        if self._mdl.novel.chapters[chId].notes:
            return self._NOTE_INDICATOR

        if self._mdl.novel.chapters[chId].chType == 0:
            for scId in self.tree.get_children(chId):
                if self._mdl.novel.sections[scId].scType != 1:
                    if self._mdl.novel.sections[scId].notes:
                        return self._NOTE_INDICATOR

        return ''

    def _collect_pl_note_indicators(self, plId):
        """Return a string that indicates plot point notes within the plot line.
        
        Positional arguments:
            plId: str -- lot line ID            
        """
        if self._mdl.novel.plotLines[plId].notes:
            return self._NOTE_INDICATOR

        for ppId in self.tree.get_children(plId):
            if self._mdl.novel.plotPoints[ppId].notes:
                return self._NOTE_INDICATOR

        return ''

    def _collect_plot_lines(self, chId):
        """Return a tuple of two strings: semicolon-separated plot lines, semicolon-separated plot points.
        
        Positional arguments:
            chId: str -- Chapter ID            
        """
        chPlotlineShortNames = []
        chPlotPointTitles = []
        chPlotlines = {}
        for plId in self._mdl.novel.plotLines:
            chPlotlines[plId] = []
        if self._mdl.novel.chapters[chId].chType == 0:
            for scId in self.tree.get_children(chId):
                if self._mdl.novel.sections[scId].scType == 0:
                    scPlotlines = self._mdl.novel.sections[scId].scPlotLines
                    for plId in scPlotlines:
                        shortName = self._mdl.novel.plotLines[plId].shortName
                        if not shortName in chPlotlineShortNames:
                            chPlotlineShortNames.append(shortName)
                    for ppId in self._mdl.novel.sections[scId].scPlotPoints:
                        chPlotlines[plId].append(ppId)
            if len(chPlotlineShortNames) == 1:
                for plId in chPlotlines:
                    for ppId in chPlotlines[plId]:
                        chPlotPointTitles.append(self._mdl.novel.plotPoints[ppId].title)
            else:
                for plId in chPlotlines:
                    for ppId in chPlotlines[plId]:
                        chPlotPointTitles.append(f'{self._mdl.novel.plotLines[plId].shortName}: {self._mdl.novel.plotPoints[ppId].title}')
        return list_to_string(chPlotlineShortNames), list_to_string(chPlotPointTitles)

    def _collect_tags(self, chId):
        """Return a string with semicolon-separated section tags.
        
        Positional arguments:
            chId: str -- Chapter ID            
        """
        chapterTags = []
        if self._mdl.novel.chapters[chId].chType == 0:
            for scId in self.tree.get_children(chId):
                if self._mdl.novel.sections[scId].scType == 0:
                    if self._mdl.novel.sections[scId].tags:
                        for tag in self._mdl.novel.sections[scId].tags:
                            if not tag in chapterTags:
                                chapterTags.append(tag)
        return list_to_string(chapterTags)

    def _collect_viewpoints(self, chId):
        """Return a string with semicolon-separated viewpoint character names.

        Positional arguments:
            chId: str -- Chapter ID            
        """
        chapterViewpoints = []
        if self._mdl.novel.chapters[chId].chType == 0:
            for scId in self.tree.get_children(chId):
                if self._mdl.novel.sections[scId].scType == 0:
                    try:
                        crId = self._mdl.novel.sections[scId].characters[0]
                        viewpoint = self._mdl.novel.characters[crId].title
                        if not viewpoint in chapterViewpoints:
                            chapterViewpoints.append(viewpoint)
                    except:
                        pass
        return list_to_string(chapterViewpoints)

    def _count_words(self, chId):
        """Return accumulated word count of all normal sections in a chapter.
        
        Positional arguments:
            chId: str -- Chapter ID            
        """
        chapterWordCount = 0
        if self._mdl.novel.chapters[chId].chType == 0:
            for scId in self.tree.get_children(chId):
                if self._mdl.novel.sections[scId].scType == 0:
                    chapterWordCount += self._mdl.novel.sections[scId].wordCount
        return chapterWordCount

    def _date_is_valid(self, section):
        """Return True if the date can be displayed in the tree view.
        
        Positional arguments:
            section: Section instance         
        """
        if section.date is None:
            return False

        if section.date == section.NULL_DATE:
            return False

        return True

    def _export_manuscript(self, event=None):
        self._ctrl.export_document(MANUSCRIPT_SUFFIX, filter=self.tree.selection()[0], ask=False)

    def _export_synopsis(self, event=None):
        self._ctrl.export_document(SECTIONS_SUFFIX, filter=self.tree.selection()[0], ask=False)

    def _get_chapter_row_data(self, chId, position=None, collect=False):
        """Return title, nodeValues, and tags for a chapter row.
        
        Positional arguments:
            chId: str -- Chapter ID
            
        Optional arguments:
            position: integer -- Accumulated word count at chapter beginning.
            collect: bool -- If True, summarize section metadata.
        """
        nodeValues = [''] * len(self.columns)
        nodeTags = []
        if self._mdl.novel.chapters[chId].chType != 0:
            # Chapter is Unused type.
            nodeTags.append('unused')
            if self._mdl.novel.chapters[chId].chLevel == 1:
                nodeTags.append('part')
        else:
            # Chapter is Normal type (or other).
            nodeTags.append('chapter')
            try:
                positionStr = f'{round(100 * position / self._wordsTotal, 1)}%'
            except:
                positionStr = ''
            wordCount = self._count_words(chId)
            if self._mdl.novel.chapters[chId].chLevel == 1:
                nodeTags.append('part')

                # Add all section wordcounts until the next part.
                srtChapters = self.tree.get_children(CH_ROOT)
                i = srtChapters.index(chId) + 1
                while i < len(srtChapters):
                    c = srtChapters[i]
                    if self._mdl.novel.chapters[c].chLevel == 1:
                        break
                    i += 1
                    wordCount += self._count_words(c)
            nodeValues[self._colPos['wc']] = wordCount
            nodeValues[self._colPos['po']] = positionStr
            if collect:
                nodeValues[self._colPos['vp']] = self._collect_viewpoints(chId)
        if collect:
            nodeValues[self._colPos['tg']] = self._collect_tags(chId)
            nodeValues[self._colPos['ac']], nodeValues[self._colPos['tp']] = self._collect_plot_lines(chId)
            nodeValues[self._colPos['nt']] = self._collect_ch_note_indicators(chId)
        else:
            nodeValues[self._colPos['nt']] = self._get_notes_indicator(self._mdl.novel.chapters[chId])
        return to_string(self._mdl.novel.chapters[chId].title), nodeValues, tuple(nodeTags)

    def _get_character_row_data(self, crId):
        """Return title, values, and tags for a character row.
        
        Positional arguments:
            crId: str -- Character ID            
        """
        nodeValues = [''] * len(self.columns)

        # Notes indicator.
        nodeValues[self._colPos['nt']] = self._get_notes_indicator(self._mdl.novel.characters[crId])

        # Count the sections that use this character as viewpoint.
        wordCount = 0
        for scId in self._mdl.novel.sections:
            if self._mdl.novel.sections[scId].scType == 0:
                if self._mdl.novel.sections[scId].characters:
                    if self._mdl.novel.sections[scId].characters[0] == crId:
                        wordCount += self._mdl.novel.sections[scId].wordCount
        if wordCount > 0:
            nodeValues[self._colPos['wc']] = wordCount

            # Words percentage per viewpoint character
            try:
                percentageStr = f'{round(100 * wordCount / self._wordsTotal, 1)}%'
            except:
                percentageStr = ''
            nodeValues[self._colPos['vp']] = percentageStr

        # Tags.
        try:
            nodeValues[self._colPos['tg']] = list_to_string(self._mdl.novel.characters[crId].tags)
        except:
            pass

        # Set color according to the character's status.
        nodeTags = []
        if self._mdl.novel.characters[crId].isMajor:
            nodeTags.append('major')
        else:
            nodeTags.append('minor')
        return to_string(self._mdl.novel.characters[crId].title), nodeValues, tuple(nodeTags)

    def _get_date_or_day(self, scId):
        """Return section date or day as a string for display."""
        if self._date_is_valid(self._mdl.novel.sections[scId]):
            return get_section_date_str(self._mdl.novel.sections[scId])

        if self._mdl.novel.sections[scId].day is not None:
            return f'{_("Day")} {self._mdl.novel.sections[scId].day}'

        return ''

        """Return the element's title, if any."""
        title = self._mdl.novel.sections[scId].title
        if not title:
            title = _('Unnamed')

    def _get_item_row_data(self, itId):
        """Return title, values, and tags for an item row.
        
        Positional arguments:
            itId: str -- Item ID            
        """
        nodeValues = [''] * len(self.columns)

        # Notes indicator.
        nodeValues[self._colPos['nt']] = self._get_notes_indicator(self._mdl.novel.items[itId])

        # tags.
        try:
            nodeValues[self._colPos['tg']] = list_to_string(self._mdl.novel.items[itId].tags)
        except:
            pass
        return to_string(self._mdl.novel.items[itId].title), nodeValues, ()

    def _get_location_row_data(self, lcId):
        """Return title, values, and tags for a location row.
        
        Positional arguments:
            lcId: str -- Location ID            
        """
        nodeValues = [''] * len(self.columns)

        # Notes indicator.
        nodeValues[self._colPos['nt']] = self._get_notes_indicator(self._mdl.novel.locations[lcId])

        # Tags.
        try:
            nodeValues[self._colPos['tg']] = list_to_string(self._mdl.novel.locations[lcId].tags)
        except:
            pass
        return to_string(self._mdl.novel.locations[lcId].title), nodeValues, ()

    def _get_notes_indicator(self, element):
        """Return a string that indicates whether the element has a note.
        
        Positional arguments:
            element: BasicElementNotes subclass instance      
        """
        if element.notes:
            return self._NOTE_INDICATOR

        return ''

    def _get_plot_line_row_data(self, plId, collect=False):
        """Return title, values, and tags for a plotline row.

        Positional arguments:
            plId: str -- Plotline ID
            
        Optional arguments:
            collect: bool -- If True, summarize section metadata.        
        """
        fullName = to_string(self._mdl.novel.plotLines[plId].title)
        title = f'({self._mdl.novel.plotLines[plId].shortName}) {fullName}'
        nodeValues = [''] * len(self.columns)
        if collect:
            nodeValues[self._colPos['nt']] = self._collect_pl_note_indicators(plId)
        else:
            nodeValues[self._colPos['nt']] = self._get_notes_indicator(self._mdl.novel.plotLines[plId])
        return title, nodeValues, ('arc')

    def _get_plot_point_row_data(self, ppId):
        """Return title, values, and tags for a plot point row.
        
        Positional arguments:
            ppId: str -- Plot point ID            
        """
        nodeValues = [''] * len(self.columns)

        # Notes indicator.
        nodeValues[self._colPos['nt']] = self._get_notes_indicator(self._mdl.novel.plotPoints[ppId])

        # Display associated section, if any.
        scId = self._mdl.novel.plotPoints[ppId].sectionAssoc
        if scId:
            sectionTitle = self._mdl.novel.sections[scId].title
            if sectionTitle is not None:
                nodeValues[self._colPos['tp']] = sectionTitle
        return to_string(self._mdl.novel.plotPoints[ppId].title), nodeValues, ('plot_point')

    def _get_prj_note_row_data(self, pnId):
        """Return title, values, and tags for a project note row.
        
        Positional arguments:
            pnId: str -- Project note ID            
        """
        nodeValues = [''] * len(self.columns)
        return to_string(self._mdl.novel.projectNotes[pnId].title), nodeValues, ()

    def _get_section_row_data(self, scId, position=None):
        """Return title, values, and tags for a section row.
        
        Positional arguments:
            scId: str -- Section ID
            
        Optional arguments:
            position: int -- Accumulated word count at section beginning.
        """

        # Time for displaying.
        if self._mdl.novel.sections[scId].time is not None:
            dispTime = self._mdl.novel.sections[scId].time.rsplit(':', 1)[0]
        else:
            dispTime = ''

        # Create a combined duration information.
        if self._mdl.novel.sections[scId].lastsDays and self._mdl.novel.sections[scId].lastsDays != '0':
            days = f'{self._mdl.novel.sections[scId].lastsDays}d '
        else:
            days = ''
        if self._mdl.novel.sections[scId].lastsHours and self._mdl.novel.sections[scId].lastsHours != '0':
            hours = f'{self._mdl.novel.sections[scId].lastsHours}h '
        else:
            hours = ''
        if self._mdl.novel.sections[scId].lastsMinutes and self._mdl.novel.sections[scId].lastsMinutes != '0':
            minutes = f'{self._mdl.novel.sections[scId].lastsMinutes}min'
        else:
            minutes = ''

        # Configure the node values and tags depending on the section type.
        nodeValues = [''] * len(self.columns)
        nodeTags = []
        if self._mdl.novel.sections[scId].scType > 1:
            stageLevel = self._mdl.novel.sections[scId].scType - 1
            # Stage.
            nodeTags.append(f'stage{stageLevel}')
        else:
            # Section is Normal or Unused type.
            positionStr = ''
            if self._mdl.novel.sections[scId].scType == 1:
                nodeTags.append('unused')
            else:
                # Set the row color according to the color mode.
                if self.coloringMode == 1:
                    nodeTags.append(f'status{self._mdl.novel.sections[scId].status}')
                elif self.coloringMode == 2 and self._mdl.novel.workPhase:
                    if self._mdl.novel.sections[scId].status == self._mdl.novel.workPhase:
                        nodeTags.append('On_schedule')
                    elif self._mdl.novel.sections[scId].status < self._mdl.novel.workPhase:
                        nodeTags.append('Behind_schedule')
                    else:
                        nodeTags.append('Before_schedule')
                try:
                    positionStr = f'{round(100 * position / self._wordsTotal, 1)}%'
                except:
                    pass
            nodeValues[self._colPos['po']] = positionStr
            nodeValues[self._colPos['wc']] = self._mdl.novel.sections[scId].wordCount
            nodeValues[self._colPos['st']] = self._mdl.novel.sections[scId].STATUS[self._mdl.novel.sections[scId].status]
            try:
                nodeValues[self._colPos['vp']] = self._mdl.novel.characters[self._mdl.novel.sections[scId].characters[0]].title
            except:
                nodeValues[self._colPos['vp']] = _('N/A')

            nodeValues[self._colPos['sc']] = self._SCENE[self._mdl.novel.sections[scId].scene]

            nodeValues[self._colPos['dt']] = self._get_date_or_day(scId)
            nodeValues[self._colPos['tm']] = dispTime
            nodeValues[self._colPos['dr']] = f'{days}{hours}{minutes}'

            # Display plot lines the section belongs to.
            scPlotlineShortNames = []
            scPlotPointTitles = []
            scPlotlines = self._mdl.novel.sections[scId].scPlotLines
            for plId in scPlotlines:
                shortName = self._mdl.novel.plotLines[plId].shortName
                if not shortName in scPlotlineShortNames:
                    scPlotlineShortNames.append(shortName)
            for ppId in self._mdl.novel.sections[scId].scPlotPoints:
                if len(scPlotlineShortNames) == 1:
                    scPlotPointTitles.append(self._mdl.novel.plotPoints[ppId].title)
                else:
                    plId = self._mdl.novel.sections[scId].scPlotPoints[ppId]
                    scPlotPointTitles.append(f'{self._mdl.novel.plotLines[plId].shortName}: {self._mdl.novel.plotPoints[ppId].title}')
            nodeValues[self._colPos['ac']] = list_to_string(scPlotlineShortNames)
            nodeValues[self._colPos['tp']] = list_to_string(scPlotPointTitles)

        # Notes indicator.
        nodeValues[self._colPos['nt']] = self._get_notes_indicator(self._mdl.novel.sections[scId])

        # Section tags.
        try:
            nodeValues[self._colPos['tg']] = list_to_string(self._mdl.novel.sections[scId].tags)
        except:
            pass
        return to_string(self._mdl.novel.sections[scId].title), nodeValues, tuple(nodeTags)

    def _on_close_branch(self, event):
        """Event handler for manually collapsing a branch."""
        self._update_node_values(self.tree.selection()[0], collect=True)

    def _on_move_node(self, event):
        """Event handler for manually moving a node."""
        self._ctrl.move_node(
            self.tree.selection()[0],
            self.tree.identify_row(event.y)
            )

    def _on_open_branch(self, event):
        """Event handler for manually expanding a branch."""
        self._update_node_values(self.tree.selection()[0], collect=False)

    def _on_open_context_menu(self, event):
        """Event handler for the tree's context menu.
        
        - Configure the context menu depending on the selected branch and the program state.
        - Open it.
        """
        if self._mdl is None:
            return

        row = self.tree.identify_row(event.y)
        if row:
            self.go_to_node(row)
            if row.startswith(ROOT_PREFIX):
                prefix = row
            else:
                prefix = row[:2]
            if prefix in (CH_ROOT, CHAPTER_PREFIX, SECTION_PREFIX):
                # Context is within the "Book" branch.
                if self._ctrl.isLocked:
                    # No changes allowed.
                    self._nvCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Type'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Section'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Chapter'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Part'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Insert Stage'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Change Level'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Join with previous'), state='disabled')
                elif prefix.startswith(CH_ROOT):
                    # Context is the "Book" branch.
                    self._nvCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Type'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Set Status'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Add Section'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Add Chapter'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Add Part'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Insert Stage'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Change Level'), state='disabled')
                    self._nvCtxtMenu.entryconfig(_('Join with previous'), state='disabled')
                else:
                    # Context is a chapter/section.
                    self._nvCtxtMenu.entryconfig(_('Delete'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Set Type'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Set Status'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Add Section'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Add Chapter'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Add Part'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Insert Stage'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Change Level'), state='normal')
                    self._nvCtxtMenu.entryconfig(_('Join with previous'), state='normal')
                    if prefix.startswith(CHAPTER_PREFIX):
                        # Context is a chapter.
                        self._nvCtxtMenu.entryconfig(_('Join with previous'), state='disabled')
                        if row == self._mdl.trashBin:
                            # Context is the "Trash" chapter.
                            self._nvCtxtMenu.entryconfig(_('Set Type'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Change Level'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Add Section'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Add Chapter'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Add Part'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Insert Stage'), state='disabled')
                    if prefix.startswith(SECTION_PREFIX):
                        if self._mdl.novel.sections[row].scType < 2:
                            # Context is a section.
                            self._nvCtxtMenu.entryconfig(_('Change Level'), state='disabled')
                        else:
                            # Context is a stage.
                            self._nvCtxtMenu.entryconfig(_('Set Type'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                            self._nvCtxtMenu.entryconfig(_('Join with previous'), state='disabled')
                try:
                    self._nvCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._nvCtxtMenu.grab_release()
            elif prefix in (CR_ROOT, CHARACTER_PREFIX, LC_ROOT, LOCATION_PREFIX, IT_ROOT, ITEM_PREFIX):
                # Context is character/location/item.
                if self._ctrl.isLocked:
                    # No changes allowed.
                    self._wrCtxtMenu.entryconfig(_('Add'), state='disabled')
                    self._wrCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._wrCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                    self._wrCtxtMenu.entryconfig(_('Export manuscript filtered by viewpoint'), state='disabled')
                    self._wrCtxtMenu.entryconfig(_('Export synopsis filtered by viewpoint'), state='disabled')
                else:
                    self._wrCtxtMenu.entryconfig(_('Add'), state='normal')
                    if prefix.startswith('wr'):
                        # Context is the root of a world element type branch.
                        self._wrCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    else:
                        # Context is a world element.
                        self._wrCtxtMenu.entryconfig(_('Delete'), state='normal')
                    if prefix.startswith(CHARACTER_PREFIX) or  row.endswith(CHARACTER_PREFIX):
                        # Context is a character.
                        self._wrCtxtMenu.entryconfig(_('Set Status'), state='normal')
                        self._wrCtxtMenu.entryconfig(_('Export manuscript filtered by viewpoint'), state='normal')
                        self._wrCtxtMenu.entryconfig(_('Export synopsis filtered by viewpoint'), state='normal')
                    else:
                        # Context is not a character.
                        self._wrCtxtMenu.entryconfig(_('Set Status'), state='disabled')
                        self._wrCtxtMenu.entryconfig(_('Export manuscript filtered by viewpoint'), state='disabled')
                        self._wrCtxtMenu.entryconfig(_('Export synopsis filtered by viewpoint'), state='disabled')
                try:
                    self._wrCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._wrCtxtMenu.grab_release()
            elif prefix in (PL_ROOT, PLOT_LINE_PREFIX, PLOT_POINT_PREFIX):
                # Context is Plot line/Plot point.
                if self._ctrl.isLocked:
                    # No changes allowed.
                    self._plCtxtMenu.entryconfig(_('Add Plot line'), state='disabled')
                    self._plCtxtMenu.entryconfig(_('Add Plot point'), state='disabled')
                    self._plCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._plCtxtMenu.entryconfig(_('Export manuscript filtered by plot line'), state='disabled')
                    self._plCtxtMenu.entryconfig(_('Export synopsis filtered by plot line'), state='disabled')
                elif prefix.startswith(PL_ROOT):
                    self._plCtxtMenu.entryconfig(_('Add Plot line'), state='normal')
                    self._plCtxtMenu.entryconfig(_('Add Plot point'), state='disabled')
                    self._plCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._plCtxtMenu.entryconfig(_('Export manuscript filtered by plot line'), state='disabled')
                    self._plCtxtMenu.entryconfig(_('Export synopsis filtered by plot line'), state='disabled')
                else:
                    self._plCtxtMenu.entryconfig(_('Add Plot line'), state='normal')
                    self._plCtxtMenu.entryconfig(_('Add Plot point'), state='normal')
                    self._plCtxtMenu.entryconfig(_('Delete'), state='normal')
                    if prefix == PLOT_LINE_PREFIX:
                        self._plCtxtMenu.entryconfig(_('Export manuscript filtered by plot line'), state='normal')
                        self._plCtxtMenu.entryconfig(_('Export synopsis filtered by plot line'), state='normal')
                    else:
                        self._plCtxtMenu.entryconfig(_('Export manuscript filtered by plot line'), state='disabled')
                        self._plCtxtMenu.entryconfig(_('Export synopsis filtered by plot line'), state='disabled')
                try:
                    self._plCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._plCtxtMenu.grab_release()
            elif prefix in (PN_ROOT, PRJ_NOTE_PREFIX):
                # Context is Project note.
                if self._ctrl.isLocked:
                    # No changes allowed.
                    self._pnCtxtMenu.entryconfig(_('Add Project note'), state='disabled')
                    self._pnCtxtMenu.entryconfig(_('Delete'), state='disabled')
                elif prefix.startswith(PN_ROOT):
                    self._pnCtxtMenu.entryconfig(_('Add Project note'), state='normal')
                    self._pnCtxtMenu.entryconfig(_('Delete'), state='normal')
                try:
                    self._pnCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._pnCtxtMenu.grab_release()

    def _on_select_node(self, event):
        """Event handler for node selection.
        
        - Show the node's properties.
        - Add the node ID to the browsing history.
        """
        try:
            nodeId = self.tree.selection()[0]
        except IndexError:
            return

        self._history.append_node(nodeId)
        self._ui.on_change_selection(nodeId)

    def _update_node_values(self, nodeId, collect=False):
        """Add/remove node values collected from the node's children.
        
        Positional arguments:
            nodeId: str -- Node ID.
        
        Optional arguments:
            collect: bool -- If True, add the collected values; if False, remove them.
        """
        if nodeId.startswith(CHAPTER_PREFIX):
            positionStr = self.tree.item(nodeId)['values'][self._colPos['po']]
            __, nodeValues, __ = self._get_chapter_row_data(nodeId, position=None, collect=collect)
            nodeValues[self._colPos['po']] = positionStr
            self.tree.item(nodeId, values=nodeValues)
            return

        if nodeId.startswith(PLOT_LINE_PREFIX):
            __, nodeValues, __ = self._get_plot_line_row_data(nodeId, collect=collect)
            self.tree.item(nodeId, values=nodeValues)
            return


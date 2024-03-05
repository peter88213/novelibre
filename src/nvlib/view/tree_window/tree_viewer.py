"""Provide a tkinter based novelibre tree view.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.model.nv_treeview import NvTreeview
from nvlib.nv_globals import prefs
from nvlib.view.tree_window.history_list import HistoryList
from nvlib.widgets.context_menu import ContextMenu
from novxlib.model.section import Section
from novxlib.novx_globals import AC_ROOT
from novxlib.novx_globals import ARC_POINT_PREFIX
from novxlib.novx_globals import ARC_PREFIX
from novxlib.novx_globals import CHAPTER_PREFIX
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import CH_ROOT
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import ITEM_PREFIX
from novxlib.novx_globals import IT_ROOT
from novxlib.novx_globals import LC_ROOT
from novxlib.novx_globals import LOCATION_PREFIX
from novxlib.novx_globals import MANUSCRIPT_SUFFIX
from novxlib.novx_globals import SECTIONS_SUFFIX
from novxlib.novx_globals import PN_ROOT
from novxlib.novx_globals import PRJ_NOTE_PREFIX
from novxlib.novx_globals import ROOT_PREFIX
from novxlib.novx_globals import SECTION_PREFIX
from novxlib.novx_globals import _
from novxlib.novx_globals import list_to_string
from novxlib.novx_globals import string_to_list
import tkinter as tk
import tkinter.font as tkFont


class TreeViewer(ttk.Frame):
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
        ar=(_('A/R'), 'pacing_width'),
        tp=(_('Plot points'), 'points_width'),
        )
    # Key: column ID
    # Value: (column title, column width)

    _ROOT_TITLES = {
        CH_ROOT: _('Book'),
        CR_ROOT: _('Characters'),
        LC_ROOT: _('Locations'),
        IT_ROOT: _('Items'),
        AC_ROOT: _('Plot lines'),
        PN_ROOT: _('Project notes'),
        }

    _SCN_PACING = [
        _('A'),
        _('R'),
        _('C'),
        ]
    _SCN_STATUS = [
        None,
        _('Outline'),
        _('Draft'),
        _('1st Edit'),
        _('2nd Edit'),
        _('Done')
        ]

    def __init__(self, parent, model, view, controller, kwargs, **kw):
        """Put a tkinter tree in the specified parent widget.
        
        Positional arguments:
            parent -- parent widget for displaying the tree view.
            view -- GUI class reference.        
        """
        super().__init__(parent, **kw)
        self._mdl = model
        self._ui = view
        self._ctrl = controller
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
        self.tree.tag_configure('chapter', foreground=kwargs['color_chapter'])
        self.tree.tag_configure('arc', font=('', fontSize, 'bold'), foreground=kwargs['color_arc'])
        self.tree.tag_configure('plot_point', foreground=kwargs['color_arc'])
        self.tree.tag_configure('unused', foreground=kwargs['color_unused'])
        self.tree.tag_configure('stage1', font=('', fontSize, 'bold'), foreground=kwargs['color_stage'])
        self.tree.tag_configure('stage2', foreground=kwargs['color_stage'])
        self.tree.tag_configure('part', font=('', fontSize, 'bold'))
        self.tree.tag_configure('major', foreground=kwargs['color_major'])
        self.tree.tag_configure('minor', foreground=kwargs['color_minor'])
        self.tree.tag_configure('status1', foreground=kwargs['color_outline'])
        self.tree.tag_configure('status2', foreground=kwargs['color_draft'])
        self.tree.tag_configure('status3', foreground=kwargs['color_1st_edit'])
        self.tree.tag_configure('status4', foreground=kwargs['color_2nd_edit'])
        self.tree.tag_configure('status5', foreground=kwargs['color_done'])
        self.tree.tag_configure('On_schedule', foreground=kwargs['color_on_schedule'])
        self.tree.tag_configure('Behind_schedule', foreground=kwargs['color_behind_schedule'])
        self.tree.tag_configure('Before_schedule', foreground=kwargs['color_before_schedule'])

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
        self._bind_events(**kwargs)

    def close_children(self, parent):
        """Recursively close children nodes.
        
        Positional arguments:
            parent: str -- Root node of the branch to close.
        """
        self.tree.item(parent, open=False)
        if parent.startswith(CHAPTER_PREFIX):
            self._configure_chapter_columns(parent, collect=True)
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

    def go_to_node(self, node):
        """Select and view a node.
        
        Positional arguments:
            node: str -- Tree element to select and show.
        """
        try:
            self.tree.focus_set()
            self.tree.selection_set(node)
            self.tree.see(node)
            self.tree.focus(node)
        except:
            pass

    def next_node(self, thisNode):
        """Return the next node ID  of the same element type as thisNode.
        
        Positional arguments: 
            thisNode: str -- node ID
            root: str -- root ID of the branch to search 
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
        if parent.startswith(CHAPTER_PREFIX):
            self._configure_chapter_columns(parent, collect=False)
        for child in self.tree.get_children(parent):
            self.open_children(child)

    def prev_node(self, thisNode):
        """Return the previous node ID of the same element type as thisNode.

        Positional arguments: 
            thisNode: str -- node ID
            root: str -- root ID of the branch to search 
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
                self._configure_chapter_columns(parent, collect=True)
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
                    title, columns, nodeTags = self._configure_section_display(elemId, position=scnPos)
                    if self._mdl.novel.sections[elemId].scType == 0:
                        scnPos += self._mdl.novel.sections[elemId].wordCount
                elif elemId.startswith(CHARACTER_PREFIX):
                    title, columns, nodeTags = self._configure_character_display(elemId)
                elif elemId.startswith(LOCATION_PREFIX):
                    title, columns, nodeTags = self._configure_location_display(elemId)
                elif elemId.startswith(ITEM_PREFIX):
                    title, columns, nodeTags = self._configure_item_display(elemId)
                elif elemId.startswith(CHAPTER_PREFIX):
                    chpPos = scnPos
                    # save chapter start position, because the positions of the
                    # chapters sections will now be added to scnPos.
                    scnPos = update_branch(elemId, scnPos)
                    doCollect = not self.tree.item(elemId, 'open')
                    title, columns, nodeTags = self._configure_chapter_display(elemId, position=chpPos, collect=doCollect)
                elif elemId.startswith(ARC_PREFIX):
                    update_branch(elemId, scnPos)
                    title, columns, nodeTags = self._configure_arc_display(elemId)
                elif elemId.startswith(ARC_POINT_PREFIX):
                    title, columns, nodeTags = self._configure_plot_point_display(elemId)
                elif elemId.startswith(PRJ_NOTE_PREFIX):
                    title, columns, nodeTags = self._configure_prj_note_display(elemId)
                else:
                    title = self._ROOT_TITLES[elemId]
                    columns = []
                    nodeTags = 'root'
                    update_branch(elemId, scnPos)
                self.tree.item(elemId, text=title, values=columns, tags=nodeTags)
            return scnPos

        if self.skipUpdate:
            self.skipUpdate = False
        elif self._mdl.prjFile is not None:
            self._wordsTotal = self._mdl.get_counts()[0]
            update_branch('')
            self.tree.configure(selectmode='extended')

    def _bind_events(self, **kwargs):
        self.tree.bind('<<TreeviewSelect>>', self._on_select_node)
        self.tree.bind('<<TreeviewOpen>>', self._on_open_branch)
        self.tree.bind('<<TreeviewClose>>', self._on_close_branch)
        self.tree.bind('<Delete>', self._ctrl.delete_elements)
        self.tree.bind(kwargs['button_context_menu'], self._on_open_context_menu)
        self.tree.bind('<Alt-B1-Motion>', self._on_move_node)

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
        self._nvCtxtMenu.add_command(label=_('Delete'), command=self._ctrl.delete_elements)
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
        self._wrCtxtMenu.add_command(label=_('Delete'), command=self._ctrl.delete_elements)
        self._wrCtxtMenu.add_separator()
        self._wrCtxtMenu.add_cascade(label=_('Set Status'), menu=self.crStatusMenu)

        #--- Create a plot line context menu.
        self._acCtxtMenu = ContextMenu(self.tree, tearoff=0)
        self._acCtxtMenu.add_command(label=_('Add Plot line'), command=self._ctrl.add_arc)
        self._acCtxtMenu.add_command(label=_('Add Plot point'), command=self._ctrl.add_turning_point)
        self._acCtxtMenu.add_separator()
        self._acCtxtMenu.add_command(label=_('Export manuscript filtered by plot line'), command=self._export_manuscript)
        self._acCtxtMenu.add_command(label=_('Export synopsis filtered by plot line'), command=self._export_synopsis)
        self._acCtxtMenu.add_separator()
        self._acCtxtMenu.add_command(label=_('Delete'), command=self._ctrl.delete_elements)

        #--- Create a project note context menu.
        self._pnCtxtMenu = ContextMenu(self.tree, tearoff=0)
        self._pnCtxtMenu.add_command(label=_('Add Project note'), command=self._ctrl.add_project_note)
        self._pnCtxtMenu.add_separator()
        self._pnCtxtMenu.add_command(label=_('Delete'), command=self._ctrl.delete_elements)

    def _configure_arc_display(self, acId):
        """Configure project note formatting and columns."""
        title = self._mdl.novel.arcs[acId].title
        if not title:
            title = _('Unnamed')
        title = f'({self._mdl.novel.arcs[acId].shortName}) {title}'
        columns = []
        for __ in self.columns:
            columns.append('')
        nodeTags = ['arc']
        return title, columns, tuple(nodeTags)

    def _configure_chapter_columns(self, nodeId, collect=False):
        """Add/remove column items collected from the chapter's sections.
        
        Positional arguments:
        nodeId: str -- Chapter ID.
        
        Optional arguments:
        collect: bool -- If True, add the collected metadata; if False, remove it.
        """
        if nodeId.startswith(CHAPTER_PREFIX):
            chId = nodeId
            positionStr = self.tree.item(nodeId)['values'][self._colPos['po']]
            __, columns, __ = self._configure_chapter_display(chId, position=None, collect=collect)
            columns[self._colPos['po']] = positionStr
            self.tree.item(nodeId, values=columns)

    def _configure_chapter_display(self, chId, position=None, collect=False):
        """Configure chapter formatting and columns.
        
        Positional arguments:
            chId: str -- Chapter ID
            
        Optional arguments:
            position: integer -- Word count at the beginning of the chapter.
            collect: bool -- If True, summarize section metadata.
        """

        def count_words(chId):
            """Accumulate word counts of all normal sections in a chapter."""
            chapterWordCount = 0
            if self._mdl.novel.chapters[chId].chType == 0:
                for scId in self.tree.get_children(chId):
                    if self._mdl.novel.sections[scId].scType == 0:
                        chapterWordCount += self._mdl.novel.sections[scId].wordCount
            return chapterWordCount

        def collect_viewpoints(chId):
            """Return a string with semicolon-separated viewpoint character names."""
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

        def collect_tags(chId):
            """Return a string with semicolon-separated section tags."""
            chapterTags = []
            if self._mdl.novel.chapters[chId].chType == 0:
                for scId in self.tree.get_children(chId):
                    if self._mdl.novel.sections[scId].scType == 0:
                        if self._mdl.novel.sections[scId].tags:
                            for tag in self._mdl.novel.sections[scId].tags:
                                if not tag in chapterTags:
                                    chapterTags.append(tag)
            return list_to_string(chapterTags)

        def collect_arcs(chId):
            """Return a tuple of two strings: semicolon-separated plot lines, semicolon-separated plot points."""
            chPlotlineShortNames = []
            chPlotPointTitles = []
            chPlotlines = {}
            for acId in self._mdl.novel.arcs:
                chPlotlines[acId] = []
            if self._mdl.novel.chapters[chId].chType == 0:
                for scId in self.tree.get_children(chId):
                    if self._mdl.novel.sections[scId].scType == 0:
                        scPlotlines = self._mdl.novel.sections[scId].scArcs
                        for acId in scPlotlines:
                            shortName = self._mdl.novel.arcs[acId].shortName
                            if not shortName in chPlotlineShortNames:
                                chPlotlineShortNames.append(shortName)
                        for tpId in self._mdl.novel.sections[scId].scTurningPoints:
                            chPlotlines[acId].append(tpId)
                if len(chPlotlineShortNames) == 1:
                    for acId in chPlotlines:
                        for tpId in chPlotlines[acId]:
                            chPlotPointTitles.append(self._mdl.novel.turningPoints[tpId].title)
                else:
                    for acId in chPlotlines:
                        for tpId in chPlotlines[acId]:
                            chPlotPointTitles.append(f'{self._mdl.novel.arcs[acId].shortName}: {self._mdl.novel.turningPoints[tpId].title}')
            return list_to_string(chPlotlineShortNames), list_to_string(chPlotPointTitles)

        def collect_note_indicators(chId):
            """Return a string that indicates section notes within the chapter."""
            indicator = ''
            if self._mdl.novel.chapters[chId].chType == 0:
                for scId in self.tree.get_children(chId):
                    if self._mdl.novel.sections[scId].scType == 0:
                        if self._mdl.novel.sections[scId].notes:
                            indicator = _('N')
            return indicator

        title = self._mdl.novel.chapters[chId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')
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
            wordCount = count_words(chId)
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
                    wordCount += count_words(c)
            columns[self._colPos['wc']] = wordCount
            columns[self._colPos['po']] = positionStr
            if collect:
                columns[self._colPos['vp']] = collect_viewpoints(chId)
        if collect:
            columns[self._colPos['tg']] = collect_tags(chId)
            columns[self._colPos['ac']], columns[self._colPos['tp']] = collect_arcs(chId)
            columns[self._colPos['nt']] = collect_note_indicators(chId)
        return title, columns, tuple(nodeTags)

    def _configure_character_display(self, crId):
        """Configure character formatting and columns."""
        title = self._mdl.novel.characters[crId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')

        if self._mdl.novel.characters[crId].notes:
            columns[self._colPos['nt']] = _('N')

        # Count the sections that use this character as viewpoint.
        wordCount = 0
        for scId in self._mdl.novel.sections:
            if self._mdl.novel.sections[scId].scType == 0:
                if self._mdl.novel.sections[scId].characters:
                    if self._mdl.novel.sections[scId].characters[0] == crId:
                        wordCount += self._mdl.novel.sections[scId].wordCount
        if wordCount > 0:
            columns[self._colPos['wc']] = wordCount

            # Words percentage per viewpoint character
            try:
                percentageStr = f'{round(100 * wordCount / self._wordsTotal, 1)}%'
            except:
                percentageStr = ''
            columns[self._colPos['vp']] = percentageStr

        # Tags.
        try:
            columns[self._colPos['tg']] = list_to_string(self._mdl.novel.characters[crId].tags)
        except:
            pass

        # Set color according to the character's status.
        nodeTags = []
        if self._mdl.novel.characters[crId].isMajor:
            nodeTags.append('major')
        else:
            nodeTags.append('minor')
        return title, columns, tuple(nodeTags)

    def _configure_item_display(self, itId):
        """Configure item formatting and columns."""
        title = self._mdl.novel.items[itId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')

        # tags.
        try:
            columns[self._colPos['tg']] = list_to_string(self._mdl.novel.items[itId].tags)
        except:
            pass
        return title, columns, ()

    def _configure_location_display(self, lcId):
        """Configure location formatting and columns."""
        title = self._mdl.novel.locations[lcId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')

        # Tags.
        try:
            columns[self._colPos['tg']] = list_to_string(self._mdl.novel.locations[lcId].tags)
        except:
            pass
        return title, columns, ()

    def _configure_prj_note_display(self, pnId):
        """Configure project note formatting and columns."""
        title = self._mdl.novel.projectNotes[pnId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')
        return title, columns, ()

    def _configure_section_display(self, scId, position=None):
        """Configure section formatting and columns."""
        title = self._mdl.novel.sections[scId].title
        if not title:
            title = _('Unnamed')

        # Date or day for displaying.
        if self._mdl.novel.sections[scId].date is not None and self._mdl.novel.sections[scId].date != Section.NULL_DATE:
            dispDate = self._mdl.novel.sections[scId].date
        else:
            if self._mdl.novel.sections[scId].day is not None:
                dispDate = f'{_("Day")} {self._mdl.novel.sections[scId].day}'
            else:
                dispDate = ''

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

        # Configure the columns depending on the section type.
        columns = []
        for __ in self.columns:
            columns.append('')
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
            columns[self._colPos['po']] = positionStr
            columns[self._colPos['wc']] = self._mdl.novel.sections[scId].wordCount
            columns[self._colPos['st']] = self._SCN_STATUS[self._mdl.novel.sections[scId].status]
            try:
                columns[self._colPos['vp']] = self._mdl.novel.characters[self._mdl.novel.sections[scId].characters[0]].title
            except:
                columns[self._colPos['vp']] = _('N/A')

            columns[self._colPos['ar']] = self._SCN_PACING[self._mdl.novel.sections[scId].scPacing]

            columns[self._colPos['dt']] = dispDate
            columns[self._colPos['tm']] = dispTime
            columns[self._colPos['dr']] = f'{days}{hours}{minutes}'

            # Display plot lines the section belongs to.
            scPlotlineShortNames = []
            scPlotPointTitles = []
            scPlotlines = self._mdl.novel.sections[scId].scArcs
            for acId in scPlotlines:
                shortName = self._mdl.novel.arcs[acId].shortName
                if not shortName in scPlotlineShortNames:
                    scPlotlineShortNames.append(shortName)
            for tpId in self._mdl.novel.sections[scId].scTurningPoints:
                if len(scPlotlineShortNames) == 1:
                    scPlotPointTitles.append(self._mdl.novel.turningPoints[tpId].title)
                else:
                    acId = self._mdl.novel.sections[scId].scTurningPoints[tpId]
                    scPlotPointTitles.append(f'{self._mdl.novel.arcs[acId].shortName}: {self._mdl.novel.turningPoints[tpId].title}')
            columns[self._colPos['ac']] = list_to_string(scPlotlineShortNames)
            columns[self._colPos['tp']] = list_to_string(scPlotPointTitles)

        # "Section has notes" indicator.
        if self._mdl.novel.sections[scId].notes:
            columns[self._colPos['nt']] = _('N')

        # Section tags.
        try:
            columns[self._colPos['tg']] = list_to_string(self._mdl.novel.sections[scId].tags)
        except:
            pass
        return title, columns, tuple(nodeTags)

    def _configure_plot_point_display(self, tpId):
        """Configure plot point formatting and columns."""
        title = self._mdl.novel.turningPoints[tpId].title
        if not title:
            title = _('Unnamed')
        columns = []
        for __ in self.columns:
            columns.append('')

        # "Point has notes" indicator.
        if self._mdl.novel.turningPoints[tpId].notes:
            columns[self._colPos['nt']] = _('N')

        # Display associated section, if any.
        scId = self._mdl.novel.turningPoints[tpId].sectionAssoc
        if scId:
            sectionTitle = self._mdl.novel.sections[scId].title
            if sectionTitle is not None:
                columns[self._colPos['tp']] = sectionTitle
        return title, columns, ('plot_point')

    def _export_manuscript(self, event=None):
        self._ctrl.export_document(MANUSCRIPT_SUFFIX, filter=self.tree.selection()[0], ask=False)

    def _export_synopsis(self, event=None):
        self._ctrl.export_document(SECTIONS_SUFFIX, filter=self.tree.selection()[0], ask=False)

    def _on_close_branch(self, event=None):
        """Event handler for manually collapsing a branch."""
        try:
            self._configure_chapter_columns(self.tree.selection()[0], collect=True)
        except:
            pass

    def _on_move_node(self, event):
        self._ctrl.move_node(
            self.tree.selection()[0],
            self.tree.identify_row(event.y)
            )

    def _on_open_branch(self, event=None):
        """Event handler for manually expanding a branch."""
        try:
            self._configure_chapter_columns(self.tree.selection()[0], collect=False)
        except:
            pass

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
            elif prefix in (AC_ROOT, ARC_PREFIX, ARC_POINT_PREFIX):
                # Context is Plot line/Plot point.
                if self._ctrl.isLocked:
                    # No changes allowed.
                    self._acCtxtMenu.entryconfig(_('Add Plot line'), state='disabled')
                    self._acCtxtMenu.entryconfig(_('Add Plot point'), state='disabled')
                    self._acCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._acCtxtMenu.entryconfig(_('Export manuscript filtered by plot line'), state='disabled')
                    self._acCtxtMenu.entryconfig(_('Export synopsis filtered by plot line'), state='disabled')
                elif prefix.startswith(AC_ROOT):
                    self._acCtxtMenu.entryconfig(_('Add Plot line'), state='normal')
                    self._acCtxtMenu.entryconfig(_('Add Plot point'), state='disabled')
                    self._acCtxtMenu.entryconfig(_('Delete'), state='disabled')
                    self._acCtxtMenu.entryconfig(_('Export manuscript filtered by plot line'), state='disabled')
                    self._acCtxtMenu.entryconfig(_('Export synopsis filtered by plot line'), state='disabled')
                else:
                    self._acCtxtMenu.entryconfig(_('Add Plot line'), state='normal')
                    self._acCtxtMenu.entryconfig(_('Add Plot point'), state='normal')
                    self._acCtxtMenu.entryconfig(_('Delete'), state='normal')
                    if prefix == ARC_PREFIX:
                        self._acCtxtMenu.entryconfig(_('Export manuscript filtered by plot line'), state='normal')
                        self._acCtxtMenu.entryconfig(_('Export synopsis filtered by plot line'), state='normal')
                    else:
                        self._acCtxtMenu.entryconfig(_('Export manuscript filtered by plot line'), state='disabled')
                        self._acCtxtMenu.entryconfig(_('Export synopsis filtered by plot line'), state='disabled')
                try:
                    self._acCtxtMenu.tk_popup(event.x_root, event.y_root, 0)
                finally:
                    self._acCtxtMenu.grab_release()
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

    def _on_select_node(self, event=None):
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


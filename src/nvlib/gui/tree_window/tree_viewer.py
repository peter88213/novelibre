"""Provide a tkinter based novelibre tree view.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.controller.sub_controller import SubController
from nvlib.gui.observer import Observer
from nvlib.gui.tree_window.history_list import HistoryList
from nvlib.model.data.py_calendar import PyCalendar
from nvlib.model.nv_treeview import NvTreeview
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import PN_ROOT
from nvlib.novx_globals import PRJ_NOTE_PREFIX
from nvlib.novx_globals import ROOT_PREFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.novx_globals import STATUS
from nvlib.novx_globals import list_to_string
from nvlib.novx_globals import string_to_list
from nvlib.nv_globals import NOT_ASSIGNED
from nvlib.nv_globals import prefs
from nvlib.nv_globals import to_string
from nvlib.nv_locale import _
import tkinter.font as tkFont


class TreeViewer(ttk.Frame, Observer, SubController):
    """Widget for novelibre tree view."""
    COLORING_MODES = [_('None'), _('Status'), _('Work phase')]
    # List[str] -- Section row coloring modes.

    _COLUMNS = dict(
        wc=(_('Words'), 'wc_width'),
        vp=(_('Viewpoint'), 'vp_width'),
        st=(_('Status'), 'status_width'),
        nt=(f"{_('N')}◳", 'nt_width'),
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
    _COMMENT_INDICATOR = '◳'

    def __init__(self, parent, model, view, **kw):
        """Put a tkinter tree in the specified parent widget.
        
        Positional arguments:
            parent -- parent widget for displaying the tree view.
            view -- GUI class reference.        
        """
        super().__init__(parent, **kw)
        self._mdl = model
        self._ui = view
        self._wordsTotal = None

        self.skipUpdate = False
        self._branch_status = {}
        # open/close

        # Create a novel tree.
        self.tree = NvTreeview(self)
        scrollX = ttk.Scrollbar(
            self,
            orient='horizontal',
            command=self.tree.xview,
        )
        scrollY = ttk.Scrollbar(
            self.tree,
            orient='vertical',
            command=self.tree.yview,
        )
        self.tree.configure(xscrollcommand=scrollX.set)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollX.pack(side='bottom', fill='x')
        scrollY.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)

        #--- Add columns to the tree.
        self.configure_columns()

        #--- configure tree row display.
        fontSize = tkFont.nametofont('TkDefaultFont').actual()['size']
        self.tree.tag_configure(
            'root',
            font=('', fontSize, 'bold'),
        )
        self.tree.tag_configure(
            'chapter',
            foreground=prefs['color_chapter'],
        )
        self.tree.tag_configure(
            'arc',
            font=('', fontSize, 'bold'),
            foreground=prefs['color_arc'],
        )
        self.tree.tag_configure(
            'plot_point',
            foreground=prefs['color_arc'],
        )
        self.tree.tag_configure(
            'unused',
            foreground=prefs['color_unused'],
        )
        self.tree.tag_configure(
            'epigraph',
            foreground=prefs['color_chapter'],
        )
        self.tree.tag_configure(
            'stage1',
            font=('', fontSize, 'bold'),
            foreground=prefs['color_stage'],
        )
        self.tree.tag_configure(
            'stage2',
            foreground=prefs['color_stage'],
        )
        self.tree.tag_configure(
            'part',
            font=('', fontSize, 'bold'),
        )
        self.tree.tag_configure(
            'major',
            foreground=prefs['color_major'],
        )
        self.tree.tag_configure(
            'minor',
            foreground=prefs['color_minor'],
        )
        self.tree.tag_configure(
            'status1',
            foreground=prefs['color_outline'],
        )
        self.tree.tag_configure(
            'status2',
            foreground=prefs['color_draft'],
        )
        self.tree.tag_configure(
            'status3',
            foreground=prefs['color_1st_edit'],
        )
        self.tree.tag_configure(
            'status4',
            foreground=prefs['color_2nd_edit'],
        )
        self.tree.tag_configure(
            'status5',
            foreground=prefs['color_done'],
        )
        self.tree.tag_configure(
            'On_schedule',
            foreground=prefs['color_on_schedule'],
        )
        self.tree.tag_configure(
            'Behind_schedule',
            foreground=prefs['color_behind_schedule'],
        )
        self.tree.tag_configure(
            'Before_schedule',
            foreground=prefs['color_before_schedule'],
        )

        #--- Browsing history.
        self._history = HistoryList()

        # -- Section coloring mode.
        try:
            self.coloringMode = int(prefs['coloring_mode'])
        except:
            self.coloringMode = 0
        if self.coloringMode > len(self.COLORING_MODES):
            self.coloringMode = 0

    def close_children(self, parent):
        """Recursively close children nodes.
        
        Positional arguments:
            parent: str -- Root node of the branch to close.
        """
        self.tree.item(parent, open=False)
        self._update_node_values(parent, collect=True)
        for child in self.tree.get_children(parent):
            self.close_children(child)

    def collapse_all(self, event=None):
        self.close_children('')

    def collapse_selected(self, event=None):
        self.close_children(self.tree.selection()[0])

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
            self.tree.column(
                column[1],
                width=int(prefs[column[2]]),
                minwidth=3,
                stretch=False
            )
        self.tree.column(
            '#0',
            width=int(prefs['title_width']),
            stretch=False
        )

    def expand_all(self, event=None):
        self.open_children('')
        try:
            node = self.tree.selection()[0]
        except:
            pass
        else:
            self.see_node(node)
            self.tree.focus(node)

    def expand_selected(self, event=None):
        self.open_children(self.tree.selection()[0])

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

    def load_next(self, event=None):
        """Load the next tree element of the same type."""
        thisNode = self.tree.selection()[0]
        nextNode = self.next_node(thisNode)
        if nextNode:
            self.go_to_node(nextNode)
        return('break')

    def load_prev(self, event=None):
        """Load the next tree element of the same type."""
        thisNode = self.tree.selection()[0]
        prevNode = self.prev_node(thisNode)
        if prevNode:
            self.go_to_node(prevNode)
        return('break')

    def next_node(self, thisNode):
        """Return the next node ID of the same element type as thisNode.
        
        Positional arguments: 
            thisNode: str -- node ID
        """

        def search_tree(parent, result, flag):
            # Search the tree for the node ID after thisNode.
            for child in self.tree.get_children(parent):
                if result:
                    break

                if child.startswith(prefix):
                    if prefix == CHAPTER_PREFIX:
                        if (self._mdl.novel.chapters[child].chLevel
                            != self._mdl.novel.chapters[thisNode].chLevel
                        ):
                            continue

                    elif prefix == SECTION_PREFIX:
                        if self._mdl.novel.sections[thisNode].scType > 1:
                            if (self._mdl.novel.sections[child].scType
                                != self._mdl.novel.sections[thisNode].scType
                            ):
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

    def on_close(self):
        """Actions to be performed when a project is closed."""
        self.reset_view()

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
            # Search the tree for the node ID before thisNode.
            for child in self.tree.get_children(parent):
                if result:
                    break

                if child.startswith(prefix):
                    if prefix == CHAPTER_PREFIX:
                        if (self._mdl.novel.chapters[child].chLevel
                            != self._mdl.novel.chapters[thisNode].chLevel
                        ):
                            continue

                    elif prefix == SECTION_PREFIX:
                        if self._mdl.novel.sections[thisNode].scType > 1:
                            if (self._mdl.novel.sections[child].scType
                                != self._mdl.novel.sections[thisNode].scType
                            ):
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
            self._branch_status[category] = self.tree.item(
                category, option='open')
            for branch in self.tree.get_children(category):
                self._branch_status[branch] = self.tree.item(
                    branch, option='open')

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

    def show_book(self, event=None):
        self.collapse_all()
        self.show_branch(CH_ROOT)

    def show_branch(self, node):
        """Go to node and open children.
        
        Positional arguments:
            node: str -- Root element of the branch to open.
        """
        self.go_to_node(node)
        self.open_children(node)
        return 'break'
        # this stops event propagation and allows for
        # re-mapping e.g. the F10 key
        # see:
        # https://stackoverflow.com/a/22910425

    def show_chapter_level(self, event=None):
        """Show the book on chapter level.
        
        Open all Book/part nodes and close 
        all chapter nodes in the tree viewer.
        """

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

    def show_characters(self, event=None):
        self.collapse_all()
        self.show_branch(CR_ROOT)

    def show_items(self, event=None):
        self.collapse_all()
        self.show_branch(IT_ROOT)

    def show_locations(self, event=None):
        self.collapse_all()
        self.show_branch(LC_ROOT)

    def show_plot_lines(self, event=None):
        self.collapse_all()
        self.show_branch(PL_ROOT)

    def show_project_notes(self, event=None):
        self.collapse_all()
        self.show_branch(PN_ROOT)

    def restore_branch_status(self):
        for branch in self._branch_status:
            try:
                self.tree.item(
                    branch,
                    open=self._branch_status[branch]
                )
            except:
                pass

    def update_tree(self):

        def update_branch(node, scnPos=0, isEpigraph=False):
            # Recursive tree walker.
            #     node: str -- Node ID to start from.
            #     scnPos: int -- Word count so far.
            # Return the incremented word count.
            for elemId in self.tree.get_children(node):
                if elemId.startswith(SECTION_PREFIX):
                    (
                        title,
                        nodeValues,
                        nodeTags
                    ) = self._get_section_row_data(
                        elemId,
                        isEpigraph,
                        position=scnPos
                    )
                    if self._mdl.novel.sections[elemId].scType == 0:
                        scnPos += self._mdl.novel.sections[elemId].wordCount
                        isEpigraph = False
                elif elemId.startswith(CHARACTER_PREFIX):
                    (
                        title,
                        nodeValues,
                        nodeTags
                    ) = self._get_character_row_data(elemId)
                elif elemId.startswith(LOCATION_PREFIX):
                    (
                        title,
                        nodeValues,
                        nodeTags
                    ) = self._get_location_row_data(elemId)
                elif elemId.startswith(ITEM_PREFIX):
                    (
                        title,
                        nodeValues,
                        nodeTags
                    ) = self._get_item_row_data(elemId)
                elif elemId.startswith(CHAPTER_PREFIX):
                    chpPos = scnPos
                    # save chapter start position, because the positions of
                    # the chapters sections will now be added to scnPos.
                    scnPos = update_branch(
                        elemId,
                        scnPos=scnPos,
                        isEpigraph=self._mdl.novel.chapters[elemId].hasEpigraph
                    )
                    isCollapsed = not self.tree.item(elemId, 'open')
                    (
                        title,
                        nodeValues,
                        nodeTags
                    ) = self._get_chapter_row_data(
                        elemId,
                        position=chpPos,
                        collect=isCollapsed
                    )
                elif elemId.startswith(PLOT_LINE_PREFIX):
                    update_branch(elemId, scnPos)
                    isCollapsed = not self.tree.item(elemId, 'open')
                    (
                        title,
                        nodeValues,
                        nodeTags
                    ) = self._get_plot_line_row_data(
                        elemId,
                        collect=isCollapsed
                    )
                elif elemId.startswith(PLOT_POINT_PREFIX):
                    (
                        title,
                        nodeValues,
                        nodeTags
                    ) = self._get_plot_point_row_data(elemId)
                elif elemId.startswith(PRJ_NOTE_PREFIX):
                    (
                        title,
                        nodeValues,
                        nodeTags
                    ) = self._get_prj_note_row_data(elemId)
                else:
                    title = self._ROOT_TITLES[elemId]
                    nodeValues = []
                    nodeTags = 'root'
                    update_branch(elemId, scnPos)
                self.tree.item(
                    elemId, text=title,
                    values=nodeValues,
                    tags=nodeTags
                )
            return scnPos

        self._wordsTotal = self._mdl.get_counts()[0]
        update_branch('')

    def _browse_tree(self, node):
        # Select and show a node.
        # - Do not add the move to the history list.
        # - If node doesn't exist, reset the history.
        # node: str -- History list element pointed to.
        if node and self.tree.exists(node):
            if self.tree.selection()[0] != node:
                self._history.lock()
                # make sure not to extend the history list
                self.go_to_node(node)
        else:
            self._history.reset()
            self._history.append_node(self.tree.selection()[0])

    def _collect_ch_comment_indicators(self, chId):
        """Return a string that indicates section comments within the chapter.
        
        Positional arguments:
            chId: str -- Chapter ID            
        """
        if self._mdl.novel.chapters[chId].chType == 0:
            for scId in self.tree.get_children(chId):
                if self._mdl.novel.sections[scId].scType != 1:
                    if self._mdl.novel.sections[scId].hasComment:
                        return self._COMMENT_INDICATOR

        return ''

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
        """Return a tuple of two strings. 
        
        (semicolon-separated plot lines, semicolon-separated plot points)
        
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
                        chPlotPointTitles.append(
                            self._mdl.novel.plotPoints[ppId].title)
            else:
                for plId in chPlotlines:
                    for ppId in chPlotlines[plId]:
                        chPlotPointTitles.append(
                            f'{self._mdl.novel.plotLines[plId].shortName}'
                            f': {self._mdl.novel.plotPoints[ppId].title}'
                        )
        return (
            list_to_string(chPlotlineShortNames),
            list_to_string(chPlotPointTitles)
        )

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
                        crId = self._mdl.novel.sections[scId].viepoint
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
                    chapterWordCount += (
                        self._mdl.novel.sections[scId].wordCount
                    )
        return chapterWordCount

    def _date_is_valid(self, section):
        # Return True if the date can be displayed in the tree view.
        # section: Section instance
        if section.date is None:
            return False

        if section.date == section.NULL_DATE:
            return False

        return True

    def _get_chapter_row_data(self, chId, position=None, collect=False):
        # Return title, nodeValues, and tags for a chapter row.
        #  chId: str -- Chapter ID
        #  position: integer -- Accumulated word count at chapter beginning.
        #  collect: bool -- If True, summarize section metadata.
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
            (
                nodeValues[self._colPos['ac']],
                nodeValues[self._colPos['tp']]
            ) = self._collect_plot_lines(chId)
            nodeValues[self._colPos['nt']] = (
                f'{self._collect_ch_note_indicators(chId)}'
                f'{self._collect_ch_comment_indicators(chId)}'
            )
        else:
            nodeValues[self._colPos['nt']] = self._get_notes_indicator(
                self._mdl.novel.chapters[chId])
        return to_string(
            self._mdl.novel.chapters[chId].title), nodeValues, tuple(nodeTags)

    def _get_character_row_data(self, crId):
        # Return title, values, and tags for a character row.
        nodeValues = [''] * len(self.columns)

        # Notes indicator.
        nodeValues[self._colPos['nt']] = self._get_notes_indicator(
            self._mdl.novel.characters[crId])

        # Count the sections that use this character as viewpoint.
        wordCount = 0
        for scId in self._mdl.novel.sections:
            if self._mdl.novel.sections[scId].scType == 0:
                if self._mdl.novel.sections[scId].characters:
                    if self._mdl.novel.sections[scId].viewpoint == crId:
                        wordCount += self._mdl.novel.sections[scId].wordCount
        if wordCount > 0:
            nodeValues[self._colPos['wc']] = wordCount

            # Words percentage per viewpoint character
            try:
                percentage = round(100 * wordCount / self._wordsTotal, 1)
                percentageStr = f'{percentage}%'
            except:
                percentageStr = ''
            nodeValues[self._colPos['vp']] = percentageStr

        # Tags.
        try:
            nodeValues[self._colPos['tg']] = list_to_string(
                self._mdl.novel.characters[crId].tags)
        except:
            pass

        # Set color according to the character's status.
        nodeTags = []
        if self._mdl.novel.characters[crId].isMajor:
            nodeTags.append('major')
        else:
            nodeTags.append('minor')
        return to_string(
            self._mdl.novel.characters[crId].title
            ), nodeValues, tuple(nodeTags)

    def _get_date_or_day(self, scId):
        # Return section date or day as a string for display.
        if self._date_is_valid(self._mdl.novel.sections[scId]):
            if prefs['localize_date']:
                return self._mdl.novel.sections[scId].localeDate
            else:
                return self._mdl.novel.sections[scId].date

        if self._mdl.novel.sections[scId].day is not None:
            return f'{_("Day")} {self._mdl.novel.sections[scId].day}'

        return ''

    def _get_item_row_data(self, itId):
        # Return title, values, and tags for an item row.
        nodeValues = [''] * len(self.columns)

        # Notes indicator.
        nodeValues[self._colPos['nt']] = self._get_notes_indicator(
            self._mdl.novel.items[itId])

        # tags.
        try:
            nodeValues[self._colPos['tg']] = list_to_string(
                self._mdl.novel.items[itId].tags)
        except:
            pass
        return to_string(
            self._mdl.novel.items[itId].title
            ), nodeValues, ()

    def _get_location_row_data(self, lcId):
        # Return title, values, and tags for a location row.
        nodeValues = [''] * len(self.columns)

        # Notes indicator.
        nodeValues[self._colPos['nt']] = self._get_notes_indicator(
            self._mdl.novel.locations[lcId])

        # Tags.
        try:
            nodeValues[self._colPos['tg']] = list_to_string(
                self._mdl.novel.locations[lcId].tags)
        except:
            pass
        return to_string(
            self._mdl.novel.locations[lcId].title
            ), nodeValues, ()

    def _get_comment_indicator(self, element):
        # Return a string that indicates whether the section contents
        # includes comments.
        if element.hasComment:
            return self._COMMENT_INDICATOR

        return ''

    def _get_notes_indicator(self, element):
        # Return a string that indicates whether the element has a note.
        if element.notes:
            return self._NOTE_INDICATOR

        return ''

    def _get_plot_line_row_data(self, plId, collect=False):
        # Return title, values, and tags for a plotline row.
        # collect: bool -- If True, summarize section metadata.
        fullName = to_string(self._mdl.novel.plotLines[plId].title)
        title = f'({self._mdl.novel.plotLines[plId].shortName}) {fullName}'
        nodeValues = [''] * len(self.columns)
        if collect:
            nodeValues[self._colPos['nt']] = (
                self._collect_pl_note_indicators(plId)
            )
        else:
            nodeValues[self._colPos['nt']] = (
                self._get_notes_indicator(self._mdl.novel.plotLines[plId])
            )
        return title, nodeValues, ('arc')

    def _get_plot_point_row_data(self, ppId):
        # Return title, values, and tags for a plot point row.
        nodeValues = [''] * len(self.columns)

        # Notes indicator.
        nodeValues[self._colPos['nt']] = self._get_notes_indicator(
            self._mdl.novel.plotPoints[ppId])

        # Display associated section, if any.
        scId = self._mdl.novel.plotPoints[ppId].sectionAssoc
        if scId:
            sectionTitle = self._mdl.novel.sections[scId].title
            if sectionTitle is not None:
                nodeValues[self._colPos['tp']] = sectionTitle
        return to_string(
            self._mdl.novel.plotPoints[ppId].title
            ), nodeValues, ('plot_point')

    def _get_prj_note_row_data(self, pnId):
        # Return title, values, and tags for a project note row.
        nodeValues = [''] * len(self.columns)
        return to_string(
            self._mdl.novel.projectNotes[pnId].title
            ), nodeValues, ()

    def _get_section_row_data(self, scId, isEpigraph, position=None):
        # Return title, values, and tags for a section row.
        # position: int -- Accumulated word count at section beginning.

        # Time for displaying.
        if self._mdl.novel.sections[scId].time is not None:
            dispTime = PyCalendar.time_disp(
                self._mdl.novel.sections[scId].time)
        else:
            dispTime = ''

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
                if isEpigraph:
                    nodeTags.append('epigraph')
                elif self.coloringMode == 1:
                    nodeTags.append(
                        f'status{self._mdl.novel.sections[scId].status}'
                    )
                elif self.coloringMode == 2 and self._mdl.novel.workPhase:
                    if (self._mdl.novel.sections[scId].status
                        == self._mdl.novel.workPhase
                    ):
                        nodeTags.append('On_schedule')
                    elif (self._mdl.novel.sections[scId].status
                          < self._mdl.novel.workPhase
                    ):
                        nodeTags.append('Behind_schedule')
                    else:
                        nodeTags.append('Before_schedule')
                try:
                    position = round(100 * position / self._wordsTotal, 1)
                    positionStr = f'{position}%'
                except:
                    pass
            nodeValues[self._colPos['po']] = positionStr
            nodeValues[self._colPos['wc']] = (
                self._mdl.novel.sections[scId].wordCount
            )
            nodeValues[self._colPos['st']] = STATUS[
                self._mdl.novel.sections[scId].status
            ]
            try:
                nodeValues[self._colPos['vp']] = (
                    self._mdl.novel.characters[
                        self._mdl.novel.sections[scId].viewpoint
                    ].title
                )
            except:
                nodeValues[self._colPos['vp']] = NOT_ASSIGNED

            nodeValues[self._colPos['sc']] = (
                self._SCENE[self._mdl.novel.sections[scId].scene]
            )
            nodeValues[self._colPos['dt']] = self._get_date_or_day(scId)
            nodeValues[self._colPos['tm']] = dispTime
            nodeValues[self._colPos['dr']] = PyCalendar.get_duration_str(
                self._mdl.novel.sections[scId])

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
                    scPlotPointTitles.append(
                        self._mdl.novel.plotPoints[ppId].title)
                else:
                    plId = self._mdl.novel.sections[scId].scPlotPoints[ppId]
                    scPlotPointTitles.append(
                        f'{self._mdl.novel.plotLines[plId].shortName}: '
                        f'{self._mdl.novel.plotPoints[ppId].title}'
                    )
            nodeValues[self._colPos['ac']] = list_to_string(
                scPlotlineShortNames)
            nodeValues[self._colPos['tp']] = list_to_string(
                scPlotPointTitles)

        # Notes indicator.
        nodeValues[self._colPos['nt']] = (
            f'{self._get_notes_indicator(self._mdl.novel.sections[scId])}'
            f'{self._get_comment_indicator(self._mdl.novel.sections[scId])}'
        )

        # Section tags.
        try:
            nodeValues[self._colPos['tg']] = list_to_string(
                self._mdl.novel.sections[scId].tags)
        except:
            pass
        return to_string(
            self._mdl.novel.sections[scId].title
        ), nodeValues, tuple(nodeTags)

    def _on_close_branch(self, event):
        # Event handler for manually collapsing a branch.
        self._update_node_values(self.tree.selection()[0], collect=True)

    def _on_open_branch(self, event):
        # Event handler for manually expanding a branch.
        self._update_node_values(self.tree.selection()[0], collect=False)

    def _on_select_node(self, event):
        # Event handler for node selection.
        # - Add the node ID to the browsing history.
        # - Call the controller.
        try:
            nodeId = self.tree.selection()[0]
        except IndexError:
            return

        self._history.append_node(nodeId)
        self._ui.on_change_selection(nodeId)

    def _update_node_values(self, nodeId, collect=False):
        # Add/remove node values collected from the node's children.
        # nodeId: str -- Node ID.
        # collect: bool -- If True, add the collected values;
        #                  if False, remove them.
        if nodeId.startswith(CHAPTER_PREFIX):
            positionStr = self.tree.item(nodeId)['values'][self._colPos['po']]
            __, nodeValues, __ = self._get_chapter_row_data(
                nodeId, position=None, collect=collect)
            nodeValues[self._colPos['po']] = positionStr
            self.tree.item(nodeId, values=nodeValues)
            return

        if nodeId.startswith(PLOT_LINE_PREFIX):
            __, nodeValues, __ = self._get_plot_line_row_data(
                nodeId, collect=collect)
            self.tree.item(nodeId, values=nodeValues)
            return


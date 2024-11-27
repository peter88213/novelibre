"""Provide a service class for novelibre tree element handling.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import filedialog

from mvclib.controller.service_base import ServiceBase
from nvlib.gui.pop_up.data_import_dialog import DataImportDialog
from nvlib.gui.widgets.nv_simpledialog import askinteger
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import Error
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import PN_ROOT
from nvlib.novx_globals import PRJ_NOTE_PREFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.novx_globals import _


class ElementManager(ServiceBase):

    _MAX_NR_NEW_SECTIONS = 20
    # maximum number of sections to add in bulk
    _INI_NR_NEW_SECTIONS = 1
    # initial value when asking for the number of sections to add

    def add_new_chapter(self, **kwargs):
        """Create a chapter instance and add it to the novel.
             
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            chType: int -- Chapter type. Default: 0.
            NoNumber: str -- Do not auto-number this chapter. Default: None.
            
        Return the chapter ID, if successful.
        """
        if self._ctrl.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_new_chapter(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_new_character(self, **kwargs):
        """Create a character instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title.
            isMajor: bool -- If True, make the new character a major character. Default: False.
            
        Return the element's ID, if successful.
        """
        if self._ctrl.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_new_character(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_new_child(self):
        """Add a child element to an element.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if self._mdl.prjFile is None:
            return

        if self._ctrl.check_lock():
            return

        try:
            selection = self._ui.selectedNode
        except:
            return

        if selection == CH_ROOT:
            return self.add_new_chapter(targetNode=selection)

        if selection.startswith(CHAPTER_PREFIX):
            return self.add_new_section(targetNode=selection)

        if selection.startswith(PLOT_LINE_PREFIX):
            return self.add_new_plot_point(targetNode=selection)

        if selection == CR_ROOT:
            return self.add_new_character(targetNode=selection)

        if selection == LC_ROOT:
            return self.add_new_location(targetNode=selection)

        if selection == IT_ROOT:
            return self.add_new_item(targetNode=selection)

        if selection == PL_ROOT:
            return self.add_new_plot_line(targetNode=selection)

        if selection == PN_ROOT:
            return self.add_new_project_note(targetNode=selection)

    def add_new_element(self):
        """Create an element instance and add it to the novel.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if self._mdl.prjFile is None:
            return

        if self._ctrl.check_lock():
            return

        try:
            selection = self._ui.selectedNode
        except:
            return

        if selection.startswith(SECTION_PREFIX):
            if self._mdl.novel.sections[selection].scType < 2:
                return self.add_new_section(targetNode=selection)

            return self.add_new_stage(targetNode=selection)

        if CHAPTER_PREFIX in selection:
            return self.add_new_chapter(targetNode=selection)

        if CHARACTER_PREFIX in selection:
            return self.add_new_character(targetNode=selection)

        if LOCATION_PREFIX in selection:
            return self.add_new_location(targetNode=selection)

        if ITEM_PREFIX in selection:
            return self.add_new_item(targetNode=selection)

        if PLOT_LINE_PREFIX in selection:
            return self.add_new_plot_line(targetNode=selection)

        if PRJ_NOTE_PREFIX in selection:
            return self.add_new_project_note(targetNode=selection)

        if selection.startswith(PLOT_POINT_PREFIX):
            return self.add_new_plot_point(targetNode=selection)

    def add_new_item(self, **kwargs):
        """Create an item instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        if self._ctrl.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_new_item(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_new_location(self, **kwargs):
        """Create a location instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        if self._ctrl.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_new_location(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_multiple_new_sections(self):
        """Ask how many sections are to be added, then call the controller."""
        n = askinteger(
            title=_('New'),
            prompt=_('How many sections to add?'),
            initialvalue=self._INI_NR_NEW_SECTIONS,
            minvalue=0,
            maxvalue=self._MAX_NR_NEW_SECTIONS
            )
        if n is not None:
            newNodes = []
            for __ in range(n):
                newNodes.append(self.add_new_section())
            return newNodes

    def add_new_parent(self):
        """Add a parent element to an element.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if self._mdl.prjFile is None:
            return

        if self._ctrl.check_lock():
            return

        try:
            selection = self._ui.selectedNode
        except:
            return

        if selection.startswith(SECTION_PREFIX):
            return self.add_new_chapter(targetNode=selection)

        if selection.startswith(PLOT_POINT_PREFIX):
            return self.add_new_plot_line(targetNode=selection)

    def add_new_part(self, **kwargs):
        """Create a part instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str: Part title. Default -- Auto-generated title. 
            chType: int: Part type. Default -- 0.  
            NoNumber: str: Do not auto-number this part. Default -- None.
           
        Return the chapter ID, if successful.
        """
        if self._ctrl.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_new_part(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_new_plot_line(self, **kwargs):
        """Create a plot line instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the plot line ID, if successful.
        """
        if self._ctrl.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_new_plot_line(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_new_plot_point(self, **kwargs):
        """Create a plot point instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            
        Return the plot point ID, if successful.
        """
        if self._ctrl.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_new_plot_point(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_new_project_note(self, **kwargs):
        """Create a Project note instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_new_project_note(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_new_section(self, **kwargs):
        """Create a section instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            desc: str -- Description.
            scType: int -- Section type. Default: 0.
            status: int -- Section status. Default: 1.
            scene: int -- Scene kind. Default = 0.
            appendToPrev: bool -- Append to previous section. Default: False.
            
        - Place the new node at the next free position after the selection, if possible.
        - Otherwise, do nothing. 
        
        Return the section ID, if successful.
        """
        if self._ctrl.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_new_section(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_new_stage(self, **kwargs):
        """Create a stage instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Stage title. Default: Auto-generated title. 
            desc: str -- Description.
            scType: int -- Scene type. Default: 3.
            
        Return the section ID, if successful.
        """
        if self._ctrl.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_new_stage(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def delete_elements(self, elements=None):
        """Delete elements and their children.
        
        Optional arguments:
            elements: list of IDs of the elements to delete.        
        """
        if self._ctrl.check_lock():
            return

        if elements is None:
            try:
                elements = self._ui.selectedNodes
            except:
                return

        if self._ui.tv.tree.prev(elements[0]):
            newSelection = self._ui.tv.tree.prev(elements[0])
        else:
            newSelection = self._ui.tv.tree.parent(elements[0])
        # node to be selected if the first selected element is deleted
        selectAfterDeleting = elements[0]
        deletedChildren = []
        ask = True
        for  elemId in elements:
            if elemId in deletedChildren:
                continue

            if elemId.startswith(SECTION_PREFIX):
                if self._mdl.novel.sections[elemId].scType < 2:
                    candidate = f'{_("Section")} "{self._mdl.novel.sections[elemId].title}"'
                else:
                    candidate = f'{_("Stage")} "{self._mdl.novel.sections[elemId].title}"'
            elif elemId.startswith(CHAPTER_PREFIX):
                candidate = f'{_("Chapter")} "{self._mdl.novel.chapters[elemId].title}"'
            elif elemId.startswith(CHARACTER_PREFIX):
                candidate = f'{_("Character")} "{self._mdl.novel.characters[elemId].title}"'
            elif elemId.startswith(LOCATION_PREFIX):
                candidate = f'{_("Location")} "{self._mdl.novel.locations[elemId].title}"'
            elif elemId.startswith(ITEM_PREFIX):
                candidate = f'{_("Item")} "{self._mdl.novel.items[elemId].title}"'
            elif elemId.startswith(PLOT_LINE_PREFIX):
                candidate = f'{_("Plot line")} "{self._mdl.novel.plotLines[elemId].title}"'
            elif elemId.startswith(PLOT_POINT_PREFIX):
                candidate = f'{_("Plot point")} "{self._mdl.novel.plotPoints[elemId].title}"'
            elif elemId.startswith(PRJ_NOTE_PREFIX):
                candidate = f'{_("Project note")} "{self._mdl.novel.projectNotes[elemId].title}"'
            else:
                return

            if len(elements) == 1:
                if not self._ui.ask_yes_no(_('Delete {}?').format(candidate)):
                    return

            elif ask:
                result = self._ui.ask_delete_all_skip_cancel(
                    text=f"\n\n{_('Delete {}?').format(candidate)}\n\n",
                    default=0,
                    title=_('Delete multiple elements')
                    )
                if result == 3:
                    return

                if result == 2:
                    continue

                if result == 1:
                    ask = False
            if elemId.startswith(CHAPTER_PREFIX) or elemId.startswith(PLOT_LINE_PREFIX):
                deletedChildren.extend(self._ui.tv.tree.get_children(elemId))
            self._mdl.delete_element(elemId)
            if elemId == elements[0]:
                selectAfterDeleting = newSelection
        self._ui.tv.go_to_node(selectAfterDeleting)

    def import_elements(self, prefix):
        """Import elements from an XML data file.
        
        Positional arguments:
            prefix: str -- Prefix specifying the element type to be imported.
        """
        self._ui.restore_status()
        filePath = filedialog.askopenfilename(
            filetypes=[(_('XML data file'), '.xml')]
            )
        if not filePath:
            return

        try:
            self._ctrl.dataImporter.read_source(filePath, prefix)
        except Exception as ex:
            self._ui.set_status(f'!{str(ex)}')
            return

        DataImportDialog(
            self._mdl, self._ui, self._ctrl,
            self._ctrl.dataImporter.sourceElements,
            prefix,
            )

    def join_sections(self, scId0=None, scId1=None):
        """Join section 0 with section 1.

        Optional arguments:
            scId0: str -- ID of the section to be extended
            scId1: str -- ID of the section to be discarded.
            
        If not both arguments are given, determine them from the tree selection.
        """
        if self._ctrl.check_lock():
            return

        if scId0 is None or scId1 is None:
            try:
                scId1 = self._ui.selectedNode
            except:
                return

            if not scId1.startswith(SECTION_PREFIX):
                return

            scId0 = self._ui.tv.prev_node(scId1)
            if not scId0:
                self._ui.show_error(_('There is no previous section'), title=_('Cannot join sections'))
                return

        if self._ui.ask_yes_no(f'{_("Join with previous")}?'):
            try:
                self._mdl.join_sections(scId0, scId1)
            except Error as ex:
                self._ui.show_error(str(ex), title=_('Cannot join sections'))
                return

            self.view_new_element(scId0)

    def move_node(self, node, targetNode):
        """Move a node to another position.
        
        Positional arguments:
            node: str - ID of the node to move.
            targetNode: str -- ID of the new parent/predecessor of the node.
        """
        if self._ctrl.isLocked:
            return

        if (node.startswith(SECTION_PREFIX) and targetNode.startswith(CHAPTER_PREFIX)
            ) or (node.startswith(PLOT_POINT_PREFIX) and targetNode.startswith(PLOT_LINE_PREFIX)):
            self._ui.tv.open_children(targetNode)
        self._ui.tv.skipUpdate = True
        self._mdl.move_node(node, targetNode)

    def set_character_status(self, isMajor, elemIds=None):
        """Set character status to Major.
        
        Optional arguments:
            isMajor: bool -- If True, make the characters major. Otherwise, make them minor.
            elemIds: list of character IDs to process.
        """
        if self._ctrl.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._ui.tv.open_children(CR_ROOT)
        self._mdl.set_character_status(isMajor, elemIds)

    def set_completion_status(self, newStatus, elemIds=None):
        """Set section completion status (Outline/Draft..).
        
        Positional arguments:
            newStatus: int -- New section status to be set.        
            elemIds: list of IDs to process.            
        """
        if self._ctrl.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._ui.tv.open_children(elemIds[0])
        self._mdl.set_completion_status(newStatus, elemIds)

    def set_level(self, newLevel, elemIds=None):
        """Set chapter or stage level.
        
        Positional arguments:
            newLevel: int -- New level to be set.
            elemIds: list of IDs to process.
        """
        if self._ctrl.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._mdl.set_level(newLevel, elemIds)

    def set_type(self, newType, elemIds=None):
        """Set section or chapter type Normal).
        
        Positional arguments:
            newType: int -- New type to be set.
            elemIds: list of IDs to process.
        """
        if self._ctrl.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._ui.tv.open_children(elemIds[0])
        self._mdl.set_type(newType, elemIds)

    def view_new_element(self, newNode):
        """View the element with ID newNode.
        
        - Open the properties window for the new element.
        - Show and select it in the tree view.
        - Prepare the current element's title entry for manual input.
        The order is mandatory for smooth operation.
        """
        if newNode:
            self._ui.tv.go_to_node(newNode)
            self._ui.propertiesView.show_properties(newNode)
            self._ui.propertiesView.focus_title()
        else:
            self._ui.set_status(f'!{_("Cannot create the element at this position")}.')


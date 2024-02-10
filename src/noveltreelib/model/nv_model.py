"""Provide a class for the noveltree model.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from noveltreelib.model.nv_work_file import NvWorkFile
from novxlib.model.arc import Arc
from novxlib.model.basic_element import BasicElement
from novxlib.model.chapter import Chapter
from novxlib.model.character import Character
from novxlib.model.id_generator import create_id
from novxlib.model.novel import Novel
from novxlib.model.section import Section
from novxlib.model.turning_point import TurningPoint
from novxlib.model.world_element import WorldElement
from novxlib.novx_globals import AC_ROOT
from novxlib.novx_globals import ARC_POINT_PREFIX
from novxlib.novx_globals import ARC_PREFIX
from novxlib.novx_globals import CHAPTER_PREFIX
from novxlib.novx_globals import CHARACTER_PREFIX
from novxlib.novx_globals import CH_ROOT
from novxlib.novx_globals import CR_ROOT
from novxlib.novx_globals import Error
from novxlib.novx_globals import ITEM_PREFIX
from novxlib.novx_globals import IT_ROOT
from novxlib.novx_globals import LC_ROOT
from novxlib.novx_globals import LOCATION_PREFIX
from novxlib.novx_globals import PN_ROOT
from novxlib.novx_globals import PRJ_NOTE_PREFIX
from novxlib.novx_globals import SECTION_PREFIX
from novxlib.novx_globals import _


class NvModel:
    """noveltree model representation."""

    def __init__(self):
        """Initialize instance variables.
        
        Positional arguments:
            tree: NvTreeview -- The tree view shared by model and view.
        """
        self.tree = None
        # strategy class
        self.prjFile = None
        self.novel = None
        self._clients = []
        # objects to be updated on model change

        self.trashBin = None
        self.wordCount = 0
        self._internalModificationFlag = False

    @property
    def isModified(self):
        # Boolean -- True if there are unsaved changes.
        return self._internalModificationFlag

    @isModified.setter
    def isModified(self, setFlag):
        self._internalModificationFlag = setFlag
        for client in self._clients:
            client.refresh()

    def add_arc(self, **kwargs):
        """Add an arc to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        - If the target node is of the same type as the new node, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the last position.   

        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', '')
        index = 'end'
        if targetNode.startswith(ARC_PREFIX):
            index = self.tree.index(targetNode) + 1
        acId = create_id(self.novel.arcs, prefix=ARC_PREFIX)
        self.novel.arcs[acId] = Arc(
            title=kwargs.get('title', f'{_("New Arc")} ({acId})'),
            desc='',
            shortName=acId,
            on_element_change=self.on_element_change,
            )
        self.tree.insert(AC_ROOT, index, acId)
        return acId

    def add_chapter(self, **kwargs):
        """Add a chapter to the novel.
             
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            chType: int -- Chapter type. Default: 0.
            NoNumber: str -- Do not auto-number this chapter. Default: None.
            
        - Place the new node at the next free position after the target node, if possible.
        - Otherwise, put the new node at the beginning of the "Book" tree. 
        
        Return the chapter ID, if successful.
        """
        targetNode = kwargs.get('targetNode', '')
        index = 'end'
        if targetNode.startswith(SECTION_PREFIX):
            targetNode = self.tree.parent(targetNode)
        if targetNode.startswith(CHAPTER_PREFIX):
            index = self.tree.index(targetNode) + 1
            targetNode = self.tree.parent(targetNode)
        chId = create_id(self.novel.chapters, prefix=CHAPTER_PREFIX)
        self.novel.chapters[chId] = Chapter(
            title=kwargs.get('title', f'{_("New Chapter")} ({chId})'),
            desc='',
            chLevel=2,
            chType=kwargs.get('chType', 0),
            noNumber=kwargs.get('NoNumber', False),
            isTrash=False,
            on_element_change=self.on_element_change,
            )
        self.tree.insert(CH_ROOT, index, chId)
        return chId

    def add_character(self, **kwargs):
        """Add a character to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title.
            isMajor: bool -- If True, make the new character a major character. Default: False.
            
        - If the target node is of the same type as the new node, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the last position.   

        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', '')
        index = 'end'
        if targetNode.startswith(CHARACTER_PREFIX):
            index = self.tree.index(targetNode) + 1
        crId = create_id(self.novel.characters, prefix=CHARACTER_PREFIX)
        self.novel.characters[crId] = Character(
            title=kwargs.get('title', f'{_("New Character")} ({crId})'),
            desc='',
            aka='',
            tags='',
            notes='',
            bio='',
            goals='',
            fullName='',
            isMajor=kwargs.get('isMajor', False),
            links={},
            on_element_change=self.on_element_change,
            )
        self.tree.insert(CR_ROOT, index, crId)
        return crId

    def add_item(self, **kwargs):
        """Add an item to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        - If the target node is of the same type as the new node, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the last position.   

        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', '')
        index = 'end'
        if targetNode.startswith(ITEM_PREFIX):
            index = self.tree.index(targetNode) + 1
        itId = create_id(self.novel.items, prefix=ITEM_PREFIX)
        self.novel.items[itId] = WorldElement(
            title=kwargs.get('title', f'{_("New Item")} ({itId})'),
            desc='',
            aka='',
            tags='',
            links={},
            on_element_change=self.on_element_change,
            )
        self.tree.insert(IT_ROOT, index, itId)
        return itId

    def add_location(self, **kwargs):
        """Add a location to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        - If the target node is of the same type as the new node, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the last position.   

        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', '')
        index = 'end'
        if targetNode.startswith(LOCATION_PREFIX):
            index = self.tree.index(targetNode) + 1
        lcId = create_id(self.novel.locations, prefix=LOCATION_PREFIX)
        self.novel.locations[lcId] = WorldElement(
            title=kwargs.get('title', f'{_("New Location")} ({lcId})'),
            desc='',
            aka='',
            tags='',
            links={},
            on_element_change=self.on_element_change,
            )
        self.tree.insert(LC_ROOT, index, lcId)
        return lcId

    def add_part(self, **kwargs):
        """Add a part to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str: Part title. Default -- Auto-generated title. 
            chType: int: Part type. Default -- 0.  
            NoNumber: str: Do not auto-number this part. Default -- None.
           
        - Place the new node at the next free position after the target node, if possible.
        - Otherwise, put the new node at the last position in the book tree. 
        
        Return the chapter ID, if successful.
        """
        targetNode = kwargs.get('targetNode', '')
        index = 'end'
        if targetNode.startswith(SECTION_PREFIX):
            targetNode = self.tree.parent(targetNode)
        if targetNode.startswith(CHAPTER_PREFIX):
            index = self.tree.index(targetNode) + 1
            targetNode = self.tree.parent(targetNode)
        chId = create_id(self.novel.chapters, prefix=CHAPTER_PREFIX)
        self.novel.chapters[chId] = Chapter(
            title=kwargs.get('title', f'{_("New Part")} ({chId})'),
            desc='',
            chLevel=1,
            chType=kwargs.get('chType', 0),
            noNumber=kwargs.get('NoNumber', False),
            isTrash=False,
            on_element_change=self.on_element_change,
            )
        self.tree.insert(CH_ROOT, index, chId)
        return chId

    def add_project_note(self, **kwargs):
        """Add a prjFile note to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        - If the target node is of the same type as the new node, 
          place the new node after the target node.
        - Otherwise, place the new node at the first position.   

        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', '')
        index = 'end'
        if targetNode.startswith(PRJ_NOTE_PREFIX):
            index = self.tree.index(targetNode) + 1
        pnId = create_id(self.novel.projectNotes, prefix=PRJ_NOTE_PREFIX)
        self.novel.projectNotes[pnId] = BasicElement(
            title=kwargs.get('title', f'{_("New Note")} ({pnId})'),
            desc='',
            on_element_change=self.on_element_change,
            )
        self.tree.insert(PN_ROOT, index, pnId)
        return pnId

    def add_section(self, **kwargs):
        """Add a section to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            desc: str -- Description.
            scType: int -- Section type. Default: 0.
            status: int -- Section status. Default: 1.
            scPacing: int -- Action/Reaction/Custom. Default = 0.
            appendToPrev: bool -- Append to previous section. Default: False.
            
        - Place the new node at the next free position after the target node, if possible.
        - If the target node is a chapter, place the new node at the chapter end.
        - Otherwise, do nothing. 
        
        Return the section ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            return

        if targetNode.startswith(SECTION_PREFIX):
            parent = self.tree.parent(targetNode)
            index = self.tree.index(targetNode) + 1
        elif targetNode.startswith(CHAPTER_PREFIX):
            parent = targetNode
            index = 'end'
        else:
            return

        parentType = self.novel.chapters[parent].chType
        if parentType != 0:
            newType = parentType
        else:
            newType = kwargs.get('scType', 0)
        scId = create_id(self.novel.sections, prefix=SECTION_PREFIX)
        self.novel.sections[scId] = Section(
            title=kwargs.get('title', f'{_("New Section")} ({scId})'),
            desc=kwargs.get('desc', ''),
            scType=newType,
            scPacing=kwargs.get('scPacing', 0),
            status=kwargs.get('status', 1),
            appendToPrev=kwargs.get('appendToPrev', False),
            characters=[],
            locations=[],
            items=[],
            on_element_change=self.on_element_change,
            )
        self.novel.sections[scId].sectionContent = '<p></p>'
        self.tree.insert(parent, index, scId)
        return scId

    def add_stage(self, **kwargs):
        """Add a stage to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Stage title. Default: Auto-generated title. 
            desc: str -- Description.
            scType: int -- Scene type. Default: 3.
            
        - Place the new node at the next free position after the target node, if possible.
        - Otherwise, do nothing. 
        
        Return the section ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            return

        if targetNode.startswith(SECTION_PREFIX):
            parent = self.tree.parent(targetNode)
            index = self.tree.index(targetNode) + 1
        elif targetNode.startswith(CHAPTER_PREFIX):
            parent = targetNode
            index = 0
        else:
            return

        scId = create_id(self.novel.sections, prefix=SECTION_PREFIX)
        self.novel.sections[scId] = Section(
            title=kwargs.get('title', f'{_("Stage")}'),
            desc=kwargs.get('desc', ''),
            scType=kwargs.get('scType', 3),
            status=0,
            scPacing=0,
            on_element_change=self.on_element_change,
            )
        self.tree.insert(parent, index, scId)
        return scId

    def add_turning_point(self, **kwargs):
        """Add a turning point to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title.
            
        - Place the new node at the next free position after the target node, if possible.
        - Otherwise, do nothing. 
        
        Return the turning point ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            return

        index = 'end'
        if targetNode.startswith(ARC_POINT_PREFIX):
            parent = self.tree.parent(targetNode)
            index = self.tree.index(targetNode) + 1
        elif targetNode.startswith(ARC_PREFIX):
            parent = targetNode
        else:
            return

        tpId = create_id(self.novel.turningPoints, prefix=ARC_POINT_PREFIX)
        self.novel.turningPoints[tpId] = TurningPoint(
            title=kwargs.get('title', f'{_("New Turning point")} ({tpId})'),
            desc='',
            on_element_change=self.on_element_change,
            )
        self.tree.insert(parent, index, tpId)
        return tpId

    def close_project(self):
        self.isModified = False
        self.tree.on_element_change = self.tree.do_nothing
        self.novel = None
        self.prjFile = None

    def delete_element(self, elemId):
        """Delete an element and its children.
        
        Positional arguments:
            elemId: str -- ID of the element to delete.
        
        - Move sections to the "Trash" chapter.
        - Delete parts/chapters and move their children sections to the "Trash" chapter.
        - Delete characters/locations/items and remove their section references.
        - Delete stages.
        - Delete arcs and remove their turning points and section references.
        - Delete turning points and remove their section references.
        - Delete prjFile notes.
        """

        def waste_sections(elemId):
            """Move all sections under the element specified by elemId to the 'trash bin'."""
            if elemId.startswith(SECTION_PREFIX):
                if self.novel.sections[elemId].scType < 2:
                    # Move the section to the trash bin.
                    self.tree.move(elemId, self.trashBin, 0)
                    self.novel.sections[elemId].scType = 1
                    # Remove turning point and arc references.
                    arcReferences = self.novel.sections[elemId].scArcs
                    tpReferences = self.novel.sections[elemId].scTurningPoints
                    self.novel.sections[elemId].scArcs = []
                    self.novel.sections[elemId].scTurningPoints = {}
                    for acId in arcReferences:
                        sections = self.novel.arcs[acId].sections
                        sections.remove(elemId)
                        self.novel.arcs[acId].sections = sections
                    for ptId in tpReferences:
                        self.novel.turningPoints[ptId].sectionAssoc = None
                else:
                    # Delete the stage.
                    self.tree.delete(elemId)
                    del self.novel.sections[elemId]
            else:
                # Delete chapter and go one level down.
                for childNode in self.tree.get_children(elemId):
                    waste_sections(childNode)
                del self.novel.chapters[elemId]

        if elemId == self.trashBin:
            # Remove the "trash bin".
            for scId in self.tree.get_children(elemId):
                del self.novel.sections[scId]
            del self.novel.chapters[elemId]
            self.tree.delete(elemId)
            self.trashBin = None
        elif elemId.startswith(CHARACTER_PREFIX):
            # Delete a character and remove references.
            self.tree.delete(elemId)
            del self.novel.characters[elemId]
            for scId in self.novel.sections:
                try:
                    scCharacters = self.novel.sections[scId].characters
                    scCharacters.remove(elemId)
                    self.novel.sections[scId].characters = scCharacters
                except:
                    pass
        elif elemId.startswith(LOCATION_PREFIX):
            # Delete a location and remove references.
            self.tree.delete(elemId)
            del self.novel.locations[elemId]
            for scId in self.novel.sections:
                try:
                    scLocations = self.novel.sections[scId].locations
                    scLocations.remove(elemId)
                    self.novel.sections[scId].locations = scLocations
                except:
                    pass
        elif elemId.startswith(ITEM_PREFIX):
            # Delete an item and remove references.
            self.tree.delete(elemId)
            del self.novel.items[elemId]
            for scId in self.novel.sections:
                try:
                    scItems = self.novel.sections[scId].items
                    scItems.remove(elemId)
                    self.novel.sections[scId].items = scItems
                except:
                    pass
        elif elemId.startswith(ARC_PREFIX):
            # Delete an arc and remove references.
            if self.novel.arcs[elemId].sections:
                for scId in self.novel.arcs[elemId].sections:
                    self.novel.sections[scId].scArcs.remove(elemId)
                for tpId in self.tree.get_children(elemId):
                    scId = self.novel.turningPoints[tpId].sectionAssoc
                    if scId is not None:
                        del(self.novel.sections[scId].scTurningPoints[tpId])
                    del self.novel.turningPoints[tpId]
            del self.novel.arcs[elemId]
            self.tree.delete(elemId)
        elif elemId.startswith(ARC_POINT_PREFIX):
            # Delete an turning point and remove references.
            scId = self.novel.turningPoints[elemId].sectionAssoc
            if scId is not None:
                del(self.novel.sections[scId].scTurningPoints[elemId])
            del self.novel.turningPoints[elemId]
            self.tree.delete(elemId)
        elif elemId.startswith(PRJ_NOTE_PREFIX):
            # Delete a prjFile note.
            self.tree.delete(elemId)
            del self.novel.projectNotes[elemId]
        else:
            # Part/chapter/section selected.
            if self.trashBin is None:
                # Create a "trash bin"; use the first free chapter ID.
                self.trashBin = create_id(self.novel.chapters, prefix=CHAPTER_PREFIX)
                self.novel.chapters[self.trashBin] = Chapter(
                    title=_('Trash'),
                    desc='',
                    chLevel=2,
                    chType=3,
                    noNumber=True,
                    isTrash=True,
                    on_element_change=self.on_element_change,
                    )
                self.tree.append(CH_ROOT, self.trashBin)
            if elemId.startswith(SECTION_PREFIX):
                if self.tree.parent(elemId) == self.trashBin:
                    # Remove section, if already in trash bin.
                    self.tree.delete(elemId)
                    del self.novel.sections[elemId]
                else:
                    # Move section to the "trash bin".
                    waste_sections(elemId)
            else:
                # Delete part/chapter and move child sections to the "trash bin".
                waste_sections(elemId)
                self.tree.delete(elemId)
            # Make sure the whole "trash bin" is unused.
            self.set_type(3, [self.trashBin])

    def get_counts(self):
        """Return a tuple with total numbers:
        
        Total number of words in "normal" sections, 
        Total number of used "normal" sections,
        Total number of used "normal" chapters,
        Total number of used "normal" parts.
        """
        partCount = 0
        chapterCount = 0
        sectionCount = 0
        wordCount = 0
        for chId in self.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].chType == 0:
                for scId in self.tree.get_children(chId):
                    if self.novel.sections[scId].scType == 0:
                        sectionCount += 1
                        wordCount += self.novel.sections[scId].wordCount
                if self.novel.chapters[chId].chLevel == 1:
                    partCount += 1
                else:
                    chapterCount += 1
        self.wordCount = wordCount
        return wordCount, sectionCount, chapterCount, partCount

    def get_status_counts(self):
        """Return a list with word count totals depending of section status.
        
        Position 0 -- None 
        Position 1 -- Total number of words in "outline" sections 
        Position 2 -- Total number of words in "draft" sections
        Position 3 -- Total number of words in "1st Edit" sections
        Position 4 -- Total number of words in "2nd Edit" sections
        Position 5 -- Total number of words in "Done" sections
        """
        counts = [None, 0, 0, 0, 0, 0]
        for scId in self.novel.sections:
            if self.novel.sections[scId].scType == 0:
                if self.novel.sections[scId].status is not None:
                    counts[self.novel.sections[scId].status] += self.novel.sections[scId].wordCount
        return counts

    def join_sections(self, ScId0, ScId1):
        """Join section 0 with section 1.
        
        Positional arguments:
            scId0: str -- ID of the section to be extended
            scId1: str -- ID of the section to be discarded.
            
        Discard section 1, keep section 0.
        Raise Error in case of error.
        """

        def join_str(text0, text1, newline='\n'):
            if text0 is None:
                text0 = ''
            if text1 is None:
                text1 = ''
            if text0 or text1:
                text0 = f'{text0}{newline}{text1}'.strip()
            return text0

        def join_lst(list0, list1):
            if list1:
                for elemId in list1:
                    if not list0:
                        list0 = []
                    if not elemId in list0:
                        list0.append(elemId)

        if not ScId1.startswith(SECTION_PREFIX):
            return

        # Check type.
        if self.novel.sections[ScId1].scType != self.novel.sections[ScId0].scType:
            raise Error(_('The sections are not of the same type'))

        # Check viewpoint.
        if self.novel.sections[ScId1].characters:
            if self.novel.sections[ScId1].characters:
                if self.novel.sections[ScId0].characters:
                    if self.novel.sections[ScId1].characters[0] != self.novel.sections[ScId0].characters[0]:
                        raise Error(_('The sections have different viewpoints'))

                else:
                    self.novel.sections[ScId0].characters.append(self.novel.sections[ScId1].characters[0])

        # Join titles.
        joinedTitles = f'{self.novel.sections[ScId0].title} & {self.novel.sections[ScId1].title}'
        self.novel.sections[ScId0].title = joinedTitles

        # Join content.
        content0 = self.novel.sections[ScId0].sectionContent
        content1 = self.novel.sections[ScId1].sectionContent
        # this is because sectionContent is a property
        self.novel.sections[ScId0].sectionContent = join_str(content0, content1, newline='')

        # Join description, goal, conflict, outcome, notes.
        self.novel.sections[ScId0].desc = join_str(self.novel.sections[ScId0].desc, self.novel.sections[ScId1].desc)
        self.novel.sections[ScId0].goal = join_str(self.novel.sections[ScId0].goal, self.novel.sections[ScId1].goal)
        self.novel.sections[ScId0].conflict = join_str(self.novel.sections[ScId0].conflict, self.novel.sections[ScId1].conflict)
        self.novel.sections[ScId0].outcome = join_str(self.novel.sections[ScId0].outcome, self.novel.sections[ScId1].outcome)
        self.novel.sections[ScId0].notes = join_str(self.novel.sections[ScId0].notes, self.novel.sections[ScId1].notes)

        # Join characters, locations, items, tags.
        join_lst(self.novel.sections[ScId0].characters, self.novel.sections[ScId1].characters)
        join_lst(self.novel.sections[ScId0].locations, self.novel.sections[ScId1].locations)
        join_lst(self.novel.sections[ScId0].items, self.novel.sections[ScId1].items)
        join_lst(self.novel.sections[ScId0].tags, self.novel.sections[ScId1].tags)

        # Move arc associations.
        for scArc in self.novel.sections[ScId1].scArcs:
            self.novel.arcs[scArc].sections.remove(ScId1)
            if not ScId0 in self.novel.arcs[scArc].sections:
                self.novel.arcs[scArc].sections.append(ScId0)
            if not scArc in self.novel.sections[ScId0].scArcs:
                self.novel.sections[ScId0].scArcs.append(scArc)

        # Move turning point associations.
        for ptId in self.novel.sections[ScId1].scTurningPoints:
            self.novel.turningPoints[ptId].sectionAssoc = ScId0
            self.novel.sections[ScId0].scTurningPoints[ptId] = self.novel.sections[ScId1].scTurningPoints[ptId]

        # Add duration.
        try:
            lastsMin1 = int(self.novel.sections[ScId1].lastsMinutes)
        except:
            lastsMin1 = 0
        try:
            lastsMin0 = int(self.novel.sections[ScId0].lastsMinutes)
        except:
            lastsMin0 = 0
        hoursLeft, lastsMin0 = divmod((lastsMin0 + lastsMin1), 60)
        self.novel.sections[ScId0].lastsMinutes = str(lastsMin0)
        try:
            lastsHours1 = int(self.novel.sections[ScId1].lastsHours)
        except:
            lastsHours1 = 0
        try:
            lastsHours0 = int(self.novel.sections[ScId0].lastsHours)
        except:
            lastsHours0 = 0
        daysLeft, lastsHours0 = divmod((lastsHours0 + lastsHours1 + hoursLeft), 24)
        self.novel.sections[ScId0].lastsHours = str(lastsHours0)
        try:
            lastsDays1 = int(self.novel.sections[ScId1].lastsDays)
        except:
            lastsDays1 = 0
        try:
            LastsDays0 = int(self.novel.sections[ScId0].lastsDays)
        except:
            LastsDays0 = 0
        LastsDays0 = LastsDays0 + lastsDays1 + daysLeft
        self.novel.sections[ScId0].lastsDays = str(LastsDays0)
        del(self.novel.sections[ScId1])
        # deleting section 1 object instance
        self.tree.delete(ScId1)
        # removing section 1 reference from the tree

    def move_node(self, node, targetNode):
        """Move a node to another position.
        
        Positional elements:
            node: str - ID of the node to move.
            targetNode: str -- ID of the new parent/predecessor of the node.
        """
        if node == self.trashBin:
            return

        if node[:2] == targetNode[:2]:
            self.tree.move(node, self.tree.parent(targetNode), self.tree.index(targetNode))
        elif (node.startswith(SECTION_PREFIX) and targetNode.startswith(CHAPTER_PREFIX)
              )or (node.startswith(ARC_POINT_PREFIX) and targetNode.startswith(ARC_PREFIX)):
            if not self.tree.get_children(targetNode):
                self.tree.move(node, targetNode, 0)
            elif self.tree.prev(targetNode):
                self.tree.move(node, self.tree.prev(targetNode), 'end')

    def new_project(self, tree):
        """Create a noveltree project instance."""
        self.novel = Novel(
            title='',
            desc='',
            authorName='',
            wordTarget=0,
            wordCountStart=0,
            languageCode='',
            countryCode='',
            renumberChapters=False,
            renumberParts=False,
            renumberWithinParts=False,
            romanChapterNumbers=False,
            romanPartNumbers=False,
            saveWordCount=True,
            workPhase=None,
            chapterHeadingPrefix=f"{_('Chapter')} ",
            chapterHeadingSuffix='',
            partHeadingPrefix=f"{_('Part')} ",
            partHeadingSuffix='',
            customGoal='',
            customConflict='',
            customOutcome='',
            customChrBio='',
            customChrGoals='',
            tree=tree,
            on_element_change=self.on_element_change,
            )
        self.novel.check_locale()
        # setting the the system locale as document language/country
        self.prjFile = NvWorkFile('')
        self.prjFile.novel = self.novel
        self._initialize_tree(self.on_element_change)

    def on_element_change(self):
        """Callback function to report model element modifications."""
        self.isModified = True

    def open_project(self, filePath):
        """Initialize instance variables.
        
        Positional arguments:
            filePath: str -- path to the prjFile file.
        """
        self.novel = Novel(tree=self.tree)
        self.prjFile = NvWorkFile(filePath)
        self.prjFile.novel = self.novel
        self.prjFile.read()
        if self.prjFile.wcLogUpdate and self.novel.saveWordCount:
            self.isModified = True
        else:
            self.isModified = False
        self._initialize_tree(self.on_element_change)

    def register_client(self, client):
        if not client in self._clients:
            self._clients.append(client)

    def renumber_chapters(self):
        """Modify chapter headings."""
        ROMAN = [
            (1000, 'M'),
            (900, 'CM'),
            (500, 'D'),
            (400, 'CD'),
            (100, 'C'),
            (90, 'XC'),
            (50, 'L'),
            (40, 'XL'),
            (10, 'X'),
            (9, 'IX'),
            (5, 'V'),
            (4, 'IV'),
            (1, 'I'),
        ]

        def number_to_roman(n):
            """Return n as a Roman number.
            
            Credit goes to the user 'Aristide' on stack overflow.
            https://stackoverflow.com/a/47713392
            """
            result = []
            for (arabic, roman) in ROMAN:
                (factor, n) = divmod(n, arabic)
                result.append(roman * factor)
                if n == 0:
                    break

            return "".join(result)

        chapterCount = 0
        partCount = 0
        for chId in self.tree.get_children(CH_ROOT):
            if self.novel.chapters[chId].noNumber:
                continue

            if self.novel.chapters[chId].chType != 0:
                continue

            if self.novel.chapters[chId].chLevel == 2:
                # regular chapter (level 2)
                if not self.novel.renumberChapters:
                    continue

            else:
                # part (level 1)
                if self.novel.renumberWithinParts:
                    chapterCount = 0
                if not self.novel.renumberParts:
                    continue

            headingPrefix = ''
            headingSuffix = ''
            if self.novel.chapters[chId].chLevel == 2:
                chapterCount += 1
                if self.novel.romanChapterNumbers:
                    number = number_to_roman(chapterCount)
                else:
                    number = str(chapterCount)
                if self.novel.chapterHeadingPrefix is not None:
                    headingPrefix = self.novel.chapterHeadingPrefix
                if self.novel.chapterHeadingSuffix is not None:
                    headingSuffix = self.novel.chapterHeadingSuffix
            else:
                partCount += 1
                if self.novel.romanPartNumbers:
                    number = number_to_roman(partCount)
                else:
                    number = str(partCount)
                if self.novel.partHeadingPrefix is not None:
                    headingPrefix = self.novel.partHeadingPrefix
                if self.novel.partHeadingSuffix is not None:
                    headingSuffix = self.novel.partHeadingSuffix
            self.novel.chapters[chId].title = f'{headingPrefix}{number}{headingSuffix}'

    def reset_tree(self):
        """Clear the tree."""
        self.tree.reset()
        self.trashBin = None

    def save_project(self, filePath=None):
        """Write the noveltree project file, and set "unchanged" status."""
        if filePath is not None:
            self.prjFile.filePath = filePath
        self.prjFile.write()
        self.isModified = False

    def set_level(self, newLevel, elemIds):
        """Set chapter or stage level.
        
        Positional arguments:
            newLevel: int -- New level to be set.
            elemIds: list of IDs to process.
        """
        for elemId in elemIds:
            if elemId.startswith(CHAPTER_PREFIX):
                self.novel.chapters[elemId].chLevel = newLevel
            elif elemId.startswith(SECTION_PREFIX):
                if self.novel.sections[elemId].scType > 1:
                    self.novel.sections[elemId].scType = newLevel + 1

    def set_character_status(self, isMajor, elemIds):
        """Recursively set character status (Major/Minor).
        
        Positional arguments:
            isMajor: bool -- If True, make the characters major. Otherwise, make them minor.
            elemIds: list of IDs to process.
        """
        for crId in elemIds:
            if crId.startswith(CHARACTER_PREFIX):
                self.novel.characters[crId].isMajor = isMajor
            elif crId == CR_ROOT:
                # Set status of all characters.
                self.set_character_status(isMajor, self.tree.get_children(crId))

    def set_section_edit_status(self, newStatus, elemIds):
        """Recursively set section completion status (Outline/Draft..).
        
        Positional arguments:
            newStatus: int -- New section status to be set.        
            elemIds: list of IDs to process.

        TODO: Rename this method to set_completion_status()            
        """
        for elemId in elemIds:
            if elemId.startswith(SECTION_PREFIX):
                if self.novel.sections[elemId].scType < 2:
                    self.novel.sections[elemId].status = newStatus
            elif elemId.startswith(CHAPTER_PREFIX) or elemId.startswith(CH_ROOT):
                self.set_section_edit_status(newStatus, self.tree.get_children(elemId))
                # going one level down

    def set_type(self, newType, elemIds):
        """Recursively set section or chapter type (Normal/Unused).
        
        Positional arguments:
            newType: int -- New type to be set.
            elemIds: list of IDs to process.
        """
        for elemId in elemIds:
            if elemId.startswith(SECTION_PREFIX):
                if self.novel.sections[elemId].scType < 2:
                    parentType = self.novel.chapters[self.tree.parent(elemId)].chType
                    if parentType > 0:
                        newType = parentType
                    self.novel.sections[elemId].scType = newType
            elif elemId.startswith(CHAPTER_PREFIX):
                self.tree.item(elemId, open=True)
                chapter = self.novel.chapters[elemId]
                if chapter.isTrash:
                    newType = 1
                chapter.chType = newType
                if newType > 0:
                    self.set_type(newType, self.tree.get_children(elemId))
                    # going one level down

    def unregister_client(self, client):
        try:
            self._clients.remove(client)
        except:
            pass

    def _initialize_tree(self, on_element_change):
        """Iterate the tree and configure the elements."""

        def initialize_branch(node):
            """Recursive tree walker.
            
            Positional arguments: 
                node: str -- Node ID to start from.
            """
            for elemId in self.tree.get_children(node):
                if elemId.startswith(SECTION_PREFIX):
                    self.novel.sections[elemId].on_element_change = on_element_change
                elif elemId.startswith(CHARACTER_PREFIX):
                    self.novel.characters[elemId].on_element_change = on_element_change
                elif elemId.startswith(LOCATION_PREFIX):
                    self.novel.locations[elemId].on_element_change = on_element_change
                elif elemId.startswith(ITEM_PREFIX):
                    self.novel.items[elemId].on_element_change = on_element_change
                elif elemId.startswith(CHAPTER_PREFIX):
                    initialize_branch(elemId)
                    self.novel.chapters[elemId].on_element_change = on_element_change
                    if self.novel.chapters[elemId].isTrash:
                        self.trashBin = elemId
                elif elemId.startswith(ARC_PREFIX):
                    initialize_branch(elemId)
                    self.novel.arcs[elemId].on_element_change = on_element_change
                elif elemId.startswith(ARC_POINT_PREFIX):
                    self.novel.turningPoints[elemId].on_element_change = on_element_change
                else:
                    initialize_branch(elemId)

        self.trashBin = None
        initialize_branch('')
        self.novel.on_element_change = on_element_change
        self.tree.on_element_change = on_element_change


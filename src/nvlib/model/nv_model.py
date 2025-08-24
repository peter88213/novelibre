"""Provide a class for the novelibre model.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.controller.services.nv_service import NvService
from nvlib.model.data.id_generator import new_id
from nvlib.model.nv_work_file import NvWorkFile
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CR_FIELD_2_DEFAULT
from nvlib.novx_globals import CR_FIELD_3_DEFAULT
from nvlib.novx_globals import CR_FIELD_1_DEFAULT
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import Error
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import NO_SCENE_FIELD_1_DEFAULT
from nvlib.novx_globals import NO_SCENE_FIELD_2_DEFAULT
from nvlib.novx_globals import NO_SCENE_FIELD_3_DEFAULT
from nvlib.novx_globals import OTHER_SCENE_FIELD_1_DEFAULT
from nvlib.novx_globals import OTHER_SCENE_FIELD_2_DEFAULT
from nvlib.novx_globals import OTHER_SCENE_FIELD_3_DEFAULT
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import PN_ROOT
from nvlib.novx_globals import PRJ_NOTE_PREFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


class NvModel:
    """novelibre model representation."""

    def __init__(self):
        self._observers = []
        # list of Observer instance references
        self._isModified = False
        # internal modification flag

        self.tree = None
        # strategy class
        self.prjFile = None
        self.novel = None
        # objects to be updated on model change

        self.trashBin = None
        self.wordCount = 0

        self.nvService = NvService()

    @property
    def isModified(self):
        # Boolean -- True if there are unsaved changes.
        return self._isModified

    @isModified.setter
    def isModified(self, setFlag):
        self._isModified = setFlag
        self.notify_observers()

    def add_new_chapter(self, **kwargs):
        """Create a chapter instance and add it to the novel.
             
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            chType: int -- Chapter type. Default: 0.
            NoNumber: str -- Do not auto-number this chapter. Default: None.
            
        - Place the new node at the next free position after the target node, 
          if possible.
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
        chId = new_id(self.novel.chapters, prefix=CHAPTER_PREFIX)
        self.novel.chapters[chId] = self.nvService.new_chapter(
            title=kwargs.get('title', f'{_("New Chapter")} ({chId})'),
            desc='',
            chLevel=2,
            chType=kwargs.get('chType', 0),
            noNumber=kwargs.get('NoNumber', False),
            isTrash=False,
            links={},
            on_element_change=self.on_element_change,
        )
        self.tree.insert(CH_ROOT, index, chId)
        return chId

    def add_new_character(self, **kwargs):
        """Create a character instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title.
            isMajor: bool -- If True, make the new character a major character. 
                             Default: False.
            
        - If the target node is of the same type as the new node, 
          place the new node after the selected node and select it.
        - Otherwise, place the new node at the last position.   

        Return the element's ID, if successful.
        """
        targetNode = kwargs.get('targetNode', '')
        index = 'end'
        if targetNode.startswith(CHARACTER_PREFIX):
            index = self.tree.index(targetNode) + 1
        crId = new_id(self.novel.characters, prefix=CHARACTER_PREFIX)
        self.novel.characters[crId] = self.nvService.new_character(
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

    def add_new_item(self, **kwargs):
        """Create an item instance and add it to the novel.
        
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
        itId = new_id(self.novel.items, prefix=ITEM_PREFIX)
        self.novel.items[itId] = self.nvService.new_world_element(
            title=kwargs.get('title', f'{_("New Item")} ({itId})'),
            desc='',
            aka='',
            tags='',
            links={},
            on_element_change=self.on_element_change,
        )
        self.tree.insert(IT_ROOT, index, itId)
        return itId

    def add_new_location(self, **kwargs):
        """Create a location instance and add it to the novel.
        
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
        lcId = new_id(self.novel.locations, prefix=LOCATION_PREFIX)
        self.novel.locations[lcId] = self.nvService.new_world_element(
            title=kwargs.get('title', f'{_("New Location")} ({lcId})'),
            desc='',
            aka='',
            tags='',
            links={},
            on_element_change=self.on_element_change,
        )
        self.tree.insert(LC_ROOT, index, lcId)
        return lcId

    def add_new_part(self, **kwargs):
        """Create a part instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str: Part title. Default -- Auto-generated title. 
            chType: int: Part type. Default -- 0.  
            NoNumber: str: Do not auto-number this part. Default -- None.
           
        - Place the new node at the next free position after the target node, 
          if possible.
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
        chId = new_id(self.novel.chapters, prefix=CHAPTER_PREFIX)
        self.novel.chapters[chId] = self.nvService.new_chapter(
            title=kwargs.get('title', f'{_("New Part")} ({chId})'),
            desc='',
            chLevel=1,
            chType=kwargs.get('chType', 0),
            noNumber=kwargs.get('NoNumber', False),
            isTrash=False,
            links={},
            on_element_change=self.on_element_change,
        )
        self.tree.insert(CH_ROOT, index, chId)
        return chId

    def add_new_plot_line(self, **kwargs):
        """Create a plot line instance and add it to the novel.
        
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
        if targetNode.startswith(PLOT_LINE_PREFIX):
            index = self.tree.index(targetNode) + 1
        plId = new_id(self.novel.plotLines, prefix=PLOT_LINE_PREFIX)
        self.novel.plotLines[plId] = self.nvService.new_plot_line(
            title=kwargs.get('title', f'{_("New Plot line")} ({plId})'),
            desc='',
            shortName=plId,
            sections=[],
            links={},
            on_element_change=self.on_element_change,
        )
        self.tree.insert(PL_ROOT, index, plId)
        return plId

    def add_new_plot_point(self, **kwargs):
        """Create a plot point instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title.
            
        - Place the new node at the next free position after the target node,
          if possible.
        - Otherwise, do nothing. 
        
        Return the plot point ID, if successful.
        """
        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            return

        index = 'end'
        if targetNode.startswith(PLOT_POINT_PREFIX):
            parent = self.tree.parent(targetNode)
            index = self.tree.index(targetNode) + 1
        elif targetNode.startswith(PLOT_LINE_PREFIX):
            parent = targetNode
        else:
            return

        ppId = new_id(self.novel.plotPoints, prefix=PLOT_POINT_PREFIX)
        self.novel.plotPoints[ppId] = self.nvService.new_plot_point(
            title=kwargs.get('title', f'{_("New Plot point")} ({ppId})'),
            desc='',
            links={},
            on_element_change=self.on_element_change,
        )
        self.tree.insert(parent, index, ppId)
        return ppId

    def add_new_project_note(self, **kwargs):
        """Create a project note instance and add it to the novel.
        
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
        pnId = new_id(self.novel.projectNotes, prefix=PRJ_NOTE_PREFIX)
        self.novel.projectNotes[pnId] = self.nvService.new_basic_element(
            title=kwargs.get('title', f'{_("New Note")} ({pnId})'),
            desc='',
            links={},
            on_element_change=self.on_element_change,
        )
        self.tree.insert(PN_ROOT, index, pnId)
        return pnId

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
            
        - Place the new node at the next free position after the target node, 
          if possible.
        - If the target node is a chapter, place the new node at the 
          chapter end.
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
        scId = new_id(self.novel.sections, prefix=SECTION_PREFIX)
        self.novel.sections[scId] = self.nvService.new_section(
            title=kwargs.get('title', f'{_("New Section")} ({scId})'),
            desc=kwargs.get('desc', ''),
            scType=newType,
            scene=kwargs.get('scene', 0),
            status=kwargs.get('status', 1),
            appendToPrev=kwargs.get('appendToPrev', False),
            characters=[],
            locations=[],
            items=[],
            links={},
            on_element_change=self.on_element_change,
        )
        self.novel.sections[scId].sectionContent = '<p></p>'
        self.tree.insert(parent, index, scId)
        return scId

    def add_new_stage(self, **kwargs):
        """Create a stage instance and add it to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Stage title. Default: Auto-generated title. 
            desc: str -- Description.
            scType: int -- Scene type. Default: 3.
            
        - Place the new node at the next free position after the target node, 
          if possible.
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

        scId = new_id(self.novel.sections, prefix=SECTION_PREFIX)
        self.novel.sections[scId] = self.nvService.new_section(
            title=kwargs.get('title', f'{_("Stage")}'),
            desc=kwargs.get('desc', ''),
            scType=kwargs.get('scType', 3),
            status=0,
            scene=0,
            links={},
            on_element_change=self.on_element_change,
        )
        self.tree.insert(parent, index, scId)
        return scId

    def add_observer(self, client):
        """Add an Observer instance to the list."""
        if not client in self._observers:
            self._observers.append(client)

    def close_project(self):
        self._isModified = False
        # writing the public isModified property here would trigger a refresh
        self.tree.on_element_change = self.tree.do_nothing
        self.novel = None
        self.prjFile = None

    def create_project(self, tree):
        """Create a novelibre project instance."""
        self.novel = self.nvService.new_novel(
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
            noSceneField1=NO_SCENE_FIELD_1_DEFAULT,
            noSceneField2=NO_SCENE_FIELD_2_DEFAULT,
            noSceneField3=NO_SCENE_FIELD_3_DEFAULT,
            otherSceneField1=OTHER_SCENE_FIELD_1_DEFAULT,
            otherSceneField2=OTHER_SCENE_FIELD_2_DEFAULT,
            otherSceneField3=OTHER_SCENE_FIELD_3_DEFAULT,
            crField1=CR_FIELD_1_DEFAULT,
            crField2=CR_FIELD_2_DEFAULT,
            crField3=CR_FIELD_3_DEFAULT,
            links=[],
            tree=tree,
            on_element_change=self.on_element_change,
        )
        self.novel.check_locale()
        # setting the the system locale as document language/country
        self.prjFile = NvWorkFile('')
        self.prjFile.novel = self.novel
        self._initialize_tree(self.on_element_change)

    def delete_element(self, elemId, trash=True):
        """Delete an element and its children.
        
        Positional arguments:
            elemId: str -- ID of the element to delete.
            
        Optional elements:
            trash: Boolean -- If True, move elements to the "Trash Bin" 
                              instead of deleting them.
        
        - Move sections to the "Trash" chapter.
        - Delete parts/chapters and move their children sections 
          to the "Trash" chapter.
        - Delete characters/locations/items and remove their section 
          references.
        - Delete stages.
        - Delete plotLines and remove their plot points and section 
          references.
        - Delete plot points and remove their section references.
        - Delete project notes.
        """

        def waste_sections(elemId):
            # Move all sections under the element specified by elemId
            # to the 'trash bin'.
            # Reads the "trash" variable of the calling method.
            if elemId.startswith(SECTION_PREFIX):
                if self.novel.sections[elemId].scType < 2:
                    # Remove plot point and plot line references.
                    arcReferences = self.novel.sections[elemId].scPlotLines
                    tpReferences = self.novel.sections[elemId].scPlotPoints
                    self.novel.sections[elemId].scPlotLines = []
                    self.novel.sections[elemId].scPlotPoints = {}
                    for plId in arcReferences:
                        sections = self.novel.plotLines[plId].sections
                        sections.remove(elemId)
                        self.novel.plotLines[plId].sections = sections
                    for ppId in tpReferences:
                        self.novel.plotPoints[ppId].sectionAssoc = None
                    if trash:
                        # Move the section to the trash bin.
                        self.tree.move(elemId, self.trashBin, 0)
                        self.novel.sections[elemId].scType = 1
                    else:
                        # Delete the section.
                        del self.novel.sections[elemId]
                        self.tree.delete(elemId)
                else:
                    # Delete the stage.
                    del self.novel.sections[elemId]
                    self.tree.delete(elemId)
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
            del self.novel.characters[elemId]
            self.tree.delete(elemId)
            for scId in self.novel.sections:
                try:
                    scCharacters = self.novel.sections[scId].characters
                    scCharacters.remove(elemId)
                    self.novel.sections[scId].characters = scCharacters
                except:
                    pass
        elif elemId.startswith(LOCATION_PREFIX):
            # Delete a location and remove references.
            del self.novel.locations[elemId]
            self.tree.delete(elemId)
            for scId in self.novel.sections:
                try:
                    scLocations = self.novel.sections[scId].locations
                    scLocations.remove(elemId)
                    self.novel.sections[scId].locations = scLocations
                except:
                    pass
        elif elemId.startswith(ITEM_PREFIX):
            # Delete an item and remove references.
            del self.novel.items[elemId]
            self.tree.delete(elemId)
            for scId in self.novel.sections:
                try:
                    scItems = self.novel.sections[scId].items
                    scItems.remove(elemId)
                    self.novel.sections[scId].items = scItems
                except:
                    pass
        elif elemId.startswith(PLOT_LINE_PREFIX):
            # Delete a plot line and remove references.
            if self.novel.plotLines[elemId].sections:
                for scId in self.novel.plotLines[elemId].sections:
                    self.novel.sections[scId].scPlotLines.remove(elemId)
                for ppId in self.tree.get_children(elemId):
                    scId = self.novel.plotPoints[ppId].sectionAssoc
                    if scId is not None:
                        del(self.novel.sections[scId].scPlotPoints[ppId])
                    del self.novel.plotPoints[ppId]
            del self.novel.plotLines[elemId]
            self.tree.delete(elemId)
        elif elemId.startswith(PLOT_POINT_PREFIX):
            # Delete a plot point and remove references.
            scId = self.novel.plotPoints[elemId].sectionAssoc
            if scId is not None:
                del(self.novel.sections[scId].scPlotPoints[elemId])
            del self.novel.plotPoints[elemId]
            self.tree.delete(elemId)
        elif elemId.startswith(PRJ_NOTE_PREFIX):
            # Delete a project note.
            del self.novel.projectNotes[elemId]
            self.tree.delete(elemId)
        else:
            # Part/chapter/section selected.
            if trash and self.trashBin is None:
                # Create a "trash bin"; use the first free chapter ID.
                self.trashBin = new_id(
                    self.novel.chapters,
                    prefix=CHAPTER_PREFIX,
                )
                self.novel.chapters[self.trashBin] = (
                    self.nvService.new_chapter(
                        title=_('Trash'),
                        desc='',
                        chLevel=2,
                        chType=1,
                        noNumber=True,
                        isTrash=True,
                        on_element_change=self.on_element_change,
                    )
                )
                self.tree.append(CH_ROOT, self.trashBin)
            if elemId.startswith(SECTION_PREFIX):
                if self.tree.parent(elemId) == self.trashBin:
                    # Remove section, if already in trash bin.
                    del self.novel.sections[elemId]
                    self.tree.delete(elemId)
                else:
                    # Move section to the "trash bin".
                    waste_sections(elemId)
            else:
                # Delete part/chapter and move child sections
                # to the "trash bin".
                waste_sections(elemId)
                self.tree.delete(elemId)
            if trash:
                # Make sure the whole "trash bin" is unused.
                self.set_type(1, [self.trashBin])

    def delete_observer(self, client):
        """Remove an Observer instance from the list."""
        if client in self._observers:
            self._observers.remove(client)

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
                    counts[self.novel.sections[scId].status
                           ] += self.novel.sections[scId].wordCount
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
        if (
            self.novel.sections[ScId1].scType
            != self.novel.sections[ScId0].scType
        ):
            raise Error(_('The sections are not of the same type'))

        # Check viewpoint.
        if self.novel.sections[ScId1].characters:
            if self.novel.sections[ScId1].characters:
                if self.novel.sections[ScId0].characters:
                    if (self.novel.sections[ScId1].viewpoint
                        != self.novel.sections[ScId0].viewpoint
                ):
                        raise Error(
                            _('The sections have different viewpoints')
                        )

                else:
                    self.novel.sections[ScId0].characters.append(
                        self.novel.sections[ScId1].viewpoint
                    )

        # Join titles.
        joinedTitles = (
            f'{self.novel.sections[ScId0].title}'
            f' & {self.novel.sections[ScId1].title}'
        )
        self.novel.sections[ScId0].title = joinedTitles

        # Join content.
        content0 = self.novel.sections[ScId0].sectionContent
        content1 = self.novel.sections[ScId1].sectionContent
        # this is because sectionContent is a property
        self.novel.sections[ScId0].sectionContent = join_str(
            content0, content1, newline='')

        # Join description, goal, conflict, outcome, notes.
        self.novel.sections[ScId0].desc = join_str(
            self.novel.sections[ScId0].desc,
            self.novel.sections[ScId1].desc
        )
        self.novel.sections[ScId0].goal = join_str(
            self.novel.sections[ScId0].goal,
            self.novel.sections[ScId1].goal
        )
        self.novel.sections[ScId0].conflict = join_str(
            self.novel.sections[ScId0].conflict,
            self.novel.sections[ScId1].conflict
        )
        self.novel.sections[ScId0].outcome = join_str(
            self.novel.sections[ScId0].outcome,
            self.novel.sections[ScId1].outcome
        )
        self.novel.sections[ScId0].notes = join_str(
            self.novel.sections[ScId0].notes,
            self.novel.sections[ScId1].notes
        )

        # Join characters, locations, items, tags.
        join_lst(
            self.novel.sections[ScId0].characters,
            self.novel.sections[ScId1].characters
        )
        join_lst(
            self.novel.sections[ScId0].locations,
            self.novel.sections[ScId1].locations
        )
        join_lst(
            self.novel.sections[ScId0].items,
            self.novel.sections[ScId1].items
        )
        join_lst(
            self.novel.sections[ScId0].tags,
            self.novel.sections[ScId1].tags
        )

        # Move plot line associations.
        for scPlotLine in self.novel.sections[ScId1].scPlotLines:
            self.novel.plotLines[scPlotLine].sections.remove(ScId1)
            if not ScId0 in self.novel.plotLines[scPlotLine].sections:
                self.novel.plotLines[scPlotLine].sections.append(ScId0)
            if not scPlotLine in self.novel.sections[ScId0].scPlotLines:
                self.novel.sections[ScId0].scPlotLines.append(scPlotLine)

        # Move plot point associations.
        for ppId in self.novel.sections[ScId1].scPlotPoints:
            self.novel.plotPoints[ppId].sectionAssoc = ScId0
            self.novel.sections[ScId0].scPlotPoints[ppId] = (
                self.novel.sections[ScId1].scPlotPoints[ppId]
            )

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
        daysLeft, lastsHours0 = divmod(
            (lastsHours0 + lastsHours1 + hoursLeft), 24
        )
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
            self.tree.move(
                node,
                self.tree.parent(targetNode),
                self.tree.index(targetNode),
            )
        elif (
                (
                    node.startswith(SECTION_PREFIX)
                    and targetNode.startswith(CHAPTER_PREFIX)
                )or (
                        node.startswith(PLOT_POINT_PREFIX)
                        and targetNode.startswith(PLOT_LINE_PREFIX)
                    )
        ):
            if not self.tree.get_children(targetNode):
                self.tree.move(node, targetNode, 0)
            elif self.tree.prev(targetNode):
                self.tree.move(node, self.tree.prev(targetNode), 'end')

    def notify_observers(self):
        for client in self._observers:
            client.refresh()

    def on_element_change(self):
        """Callback function that reports changes."""
        self.isModified = True

    def open_project(self, filePath):
        """Initialize instance variables.
        
        Positional arguments:
            filePath: str -- path to the prjFile file.
        """
        self.novel = self.nvService.new_novel(
            tree=self.tree,
            links={},
            noSceneField1=NO_SCENE_FIELD_1_DEFAULT,
            noSceneField2=NO_SCENE_FIELD_2_DEFAULT,
            noSceneField3=NO_SCENE_FIELD_3_DEFAULT,
            otherSceneField1=OTHER_SCENE_FIELD_1_DEFAULT,
            otherSceneField2=OTHER_SCENE_FIELD_2_DEFAULT,
            otherSceneField3=OTHER_SCENE_FIELD_3_DEFAULT,
            crField1=CR_FIELD_1_DEFAULT,
            crField2=CR_FIELD_2_DEFAULT,
            crField3=CR_FIELD_3_DEFAULT,
        )
        self.prjFile = NvWorkFile(filePath)
        self.prjFile.novel = self.novel
        self.prjFile.read()
        if self.prjFile.wcLogUpdate and self.novel.saveWordCount:
            self.isModified = True
        else:
            self.isModified = False
        self._initialize_tree(self.on_element_change)

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
            # Return n as a Roman number.
            # Credit goes to the user "Aristide" on stack overflow.
            # https://stackoverflow.com/a/47713392
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
            self.novel.chapters[chId].title = (
                f'{headingPrefix}{number}'
                f'{headingSuffix}'
            )

    def reset_tree(self):
        """Clear the tree."""
        self.tree.reset()
        self.trashBin = None

    def save_project(self, filePath=None):
        """Write the novelibre project file, and set "unchanged" status."""
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
            isMajor: bool -- If True, make the characters major. 
                             Otherwise, make them minor.
            elemIds: list of IDs to process.
        """
        for crId in elemIds:
            if crId.startswith(CHARACTER_PREFIX):
                self.novel.characters[crId].isMajor = isMajor
            elif crId == CR_ROOT:
                # Set status of all characters.
                self.set_character_status(
                    isMajor,
                    self.tree.get_children(crId)
                )

    def set_completion_status(self, newStatus, elemIds):
        """Recursively set section completion status (Outline/Draft..).
        
        Positional arguments:
            newStatus: int -- New section status to be set.        
            elemIds: list of IDs to process.
        """
        for elemId in elemIds:
            if elemId.startswith(SECTION_PREFIX):
                if self.novel.sections[elemId].scType < 2:
                    self.novel.sections[elemId].status = newStatus
            elif (
                elemId.startswith(CHAPTER_PREFIX)
                or elemId.startswith(CH_ROOT)
            ):
                self.set_completion_status(
                    newStatus,
                    self.tree.get_children(elemId)
                )
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
                    parentType = (
                        self.novel.chapters[self.tree.parent(elemId)].chType
                    )
                    if parentType > 0:
                        newType = parentType
                    self.novel.sections[elemId].scType = newType
            elif elemId.startswith(CHAPTER_PREFIX):
                chapter = self.novel.chapters[elemId]
                if chapter.isTrash:
                    newType = 1
                chapter.chType = newType
                if newType > 0:
                    self.set_type(newType, self.tree.get_children(elemId))
                    # going one level down

    def set_viewpoint(self, crId, elemIds):
        """Recursively set the section viewpoint.
        
        Positional arguments:
            crId: str -- viewpoint character ID to be set.
            elemIds: list of IDs to process.
        """
        for elemId in elemIds:
            if elemId.startswith(SECTION_PREFIX):
                if self.novel.sections[elemId].scType < 2:
                    self.novel.sections[elemId].viewpoint = crId
            elif (
                elemId.startswith(CHAPTER_PREFIX)
                or elemId.startswith(CH_ROOT)
            ):
                self.set_viewpoint(
                    crId,
                    self.tree.get_children(elemId)
                )
                # going one level down

    def _initialize_tree(self, on_element_change):
        """Iterate the tree and configure the elements."""

        def initialize_branch(node):
            # Recursive tree walker.
            #    node: str -- Node ID to start from.
            for elemId in self.tree.get_children(node):
                if elemId.startswith(SECTION_PREFIX):
                    self.novel.sections[elemId].on_element_change = (
                        on_element_change
                    )
                elif elemId.startswith(CHARACTER_PREFIX):
                    self.novel.characters[elemId].on_element_change = (
                        on_element_change
                    )
                elif elemId.startswith(LOCATION_PREFIX):
                    self.novel.locations[elemId].on_element_change = (
                        on_element_change
                    )
                elif elemId.startswith(ITEM_PREFIX):
                    self.novel.items[elemId].on_element_change = (
                        on_element_change
                    )
                elif elemId.startswith(CHAPTER_PREFIX):
                    initialize_branch(elemId)
                    self.novel.chapters[elemId].on_element_change = (
                        on_element_change
                    )
                    if self.novel.chapters[elemId].isTrash:
                        self.trashBin = elemId
                elif elemId.startswith(PLOT_LINE_PREFIX):
                    initialize_branch(elemId)
                    self.novel.plotLines[elemId].on_element_change = (
                        on_element_change
                    )
                elif elemId.startswith(PLOT_POINT_PREFIX):
                    self.novel.plotPoints[elemId].on_element_change = (
                        on_element_change
                    )
                else:
                    initialize_branch(elemId)

        self.trashBin = None
        initialize_branch('')
        self.novel.on_element_change = on_element_change
        self.tree.on_element_change = on_element_change


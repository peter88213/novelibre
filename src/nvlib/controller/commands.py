"""Provide a controller mixin class for novelibre user interaction.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from shutil import copy2
import sys
from tkinter import filedialog
import webbrowser

from nvlib.novx_globals import BRF_SYNOPSIS_SUFFIX
from nvlib.novx_globals import CHAPTERS_SUFFIX
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHARACTERS_SUFFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CHARACTER_REPORT_SUFFIX
from nvlib.novx_globals import CHARLIST_SUFFIX
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import DATA_SUFFIX
from nvlib.novx_globals import Error
from nvlib.novx_globals import GRID_SUFFIX
from nvlib.novx_globals import ITEMLIST_SUFFIX
from nvlib.novx_globals import ITEMS_SUFFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import ITEM_REPORT_SUFFIX
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import LOCATIONS_SUFFIX
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import LOCATION_REPORT_SUFFIX
from nvlib.novx_globals import LOCLIST_SUFFIX
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.novx_globals import PARTS_SUFFIX
from nvlib.novx_globals import PLOTLINES_SUFFIX
from nvlib.novx_globals import PLOTLIST_SUFFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PLOT_POINT_PREFIX
from nvlib.novx_globals import PL_ROOT
from nvlib.novx_globals import PN_ROOT
from nvlib.novx_globals import PRJ_NOTE_PREFIX
from nvlib.novx_globals import PROOF_SUFFIX
from nvlib.novx_globals import SECTIONLIST_SUFFIX
from nvlib.novx_globals import SECTIONS_SUFFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.novx_globals import STAGES_SUFFIX
from nvlib.novx_globals import XREF_SUFFIX
from nvlib.novx_globals import _
from nvlib.novx_globals import norm_path
from nvlib.nv_globals import open_help
from nvlib.nv_globals import prefs
from nvlib.view.pop_up.export_options_dialog import ExportOptionsDialog
from nvlib.view.pop_up.plugin_manager_dialog import PluginManagerDialog
from nvlib.view.pop_up.reimport_dialog import ReimportDialog
from nvlib.view.pop_up.view_options_dialog import ViewOptionsDialog
from nvlib.view.widgets.nv_simpledialog import SimpleDialog
from nvlib.view.widgets.nv_simpledialog import askinteger
from nvlib.nv_globals import HOME_URL


class Commands:

    _MAX_NR_NEW_SECTIONS = 20
    # maximum number of sections to add in bulk
    _INI_NR_NEW_SECTIONS = 1
    # initial value when asking for the number of sections to add

    def add_chapter(self, **kwargs):
        """Add a chapter to the novel.
             
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            chType: int -- Chapter type. Default: 0.
            NoNumber: str -- Do not auto-number this chapter. Default: None.
            
        Return the chapter ID, if successful.
        """
        if self.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_chapter(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_character(self, **kwargs):
        """Add a character to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title.
            isMajor: bool -- If True, make the new character a major character. Default: False.
            
        Return the element's ID, if successful.
        """
        if self.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_character(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_child(self, event=None):
        """Add a child element to an element.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if self._mdl.prjFile is None:
            return

        if self.check_lock():
            return

        try:
            selection = self._ui.selectedNode
        except:
            return

        if selection == CH_ROOT:
            self.add_chapter(targetNode=selection)
            return

        if selection.startswith(CHAPTER_PREFIX):
            self.add_section(targetNode=selection)
            return

        if selection.startswith(PLOT_LINE_PREFIX):
            self.add_plot_point(targetNode=selection)
            return

        if selection == CR_ROOT:
            self.add_character(targetNode=selection)
            return

        if selection == LC_ROOT:
            self.add_location(targetNode=selection)
            return

        if selection == IT_ROOT:
            self.add_item(targetNode=selection)
            return

        if selection == PL_ROOT:
            self.add_plot_line(targetNode=selection)
            return

        if selection == PN_ROOT:
            self.add_project_note(targetNode=selection)

    def add_element(self, event=None):
        """Add an element to the novel.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if self._mdl.prjFile is None:
            return

        if self.check_lock():
            return

        try:
            selection = self._ui.selectedNode
        except:
            return

        if selection.startswith(SECTION_PREFIX):
            if self._mdl.novel.sections[selection].scType < 2:
                self.add_section(targetNode=selection)
                return

            self.add_stage(targetNode=selection)
            return

        if CHAPTER_PREFIX in selection:
            self.add_chapter(targetNode=selection)
            return

        if CHARACTER_PREFIX in selection:
            self.add_character(targetNode=selection)
            return

        if LOCATION_PREFIX in selection:
            self.add_location(targetNode=selection)
            return

        if ITEM_PREFIX in selection:
            self.add_item(targetNode=selection)
            return

        if PLOT_LINE_PREFIX in selection:
            self.add_plot_line(targetNode=selection)
            return

        if PRJ_NOTE_PREFIX in selection:
            self.add_project_note(targetNode=selection)
            return

        if selection.startswith(PLOT_POINT_PREFIX):
            self.add_plot_point(targetNode=selection)

    def add_item(self, **kwargs):
        """Add an item to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        if self.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_item(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_location(self, **kwargs):
        """Add a location to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        if self.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_location(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_multiple_sections(self):
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
                self.add_section()

    def add_parent(self, event=None):
        """Add a parent element to an element.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if self._mdl.prjFile is None:
            return

        if self.check_lock():
            return

        try:
            selection = self._ui.selectedNode
        except:
            return

        if selection.startswith(SECTION_PREFIX):
            self.add_chapter(targetNode=selection)
        elif selection.startswith(PLOT_POINT_PREFIX):
            self.add_plot_line(targetNode=selection)

    def add_part(self, **kwargs):
        """Add a part to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str: Part title. Default -- Auto-generated title. 
            chType: int: Part type. Default -- 0.  
            NoNumber: str: Do not auto-number this part. Default -- None.
           
        Return the chapter ID, if successful.
        """
        if self.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_part(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_plot_line(self, **kwargs):
        """Add a plot line to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the plot line ID, if successful.
        """
        if self.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_plot_line(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_plot_point(self, **kwargs):
        """Add a plot point to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            
        Return the plot point ID, if successful.
        """
        if self.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_plot_point(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_project_note(self, **kwargs):
        """Add a Project note to the novel.
        
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
        newNode = self._mdl.add_project_note(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_section(self, **kwargs):
        """Add a section to the novel.
        
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
        if self.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_section(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def add_stage(self, **kwargs):
        """Add a stage to the novel.
        
        Keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Stage title. Default: Auto-generated title. 
            desc: str -- Description.
            scType: int -- Scene type. Default: 3.
            
        Return the section ID, if successful.
        """
        if self.check_lock():
            return

        targetNode = kwargs.get('targetNode', None)
        if targetNode is None:
            try:
                kwargs['targetNode'] = self._ui.selectedNode
            except:
                pass
        newNode = self._mdl.add_stage(**kwargs)
        self.view_new_element(newNode)
        return newNode

    def close_project(self, event=None, doNotSave=False):
        return self.on_close(doNotSave)

    def copy_css(self, event=None):
        """Copy the provided css style sheet into the project directory."""
        try:
            projectDir, __ = os.path.split(self._mdl.prjFile.filePath)
            copy2(f'{os.path.dirname(sys.argv[0])}/css/novx.css', projectDir)
            message = _('Style sheet copied into the project folder.')
        except Exception as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(message)

    def delete_elements(self, event=None, elements=None):
        """Delete elements and their children.
        
        Optional arguments:
            elements: list of IDs of the elements to delete.        
        """
        if self.check_lock():
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
        chapterInElements = False
        ask = True
        for  elemId in elements:
            if elemId.startswith(SECTION_PREFIX):
                if chapterInElements and self._ui.tv.tree.parent(elemId) == self._mdl.trashBin:
                    # the section has belonged to a chapter that is already deleted
                    continue

                if self._mdl.novel.sections[elemId].scType < 2:
                    candidate = f'{_("Section")} "{self._mdl.novel.sections[elemId].title}"'
                else:
                    candidate = f'{_("Stage")} "{self._mdl.novel.sections[elemId].title}"'
            elif elemId.startswith(CHAPTER_PREFIX):
                candidate = f'{_("Chapter")} "{self._mdl.novel.chapters[elemId].title}"'
                chapterInElements = True
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
                result = SimpleDialog(
                    None,
                    text=f"\n\n{_('Delete {}?').format(candidate)}\n\n",
                    buttons=[_('Yes'), _('All'), _('No'), _('Cancel')],
                    default=0,
                    cancel=3,
                    title=_('Delete multiple elements')
                    ).go()
                if result == 3:
                    return

                if result == 2:
                    continue

                if result == 1:
                    ask = False
            self._mdl.delete_element(elemId)
            if elemId == elements[0]:
                selectAfterDeleting = newSelection
        self._ui.tv.go_to_node(selectAfterDeleting)

    def discard_manuscript(self):
        """Rename the current editable manuscript. 
        
        This might be useful to avoid confusion in certain cases.
        """
        fileName, __ = os.path.splitext(self._mdl.prjFile.filePath)
        manuscriptPath = f'{fileName}{MANUSCRIPT_SUFFIX}.odt'
        if os.path.isfile(manuscriptPath):
            prjPath, manuscriptName = os.path.split(manuscriptPath)
            if os.path.isfile(f'{prjPath}/.~lock.{manuscriptName}#'):
                self._ui.set_status(f"!{_('Please close the manuscript first')}.")
            elif self._ui.ask_yes_no(f"{_('Discard manuscript')}?", self._mdl.novel.title):
                os.replace(manuscriptPath, f'{fileName}{MANUSCRIPT_SUFFIX}.odt.bak')
                self._ui.set_status(f"{_('Manuscript discarded')}.")

    def export_plot_grid(self, event=None):
        self.export_document(GRID_SUFFIX)

    def export_plot_lines_desc(self, event=None):
        self.export_document(PLOTLINES_SUFFIX, lock=False)

    def export_plot_list(self, event=None):
        self.export_document(PLOTLIST_SUFFIX, lock=False)

    def export_story_structure_desc(self, event=None):
        self.export_document(STAGES_SUFFIX)

    def import_plot_lines(self, event=None):
        self.import_elements(PLOT_LINE_PREFIX)

    def join_sections(self, event=None, scId0=None, scId1=None):
        """Join section 0 with section 1.

        Optional arguments:
            scId0: str -- ID of the section to be extended
            scId1: str -- ID of the section to be discarded.
            
        If not both arguments are given, determine them from the tree selection.
        """
        if self.check_lock():
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
        if not self.isLocked:
            if (node.startswith(SECTION_PREFIX) and targetNode.startswith(CHAPTER_PREFIX)
                ) or (node.startswith(PLOT_POINT_PREFIX) and targetNode.startswith(PLOT_LINE_PREFIX)):
                self._ui.tv.open_children(targetNode)
            self._ui.tv.skipUpdate = True
            self._mdl.move_node(node, targetNode)

    def new_project(self, event=None):
        """Create a novelibre project instance."""
        if self._mdl.prjFile is not None:
            self.close_project()
        self._mdl.new_project(self._ui.tv.tree)
        self._ui.show_path(_('Unnamed'))
        # setting the path bar
        self.enable_menu()
        self.update_status()
        # setting the status bar
        self._ui.tv.go_to_node(CH_ROOT)
        self.refresh_tree()
        self.save_project()
        return 'break'

    def open_export_options(self, event=None):
        """Open a toplevel window to edit the export options."""
        ExportOptionsDialog(self._mdl, self._ui, self)
        return 'break'

    def open_help(self, event=None):
        open_help('')

    def open_homepage(self, event=None):
        webbrowser.open(HOME_URL)

    def open_installationFolder(self, event=None):
        """Open the installation folder with the OS file manager."""
        installDir = os.path.dirname(sys.argv[0])
        try:
            os.startfile(norm_path(installDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(installDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(installDir))
                    # Mac
                except:
                    pass
        return 'break'

    def open_link(self, element, linkIndex):
        """Open a linked file.
        
        Positional arguments:
            element: BasicElement or subclass.
            linkIndex: int -- Index of the link to open.
            
        First try to open the link using its relative path.
        If this fails, try to open it using the "full" path. 
        On success, fix the link. 
        Otherwise, show an error message. 
        
        The linkProcessor strategy can be overridden e.g. by plugins.
        """
        linkPath = list(element.links)[linkIndex]
        fullPath = element.links[linkPath]
        try:
            self.linkProcessor.open_link(linkPath, self.launchers)
            # using the relative path
        except:

            # The relative link seems to be broken. Try the full path.
            if fullPath is not None:
                newPath = self.linkProcessor.shorten_path(fullPath)
            else:
                newPath = ''
            # fixing the link using the full path
            try:
                self.linkProcessor.open_link(newPath, self.launchers)
            except Exception as ex:

                # The full path is also broken.
                self._ui.show_error(
                    str(ex),
                    title=_('Cannot open link')
                    )
            else:
                # Replace the broken link with the fixed one.
                links = element.links
                del links[linkPath]
                links[newPath] = fullPath
                element.links = links
                self._ui.set_status(_('Broken link fixed'))
        else:
            # Relative path is o.k. -- now check the full path.
            pathOk = self.linkProcessor.expand_path(linkPath)
            if fullPath != pathOk:
                # Replace the broken full path.
                links = element.links
                links[linkPath] = pathOk
                element.links = links
                self._ui.set_status(_('Broken link fixed'))

    def open_plugin_manager(self, event=None):
        """Open a toplevel window to manage the plugins."""
        PluginManagerDialog(self._mdl, self._ui, self)
        return 'break'

    def open_project(self, event=None, filePath='', doNotSave=False):
        """Create a novelibre project instance and read the file.
        
        Optional arguments:
            filePath: str -- The new project's file name.
        
        If no file name is given, a file picker is opened.
        Display project title, description and status.
        Return True on success, otherwise return False.
        """
        self._ui.restore_status()
        filePath = self.select_project(filePath)
        if not filePath:
            return False

        prefs['last_open'] = filePath

        if self._mdl.prjFile is not None:
            self.close_project(doNotSave=doNotSave)
        try:
            self._mdl.open_project(filePath)
        except Error as ex:
            self.close_project(doNotSave=doNotSave)
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ui.show_path(f'{norm_path(self._mdl.prjFile.filePath)}')
        self.enable_menu()

        self.refresh_tree()
        self._ui.show_path(_('{0} (last saved on {1})').format(norm_path(self._mdl.prjFile.filePath), self._mdl.prjFile.fileDate))
        self.update_status()
        self._ui.contentsView.view_text()
        if self._mdl.prjFile.has_lockfile():
            self.lock()
        self._ui.tv.show_branch(CH_ROOT)
        return True

    def open_project_folder(self, event=None):
        """Open the project folder with the OS file manager."""
        if not self.save_project():
            if not self._mdl:
                return

            if not self._mdl.prjFile:
                return

            if self._mdl.prjFile.filePath is None:
                return

        projectDir, __ = os.path.split(self._mdl.prjFile.filePath)
        try:
            os.startfile(norm_path(projectDir))
            # Windows
        except:
            try:
                os.system('xdg-open "%s"' % norm_path(projectDir))
                # Linux
            except:
                try:
                    os.system('open "%s"' % norm_path(projectDir))
                    # Mac
                except:
                    pass
        return 'break'

    def open_project_updater(self, event=None):
        """Update the project from a previously exported document.
        
        Using a toplevel window with a pick list of refresh sources.
        """
        ReimportDialog(self._mdl, self._ui, self)
        return 'break'

    def open_view_options(self, event=None):
        """Open a toplevel window to edit the view options."""
        ViewOptionsDialog(self._mdl, self._ui, self)
        return 'break'

    def refresh_tree(self, event=None):
        """Update all registered views."""
        self._ui.propertiesView.apply_changes()
        self._mdl.renumber_chapters()
        self._mdl.prjFile.adjust_section_types()
        self._mdl.novel.update_plot_lines()
        self._ui.refresh()
        return 'break'

    def reload_project(self, event=None):
        """Discard changes and reload the project."""
        if self._mdl.prjFile is None:
            return 'break'

        if self._mdl.isModified and not self._ui.ask_yes_no(_('Discard changes and reload the project?')):
            return 'break'

        if self._mdl.prjFile.has_changed_on_disk() and not self._ui.ask_yes_no(_('File has changed on disk. Reload anyway?')):
            return 'break'

        # this is to avoid saving when closing the project
        if self.open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True):
            # includes closing
            self._ui.set_status(_('Project successfully restored from disk.'))
        return 'break'

    def restore_backup(self, event=None):
        """Discard changes and restore the latest backup file."""
        if self._mdl.prjFile is None:
            return 'break'

        latestBackup = f'{self._mdl.prjFile.filePath}.bak'
        if not os.path.isfile(latestBackup):
            self._ui.set_status(f'!{_("No backup available")}')
            return 'break'

        if self._mdl.isModified:
            if not self._ui.ask_yes_no(_('Discard changes and restore the latest backup?')):
                return 'break'

        elif not self._ui.ask_yes_no(_('Restore the latest backup?')):
            return 'break'

        try:
            os.replace(latestBackup, self._mdl.prjFile.filePath)
        except Exception as ex:
            self._ui.set_status(str(ex))
        else:
            if self.open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True):
                # Includes closing
                self._ui.set_status(_('Latest backup successfully restored.'))
        return 'break'

    def save_as(self, event=None):
        """Rename the project file and save it to disk.
        
        Return True on success, otherwise return False.
        """
        if self._mdl.prjFile is None:
            return False

        if prefs['last_open']:
            startDir, __ = os.path.split(prefs['last_open'])
        else:
            startDir = '.'
        fileName = filedialog.asksaveasfilename(
            filetypes=self._fileTypes,
            defaultextension=self._fileTypes[0][1],
            initialdir=startDir,
            )
        if fileName:
            if self._mdl.prjFile is not None:
                self._ui.propertiesView.apply_changes()
                try:
                    self._mdl.save_project(fileName)
                except Error as ex:
                    self._ui.set_status(f'!{str(ex)}')
                else:
                    self.unlock()
                    self._ui.show_path(f'{norm_path(self._mdl.prjFile.filePath)} ({_("last saved on")} {self._mdl.prjFile.fileDate})')
                    self._ui.restore_status()
                    prefs['last_open'] = self._mdl.prjFile.filePath
                    return True

        return False

    def save_project(self, event=None):
        """Save the novelibre project to disk.
        
        Return True on success, otherwise return False.
        """
        if self._mdl.prjFile is None:
            return False

        if self.check_lock():
            self._ui.set_status(f'!{_("Cannot save: The project is locked")}.')
            return False

        if self._mdl.prjFile.filePath is None:
            return self.save_as()

        if self._mdl.prjFile.has_changed_on_disk() and not self._ui.ask_yes_no(_('File has changed on disk. Save anyway?')):
            return False

        self._ui.propertiesView.apply_changes()
        try:
            self._mdl.save_project()
        except Error as ex:
            self._ui.set_status(f'!{str(ex)}')
            return False

        self._ui.show_path(f'{norm_path(self._mdl.prjFile.filePath)} ({_("last saved on")} {self._mdl.prjFile.fileDate})')
        self._ui.restore_status()
        prefs['last_open'] = self._mdl.prjFile.filePath
        return True

    def set_character_status(self, isMajor, elemIds=None):
        """Set character status to Major.
        
        Optional arguments:
            isMajor: bool -- If True, make the characters major. Otherwise, make them minor.
            elemIds: list of character IDs to process.
        """
        if self.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._ui.tv.open_children(CR_ROOT)
        self._mdl.set_character_status(isMajor, elemIds)

    def set_level(self, newLevel, elemIds=None):
        """Set chapter or stage level.
        
        Positional arguments:
            newLevel: int -- New level to be set.
            elemIds: list of IDs to process.
        """
        if self.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._mdl.set_level(newLevel, elemIds)

    def set_completion_status(self, newStatus, elemIds=None):
        """Set section completion status (Outline/Draft..).
        
        Positional arguments:
            newStatus: int -- New section status to be set.        
            elemIds: list of IDs to process.            
        """
        if self.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._ui.tv.open_children(elemIds[0])
        self._mdl.set_completion_status(newStatus, elemIds)

    def set_type(self, newType, elemIds=None):
        """Set section or chapter type Normal).
        
        Positional arguments:
            newType: int -- New type to be set.
            elemIds: list of IDs to process.
        """
        if self.check_lock():
            return

        if elemIds is None:
            try:
                elemIds = self._ui.selectedNodes
            except:
                return

        self._ui.tv.open_children(elemIds[0])
        self._mdl.set_type(newType, elemIds)

    def show_plot_list(self, event=None):
        self.show_report(PLOTLIST_SUFFIX)

    def toggle_lock(self, event=None):
        """Toggle the 'locked' status."""
        if self.isLocked:
            self.unlock()
        else:
            self.lock()
        return 'break'

    def update_from_odt(self, suffix='', event=None):
        """Update the project from an exported ODT document specified by suffix. 
        
        Optional arguments:
            suffix: str -- the document's file name suffix, indicating the document type.        
        """
        fileName, __ = os.path.splitext(self._mdl.prjFile.filePath)
        self.import_odf(sourcePath=f'{fileName}{suffix}.odt')
        return 'break'


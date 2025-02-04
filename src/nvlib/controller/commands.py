"""Provide a controller mixin class for novelibre user interaction.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import webbrowser

from nvlib.controller.services.nv_help import NvHelp
from nvlib.gui.pop_up.backup_options_dialog import BackupOptionsDialog
from nvlib.gui.pop_up.export_options_dialog import ExportOptionsDialog
from nvlib.gui.pop_up.plugin_manager_dialog import PluginManagerDialog
from nvlib.gui.pop_up.reimport_dialog import ReimportDialog
from nvlib.gui.pop_up.view_options_dialog import ViewOptionsDialog
from nvlib.novx_globals import BRF_SYNOPSIS_SUFFIX
from nvlib.novx_globals import CHAPTERS_SUFFIX
from nvlib.novx_globals import CHARACTERS_SUFFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import CHARACTER_REPORT_SUFFIX
from nvlib.novx_globals import CHARLIST_SUFFIX
from nvlib.novx_globals import DATA_SUFFIX
from nvlib.novx_globals import ELEMENT_NOTES_SUFFIX
from nvlib.novx_globals import GRID_SUFFIX
from nvlib.novx_globals import ITEMLIST_SUFFIX
from nvlib.novx_globals import ITEMS_SUFFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import ITEM_REPORT_SUFFIX
from nvlib.novx_globals import LOCATIONS_SUFFIX
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import LOCATION_REPORT_SUFFIX
from nvlib.novx_globals import LOCLIST_SUFFIX
from nvlib.novx_globals import MANUSCRIPT_SUFFIX
from nvlib.novx_globals import PARTS_SUFFIX
from nvlib.novx_globals import PLOTLINES_SUFFIX
from nvlib.novx_globals import PLOTLIST_SUFFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PROJECTNOTES_SUFFIX
from nvlib.novx_globals import PROOF_SUFFIX
from nvlib.novx_globals import SECTIONLIST_SUFFIX
from nvlib.novx_globals import SECTIONS_SUFFIX
from nvlib.novx_globals import STAGES_SUFFIX
from nvlib.novx_globals import TIMETABLE_SUFFIX
from nvlib.novx_globals import XREF_SUFFIX
from nvlib.nv_globals import HOME_URL


class Commands:
    """Methods for callback functions."""

    def add_new_chapter(self, **kwargs):
        """Create a chapter instance and add it to the novel.
             
        Optional keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            chType: int -- Chapter type. Default: 0.
            NoNumber: str -- Do not auto-number this chapter. Default: None.
            
        Return the chapter ID, if successful.
        """
        if not self.check_lock():
            return self.elementManager.add_new_chapter(**kwargs)

    def add_new_character(self, **kwargs):
        """Create a character instance and add it to the novel.
        
        Optional keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title.
            isMajor: bool -- If True, make the new character a major character. Default: False.
            
        Return the element's ID, if successful.
        """
        if not self.check_lock():
            return self.elementManager.add_new_character(**kwargs)

    def add_new_child(self, event=None):
        """Add a child element to an element.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if not self.check_lock():
            return self.elementManager.add_new_child()

    def add_new_element(self, event=None):
        """Create an element instance and add it to the novel.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if not self.check_lock():
            return self.elementManager.add_new_element()

    def add_new_item(self, **kwargs):
        """Create an item instance and add it to the novel.
        
        Optional keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        if not self.check_lock():
            return self.elementManager.add_new_item(**kwargs)

    def add_new_location(self, **kwargs):
        """Create a location instance and add it to the novel.
        
        Optional keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        if not self.check_lock():
            return self.elementManager.add_new_location(**kwargs)

    def add_multiple_new_sections(self):
        """Ask how many sections are to be added, then call the controller."""
        if not self.check_lock():
            return self.elementManager.add_multiple_new_sections()

    def add_new_parent(self, event=None):
        """Add a parent element to an element.
        
        What kind of element is added, depends on the selection's prefix.
        """
        if not self.check_lock():
            return self.elementManager.add_new_parent()

    def add_new_part(self, **kwargs):
        """Create a part instance and add it to the novel.
        
        Optional keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str: Part title. Default -- Auto-generated title. 
            chType: int: Part type. Default -- 0.  
            NoNumber: str: Do not auto-number this part. Default -- None.
           
        Return the chapter ID, if successful.
        """
        if not self.check_lock():
            return self.elementManager.add_new_part(**kwargs)

    def add_new_plot_line(self, **kwargs):
        """Create a plot line instance and add it to the novel.
        
        Optional keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the plot line ID, if successful.
        """
        if not self.check_lock():
            return self.elementManager.add_new_plot_line(**kwargs)

    def add_new_plot_point(self, **kwargs):
        """Create a plot point instance and add it to the novel.
        
        Optional keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Section title. Default: Auto-generated title. 
            
        Return the plot point ID, if successful.
        """
        if not self.check_lock():
            return self.elementManager.add_new_plot_point(**kwargs)

    def add_new_project_note(self, **kwargs):
        """Create a Project note instance and add it to the novel.
        
        Optional keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Element title. Default: Auto-generated title. 
            
        Return the element's ID, if successful.
        """
        if not self.check_lock():
            return self.elementManager.add_new_project_note(**kwargs)

    def add_new_section(self, **kwargs):
        """Create a section instance and add it to the novel.
        
        Optional keyword arguments:
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
        if not self.check_lock():
            return self.elementManager.add_new_section(**kwargs)

    def add_new_stage(self, **kwargs):
        """Create a stage instance and add it to the novel.
        
        Optional keyword arguments:
            targetNode: str -- Tree position where to place a new node.
            title: str -- Stage title. Default: Auto-generated title. 
            desc: str -- Description.
            scType: int -- Scene type. Default: 3.
            
        Return the section ID, if successful.
        """
        if not self.check_lock():
            return self.elementManager.add_new_stage(**kwargs)

    def close_project(self, event=None, doNotSave=False):
        """Close the current project.
        
        Optional arguments:
            doNotSave: Boolean -- If True, close the current project without saving.
        """
        return self.on_close(doNotSave=doNotSave)

    def copy_css(self, event=None):
        """Copy the provided css style sheet into the project directory."""
        self.fileManager.copy_css()
        return 'break'

    def create_project(self, event=None):
        """Create a novelibre project instance."""
        self.fileManager.create_project()
        return 'break'

    def cut_element(self, event=None):
        self.clipboardManager.cut_element()

    def copy_element(self, event=None):
        self.clipboardManager.copy_element()

    def delete_elements(self, event=None, elements=None):
        """Delete elements and their children.
        
        Optional arguments:
            elements: list of IDs of the elements to delete.        
        """
        if not self.check_lock():
            self.elementManager.delete_elements(elements)

    def discard_manuscript(self):
        """Rename the current editable manuscript. 
        
        This might be useful to avoid confusion in certain cases.
        """
        self.fileManager.discard_manuscript()

    def exclude_plot_line(self, event=None):
        if not self.check_lock():
            self.elementManager.exclude_plot_line()

    def export_brief_synopsis(self, event=None):
        self.fileManager.export_document(BRF_SYNOPSIS_SUFFIX, lock=False, overwrite=True)

    def export_chapter_desc(self, event=None):
        self.fileManager.export_document(CHAPTERS_SUFFIX)

    def export_character_desc(self, event=None):
        self.fileManager.export_document(CHARACTERS_SUFFIX)

    def export_character_list(self, event=None):
        self.fileManager.export_document(CHARLIST_SUFFIX)

    def export_cross_references(self, event=None):
        self.fileManager.export_document(XREF_SUFFIX, lock=False, overwrite=True)

    def export_final_document(self, event=None):
        self.fileManager.export_document('', lock=False)

    def export_item_desc(self, event=None):
        self.fileManager.export_document(ITEMS_SUFFIX)

    def export_item_list(self, event=None):
        self.fileManager.export_document(ITEMLIST_SUFFIX)

    def export_location_desc(self, event=None):
        self.fileManager.export_document(LOCATIONS_SUFFIX)

    def export_location_list(self, event=None):
        self.fileManager.export_document(LOCLIST_SUFFIX)

    def export_part_desc(self, event=None):
        self.fileManager.export_document(PARTS_SUFFIX)

    def export_manuscript(self, event=None):
        self.fileManager.export_document(MANUSCRIPT_SUFFIX)

    def export_plot_grid(self, event=None):
        self.fileManager.export_document(GRID_SUFFIX)

    def export_plot_lines_desc(self, event=None):
        self.fileManager.export_document(PLOTLINES_SUFFIX, lock=False)

    def export_plot_list(self, event=None):
        self.fileManager.export_document(PLOTLIST_SUFFIX, lock=False)

    def export_proofing_manuscript(self, event=None):
        self.fileManager.export_document(PROOF_SUFFIX)

    def export_section_desc(self, event=None):
        self.fileManager.export_document(SECTIONS_SUFFIX)

    def export_section_list(self, event=None):
        self.fileManager.export_document(SECTIONLIST_SUFFIX, lock=False)

    def export_story_structure_desc(self, event=None):
        self.fileManager.export_document(STAGES_SUFFIX)

    def export_xml_data_files(self, event=None):
        self.fileManager.export_document(DATA_SUFFIX, lock=False, show=False)

    def import_character_data(self, event=None):
        if not self.check_lock():
            self.elementManager.import_elements(CHARACTER_PREFIX)

    def import_item_data(self, event=None):
        if not self.check_lock():
            self.elementManager.import_elements(ITEM_PREFIX)

    def import_location_data(self, event=None):
        if not self.check_lock():
            self.elementManager.import_elements(LOCATION_PREFIX)

    def import_odf(self, sourcePath=None, defaultExtension='.odt'):
        """Update or create the project from an ODF document.
        
        Optional arguments:
            sourcePath: str -- Path specifying the source document. If None, a file picker is used.
            defaultExtension: str -- Extension to be preset in the file picker.
        """
        if not self.check_lock():
            self.fileManager.import_odf(sourcePath, defaultExtension)

    def import_plot_lines(self, event=None):
        if not self.check_lock():
            self.elementManager.import_elements(PLOT_LINE_PREFIX)

    def include_plot_line(self, event=None):
        if not self.check_lock():
            self.elementManager.include_plot_line()

    def join_sections(self, event=None, scId0=None, scId1=None):
        """Join section 0 with section 1.

        Optional arguments:
            scId0: str -- ID of the section to be extended
            scId1: str -- ID of the section to be discarded.
            
        If not both arguments are given, determine them from the tree selection.
        """
        if not self.check_lock():
            self.elementManager.join_sections(scId0, scId1)

    def move_node(self, node, targetNode):
        """Move a node to another position.
        
        Positional arguments:
            node: str - ID of the node to move.
            targetNode: str -- ID of the new parent/predecessor of the node.
        """
        if not self.isLocked:
            self.elementManager.move_node(node, targetNode)

    def open_backup_options(self, event=None):
        """Open a toplevel window to edit the backup options."""
        BackupOptionsDialog(self._mdl, self._ui, self)
        return 'break'

    def open_export_options(self, event=None):
        """Open a toplevel window to edit the export options."""
        ExportOptionsDialog(self._mdl, self._ui, self)
        return 'break'

    def open_help(self, event=None):
        NvHelp.open_help_page('')

    def open_homepage(self, event=None):
        webbrowser.open(HOME_URL)

    def open_installationFolder(self, event=None):
        """Open the installation folder with the OS file manager."""
        self.fileManager.open_installationFolder()
        return 'break'

    def open_link(self, element, linkIndex):
        """Open a linked file.
        
        Positional arguments:
            element: BasicElement or subclass.
            linkIndex: int -- Index of the link to open.
                    
        The linkProcessor strategy can be overridden e.g. by plugins.
        """
        self.linkProcessor.open_link_by_index(element, linkIndex)

    def open_manuscript(self, event=None):
        """Export a manuscript document and open it for editing."""
        self.fileManager.export_document(MANUSCRIPT_SUFFIX, ask=False)

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
        return self.fileManager.open_project(filePath=filePath, doNotSave=doNotSave)

    def open_project_folder(self, event=None):
        """Open the project folder with the OS file manager."""
        self.fileManager.open_project_folder()
        return 'break'

    def open_project_updater(self, event=None):
        """Update the project from a previously exported document.
        
        Using a toplevel window with a pick list of refresh sources.
        """
        if not self.check_lock():
            ReimportDialog(self._mdl, self._ui, self)
        return 'break'

    def open_view_options(self, event=None):
        """Open a toplevel window to edit the view options."""
        ViewOptionsDialog(self._mdl, self._ui, self)
        return 'break'

    def paste_element(self, event=None):
        self.clipboardManager.paste_element()

    def refresh_tree(self, event=None):
        """Update the project structure."""
        self._ui.propertiesView.apply_changes()
        self._mdl.renumber_chapters()
        self._mdl.prjFile.adjust_section_types()
        self._mdl.novel.update_plot_lines()
        return 'break'

    def reload_project(self, event=None):
        """Discard changes and reload the project."""
        self.fileManager.reload_project()
        return 'break'

    def restore_backup(self, event=None):
        """Discard changes and restore the latest backup file."""
        self.fileManager.restore_backup()
        return 'break'

    def save_as(self, event=None):
        """Rename the project file and save it to disk.
        
        Return True on success, otherwise return False.
        """
        return self.fileManager.save_as()

    def save_project(self, event=None):
        """Save the novelibre project to disk.
        
        Return True on success, otherwise return False.
        """
        return self.fileManager.save_project()

    def set_chr_status_major(self, event=None):
        if not self.check_lock():
            self.elementManager.set_character_status(True)

    def set_chr_status_minor(self, event=None):
        if not self.check_lock():
            self.elementManager.set_character_status(False)

    def set_level_1(self, event=None):
        if not self.check_lock():
            self.elementManager.set_level(1)

    def set_level_2(self, event=None):
        if not self.check_lock():
            self.elementManager.set_level(2)

    def set_scn_status_outline(self, event=None):
        if not self.check_lock():
            self.elementManager.set_completion_status(1)

    def set_scn_status_draft(self, event=None):
        if not self.check_lock():
            self.elementManager.set_completion_status(2)

    def set_scn_status_1st_edit(self, event=None):
        if not self.check_lock():
            self.elementManager.set_completion_status(3)

    def set_scn_status_2nd_edit(self, event=None):
        if not self.check_lock():
            self.elementManager.set_completion_status(4)

    def set_scn_status_done(self, event=None):
        if not self.check_lock():
            self.elementManager.set_completion_status(5)

    def set_type_normal(self, event=None):
        if not self.check_lock():
            self.elementManager.set_type(0)

    def set_type_unused(self, event=None):
        if not self.check_lock():
            self.elementManager.set_type(1)

    def show_character_list(self, event=None):
        self.fileManager.show_report(CHARACTER_REPORT_SUFFIX)

    def show_notes_list(self, event=None):
        self.fileManager.show_report(ELEMENT_NOTES_SUFFIX)

    def show_item_list(self, event=None):
        self.fileManager.show_report(ITEM_REPORT_SUFFIX)

    def show_location_list(self, event=None):
        self.fileManager.show_report(LOCATION_REPORT_SUFFIX)

    def show_plot_list(self, event=None):
        self.fileManager.show_report(PLOTLIST_SUFFIX)

    def show_projectnotes_list(self, event=None):
        self.fileManager.show_report(PROJECTNOTES_SUFFIX)

    def show_timetable(self, event=None):
        self.fileManager.show_report(TIMETABLE_SUFFIX)

    def split_file(self, event=None):
        if not self.check_lock():
            self.fileSplitter.split_project()

    def toggle_lock(self, event=None):
        """Toggle the 'locked' status."""
        if self.isLocked:
            self.unlock()
        else:
            self.lock()
        return 'break'

    def update_from_manuscript(self, event=None):
        """Update the project from the previously exported manuscript document."""
        if not self.check_lock():
            fileName, __ = os.path.splitext(self._mdl.prjFile.filePath)
            self.fileManager.import_odf(sourcePath=f'{fileName}{MANUSCRIPT_SUFFIX}.odt')
        return 'break'


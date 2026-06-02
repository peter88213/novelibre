"""Provide a main view mixin class with the main menu definition.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.gui.menus.nv_context_menu import NvContextMenu
from nvlib.gui.menus.nv_menu import NvMenu
from nvlib.gui.menus.tree_context_menu import TreeContextMenu
from nvlib.gui.platform.platform_settings import KEYS
from nvlib.gui.platform.platform_settings import PLATFORM
from nvlib.novx_globals import CHAPTER_PREFIX
from nvlib.novx_globals import CHARACTER_PREFIX
from nvlib.novx_globals import ITEM_PREFIX
from nvlib.novx_globals import LOCATION_PREFIX
from nvlib.novx_globals import PLOT_LINE_PREFIX
from nvlib.novx_globals import PRJ_NOTE_PREFIX
from nvlib.novx_globals import SECTION_PREFIX
from nvlib.nv_locale import _


class MainMenu:

    def add_add_command(self, menu):
        label = _('Add')
        menu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_element,
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

    def add_clone_command(self, menu):
        label = _('Clone')
        menu.add_command(
            label=label,
            command=self._ctrl.clone_section,
        )
        menu.disableOnLock.append(label)

    def add_color_commands(self, menu, prefix=None):
        label = f"{_('Assign color')}..."
        menu.add_command(
            label=label,
            image=self.icons.colorsIcon,
            compound='left',
            command=lambda p=prefix: self._ctrl.set_color(prefix=p)
        )
        menu.disableOnLock.append(label)

        label = _('Reset color')
        menu.add_command(
            label=label,
            image=self.icons.resetColorsIcon,
            compound='left',
            command=lambda p=prefix: self._ctrl.reset_color(prefix=p)
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
            image=self.icons.levelsIcon,
            compound='left',
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
            image=self.icons.stageIcon,
            compound='left',
            command=self._ctrl.add_new_stage,
        )
        menu.disableOnLock.append(label)

    def add_set_cr_status_cascade(self, menu):
        label = _('Set Status')
        menu.add_cascade(
            label=label,
            image=self.icons.statusIcon,
            compound='left',
            menu=self.selectCharacterStatusMenu,
        )
        menu.disableOnLock.append(label)

    def add_set_status_cascade(self, menu):
        label = _('Set Status')
        menu.add_cascade(
            label=label,
            image=self.icons.statusIcon,
            compound='left',
            menu=self.selectSectionStatusMenu,
        )
        menu.disableOnLock.append(label)

    def add_set_type_cascade(self, menu):
        label = _('Set Type')
        menu.add_cascade(
            label=label,
            image=self.icons.typeIcon,
            compound='left',
            menu=self.selectTypeMenu,
        )
        menu.disableOnLock.append(label)

    def add_set_viewpoint_command(self, menu):
        label = _('Set Viewpoint...')
        menu.add_command(
            label=label,
            image=self.icons.povIcon,
            compound='left',
            command=self._ctrl.set_viewpoint,
        )
        menu.disableOnLock.append(label)

    def add_view_commands(self, menu):
        label = _('Chapter level')
        menu.add_command(
            label=label,
            image=self.icons.chaptersIcon,
            compound='left',
            command=self.tv.show_chapter_level,
        )
        menu.disableOnClose.append(label)

        label = _('Expand all')
        menu.add_command(
            label=label,
            image=self.icons.expandIcon,
            compound='left',
            command=self.tv.expand_all,
        )
        menu.disableOnClose.append(label)

        label = _('Collapse all')
        menu.add_command(
            label=label,
            image=self.icons.collapseIcon,
            compound='left',
            command=self.tv.collapse_all,
        )
        menu.disableOnClose.append(label)

    def create_menus(self):

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
            image=self.icons.newProjectIcon,
            compound='left',
            menu=self.newMenu
        )

        label = _('Open...')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.OPEN_PROJECT[1],
            image=self.icons.openProjectIcon,
            compound='left',
            command=self._ctrl.open_project,
        )

        label = _('Reload')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.RELOAD_PROJECT[1],
            image=self.icons.reloadIcon,
            compound='left',
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
            image=self.icons.unlockIcon,
            compound='left',
            command=self._ctrl.unlock,
        )
        self.fileMenu.disableOnClose.append(label)

        self.fileMenu.add_separator()

        label = _('Open Project folder')
        self.fileMenu.add_command(
            label=label,
            accelerator=KEYS.FOLDER[1],
            image=self.icons.folderIcon,
            compound='left',
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
            image=self.icons.discardManuscriptIcon,
            compound='left',
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
            image=self.icons.saveAsIcon,
            compound='left',
            command=self._ctrl.save_as,
        )
        self.fileMenu.disableOnClose.append(label)

        label = _('Close')
        self.fileMenu.add_command(
            label=label,
            image=self.icons.closeIcon,
            compound='left',
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
            image=self.icons.exitIcon,
            compound='left',
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

        label = _('Show Plot lines')
        self.viewMenu.add_command(
            label=label,
            image=self.icons.viewPlotLinesIcon,
            compound='left',
            command=self.tv.show_plot_lines,
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
            image=self.icons.settingsIcon,
            compound='left',
            command=self._ctrl.open_view_options,
        )

        self._ctrl.register_client(self.viewMenu)

        # "Chapter".
        self.chapterMenu = NvMenu()

        self.add_chapter_part_commands(self.chapterMenu)

        label = _('Add multiple chapters...')
        self.chapterMenu.add_command(
            label=label,
            image=self.icons.addMultipleIcon,
            compound='left',
            command=self._ctrl.add_multiple_new_chapters,
        )
        self.chapterMenu.disableOnLock.append(label)

        self.chapterMenu.add_separator()

        self.add_set_type_cascade(self.chapterMenu)
        self.add_change_level_cascade(self.chapterMenu)
        self.add_color_commands(self.chapterMenu, prefix=CHAPTER_PREFIX)

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

        label = _('Export part descriptions for editing')
        self.chapterMenu.add_command(
            label=label,
            command=self._ctrl.export_part_desc,
        )
        self.chapterMenu.disableOnLock.append(label)

        label = _('Export chapter table')
        self.chapterMenu.add_command(
            label=label,
            command=self._ctrl.export_chapter_table,
        )
        self.chapterMenu.disableOnLock.append(label)

        label = _('Export part table')
        self.chapterMenu.add_command(
            label=label,
            command=self._ctrl.export_part_table,
        )
        self.chapterMenu.disableOnLock.append(label)

        self.chapterMenu.add_separator()

        label = _('Show chapter board in browser')
        self.chapterMenu.add_command(
            label=label,
            command=self._ctrl.show_chapter_board,
        )

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
            image=self.icons.addMultipleIcon,
            compound='left',
            command=self._ctrl.add_multiple_new_sections,
        )
        self.sectionMenu.disableOnLock.append(label)

        self.add_clone_command(self.sectionMenu)

        self.sectionMenu.add_separator()

        self.add_set_type_cascade(self.sectionMenu)
        self.add_set_status_cascade(self.sectionMenu)
        self.add_set_viewpoint_command(self.sectionMenu)
        self.add_color_commands(self.sectionMenu, prefix=SECTION_PREFIX)

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
            command=self._ctrl.export_section_table,
        )

        label = _('Show Time table')
        self.sectionMenu.add_command(
            label=label,
            command=self._ctrl.show_time_table,
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
        self.add_color_commands(self.characterMenu, prefix=CHARACTER_PREFIX)

        self.characterMenu.add_separator()

        label = _('Import')
        self.characterMenu.add_command(
            label=label,
            image=self.icons.importIcon,
            compound='left',
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
            command=self._ctrl.export_character_table,
        )
        self.characterMenu.disableOnLock.append(label)

        self.characterMenu.add_separator()

        label = _('Show table in Browser')
        self.characterMenu.add_command(
            label=label,
            command=self._ctrl.show_character_table,
        )

        label = _('Show viewpoint board in browser')
        self.characterMenu.add_command(
            label=label,
            command=self._ctrl.show_viewpoint_board,
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
        self.add_color_commands(self.locationMenu, prefix=LOCATION_PREFIX)
        self.locationMenu.add_separator()

        label = _('Import')
        self.locationMenu.add_command(
            label=label,
            image=self.icons.importIcon,
            compound='left',
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
            command=self._ctrl.export_location_table,
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
        self.add_color_commands(self.itemMenu, prefix=ITEM_PREFIX)
        self.itemMenu.add_separator()

        label = _('Import')
        self.itemMenu.add_command(
            label=label,
            image=self.icons.importIcon,
            compound='left',
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
            command=self._ctrl.export_item_table,
        )
        self.itemMenu.disableOnLock.append(label)

        self.itemMenu.add_separator()

        label = _('Show table in Browser')
        self.itemMenu.add_command(
            label=label,
            command=self._ctrl.show_item_list,
        )

        self._ctrl.register_client(self.itemMenu)

        # "Story structure".
        self.storyStructureMenu = NvMenu()

        self.add_insert_stage_command(self.storyStructureMenu)
        self.add_change_level_cascade(self.storyStructureMenu)

        self.storyStructureMenu.add_separator()

        label = _('Export story structure description for editing')
        self.storyStructureMenu.add_command(
            label=label,
            command=self._ctrl.export_story_structure_desc,
        )
        self.storyStructureMenu.disableOnLock.append(label)

        self.storyStructureMenu.add_separator()

        label = _('Show story structure board in browser')
        self.storyStructureMenu.add_command(
            label=label,
            command=self._ctrl.show_story_structure_board,
        )

        self._ctrl.register_client(self.storyStructureMenu)

        # "Plot lines".
        self.plotLinesMenu = NvMenu()

        label = _('Add Plot line')
        self.plotLinesMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_plot_line,
        )
        self.plotLinesMenu.disableOnLock.append(label)

        label = _('Add Plot point')
        self.plotLinesMenu.add_command(
            label=label,
            image=self.icons.addIcon,
            compound='left',
            command=self._ctrl.add_new_plot_point,
        )
        self.plotLinesMenu.disableOnLock.append(label)

        self.plotLinesMenu.add_separator()

        self.add_color_commands(self.plotLinesMenu, prefix=PLOT_LINE_PREFIX)

        self.plotLinesMenu.add_separator()

        label = _('Import plot lines')
        self.plotLinesMenu.add_command(
            label=label,
            image=self.icons.importIcon,
            compound='left',
            command=self._ctrl.import_plot_lines,
        )
        self.plotLinesMenu.disableOnLock.append(label)

        self.plotLinesMenu.add_separator()

        label = _('Export plot grid for editing')
        self.plotLinesMenu.add_command(
            label=label,
            image=self.icons.gridIcon,
            compound='left',
            command=self._ctrl.export_plot_grid,
        )
        self.plotLinesMenu.disableOnLock.append(label)

        label = _('Export plot line descriptions for editing')
        self.plotLinesMenu.add_command(
            label=label,
            command=self._ctrl.export_plot_lines_desc,
        )
        self.plotLinesMenu.disableOnLock.append(label)

        self.plotLinesMenu.add_separator()

        label = _('Plot table (export only)')
        self.plotLinesMenu.add_command(
            label=label,
            command=self._ctrl.export_plot_list,
        )

        label = _('Show Plot table in browser')
        self.plotLinesMenu.add_command(
            label=label,
            command=self._ctrl.show_plot_table,
        )

        label = _('Show Plot line board in browser')
        self.plotLinesMenu.add_command(
            label=label,
            command=self._ctrl.show_plot_line_board,
        )

        label = _('Show Plot grid in browser')
        self.plotLinesMenu.add_command(
            label=label,
            command=self._ctrl.show_plot_grid,
        )

        self._ctrl.register_client(self.plotLinesMenu)

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
        self.add_color_commands(self.prjNoteMenu, prefix=PRJ_NOTE_PREFIX)
        self.prjNoteMenu.add_separator()

        label = _('Export project notes for editing')
        self.prjNoteMenu.add_command(
            label=label,
            command=self._ctrl.export_project_notes,
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

        label = _('Manuscript including unused text')
        self.exportMenu.add_command(
            label=label,
            command=self._ctrl.export_manuscript_with_unused,
        )
        self.exportMenu.disableOnLock.append(label)
        self.exportMenu.disableOnClose.append(label)

        label = _('Metadata text table for editing')
        self.exportMenu.add_command(
            label=label,
            command=self._ctrl.export_metadata_text,
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
            image=self.icons.exportIcon,
            compound='left',
            command=self._ctrl.export_xml_data_files,
        )
        self.exportMenu.disableOnClose.append(label)

        self.exportMenu.add_separator()

        label = _('Options')
        self.exportMenu.add_command(
            label=label,
            image=self.icons.settingsIcon,
            compound='left',
            command=self._ctrl.open_export_options,
        )

        self._ctrl.register_client(self.exportMenu)

        # "Tools".
        self.toolsMenu = NvMenu()

        label = _('Backup options')
        self.toolsMenu.add_command(
            label=label,
            image=self.icons.settingsIcon,
            compound='left',
            command=self._ctrl.open_backup_options,
        )

        self.toolsMenu.add_separator()

        label = _('Open installation folder')
        self.toolsMenu.add_command(
            label=label,
            image=self.icons.installationFolderIcon,
            compound='left',
            command=self._ctrl.open_installationFolder,
        )

        self.toolsMenu.add_separator()

        label = _('Plugin Manager')
        self.toolsMenu.add_command(
            label=label,
            image=self.icons.pluginsIcon,
            compound='left',
            command=self._ctrl.open_plugin_manager,
        )

        self.toolsMenu.add_separator()

        label = _('Show notes')
        self.toolsMenu.add_command(
            label=label,
            image=self.icons.stickyNoteIcon,
            compound='left',
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
            image=self.icons.helpIcon,
            compound='left',
            command=self._ctrl.open_help,
        )

        label = _('About novelibre')
        self.helpMenu.add_command(
            label=label,
            image=self.icons.nLogoIcon,
            compound='left',
            command=self._about,
        )

        label = f"novelibre {_('Home page')}"
        self.helpMenu.add_command(
            label=label,
            image=self.icons.homeIcon,
            compound='left',
            command=self._ctrl.open_homepage,
        )

        label = _('News about novelibre')
        self.helpMenu.add_command(
            label=label,
            image=self.icons.newsIcon,
            compound='left',
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

        label = _('Story structure')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.storyStructureMenu
        )
        self.mainMenu.disableOnClose.append(label)

        label = _('Plot lines')
        self.mainMenu.add_cascade(
            label=label,
            menu=self.plotLinesMenu
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

        # Book context menu.
        self.bookContextMenu = NvContextMenu()

        self.add_chapter_part_commands(self.bookContextMenu)

        self.bookContextMenu.add_separator()

        self.add_set_status_cascade(self.bookContextMenu)
        self.add_set_viewpoint_command(self.bookContextMenu)

        self.bookContextMenu.add_separator()

        self.add_view_commands(self.bookContextMenu)

        self._ctrl.register_client(self.bookContextMenu)

        # Chapter context menu.
        self.chapterContextMenu = NvContextMenu()

        self.add_add_section_command(self.chapterContextMenu)
        self.add_chapter_part_commands(self.chapterContextMenu)
        self.add_insert_stage_command(self.chapterContextMenu)

        self.chapterContextMenu.add_separator()

        label = _('Remove this chapter, keep sections')
        self.chapterContextMenu.add_command(
            label=label,
            command=self._ctrl.remove_chapter_keep_sections,
        )
        self.chapterContextMenu.disableOnLock.append(label)

        self.add_delete_command(self.chapterContextMenu)

        self.chapterContextMenu.add_separator()

        self.add_clipboard_commands(self.chapterContextMenu)

        self.chapterContextMenu.add_separator()

        self.add_change_level_cascade(self.chapterContextMenu)
        self.add_set_type_cascade(self.chapterContextMenu)
        self.add_set_status_cascade(self.chapterContextMenu)
        self.add_set_viewpoint_command(self.chapterContextMenu)
        self.add_color_commands(self.chapterContextMenu)

        self.chapterContextMenu.add_separator()

        label = _('Export this chapter')
        self.chapterContextMenu.add_cascade(
            label=label,
            image=self.icons.manuscriptIcon,
            compound='left',
            command=self._ctrl.export_filtered_manuscript,
        )
        self.chapterContextMenu.disableOnLock.append(label)

        self.chapterContextMenu.add_separator()

        self.add_view_commands(self.chapterContextMenu)

        self._ctrl.register_client(self.chapterContextMenu)

        # Character context menu.
        self.characterContextMenu = NvContextMenu()

        self.add_add_command(self.characterContextMenu)

        self.characterContextMenu.add_separator()

        self.add_delete_command(self.characterContextMenu)

        self.characterContextMenu.add_separator()

        self.add_clipboard_commands(self.characterContextMenu)

        self.characterContextMenu.add_separator()

        self.add_set_cr_status_cascade(self.characterContextMenu)
        self.add_color_commands(self.characterContextMenu)

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

        # Characters root context menu.
        self.crRootContextMenu = NvContextMenu()

        self.add_add_command(self.crRootContextMenu)

        self.crRootContextMenu.add_separator()

        self.add_set_cr_status_cascade(self.crRootContextMenu)

        self.crRootContextMenu.add_separator()

        self.add_view_commands(self.crRootContextMenu)

        self._ctrl.register_client(self.crRootContextMenu)

        # Location/item/plot point/project note context menu.
        self.elementContextMenu = NvContextMenu()

        self.add_add_command(self.elementContextMenu)

        self.elementContextMenu.add_separator()

        self.add_delete_command(self.elementContextMenu)

        self.elementContextMenu.add_separator()

        self.add_clipboard_commands(self.elementContextMenu)

        self.elementContextMenu.add_separator()
        self.add_color_commands(self.elementContextMenu)
        self.elementContextMenu.add_separator()

        self.add_view_commands(self.elementContextMenu)

        self.elementContextMenu.add_separator()

        self.add_highlight_related_command(self.elementContextMenu)

        self._ctrl.register_client(self.elementContextMenu)

        # Plot line context menu.
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
        self.add_color_commands(self.plotLineContextMenu)
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
            image=self.icons.manuscriptIcon,
            compound='left',
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

        # Locations/items/plot lines/project notes root menu.
        self.rootContextMenu = NvContextMenu()

        self.add_add_command(self.rootContextMenu)

        self.rootContextMenu.add_separator()

        self.add_view_commands(self.rootContextMenu)

        self._ctrl.register_client(self.rootContextMenu)

        # Section context menu.
        self.sectionContextMenu = NvContextMenu()

        self.add_add_section_command(self.sectionContextMenu)
        self.add_insert_stage_command(self.sectionContextMenu)

        label = _('Insert Chapter')
        self.sectionContextMenu.add_command(
            label=label,
            command=self._ctrl.insert_chapter,
        )
        self.sectionContextMenu.disableOnLock.append(label)

        self.add_clone_command(self.sectionContextMenu)
        label = _('Join with previous')
        self.sectionContextMenu.add_command(
            label=label,
            command=self._ctrl.join_sections,
        )
        self.sectionContextMenu.disableOnLock.append(label)

        self.sectionContextMenu.add_separator()

        self.add_delete_command(self.sectionContextMenu)

        self.sectionContextMenu.add_separator()

        self.add_clipboard_commands(self.sectionContextMenu)

        self.sectionContextMenu.add_separator()

        self.add_set_type_cascade(self.sectionContextMenu)
        self.add_set_status_cascade(self.sectionContextMenu)
        self.add_set_viewpoint_command(self.sectionContextMenu)
        self.add_color_commands(self.sectionContextMenu)

        self.sectionContextMenu.add_separator()

        self.add_view_commands(self.sectionContextMenu)

        self._ctrl.register_client(self.sectionContextMenu)

        # Stage context menu.
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

        # Trash bin context menu.
        self.trashContextMenu = NvContextMenu()

        self.add_delete_command(self.trashContextMenu)

        self._ctrl.register_client(self.trashContextMenu)

        self.contextMenu = TreeContextMenu(self._mdl, self)


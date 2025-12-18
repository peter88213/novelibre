"""Provide icons for the novelibre.GUI

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvlib.nv_globals import PROGRAM_DIR
from nvlib.nv_globals import prefs
import tkinter as tk


class Icons:

    def __init__(self):
        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16

        try:
            iconPath = f'{PROGRAM_DIR}/icons/{size}'
        except:
            iconPath = None

        self.addChildIcon = self.new_icon(f'{iconPath}/addChild.png')

        self.addIcon = self.new_icon(f'{iconPath}/add.png')

        self.addMultipleIcon = self.new_icon(f'{iconPath}/add_multiple.png')

        self.addParentIcon = self.new_icon(f'{iconPath}/addParent.png')

        self.chaptersIcon = self.new_icon(f'{iconPath}/chapters.png')

        self.closeIcon = self.new_icon(f'{iconPath}/close.png')

        self.collapseIcon = self.new_icon(f'{iconPath}/collapse.png')

        self.copyIcon = self.new_icon(f'{iconPath}/copy.png')

        self.cutIcon = self.new_icon(f'{iconPath}/cut.png')

        self.discardManuscriptIcon = self.new_icon(
            f'{iconPath}/discardManuscript.png')

        self.exitIcon = self.new_icon(f'{iconPath}/exit.png')

        self.expandIcon = self.new_icon(f'{iconPath}/expand.png')

        self.exportIcon = self.new_icon(f'{iconPath}/export.png')

        self.folderIcon = self.new_icon(f'{iconPath}/folder.png')

        self.goBackIcon = self.new_icon(f'{iconPath}/goBack.png')

        self.goForwardIcon = self.new_icon(f'{iconPath}/goForward.png')

        self.gotoIcon = self.new_icon(f'{iconPath}/goto.png')

        self.gridIcon = self.new_icon(f'{iconPath}/grid.png')

        self.helpIcon = self.new_icon(f'{iconPath}/help.png')

        self.highlightIcon = self.new_icon(f'{iconPath}/highlight.png')

        self.homeIcon = self.new_icon(f'{iconPath}/home.png')

        self.importIcon = self.new_icon(f'{iconPath}/import.png')

        self.installationFolderIcon = self.new_icon(
            f'{iconPath}/installation_folder.png')

        self.levelsIcon = self.new_icon(f'{iconPath}/levels.png')

        self.lockIcon = self.new_icon(f'{iconPath}/lock.png')

        self.manuscriptIcon = self.new_icon(f'{iconPath}/manuscript.png')

        self.nLogoIcon = self.new_icon(f'{iconPath}/nLogo.png')

        self.newProjectIcon = self.new_icon(f'{iconPath}/newProject.png')

        self.newsIcon = self.new_icon(f'{iconPath}/smile.png')

        self.openProjectIcon = self.new_icon(f'{iconPath}/openProject.png')

        self.pasteIcon = self.new_icon(f'{iconPath}/paste.png')

        self.pluginsIcon = self.new_icon(f'{iconPath}/plugins.png')

        self.povIcon = self.new_icon(f'{iconPath}/pov.png')

        self.propertiesIcon = self.new_icon(f'{iconPath}/properties.png')

        self.reloadIcon = self.new_icon(f'{iconPath}/reload.png')

        self.removeIcon = self.new_icon(f'{iconPath}/remove.png')

        self.resetHighlightIcon = self.new_icon(
            f'{iconPath}/reset_highlight.png')

        self.saveAsIcon = self.new_icon(f'{iconPath}/saveAs.png')

        self.saveIcon = self.new_icon(f'{iconPath}/save.png')

        self.settingsIcon = self.new_icon(f'{iconPath}/settings.png')

        self.stageIcon = self.new_icon(f'{iconPath}/stage.png')

        self.statusIcon = self.new_icon(f'{iconPath}/status.png')

        self.stickyNoteIcon = self.new_icon(f'{iconPath}/sticky_note.png')

        self.tagsIcon = self.new_icon(f'{iconPath}/tag.png')

        self.typeIcon = self.new_icon(f'{iconPath}/type.png')

        self.unlockIcon = self.new_icon(f'{iconPath}/unlock.png')

        self.updateFromManuscriptIcon = self.new_icon(
            f'{iconPath}/updateFromManuscript.png')

        self.viewBookIcon = self.new_icon(f'{iconPath}/viewBook.png')

        self.viewCharactersIcon = self.new_icon(
            f'{iconPath}/viewCharacters.png')

        self.viewItemsIcon = self.new_icon(f'{iconPath}/viewItems.png')

        self.viewLocationsIcon = self.new_icon(f'{iconPath}/viewLocations.png')

        self.viewPlotLinesIcon = self.new_icon(f'{iconPath}/viewArcs.png')

        self.viewProjectnotesIcon = self.new_icon(
            f'{iconPath}/viewProjectnotes.png')

        self.viewerIcon = self.new_icon(f'{iconPath}/viewer.png')

    def new_icon(self, iconFile):
        try:
            return tk.PhotoImage(file=iconFile)

        except:
            return None

